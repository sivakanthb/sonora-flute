"""
Vercel serverless function entry point for Flute Scale Detector.
This file is required by Vercel to run Python applications serverlessly.
"""

import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Create a minimal Flask app for Vercel
from flask import Flask, render_template, session, request, jsonify
import json
import os
from datetime import datetime
import uuid

# Initialize Flask app with proper paths
src_path = Path(__file__).parent.parent / 'src'
app = Flask(
    __name__,
    template_folder=str(src_path / 'templates'),
    static_folder=str(src_path / 'static'),
    static_url_path='/'
)

# Set a secret key for sessions
app.secret_key = os.environ.get('SECRET_KEY', 'sonora-secret-key-2024')

# Production settings
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Data file for storing user history
DATA_DIR = src_path / 'data'
DATA_DIR.mkdir(exist_ok=True)
HISTORY_FILE = DATA_DIR / 'detection_history.json'
USERS_FILE = DATA_DIR / 'users.json'


def load_user_history(user_id):
    """Load detection history for a user."""
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, 'r') as f:
            all_history = json.load(f)
        return [h for h in all_history if h.get('user_id') == user_id]
    except:
        return []


def save_detection(user_id, detection_data):
    """Save a detection result to user history."""
    try:
        all_history = []
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, 'r') as f:
                all_history = json.load(f)
        
        detection_data['user_id'] = user_id
        detection_data['timestamp'] = datetime.now().isoformat()
        all_history.append(detection_data)
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(all_history, f, indent=2)
    except:
        pass


def get_leaderboard(limit=20):
    """Get top performers on the leaderboard."""
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, 'r') as f:
            all_history = json.load(f)
        
        user_stats = {}
        for record in all_history:
            user_id = record.get('user_id')
            if user_id not in user_stats:
                user_stats[user_id] = {
                    'user_id': user_id,
                    'total_detections': 0,
                    'avg_accuracy': 0,
                    'top_scale': None,
                }
            
            user_stats[user_id]['total_detections'] += 1
            if 'confidence' in record:
                current_accuracy = user_stats[user_id].get('avg_accuracy', 0)
                user_stats[user_id]['avg_accuracy'] = (
                    (current_accuracy + record['confidence']) / 2
                )
        
        sorted_users = sorted(
            user_stats.values(),
            key=lambda x: (x['total_detections'], x['avg_accuracy']),
            reverse=True
        )
        return sorted_users[:limit]
    except:
        return []


# Routes
@app.get("/")
def index():
    """Serve the home page."""
    return render_template('home.html')


@app.get("/detector")
def detector():
    """Serve the scale detector interface."""
    return render_template('index.html')


@app.get("/learn/scales")
def learn_scales():
    """Serve the scales library page with all 10 Thaats."""
    return render_template('learn/scales.html')


@app.get("/learn/fingering")
def learn_fingering():
    """Serve the Bansuri fingering guide."""
    return render_template('learn/fingering.html')


@app.get("/learn/videos")
def learn_videos():
    """Serve tutorial videos and learning resources."""
    return render_template('learn/videos.html')


@app.get("/learn/audio")
def learn_audio():
    """Serve audio examples for scale training."""
    return render_template('learn/audio.html')


@app.get("/profile")
def profile():
    """Serve the user profile page."""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())[:8]
    
    user_id = session['user_id']
    history = load_user_history(user_id)
    
    total_detections = len(history)
    favorite_scales = {}
    
    for record in history:
        scale = record.get('scale', 'Unknown')
        favorite_scales[scale] = favorite_scales.get(scale, 0) + 1
    
    top_scale = max(favorite_scales, key=favorite_scales.get) if favorite_scales else 'None'
    
    return render_template('user/profile.html', 
                         user_id=user_id, 
                         total_detections=total_detections,
                         top_scale=top_scale,
                         favorite_scales=favorite_scales)


@app.get("/history")
def history():
    """Serve the detection history page."""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())[:8]
    
    user_id = session['user_id']
    detection_history = load_user_history(user_id)
    detection_history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return render_template('user/history.html', 
                         user_id=user_id,
                         history=detection_history)


@app.get("/leaderboard")
def leaderboard():
    """Serve the leaderboard page with top performers."""
    top_performers = get_leaderboard()
    
    return render_template('user/leaderboard.html', 
                         leaderboard=top_performers)


@app.get("/about")
def about():
    """Serve the about page."""
    return render_template('pages/about.html')


@app.get("/faq")
def faq():
    """Serve the FAQ page."""
    return render_template('pages/faq.html')


@app.get("/contact")
def contact():
    """Serve the contact page."""
    return render_template('pages/contact.html')


@app.post("/api/detection/save")
def save_detection_to_user():
    """Save a detection result to user's history."""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())[:8]
    
    user_id = session['user_id']
    data = request.get_json()
    
    save_detection(user_id, data)
    
    return jsonify({'status': 'success', 'message': 'Detection saved to your dashboard'})


@app.post("/api/detection/export")
def export_detection():
    """Export detection results as JSON."""
    data = request.get_json()
    
    export_data = {
        'scale': data.get('scale'),
        'confidence': data.get('confidence'),
        'mode': data.get('mode'),
        'candidates': data.get('candidates', []),
        'exported_at': str(datetime.now().isoformat())
    }
    
    return jsonify(export_data)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "message": "Sonora API is running - Your gateway to perfect scale detection",
        "endpoints": ["/", "/detector", "/learn/scales", "/profile"],
    }


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors by serving a proper response."""
    # Try to serve a static file if it exists
    return render_template('home.html'), 404


# Vercel requires this as the module-level application
# This is the WSGI app that Vercel will execute
app = app
