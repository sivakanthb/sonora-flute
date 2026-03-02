// ========================================
// Theme Manager - Dark Mode Toggle
// ========================================

class ThemeManager {
    constructor() {
        this.prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        this.storageKey = 'sonora-theme';
        this.init();
    }

    init() {
        const savedTheme = localStorage.getItem(this.storageKey);
        const theme = savedTheme || (this.prefersDark ? 'dark' : 'light');
        this.setTheme(theme);
    }

    setTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }
        localStorage.setItem(this.storageKey, theme);
    }

    toggle() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
        return newTheme;
    }

    getCurrent() {
        return document.documentElement.getAttribute('data-theme') || 'light';
    }
}

// ========================================
// Background Music Manager with Tone.js
// ========================================

class MusicManager {
    constructor() {
        this.isPlaying = false;
        this.storageKey = 'sonora-music-enabled';
        this.audioLoadingKey = 'sonora-audio-loaded';
        this.initAudioContext();
    }

    initAudioContext() {
        // Initialize Web Audio API for generating soothing ambient sounds
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        this.oscillators = [];
        this.gains = [];
    }

    async loadToneJS() {
        // Check if Tone.js is already loaded
        if (window.Tone) {
            return window.Tone;
        }

        // Load Tone.js from CDN
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js';
        
        return new Promise((resolve, reject) => {
            script.onload = () => resolve(window.Tone);
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    async start() {
        if (this.isPlaying) return;
        
        try {
            // Resume audio context if suspended
            if (this.audioContext.state === 'suspended') {
                await this.audioContext.resume();
            }

            // Load Tone.js and play ambient music
            const Tone = await this.loadToneJS();
            this.playAmbientFlute(Tone);
            
            this.isPlaying = true;
            localStorage.setItem(this.storageKey, 'true');
            this.updateUI();
        } catch (e) {
            console.error('Music playback failed:', e);
        }
    }

    playAmbientFlute(Tone) {
        if (this.synth) return; // Already playing

        // Create a pleasant ambient flute-like sound
        this.synth = new Tone.Synth({
            oscillator: { type: 'sine' },
            envelope: {
                attack: 2,
                decay: 3,
                sustain: 0.8,
                release: 2
            }
        }).toDestination();

        // Reduce volume for background music
        this.synth.volume.value = -15;

        // Scale of C Major (or C Raga Bhairav inspired)
        const notes = ['C4', 'D4', 'E4', 'G4', 'A4', 'C5', 'A4', 'G4', 'E4', 'D4'];
        
        this.playMelody(Tone, this.synth, notes);
    }

    playMelody(Tone, synth, notes, index = 0) {
        if (!this.isPlaying) return;

        const now = Tone.now();
        const noteDuration = 0.8;

        synth.triggerAttackRelease(notes[index % notes.length], noteDuration, now);

        const nextNoteTime = now + noteDuration + 0.2;
        setTimeout(() => {
            this.playMelody(Tone, synth, notes, index + 1);
        }, (noteDuration + 0.2) * 1000);
    }

    stop() {
        if (!this.isPlaying) return;
        
        if (this.synth) {
            this.synth.triggerRelease();
            this.synth.dispose();
            this.synth = null;
        }
        
        this.isPlaying = false;
        localStorage.setItem(this.storageKey, 'false');
        this.updateUI();
    }

    toggle() {
        if (this.isPlaying) {
            this.stop();
        } else {
            this.start();
        }
    }

    updateUI() {
        const btn = document.querySelector('.music-toggle');
        if (btn) {
            if (this.isPlaying) {
                btn.classList.add('playing');
                btn.setAttribute('aria-label', 'Stop background music');
            } else {
                btn.classList.remove('playing');
                btn.setAttribute('aria-label', 'Play background music');
            }
        }
    }

    isEnabled() {
        return localStorage.getItem(this.storageKey) === 'true';
    }

    autoPlay() {
        if (this.isEnabled()) {
            // Show tooltip that music auto-started
            setTimeout(() => this.start(), 500);
        }
    }
}

// ========================================
// Scale of the Day Generator
// ========================================

class ScaleOfTheDay {
    constructor() {
        this.scales = [
            {
                name: 'Bhairav',
                notes: 'Sa Re Ma Pa Dha Sa',
                description: 'The heroic and majestic scale. Associated with morning ragas and spiritual awakening.',
                thaat: 'Bhairav Thaat',
                key: 'C',
                characteristic: 'Energetic, devotional'
            },
            {
                name: 'Yaman',
                notes: 'Sa Re Ga Pa Dha Sa',
                description: 'The evening scale of divine grace. Known for its sweet, melodious nature.',
                thaat: 'Kalyan Thaat',
                key: 'G',
                characteristic: 'Pleasant, devotional'
            },
            {
                name: 'Kafi',
                notes: 'Sa Re Ga Ma Pa Dha Ni Sa',
                description: 'The nocturnal scale of emotional depth. Associated with longing and romantic moods.',
                thaat: 'Kafi Thaat',
                key: 'D',
                characteristic: 'Melancholic, romantic'
            },
            {
                name: 'Asavari',
                notes: 'Sa Re Ga Ma Pa Dha Ni Sa',
                description: 'The meditative scale of tranquility. Used in devotional and classical contexts.',
                thaat: 'Asavari Thaat',
                key: 'E',
                characteristic: 'Meditative, peaceful'
            },
            {
                name: 'Bilawal',
                notes: 'Sa Re Ga Ma Pa Dha Ni Sa',
                description: 'The fundamental scale. Pure and unadorned, representing the basic structure of Indian music.',
                thaat: 'Bilawal Thaat',
                key: 'F',
                characteristic: 'Pure, fundamental'
            }
        ];
    }

    getTodayScale() {
        const today = new Date();
        const dayOfYear = Math.floor((today - new Date(today.getFullYear(), 0, 0)) / 1000 / 60 / 60 / 24);
        const scaleName = this.scales[dayOfYear % this.scales.length];
        return scaleName;
    }

    renderToDOM(elementId) {
        const container = document.getElementById(elementId);
        if (!container) return;

        const scale = this.getTodayScale();
        container.innerHTML = `
            <div class="scale-of-day">
                <h3>🎵 Scale of the Day</h3>
                <div class="scale-name">${scale.name}</div>
                <p style="color: var(--text-light);"><em>${scale.thaat}</em></p>
                <p class="scale-description">${scale.description}</p>
                <p style="margin-bottom: 1rem;"><strong>Notes:</strong> ${scale.notes}</p>
                <p style="margin-bottom: 1rem;"><span class="difficulty-badge difficulty-${scale.characteristic.toLowerCase().replace(', ', '-')}">${scale.characteristic}</span></p>
                <button class="listen-btn" data-scale="${scale.name}">🎧 Listen to ${scale.name}</button>
            </div>
        `;
    }
}

// ========================================
// Interactive Scale Player
// ========================================

class InteractiveScale {
    constructor() {
        this.selectedScales = [];
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        this.oscillators = [];
    }

    async loadToneJS() {
        if (window.Tone) {
            return window.Tone;
        }
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js';
        
        return new Promise((resolve, reject) => {
            script.onload = () => resolve(window.Tone);
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    async playScale(scaleName) {
        const Tone = await this.loadToneJS();
        
        const scaleMap = {
            'Bhairav': ['C4', 'D4', 'E4', 'F#4', 'G4', 'A4', 'B4', 'C5'],
            'Yaman': ['G4', 'A4', 'B4', 'C#5', 'D5', 'E5', 'F#5', 'G5'],
            'Kafi': ['D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5'],
        };

        const notes = scaleMap[scaleName] || scaleMap['Bhairav'];

        // Create a simple synth for playing the scale
        const synth = new Tone.Synth({
            oscillator: { type: 'triangle' },
            envelope: {
                attack: 0.2,
                decay: 0.1,
                sustain: 0.3,
                release: 0.5
            }
        }).toDestination();

        // Play scale notes
        for (let i = 0; i < notes.length; i++) {
            const now = Tone.now() + i * 0.5;
            synth.triggerAttackRelease(notes[i], '0.4', now);
        }
    }

    async playNote(note) {
        const Tone = await this.loadToneJS();
        
        const synth = new Tone.PolySynth(Tone.Synth, {
            oscillator: { type: 'sine' },
            envelope: {
                attack: 0.1,
                decay: 0.2,
                sustain: 0.2,
                release: 0.4
            }
        }).toDestination();

        synth.triggerAttackRelease(note, '0.5');
    }
}

// ========================================
// Initialization
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize Theme Manager
    const themeManager = new ThemeManager();
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const newTheme = themeManager.toggle();
            themeToggle.textContent = newTheme === 'dark' ? '☀️' : '🌙';
        });
        // Set initial icon
        themeToggle.textContent = themeManager.getCurrent() === 'dark' ? '☀️' : '🌙';
    }

    // Initialize Music Manager
    const musicManager = new MusicManager();
    const musicToggle = document.querySelector('.music-toggle');
    if (musicToggle) {
        musicToggle.addEventListener('click', () => {
            musicManager.toggle();
        });
        musicManager.updateUI();
        musicManager.autoPlay();
    }

    // Initialize Scale of the Day
    const scaleOfDay = new ScaleOfTheDay();
    scaleOfDay.renderToDOM('scale-of-day-widget');

    // Listen button event
    document.addEventListener('click', async (e) => {
        if (e.target.classList.contains('listen-btn')) {
            const scaleName = e.target.getAttribute('data-scale');
            const scalePlayer = new InteractiveScale();
            await scalePlayer.playScale(scaleName);
        }
    });

    // Scale search and filter functionality
    const scaleSearch = document.getElementById('scale-search');
    if (scaleSearch) {
        scaleSearch.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const scales = document.querySelectorAll('.scale-card');
            scales.forEach(scale => {
                const name = scale.textContent.toLowerCase();
                scale.style.display = name.includes(query) ? 'block' : 'none';
            });
        });
    }

    // Difficulty filter
    const filterTags = document.querySelectorAll('.filter-tag');
    filterTags.forEach(tag => {
        tag.addEventListener('click', () => {
            tag.classList.toggle('active');
            filterScalesByDifficulty();
        });
    });

    function filterScalesByDifficulty() {
        const activeTags = Array.from(filterTags)
            .filter(tag => tag.classList.contains('active'))
            .map(tag => tag.textContent.trim().toLowerCase());

        const scales = document.querySelectorAll('.scale-card');
        scales.forEach(scale => {
            if (activeTags.length === 0) {
                scale.style.display = 'block';
            } else {
                const difficulty = scale.getAttribute('data-difficulty');
                scale.style.display = activeTags.includes(difficulty) ? 'block' : 'none';
            }
        });
    }
});

// ========================================
// Mobile Dropdown Menu Handling
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const dropdown = document.querySelector('.dropdown');
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    if (dropdownToggle && dropdownMenu && dropdown) {
        // For mobile: toggle dropdown on click instead of hover
        const isMobileDevice = () => window.matchMedia("(max-width: 768px)").matches;

        if (isMobileDevice()) {
            dropdownToggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Toggle the dropdown
                dropdownMenu.classList.toggle('show');
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', function(e) {
                if (!dropdown.contains(e.target)) {
                    dropdownMenu.classList.remove('show');
                }
            });

            // Close dropdown when a menu item is clicked
            const dropdownItems = document.querySelectorAll('.dropdown-item');
            dropdownItems.forEach(item => {
                item.addEventListener('click', function() {
                    dropdownMenu.classList.remove('show');
                });
            });

            // Handle orientation change
            window.addEventListener('orientationchange', function() {
                dropdownMenu.classList.remove('show');
            });

            // Handle window resize
            window.addEventListener('resize', function() {
                if (window.matchMedia("(min-width: 769px)").matches) {
                    dropdownMenu.classList.remove('show');
                }
            });
        }
    }
});

// Export for use in other scripts
window.ThemeManager = ThemeManager;
window.MusicManager = MusicManager;
window.ScaleOfTheDay = ScaleOfTheDay;
window.InteractiveScale = InteractiveScale;
