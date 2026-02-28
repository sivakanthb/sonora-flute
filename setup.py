from setuptools import setup, find_packages

setup(
    name="flute-scale-detector",
    version="0.1.0",
    description="An application to identify the scale being played on a flute",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "Flask==2.3.3",
        "gunicorn==21.2.0",
        "numpy>=2.0",
        "scipy>=1.10",
        "librosa>=0.10",
        "opencv-python>=4.5",
        "tensorflow>=2.13",
        "pydub>=0.25",
        "soundfile>=0.12",
        "pytest>=7.0",
    ],
)
