import cv2
import numpy as np
import os
import glob

def create_sbs(left_img, right_img):
    """Combines left and right images side-by-side into a single frame."""
    return np.hstack((left_img, right_img))

def process_videos():
    # Explicit folder target inside input_2d space
    output_dir = "input_2d/output_3d"
    os.makedirs(output_dir, exist_ok=True)
    
    # Catch both lowercase and uppercase variations of common video files
    video_files = (
        glob.glob("input_2d/*.mp4") + 
        glob.glob("input_2d/*.mkv") + 
        glob.glob("input_2d/*.MP4") + 
        glob.glob("input_2d/*.MKV")
    )
    
    if not video_files:
        print("No videos found to convert inside 'input_2d/'")
        return

    for video_path in video_files:
        filename = os.path.basename(video_path)
        
        # Don't re-process an already rendered 3D clip
        if filename.startswith("3D_SBS_") or "output_3d" in video_path:
            continue
            
        output_path = os.path.join(output_dir, f"3D_SBS_{filename}")
        print(f"Processing: {filename}...")

        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        if width == 0 or height == 0:
            print(f"Error: Could not read video properties for {filename}")
            continue
            
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
