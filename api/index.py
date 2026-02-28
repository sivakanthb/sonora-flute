import sys
import os

# Add src directory to Python path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.app import app

# Export app for Vercel
__all__ = ['app']
