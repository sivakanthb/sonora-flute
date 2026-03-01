from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/api')
def home():
    return '''
<!DOCTYPE html>
<html>
<head><title>Flute Scale Detector</title></head>
<body>
<h1>🎉 FLUTE SCALE DETECTOR IS LIVE!</h1>
<p style="font-size: 18px; color: green;">If you see this message, Flask is working on Vercel!</p>
<p>Your deployment was successful!</p>
</body>
</html>
    '''










