"""
Vercel serverless function for Flute Scale Detector.
"""

from flask import Flask, render_template
from pathlib import Path
import os
import sys

# Setup paths
api_dir = Path(__file__).parent
project_root = api_dir.parent
src_dir = project_root / 'src'

print(f"API Dir: {api_dir}")
print(f"Project Root: {project_root}")
print(f"Src Dir: {src_dir}")
print(f"Templates exist: {(src_dir / 'templates').exists()}")
print(f"Static exists: {(src_dir / 'static').exists()}")

# Add to path
sys.path.insert(0, str(src_dir))

# Create Flask app
app = Flask(
    __name__,
    template_folder=str(src_dir / 'templates'),
    static_folder=str(src_dir / 'static'),
    static_url_path='/static'
)

app.secret_key = 'sonora-secret-2024'

# Test route
@app.route('/test')
def test():
    return {'status': 'Flask is working!', 'path': str(src_dir)}

# Home route
@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        return f'''
        <h1>Template Error</h1>
        <p>Error: {str(e)}</p>
        <p>Templates path: {src_dir / 'templates'}</p>
        <p>Path exists: {(src_dir / 'templates').exists()}</p>
        ''', 500

# All other routes
@app.route('/detector')
def detector():
    try:
        return render_template('index.html')
    except Exception as e:
        return render_template('home.html')

@app.route('/learn/scales')
def learn_scales():
    try:
        return render_template('learn/scales.html')
    except:
        return render_template('home.html')

@app.route('/learn/fingering')
def learn_fingering():
    try:
        return render_template('learn/fingering.html')
    except:
        return render_template('home.html')

@app.route('/learn/videos')
def learn_videos():
    try:
        return render_template('learn/videos.html')
    except:
        return render_template('home.html')

@app.route('/learn/audio')
def learn_audio():
    try:
        return render_template('learn/audio.html')
    except:
        return render_template('home.html')

@app.route('/profile')
def profile():
    try:
        return render_template('user/profile.html', user_id='test', total_detections=0, top_scale='None', favorite_scales={})
    except:
        return render_template('home.html')

@app.route('/history')
def history():
    try:
        return render_template('user/history.html', user_id='test', history=[])
    except:
        return render_template('home.html')

@app.route('/leaderboard')
def leaderboard():
    try:
        return render_template('user/leaderboard.html', leaderboard=[])
    except:
        return render_template('home.html')

@app.route('/about')
def about():
    try:
        return render_template('pages/about.html')
    except:
        return render_template('home.html')

@app.route('/faq')
def faq():
    try:
        return render_template('pages/faq.html')
    except:
        return render_template('home.html')

@app.route('/contact')
def contact():
    try:
        return render_template('pages/contact.html')
    except:
        return render_template('home.html')

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Flute Scale Detector is running'}

# Catch-all for any other route
@app.route('/<path:path>')
def catch_all(path):
    try:
        return render_template('home.html')
    except:
        return home()

@app.errorhandler(404)
def not_found(error):
    try:
        return render_template('home.html'), 200
    except:
        return home()


