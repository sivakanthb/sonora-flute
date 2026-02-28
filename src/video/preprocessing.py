import cv2
import numpy as np

def extract_frames(video_path, frame_rate=1):
    """
    Extract frames from a video file at a specified frame rate.

    Parameters:
    - video_path: str, path to the video file.
    - frame_rate: int, number of frames to extract per second.

    Returns:
    - frames: list of numpy arrays, extracted frames from the video.
    """
    frames = []
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, int((fps or 1) / frame_rate))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) % frame_interval == 0:
            frames.append(frame)

    cap.release()
    return frames

def normalize_image(image):
    """
    Normalize the image to have pixel values between 0 and 1.

    Parameters:
    - image: numpy array, the input image.

    Returns:
    - normalized_image: numpy array, the normalized image.
    """
    return image.astype(np.float32) / 255.0


def center_crop(image, width_ratio=0.7, height_ratio=0.5):
    height, width = image.shape[:2]
    crop_w = max(1, int(width * width_ratio))
    crop_h = max(1, int(height * height_ratio))

    x0 = (width - crop_w) // 2
    y0 = (height - crop_h) // 2
    return image[y0 : y0 + crop_h, x0 : x0 + crop_w]

def preprocess_video(video_path, frame_rate=1):
    """
    Preprocess the video by extracting and normalizing frames.

    Parameters:
    - video_path: str, path to the video file.
    - frame_rate: int, number of frames to extract per second.

    Returns:
    - preprocessed_frames: list of numpy arrays, normalized frames.
    """
    frames = extract_frames(video_path, frame_rate)
    preprocessed_frames = [normalize_image(center_crop(frame)) for frame in frames]
    return preprocessed_frames