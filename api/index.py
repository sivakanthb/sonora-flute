from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = '''
<!DOCTYPE html>
<html>
<head><title>Flute Scale Detector</title></head>
<body>
<h1>🎉 FLUTE SCALE DETECTOR IS LIVE!</h1>
<p style="font-size: 18px; color: green;">If you see this message, Python is working on Vercel!</p>
<p>Your deployment was successful!</p>
</body>
</html>
        '''
        self.wfile.write(html.encode())
    
    def do_POST(self):
        self.do_GET()










