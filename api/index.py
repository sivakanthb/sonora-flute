from http.server import BaseHTTPRequestHandler
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>🎉 FLUTE SCALE DETECTOR IS LIVE!</h1><p>Flask is working on Vercel!</p>'

@app.route('/test')
def test():
    return {'status': 'ok', 'message': 'Flask app is running successfully!'}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok","message":"Python is running!"}')
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>🎉 FLUTE SCALE DETECTOR IS LIVE!</h1><p>If you see this, Python is executing!</p>')
    
    def do_POST(self):
        self.do_GET()









