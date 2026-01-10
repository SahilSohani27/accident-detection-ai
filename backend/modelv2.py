import os
from tabnanny import verbose
import cv2
import uuid
from ultralytics import YOLO

class AccidentDetector:
    def __init__(self, model_path: str):
        """
        Initializes the Accident Detector System with a trained YOLOv8 model.
        """
        self.model = YOLO(model_path)
        print(f"YOLOv8 model loaded from {model_path}")
        

    def detect_and_save_clip(
        self, video_source: str, save_folder: str,
        streak_threshold: int = 4, conf_threshold: float = 0.55,
        clip_duration: int = 10
    ):
        """
        Process video frame by frame.
        Detect accident only if it appears in N consecutive frames (streak_threshold).
        Once confirmed:
            - Save a 10-second clip as .mp4
            - Save the single frame with highest confidence as .jpg
        Returns:
            - accident_info dict
            - path to saved video
            - path to best frame image
        """
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        accident_detected = False
        accident_info = None
        accident_streak = 0
        last_xyxy, last_conf = None, 0.0

        cap = cv2.VideoCapture(video_source)
        frame_idx = 0
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25  # default fallback
        clip_frames = fps * clip_duration

        best_conf = 0.0
        best_frame = None

        # Generating unique ID for storing the clip and best frame
        unique_id = uuid.uuid4().hex[:8]

        video_path = os.path.join(save_folder, f"accident_clip_{unique_id}.mp4")
        best_frame_path = os.path.join(save_folder, f"best_frame_{unique_id}.jpg")
        out = None  # video writer

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model.predict(source=frame, conf=conf_threshold, stream=False, verbose=False)
            boxes = results[0].boxes

            accident_in_frame = False
            if boxes is not None:
                for box in boxes:
                    cls_id = int(box.cls[0].item())
                    conf = float(box.conf[0].item())
                    xyxy = box.xyxy[0].tolist()

                    if cls_id == 0 and conf >= conf_threshold:
                        accident_in_frame = True
                        last_xyxy, last_conf = xyxy, conf
                        break

            # Update streak
            if accident_in_frame:
                accident_streak += 1
            else:
                accident_streak = 0

            # Confirm accident if streak passes threshold
            if not accident_detected and accident_streak >= streak_threshold:
                accident_detected = True
                accident_info = {
                    "coordinates": last_xyxy,
                    "confidence": last_conf,
                    "frame_idx": frame_idx,
                }
                print(f"[INFO] Accident confirmed at frame {frame_idx} "
                      f"after {streak_threshold} consecutive detections, "
                      f"confidence {last_conf:.2f}")

                # Initialize video writer
                h, w = frame.shape[:2]
                fourcc = cv2.VideoWriter_fourcc(*'avc1')
                out = cv2.VideoWriter(video_path, fourcc, fps, (w, h))

                frames_remaining = clip_frames  # how many frames to capture

            # If accident is confirmed then start saving clip
            if accident_detected and out is not None and frames_remaining > 0:
                out.write(frame)
                frames_remaining -= 1

                # Track the best confidence frame
                if accident_in_frame and conf > best_conf:
                    best_conf = conf
                    best_frame = frame.copy()

                if frames_remaining == 0:
                    break

            frame_idx += 1

        cap.release()
        if out:
            out.release()

        # Save the best frame if found
        if best_frame is not None:
            cv2.imwrite(best_frame_path, best_frame)
        else:
            best_frame_path = None

        return accident_info, video_path if accident_detected else None, best_frame_path
