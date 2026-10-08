import cv2
import numpy as np
import os
import glob

def create_sbs(left_img, right_img):
    """Combines left and right images side-by-side into a single frame."""
    # Stack the two views horizontally next to each other
    sbs_frame = np.hstack((left_img, right_img))
    return sbs_frame

def process_videos():
    # Make sure output directory exists
    os.makedirs("output_3d", exist_ok=True)
    
    # Target any mp4 or mkv placed inside the input folder
    video_files = glob.glob("input_2d/.mp4") + glob.glob("input_2d/.mkv")
    
    if not video_files:
        print("No videos found to convert inside 'input_2d/'")
        return

    for video_path in video_files:
        filename = os.path.basename(video_path)
        output_path = os.path.join("output_3d", f"3D_SBS_{filename}")
        print(f"Processing: {filename} into Side-by-Side 3D...")

        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # NOTE: An SBS video is exactly TWICE as wide as the original video
        # because the left and right eyes are placed side-by-side.
        sbs_width = width * 2
        out = cv2.VideoWriter(output_path, fourcc, fps, (sbs_width, height))
        
        shift_pixels = 15  # Adjust this value to control depth perception
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Left Eye (Original frame perspective)
            left_eye = frame.copy()
            
            # Right Eye (Shifted frame perspective to create a 3D parallax effect)
            M = np.float32([[1, 0, -shift_pixels], [0, 1, 0]])
            right_eye = cv2.warpAffine(frame, M, (width, height))
            
            # Render into Side-by-Side format
            sbs_frame = create_sbs(left_eye, right_eye)
            out.write(sbs_frame)
            
        cap.release()
        out.release()
        print(f"Finished saving 3D SBS variant to {output_path}")

if _name_ == "_main_":
    process_videos()
