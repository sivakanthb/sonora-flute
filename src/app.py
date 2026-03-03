import sys
from pathlib import Path
import json
import os

from flask import Flask, render_template, session, request, jsonify

# Add parent directory to path to enable src imports
sys.path.insert(0, str(Path(__file__).parent))

# Import routes after adding to path
from api.routes import api

# Get absolute paths for templates and static
PROJECT_ROOT = Path(__file__).parent
TEMPLATE_DIR = PROJECT_ROOT / 'templates'
STATIC_DIR = PROJECT_ROOT / 'static'

# Initialize Flask app with absolute paths
app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR),
    static_url_path='/static'
)

# Set a secret key for sessions (use environment variable in production)
app.secret_key = os.environ.get('SECRET_KEY', 'sonora-secret-key-2024')

# Production settings
app.config['ENV'] = os.environ.get('FLASK_ENV', 'development')
app.config['DEBUG'] = os.environ.get('FLASK_ENV', 'development') == 'development'

# Data file for storing user history
# On serverless platforms, use /tmp for ephemeral storage
if os.environ.get('VERCEL'):
    DATA_DIR = Path('/tmp/flute_data')
else:
    DATA_DIR = Path(__file__).parent / 'data'

DATA_DIR.mkdir(exist_ok=True)
HISTORY_FILE = DATA_DIR / 'detection_history.json'
USERS_FILE = DATA_DIR / 'users.json'


def load_user_history(user_id):
    """Load detection history for a user."""
    if not HISTORY_FILE.exists():
        return []
    
    with open(HISTORY_FILE, 'r') as f:
        all_history = json.load(f)
    
    return [h for h in all_history if h.get('user_id') == user_id]


def save_detection(user_id, detection_data):
    """Save a detection result to user history."""
    all_history = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r') as f:
            all_history = json.load(f)
    
    # Add new detection with timestamp
    import datetime
    detection_data['user_id'] = user_id
    detection_data['timestamp'] = datetime.datetime.now().isoformat()
    
    all_history.append(detection_data)
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(all_history, f, indent=2)


def get_leaderboard(limit=20):
    """Get top performers on the leaderboard."""
    if not HISTORY_FILE.exists():
        return []
    
    with open(HISTORY_FILE, 'r') as f:
        all_history = json.load(f)
    
    # Calculate stats per user
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
        
        # Track average accuracy if available
        if 'confidence' in record:
            current_accuracy = user_stats[user_id].get('avg_accuracy', 0)
            user_stats[user_id]['avg_accuracy'] = (
                (current_accuracy + record['confidence']) / 2
            )
    
    # Sort by total detections and accuracy
    sorted_users = sorted(
        user_stats.values(),
        key=lambda x: (x['total_detections'], x['avg_accuracy']),
        reverse=True
    )
    
    return sorted_users[:limit]

# Register API routes
app.register_blueprint(api)


@app.get("/")
def index():
    """Serve the Sonora home page with introduction to flutes."""
    return render_template('home.html')


@app.get("/detector")
def detector():
    """Serve the Sonora scale detector interface."""
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


@app.get("/learn/indian-scales")
def learn_indian_scales():
    """Serve the Indian classical scales page."""
    return render_template('learn/indian_scales.html')


@app.get("/learn/western-scales")
def learn_western_scales():
    """Serve the Western classical scales page."""
    return render_template('learn/western_scales.html')


@app.get("/test-upskill")
def test_upskill():
    """Test route for upskill page."""
    return render_template('learn/upskill.html')


@app.get("/learn/upskill")
def learn_upskill():
    """Serve the Upskill learning resources page with comprehensive learning resources."""
    return render_template('learn/upskill.html')


@app.get("/profile")
def profile():
    """Serve the user profile page."""
    from flask import session
    
    # Generate or get user ID from session
    if 'user_id' not in session:
        import uuid
        session['user_id'] = str(uuid.uuid4())[:8]
    
    user_id = session['user_id']
    history = load_user_history(user_id)
    
    # Calculate stats
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
    from flask import session
    
    if 'user_id' not in session:
        import uuid
        session['user_id'] = str(uuid.uuid4())[:8]
    
    user_id = session['user_id']
    detection_history = load_user_history(user_id)
    
    # Sort by timestamp descending (most recent first)
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


@app.get("/about/types-of-flutes")
def about_types_of_flutes():
    """Serve the types of flutes page."""
    return render_template('about/types_of_flutes.html')


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
    from flask import session
    
    if 'user_id' not in session:
        import uuid
        session['user_id'] = str(uuid.uuid4())[:8]
    
    user_id = session['user_id']
    data = request.get_json()
    
    save_detection(user_id, data)
    
    return jsonify({'status': 'success', 'message': 'Detection saved to your dashboard'})


@app.post("/api/detection/export")
def export_detection():
    """Export detection results as JSON."""
    data = request.get_json()
    
    # Create export with metadata
    export_data = {
        'scale': data.get('scale'),
        'confidence': data.get('confidence'),
        'mode': data.get('mode'),
        'candidates': data.get('candidates', []),
        'exported_at': str(__import__('datetime').datetime.now().isoformat())
    }
    
    return jsonify(export_data)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "message": "Sonora API is running - Your gateway to perfect scale detection",
        "endpoints": ["/", "/detector", "/detect/audio", "/detect/video"],
    }

if __name__ == "__main__":
    is_production = os.environ.get('FLASK_ENV') == 'production'
    app.run(debug=not is_production, host='0.0.0.0')