from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>🎉 FLUTE SCALE DETECTOR IS LIVE!</h1><p>Flask is working on Vercel!</p>'

@app.route('/test')
def test():
    return {'status': 'ok', 'message': 'Flask app is running successfully!'}








