import cv2
import numpy as np
import os
import glob

def create_sbs(left_img, right_img):
    """Combines left and right images side-by-side."""
    return np.hstack((left_img, right_img))

def process_videos():
    # Force creation in the current root workspace directory
    os.makedirs("./output_3d", exist_ok=True)
    video_files = glob.glob("input_2d/.mp4") + glob.glob("input_2d/.mkv")
    
    if not video_files:
        print("No videos found to convert inside 'input_2d/'")
        return

    for video_path in video_files:
        filename = os.path.basename(video_path)
        output_path = os.path.join("./output_3d", f"3D_SBS_{filename}")
        print(f"Processing: {filename}...")

        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        sbs_width = width * 2
        out = cv2.VideoWriter(output_path, fourcc, fps, (sbs_width, height))
        
        shift_pixels = 15  
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            left_eye = frame.copy()
            M = np.float32([[1, 0, -shift_pixels],])
            right_eye = cv2.warpAffine(frame, M, (width, height))
            
            sbs_frame = create_sbs(left_eye, right_eye)
            out.write(sbs_frame)
            
        cap.release()
        out.release()
        print(f"Finished saving to {output_path}")

process_videos()
