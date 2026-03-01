import sys
from pathlib import Path

# Add src to path so we can import the Flask app
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from app import app

# Vercel expects the app to be exported as 'app'










