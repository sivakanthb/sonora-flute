"""
Vercel serverless function entry point for Flute Scale Detector.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from flask import Flask, render_template, session, request, jsonify
import json
import os
from datetime import datetime
import uuid

# Initialize Flask with correct paths
src_path = Path(__file__).parent.parent / 'src'
app = Flask(
    __name__,
    template_folder=str(src_path / 'templates'),
    static_folder=str(src_path / 'static'),
)

app.secret_key = os.environ.get('SECRET_KEY', 'sonora-secret-key-2024')
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Simple in-memory storage for this deployment (Vercel serverless doesn't support persistent files)
detection_cache = {}

@app.route('/')
@app.route('/index.html')
def index():
    try:
        return render_template('home.html')
    except Exception as e:
        return f"Error loading home: {str(e)}", 500

@app.route('/detector')
def detector():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading detector: {str(e)}", 500

@app.route('/learn/scales')
def learn_scales():
    try:
        return render_template('learn/scales.html')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/learn/fingering')
def learn_fingering():
    try:
        return render_template('learn/fingering.html')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/learn/videos')
def learn_videos():
    try:
        return render_template('learn/videos.html')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/learn/audio')
def learn_audio():
    try:
        return render_template('learn/audio.html')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/profile')
def profile():
    try:
        return render_template('user/profile.html', user_id='user123', total_detections=0, top_scale='None', favorite_scales={})
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/history')
def history():
    try:
        return render_template('user/history.html', user_id='user123', history=[])
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/leaderboard')
def leaderboard():
    try:
        return render_template('user/leaderboard.html', leaderboard=[])
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/about')
def about():
    try:
        return render_template('pages/about.html')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/faq')
def faq():
    try:
        return render_template('pages/faq.html')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/contact')
def contact():
    try:
        return render_template('pages/contact.html')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.post('/api/detection/save')
def save_detection():
    try:
        data = request.get_json()
        return jsonify({'status': 'success', 'message': 'Detection saved'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.post('/api/detection/export')
def export_detection():
    try:
        data = request.get_json()
        return jsonify({
            'scale': data.get('scale'),
            'confidence': data.get('confidence'),
            'exported_at': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'message': 'Flute Scale Detector is running'})

@app.errorhandler(404)
def not_found(error):
    try:
        return render_template('home.html'), 404
    except:
        return jsonify({'error': 'Not found'}), 404

# Export app for Vercel
if __name__ != '__main__':
    # When run by Vercel
    pass

