from pathlib import Path
import sys

# Add src to path
src_dir = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_dir))

# Simple WSGI application
def application(environ, start_response):
    """WSGI application for Vercel."""
    path = environ.get('PATH_INFO', '/')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # Try to serve Flask app
    try:
        from flask import Flask, render_template
        
        app = Flask(
            __name__,
            template_folder=str(src_dir / 'templates'),
            static_folder=str(src_dir / 'static'),
            static_url_path='/static'
        )
        
        @app.route('/')
        def home():
            return render_template('home.html')
        
        @app.route('/detector')
        def detector():
            return render_template('index.html')
        
        @app.route('/learn/scales')
        def learn_scales():
            return render_template('learn/scales.html')
        
        @app.route('/learn/fingering')
        def learn_fingering():
            return render_template('learn/fingering.html')
        
        @app.route('/learn/videos')
        def learn_videos():
            return render_template('learn/videos.html')
        
        @app.route('/learn/audio')
        def learn_audio():
            return render_template('learn/audio.html')
        
        @app.route('/profile')
        def profile():
            return render_template('user/profile.html', user_id='test', total_detections=0, top_scale='None', favorite_scales={})
        
        @app.route('/history')
        def history():
            return render_template('user/history.html', user_id='test', history=[])
        
        @app.route('/leaderboard')
        def leaderboard():
            return render_template('user/leaderboard.html', leaderboard=[])
        
        @app.route('/about')
        def about():
            return render_template('pages/about.html')
        
        @app.route('/faq')
        def faq():
            return render_template('pages/faq.html')
        
        @app.route('/contact')
        def contact():
            return render_template('pages/contact.html')
        
        @app.route('/<path:path>')
        def catch_all(path):
            return render_template('home.html')
        
        @app.errorhandler(404)
        def handle_404(e):
            return render_template('home.html'), 200
        
        # Process request through Flask
        return app(environ, start_response)
        
    except Exception as e:
        # Fallback error response if Flask fails
        error_msg = f"Error: {str(e)}\nPath: {src_dir}".encode()
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [error_msg]


# Also export as 'app' for Vercel's handler discovery
try:
    from flask import Flask, render_template
    
    app = Flask(
        __name__,
        template_folder=str(src_dir / 'templates'),
        static_folder=str(src_dir / 'static'),
        static_url_path='/static'
    )
    
    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/detector')
    def detector():
        return render_template('index.html')
    
    @app.route('/learn/scales')
    def learn_scales():
        return render_template('learn/scales.html')
    
    @app.route('/learn/fingering')
    def learn_fingering():
        return render_template('learn/fingering.html')
    
    @app.route('/learn/videos')
    def learn_videos():
        return render_template('learn/videos.html')
    
    @app.route('/learn/audio')
    def learn_audio():
        return render_template('learn/audio.html')
    
    @app.route('/profile')
    def profile():
        return render_template('user/profile.html', user_id='test', total_detections=0, top_scale='None', favorite_scales={})
    
    @app.route('/history')
    def history():
        return render_template('user/history.html', user_id='test', history=[])
    
    @app.route('/leaderboard')
    def leaderboard():
        return render_template('user/leaderboard.html', leaderboard=[])
    
    @app.route('/about')
    def about():
        return render_template('pages/about.html')
    
    @app.route('/faq')
    def faq():
        return render_template('pages/faq.html')
    
    @app.route('/contact')
    def contact():
        return render_template('pages/contact.html')
    
    @app.route('/<path:path>')
    def catch_all(path):
        return render_template('home.html')
    
    @app.errorhandler(404)
    def handle_404(e):
        return render_template('home.html'), 200

except Exception as e:
    # If Flask setup fails, create a dummy app
    def app(environ, start_response):
        status = '500 Internal Server Error'
        body = f'Flask setup error: {str(e)}'.encode()
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [body]



