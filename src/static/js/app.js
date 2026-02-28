/* ========================================
   Sonora - Scale Detection JavaScript
   ======================================== */

class FluteScaleDetector {
    constructor() {
        this.mediaRecorder = null;
        this.audioContext = null;
        this.analyser = null;
        this.dataArray = null;
        this.isRecording = false;
        this.recordingStartTime = null;
        this.timerInterval = null;
        this.selectedFile = null;

        this.initializeElements();
        this.setupEventListeners();
    }

    initializeElements() {
        // Mode buttons
        this.modeButtons = document.querySelectorAll('.mode-btn');
        this.modeSections = document.querySelectorAll('.mode-section');

        // Recording elements
        this.startBtn = document.getElementById('startBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.recordingTime = document.getElementById('recordingTime');
        this.statusLight = document.getElementById('statusLight');
        this.statusText = document.getElementById('statusText');
        this.waveform = document.getElementById('waveform');

        // Upload elements
        this.fileInput = document.getElementById('fileInput');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.clearFileBtn = document.getElementById('clearFileBtn');
        this.fileInfo = document.getElementById('fileInfo');
        this.fileName = document.getElementById('fileName');

        // Results elements
        this.recordSection = document.getElementById('record-section');
        this.uploadSection = document.getElementById('upload-section');
        this.resultsSection = document.getElementById('results-section');
        this.errorSection = document.getElementById('error-section');
        this.loadingSpinner = document.getElementById('loadingSpinner');
        this.resultsContent = document.getElementById('resultsContent');

        // Action buttons
        this.backBtn = document.getElementById('backBtn');
        this.errorBackBtn = document.getElementById('errorBackBtn');
    }

    setupEventListeners() {
        // Mode selection
        this.modeButtons.forEach(btn => {
            btn.addEventListener('click', () => this.switchMode(btn.dataset.mode));
        });

        // Recording controls
        this.startBtn.addEventListener('click', () => this.startRecording());
        this.stopBtn.addEventListener('click', () => this.stopRecording());

        // File upload
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.uploadBtn.addEventListener('click', () => this.uploadFile());
        this.clearFileBtn.addEventListener('click', () => this.clearFile());

        // Drag and drop
        const fileLabel = document.querySelector('.file-label');
        fileLabel.addEventListener('dragover', (e) => this.handleDragOver(e));
        fileLabel.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        fileLabel.addEventListener('drop', (e) => this.handleDrop(e));

        // Back buttons
        this.backBtn.addEventListener('click', () => this.goBack());
        this.errorBackBtn.addEventListener('click', () => this.goBack());

        // Detect again button
        const detectAgainBtn = document.getElementById('detectAgainBtn');
        if (detectAgainBtn) {
            detectAgainBtn.addEventListener('click', () => this.goBack());
        }
    }

    switchMode(mode) {
        // Update button states
        this.modeButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });

        // Update section visibility
        this.modeSections.forEach(section => {
            section.classList.remove('active');
        });

        if (mode === 'record') {
            this.recordSection.classList.add('active');
        } else if (mode === 'upload') {
            this.uploadSection.classList.add('active');
        }
    }

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.initializeAudioContext(stream);
            
            this.mediaRecorder = new MediaRecorder(stream);
            let audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                this.stopVisualization();
                await this.analyzeRecording(audioBlob);
            };

            this.mediaRecorder.start();
            this.isRecording = true;
            this.recordingStartTime = Date.now();

            // Update UI
            this.startBtn.disabled = true;
            this.stopBtn.disabled = false;
            this.statusLight.classList.add('recording');
            this.statusText.textContent = 'Recording...';

            // Start visualization and timer
            this.startVisualization();
            this.startTimer();
        } catch (error) {
            this.showError('Microphone access denied. Please allow microphone access to record.');
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;

            // Update UI
            this.startBtn.disabled = false;
            this.stopBtn.disabled = true;
            this.statusLight.classList.remove('recording');
            this.statusText.textContent = 'Processing...';

            // Stop timer and visualization
            clearInterval(this.timerInterval);
        }
    }

    initializeAudioContext(stream) {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }

        const source = this.audioContext.createMediaStreamAudioSource(stream);
        this.analyser = this.audioContext.createAnalyser();
        this.analyser.fftSize = 256;

        source.connect(this.analyser);
        this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);
    }

    startVisualization() {
        const draw = () => {
            if (!this.isRecording) return;

            this.analyser.getByteFrequencyData(this.dataArray);

            // Create waveform points
            let points = '0,30';
            const step = Math.ceil(this.dataArray.length / 150);
            for (let i = 0; i < this.dataArray.length; i += step) {
                const value = this.dataArray[i] / 255;
                const x = (i / this.dataArray.length) * 300;
                const y = 30 - value * 25;
                points += ` ${x},${y}`;
            }
            points += ' 300,30';

            this.waveform.setAttribute('points', points);
            requestAnimationFrame(draw);
        };

        draw();
    }

    stopVisualization() {
        // Reset waveform
        this.waveform.setAttribute('points', '0,30 300,30');
    }

    startTimer() {
        let seconds = 0;
        this.timerInterval = setInterval(() => {
            seconds++;
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            this.recordingTime.textContent = 
                `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        }, 1000);
    }

    async analyzeRecording(audioBlob) {
        const formData = new FormData();
        formData.append('file', audioBlob, 'recording.wav');

        try {
            this.showLoading();
            const response = await fetch('/detect/audio', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to analyze audio');
            }

            const result = await response.json();
            this.displayResults(result);
            this.statusText.textContent = 'Ready to record';
            this.recordingTime.textContent = '00:00';
        } catch (error) {
            this.showError(`Error analyzing audio: ${error.message}`);
        }
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.selectedFile = file;
            this.fileName.textContent = file.name;
            this.fileInfo.style.display = 'block';
        }
    }

    handleDragOver(event) {
        event.preventDefault();
        event.stopPropagation();
        event.currentTarget.style.borderColor = '#D4AF37';
        event.currentTarget.style.background = 'var(--bg-tertiary)';
    }

    handleDragLeave(event) {
        event.preventDefault();
        event.stopPropagation();
        event.currentTarget.style.borderColor = 'var(--border)';
        event.currentTarget.style.background = 'var(--bg-primary)';
    }

    handleDrop(event) {
        event.preventDefault();
        event.stopPropagation();

        const files = event.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (file.type.startsWith('audio/') || file.type.startsWith('video/')) {
                this.fileInput.files = files;
                this.handleFileSelect({ target: { files } });
            } else {
                this.showError('Please drop an audio or video file.');
            }
        }

        event.currentTarget.style.borderColor = 'var(--border)';
        event.currentTarget.style.background = 'var(--bg-primary)';
    }

    async uploadFile() {
        if (!this.selectedFile) {
            this.showError('Please select a file first.');
            return;
        }

        const formData = new FormData();
        formData.append('file', this.selectedFile);

        let endpoint = '/detect/audio';
        if (this.selectedFile.type.startsWith('video/')) {
            endpoint = '/detect/video';
        }

        try {
            this.showLoading();
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to analyze file');
            }

            const result = await response.json();
            this.displayResults(result);
        } catch (error) {
            this.showError(`Error analyzing file: ${error.message}`);
        }
    }

    clearFile() {
        this.selectedFile = null;
        this.fileInput.value = '';
        this.fileInfo.style.display = 'none';
    }

    displayResults(result) {
        this.loadingSpinner.style.display = 'none';
        this.resultsContent.style.display = 'block';

        // Store current result for export functionality
        this.currentResult = result;

        // Display detected scale
        document.getElementById('detectedScale').textContent = result.scale || 'Unknown';

        // Display confidence
        const confidence = (result.confidence || 0) * 100;
        const confidenceFill = document.getElementById('confidenceFill');
        confidenceFill.style.width = `${confidence}%`;
        
        // Set confidence color based on score
        if (confidence >= 75) {
            confidenceFill.style.background = 'linear-gradient(135deg, #A8E6CF, #6BB6D6)';
        } else if (confidence >= 50) {
            confidenceFill.style.background = 'linear-gradient(135deg, #E8956E, #F5C89B)';
        } else {
            confidenceFill.style.background = 'linear-gradient(135deg, #D9887B, #E8956E)';
        }
        
        document.getElementById('confidenceValue').textContent = `${Math.round(confidence)}%`;

        // Display top 3 candidates
        const candidates = (result.candidates && result.candidates.length > 0) 
            ? result.candidates.slice(0, 3) 
            : [];
        
        const badges = ['🥇', '🥈', '🥉'];
        for (let i = 0; i < 3; i++) {
            const cardId = `candidate${i + 1}`;
            const card = document.getElementById(cardId);
            
            if (candidates[i]) {
                const candidate = candidates[i];
                card.querySelector('.candidate-info p:first-child').textContent = 
                    candidate.scale || `Scale ${i + 1}`;
                card.querySelector('.candidate-info p:last-child').textContent = 
                    `${(candidate.score * 100).toFixed(1)}% confidence`;
            } else {
                card.querySelector('.candidate-info p:first-child').textContent = '-';
                card.querySelector('.candidate-info p:last-child').textContent = '-';
            }
        }

        // Display metadata
        let metadata = '';
        if (result.pitch_count) {
            metadata += `Pitch frames detected: ${result.pitch_count}`;
        }
        if (result.frame_count) {
            metadata += ` | Video frames analyzed: ${result.frame_count}`;
        }
        if (result.mode) {
            metadata += ` | Mode: ${result.mode}`;
        }
        document.getElementById('metadataText').textContent = metadata || 'Detection Complete';

        // Setup export buttons
        this.setupExportButtons();

        // Show results section
        this.recordSection.classList.remove('active');
        this.uploadSection.classList.remove('active');
        this.resultsSection.style.display = 'block';
        this.resultsSection.classList.add('active');
    }

    setupExportButtons() {
        const exportJsonBtn = document.getElementById('exportJsonBtn');
        const exportCsvBtn = document.getElementById('exportCsvBtn');
        const saveToDashboardBtn = document.getElementById('saveToDashboardBtn');

        // Remove existing listeners
        exportJsonBtn.onclick = () => this.exportAsJSON();
        exportCsvBtn.onclick = () => this.exportAsCSV();
        saveToDashboardBtn.onclick = () => this.saveToDashboard();
    }

    exportAsJSON() {
        if (!this.currentResult) return;

        const exportData = {
            scale: this.currentResult.scale,
            confidence: this.currentResult.confidence,
            candidates: this.currentResult.candidates || [],
            pitch_count: this.currentResult.pitch_count,
            frame_count: this.currentResult.frame_count,
            exported_at: new Date().toISOString()
        };

        const jsonString = JSON.stringify(exportData, null, 2);
        const blob = new Blob([jsonString], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `sonora-detection-${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);
    }

    exportAsCSV() {
        if (!this.currentResult) return;

        const headers = ['Scale', 'Confidence', 'Rank', 'Candidate Score'];
        const rows = [];

        rows.push([
            this.currentResult.scale,
            `${(this.currentResult.confidence * 100).toFixed(1)}%`,
            'Primary',
            '100%'
        ]);

        if (this.currentResult.candidates) {
            this.currentResult.candidates.slice(0, 3).forEach((candidate, index) => {
                rows.push([
                    candidate.scale,
                    '',
                    index + 2,
                    `${(candidate.score * 100).toFixed(1)}%`
                ]);
            });
        }

        let csvContent = headers.join(',') + '\n';
        csvContent += rows.map(row => row.join(',')).join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `sonora-detection-${Date.now()}.csv`;
        a.click();
        URL.revokeObjectURL(url);
    }

    async saveToDashboard() {
        if (!this.currentResult) return;

        try {
            const response = await fetch('/api/detection/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    scale: this.currentResult.scale,
                    confidence: this.currentResult.confidence,
                    candidates: this.currentResult.candidates || [],
                    mode: this.currentResult.mode || 'recording'
                })
            });

            if (!response.ok) {
                throw new Error('Failed to save detection');
            }

            const result = await response.json();
            alert('✓ Detection saved to your profile dashboard!');
        } catch (error) {
            alert(`Error saving detection: ${error.message}`);
        }
    }

    showLoading() {
        this.recordSection.classList.remove('active');
        this.uploadSection.classList.remove('active');
        this.resultsSection.style.display = 'block';
        this.resultsSection.classList.add('active');
        this.loadingSpinner.style.display = 'block';
        this.resultsContent.style.display = 'none';
    }

    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        this.recordSection.classList.remove('active');
        this.uploadSection.classList.remove('active');
        this.resultsSection.style.display = 'none';
        this.errorSection.style.display = 'block';
        this.errorSection.classList.add('active');
    }

    goBack() {
        // Reset recording state
        if (this.isRecording) {
            this.stopRecording();
        }
        this.recordingTime.textContent = '00:00';
        this.statusText.textContent = 'Ready to record';
        this.statusLight.classList.remove('recording');

        // Hide all sections
        this.resultsSection.style.display = 'none';
        this.errorSection.style.display = 'none';

        // Show record section
        this.recordSection.classList.add('active');
        this.modeButtons[0].classList.add('active');
        this.modeButtons[1].classList.remove('active');
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new FluteScaleDetector();
});
