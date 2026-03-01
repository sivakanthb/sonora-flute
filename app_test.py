from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Flute Scale Detector is LIVE! 🎉</h1><p>If you see this, the Flask app is working!</p>'

@app.route('/test')
def test():
    return {'status': 'ok', 'message': 'Flask is running!'}
