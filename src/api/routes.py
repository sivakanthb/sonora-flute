from flask import Blueprint, request, jsonify
from audio.preprocessing import preprocess_audio
from video.preprocessing import preprocess_video
from video.fingering_detection import detect_fingering
from models.inference import infer_scale_from_audio, infer_scale_from_video

import os
import tempfile

api = Blueprint('api', __name__)


def _save_uploaded_file(uploaded_file, suffix: str) -> str:
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    uploaded_file.save(path)
    return path


def _guess_suffix(filename: str, default_suffix: str) -> str:
    if not filename:
        return default_suffix
    _, ext = os.path.splitext(filename)
    return ext if ext else default_suffix

@api.route('/detect/audio', methods=['POST'])
def detect_audio_scale():
    audio_file = request.files.get('file')
    if not audio_file:
        return jsonify({'error': 'No audio file provided'}), 400

    temp_path = _save_uploaded_file(audio_file, _guess_suffix(audio_file.filename, '.wav'))
    try:
        sample_rate, audio_data = preprocess_audio(temp_path)
        result = infer_scale_from_audio(audio_data=audio_data, sample_rate=sample_rate)
        return jsonify(result)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@api.route('/detect/video', methods=['POST'])
def detect_video_scale():
    video_file = request.files.get('file')
    if not video_file:
        return jsonify({'error': 'No video file provided'}), 400

    temp_path = _save_uploaded_file(video_file, _guess_suffix(video_file.filename, '.mp4'))
    try:
        preprocessed_video = preprocess_video(temp_path)
        video_histogram = detect_fingering(preprocessed_video)
        result = infer_scale_from_video(video_histogram)
        result['frame_count'] = len(preprocessed_video)
        result['mode'] = 'video-heuristic'
        return jsonify(result)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)