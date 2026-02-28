# Sonora - Discover Your Musical Voice

A beautiful, interactive web application that identifies the musical scale being played on a flute from either **live microphone input** or **uploaded audio/video files**. Includes an elegant home page celebrating the beauty and history of the flute.

## ✨ Features

- **🏠 Beautiful Home Page**: Introduction to the flute with history, learning resources, and external links
- **🎤 Live Recording Mode**: Record flute music directly from your microphone with real-time waveform visualization
- **📁 File Upload Mode**: Analyze pre-recorded audio (WAV, MP3) or video (MP4, MOV) files
- **🎨 Elegant UI**: Soothing, breezy interface reflecting the melody of the flute with soft blues and lavenders
- **📊 Detailed Results**: See detected scale, confidence score, and top 5 candidate scales
- **📖 Educational Content**: Learn flute history, find courses, and discover learning apps
- **🎵 Audio Processing**: Normalizes, denoises, and extracts dominant pitch over time
- **🎬 Video Processing**: Analyzes flute fingering position for scale detection
- **🤖 Smart Classification**: Scores all 12 major and 12 natural minor scales
- **⚡ Real-time Feedback**: Instant visualization and analysis results
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile

## 📋 Project Structure

```
flute-scale-detector
├── src
│   ├── app.py                      # Main Flask application with dual-page routing
│   ├── templates
│   │   ├── home.html               # Beautiful home page with flute intro & resources
│   │   └── index.html              # Scale detector interface
│   ├── static
│   │   ├── css
│   │   │   └── style.css           # Unified styles for both pages
│   │   └── js
│   │       ├── app.js              # Detector functionality
│   │       └── home.js             # Home page interactions
│   ├── audio
│   │   ├── preprocessing.py        # Audio preprocessing functions
│   │   └── pitch_tracking.py       # Pitch tracking algorithms
│   ├── video
│   │   ├── preprocessing.py        # Video preprocessing functions
│   │   └── fingering_detection.py  # Fingering detection methods
│   ├── models
│   │   ├── scale_classifier.py     # Scale classification model
│   │   └── inference.py            # Inference functions
│   ├── api
│   │   └── routes.py               # API routes for detection
│   └── types
│       └── index.py                # Data types and interfaces
├── tests
│   └── test_scale_classifier.py    # Unit tests
├── requirements.txt                # Project dependencies
├── pyproject.toml                  # Project configuration
├── README.md                       # This file
├── UI_GUIDE.md                     # Detailed UI usage guide
└── .gitignore                      # Git ignore configuration
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Modern web browser with Web Audio API support
- Microphone access (for live recording mode)

### Installation

1. Clone or navigate to the repository:
   ```bash
   cd flute-scale-detector
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python src/app.py
```

The application will be available at `http://localhost:5000`

## 🎯 Usage

### � Home Page (`/`)

The home page features:

- **🎵 Beautiful Introduction**: Learn about the timeless beauty of the flute
- **📜 Flute Timeline**: Explore a 40,000-year history from ancient origins to modern times
- **📚 Educational Highlights**: Six essential aspects of the flute (Pure Sound, Universal Presence, Technical Brilliance, Expressive Range, Vast Repertoire, and Artistic Expression)
- **🔗 Learning Resources**: Curated links to courses, apps, and communities
- **🎤 Easy Navigation**: Direct button to launch the Scale Detector

### 🌐 Detector Page (`/detector`)

For detailed usage instructions, see [UI_GUIDE.md](UI_GUIDE.md)

Simply open `http://localhost:5000/detector` in your browser and:

1. **For Live Recording**:
   - Click "Live Recording" button
   - Click "Start Recording"
   - Play your flute
   - Click "Stop Recording"
   - View results with detected scale and confidence

2. **For File Upload**:
   - Click "Upload File" button
   - Drag & drop or select an audio/video file
   - Click "Analyze File"
   - View detailed results

## 📡 API Endpoints

#### Web Pages
- `GET /` - Home page (introduction to flutes with resources)
- `GET /detector` - Scale detector interface
- `GET /health` - Health check endpoint

#### Detection APIs
- `POST /detect/audio` - Analyze audio file
  - Form-data: `file=<audio_file>`
  - Returns: `{scale, confidence, candidates, pitch_count}`

- `POST /detect/video` - Analyze video file
  - Form-data: `file=<video_file>`
  - Returns: `{scale, confidence, candidates, frame_count, mode}`

#### Example API Calls

**Audio Analysis**:
```bash
curl -X POST http://localhost:5000/detect/audio -F "file=@sample.wav"
```

**Video Analysis**:
```bash
curl -X POST http://localhost:5000/detect/video -F "file=@sample.mp4"
```

**Response Example**:
```json
{
  "scale": "G Major",
  "confidence": 0.87,
  "candidates": [
    {"scale": "G Major", "score": 0.87},
    {"scale": "E Minor", "score": 0.71},
    {"scale": "A Major", "score": 0.68},
    {"scale": "C# Minor", "score": 0.65},
    {"scale": "D Major", "score": 0.62}
  ],
  "pitch_count": 856
}
```

## 🎨 Design

The UI features a **classic, traditional, and ambient** aesthetic:

- **Color Scheme**: Warm earth tones (browns, golds, creams) inspired by classical instruments
- **Typography**: Clear hierarchy and readable fonts
- **Animations**: Smooth transitions and gentle visual feedback
- **Responsive**: Adapts beautifully to any screen size
- **Accessibility**: Full keyboard navigation and dark mode support

## ⚙️ Configuration

### Audio Settings
- Sample rate: 22,050 Hz (optimized for flute)
- Frequency range: 220-1400 Hz (typical flute range)
- FFT size: 2048 bins
- Hop length: 256 samples

### Scale Detection
- Detects all 12 major scales (C, C#, D, ..., B)
- Detects all 12 natural minor scales (A, A#, B#, ..., G#)
- Uses pitch-class histogram matching
- Confidence scoring based on scale tone prevalence

## 📦 Dependencies

- **Flask**: Web framework
- **NumPy**: Numerical computing
- **SciPy**: Scientific computing
- **Librosa**: Audio analysis
- **OpenCV**: Video processing
- **TensorFlow**: Deep learning (optional for future enhancements)
- **Pytest**: Testing framework

See [requirements.txt](requirements.txt) for specific versions.

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run specific tests:
```bash
pytest tests/test_scale_classifier.py -v
```

## 📚 How It Works

### Audio Analysis Pipeline
1. **Load & Preprocess**: Normalizes audio and applies denoising
2. **Pitch Tracking**: Uses Librosa's piptrack to extract dominant pitch per frame
3. **Feature Extraction**: Builds 12-bin pitch-class histogram
4. **Scale Classification**: Matches histogram against all 24 scales
5. **Confidence Calculation**: Computes confidence based on scale score differences

### Video Analysis Pipeline
1. **Frame Extraction**: Samples video at specified frame rate
2. **Preprocessing**: Normalizes and crops frames
3. **Fingering Detection**: Analyzes hole coverage patterns
4. **Pitch Mapping**: Maps fingering patterns to likely pitch classes
5. **Scale Classification**: Same as audio pipeline

## 🐛 Troubleshooting

**Microphone not working?**
- Check browser microphone permissions
- Ensure no other app is using the microphone
- Try a different browser

**File upload failing?**
- Verify file format is supported (WAV, MP3, MP4, MOV)
- Check file size is reasonable (<100MB)
- Ensure audio contains audible pitch

**Poor detection results?**
- Record in quiet environment
- Ensure clear, steady notes
- Minimize background noise

See [UI_GUIDE.md](UI_GUIDE.md) for more troubleshooting tips.

## 🔮 Future Enhancements

- [ ] Real-time pitch visualization
- [ ] Scale history and statistics
- [ ] Tuning feedback
- [ ] Fingering suggestions
- [ ] Multi-scale detection
- [ ] Export results as CSV/PDF
- [ ] Mobile app version
- [ ] Cloud-based processing

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## 💡 Tips for Best Results

**For Live Recording**:
- Use a quiet environment
- Play steady, clear notes
- Record at least 3-5 seconds
- Keep microphone at consistent distance

**For File Upload**:
- Use high-quality audio (WAV, FLAC preferred)
- Ensure 30fps+ video frame rate
- Avoid heavy compression
- Clear, unambiguous flute sound works best

---

**Made with ❤️ for flute musicians and music enthusiasts**  
Version 1.0.0 | Last Updated February 27, 2026
