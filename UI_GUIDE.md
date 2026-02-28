# Sonora - UI Guide

## Overview

Sonora features an elegant, soothing web-based interface that allows you to identify musical scales from flute performances. The interface supports both **live recording** and **file upload** modes.

## Features

### 🎤 Live Recording Mode
Record flute music directly from your microphone in real-time:

- **Start Recording**: Click the "Start Recording" button to begin capturing audio from your microphone
- **Visual Feedback**: Real-time waveform visualization shows the audio being captured
- **Timer**: A countdown timer shows the duration of your recording
- **Status Indicator**: The recording indicator shows when the microphone is active
- **Stop Recording**: Click "Stop Recording" when finished; the app automatically analyzes the audio

### 📁 File Upload Mode
Upload pre-recorded audio or video files for analysis:

- **Drag & Drop**: Simply drag audio or video files onto the upload area
- **Click to Upload**: Click the upload area to browse and select files
- **Multiple Formats**: Supports audio (WAV, MP3) and video (MP4, MOV) files
- **File Preview**: Selected filename is displayed before analysis
- **Clear Selection**: Remove a selected file and choose another

### 📊 Results Display
After analysis, you'll see:

- **Detected Scale**: The primary scale identified by the detector
- **Confidence Score**: How confident the detector is in the result (0-100%)
- **Visual Confidence Bar**: Color-coded bar showing confidence level
- **Top Candidates**: List of the top 5 most likely scales with their scores
- **Metadata**: Additional information such as number of frames analyzed

## Design Aesthetic

The interface uses a **classic, traditional, and ambient** design theme:

- **Color Palette**: Warm earth tones (browns, golds, creams) reminiscent of classical instruments
- **Typography**: Clear, readable fonts with proper hierarchy
- **Subtle Animations**: Smooth transitions and gentle visual feedback
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Dark Mode Support**: Automatically adapts to system preference for light/dark theme

## Getting Started

### Running the Application

```bash
cd flute-scale-detector
python src/app.py
```

The application will start on `http://localhost:5000`

### Using Live Recording

1. Open the application in your browser
2. Click the **"Live Recording"** button
3. Allow microphone access when prompted by your browser
4. Click **"Start Recording"** and play your flute
5. Click **"Stop Recording"** when finished
6. View the results with detected scale and confidence

### Using File Upload

1. Open the application in your browser
2. Click the **"Upload File"** button
3. Either:
   - Drag an audio/video file onto the upload area, or
   - Click to browse and select a file
4. Click **"Analyze File"**
5. View the detection results

## Technical Details

### Supported Audio Formats
- WAV (Waveform Audio File Format)
- MP3 (MPEG-1 Audio Layer 3)
- FLAC (Free Lossless Audio Codec)
- And other formats supported by your browser

### Supported Video Formats
- MP4 (MPEG-4)
- MOV (QuickTime)
- WebM
- Other formats with embedded audio

### Analysis Information

**Live Recording**:
- Sample rate: 22050 Hz (optimized for flute frequencies)
- Frequency range: 220-1400 Hz (typical flute range)
- Detection method: Librosa pitch tracking with scale classification

**File Upload**:
- Video mode: Analyzes flute fingering position
- Audio mode: Analyzes pitch content
- Automatic format detection

## API Endpoints

The underlying API provides:

- `GET /` - Serves the web interface (HTML)
- `POST /detect/audio` - Analyzes audio files (accepts audio file in form-data)
- `POST /detect/video` - Analyzes video files (accepts video file in form-data)
- `GET /health` - Health check endpoint

## Browser Requirements

- Modern web browser with Web Audio API support
- Microphone access (for live recording)
- JavaScript enabled

### Tested Browsers
- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Keyboard Shortcuts

- Tab: Navigate between UI elements
- Enter: Activate focused button
- Space: Toggle recording (when focused on Start/Stop button)

## Troubleshooting

### Microphone Not Working
- Check browser permissions for microphone access
- Ensure no other application is exclusively using the microphone
- Try a different browser
- Restart your browser

### File Upload Fails
- Verify file format is supported (WAV, MP3, MP4, MOV)
- Check file size is reasonable (<100MB)
- Ensure audio/video file contains valid data
- Try uploading a smaller file to test

### Results Not Appearing
- Ensure audio is clear and contains audible pitch
- Very quiet or extremely distorted audio may not produce results
- Video files should have clear fingering visible
- Check browser console for error messages

### Slow Analysis
- Analysis time depends on file duration and system performance
- Longer recordings take proportionally longer to analyze
- Video analysis takes slightly longer than audio-only analysis

## Future Features

Planned enhancements:
- Real-time pitch visualization
- Scale history and statistics
- Tuning feedback
- Fingering suggestions
- Multi-scale detection
- Export analysis results

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Ensure Flask and librosa are properly configured
4. Check browser developer console (F12) for errors

## Performance Tips

1. **For best results**:
   - Record in a quiet environment
   - Play steady, clear notes
   - Avoid background noise

2. **For live recording**:
   - Allow 3-5 seconds minimum
   - Avoid sudden loud sounds
   - Keep microphone at consistent distance

3. **For file upload**:
   - Use high-quality audio files (WAV, FLAC preferred)
   - Ensure clear, uncompressed audio where possible
   - For video, ensure 30fps+ frame rate

---

**Version**: 1.0.0  
**Last Updated**: February 27, 2026  
**License**: MIT
