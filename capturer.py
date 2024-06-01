# ---------------------------------------------------------------------------------------------------
# Este archivo contiene el módulo del capturador de imágenes y video del sistema
# ---------------------------------------------------------------------------------------------------
import cv2 

def process_video(video_path):
    video_capture = cv2.VideoCapture(video_path)
    
    frame_count = 0
    timestamps = []
    frames = []
    
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps) 
    
    while video_capture.isOpened():
        ret, frame = video_capture.read()
        
        if ret and frame_count % frame_interval == 0:
            frames.append(frame)
            timestamps.append(video_capture.get(cv2.CAP_PROP_POS_MSEC))
            
        frame_count += 1
        
        if not ret:
            break
    
    video_capture.release()
    cv2.destroyAllWindows()
    
    # Convert timestamps from milliseconds to minutes and seconds
    timestamps_min_sec = [(int(timestamp) // 60000, int((timestamp % 60000) / 1000)) for timestamp in timestamps]
    
    return frames, timestamps_min_sec

def process_image(image, timestamp):

    pass

# Example usage
video_path = "videos/video_1.mp4"
frames, timestamps = process_video(video_path)

for i, (frame, (minutes, seconds)) in enumerate(zip(frames, timestamps)):
    print(f"Frame {i} saved at timestamp {minutes} minutes and {seconds} seconds.")