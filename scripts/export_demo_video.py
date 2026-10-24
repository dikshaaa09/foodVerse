import os
import shutil
from PIL import Image, ImageSequence
import imageio

SOURCE_WEBP = r"C:\Users\divya\.gemini\antigravity-ide\brain\855f5d85-b91a-47ad-a824-de248e8966b7\foodverse_ui_test_1792837609778.webp"
TARGET_WEBP = r"d:\project2\food_verse_ai_demo.webp"
TARGET_MP4 = r"d:\project2\food_verse_ai_demo.mp4"
ASSETS_MP4 = r"d:\project2\assets\food_verse_ai_demo.mp4"

print("Copying animated WebP to project directory...")
shutil.copyfile(SOURCE_WEBP, TARGET_WEBP)
print(f"Copied WebP -> {TARGET_WEBP}")

print("Extracting frames and compiling 1.5-minute MP4 video...")
im = Image.open(SOURCE_WEBP)
n_frames = getattr(im, "n_frames", 1)
print(f"Total source frames: {n_frames}")

# Target duration: ~90 seconds (1.5 min)
# FPS = n_frames / 90
target_duration_sec = 90.0
fps = max(round(n_frames / target_duration_sec, 2), 1.0)
print(f"Calculated FPS for ~1.5 min duration: {fps} FPS")

import numpy as np

writer = imageio.get_writer(
    TARGET_MP4,
    fps=fps,
    codec="libx264",
    quality=8,
    pixelformat="yuv420p"
)

frame_idx = 0
for frame in ImageSequence.Iterator(im):
    # Ensure RGB
    rgb_frame = frame.convert("RGB")
    # Resize slightly if dimensions are odd (h.264 requires even dimensions)
    w, h = rgb_frame.size
    new_w = w if w % 2 == 0 else w - 1
    new_h = h if h % 2 == 0 else h - 1
    if (new_w, new_h) != (w, h):
        rgb_frame = rgb_frame.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    writer.append_data(np.array(rgb_frame))
    frame_idx += 1
    if frame_idx % 100 == 0:
        print(f"Processed {frame_idx}/{n_frames} frames...")

writer.close()
print(f"MP4 export successfully completed: {TARGET_MP4}")

# Copy to assets as well
shutil.copyfile(TARGET_MP4, ASSETS_MP4)
print(f"Copied MP4 to assets -> {ASSETS_MP4}")

mp4_size_mb = os.path.getsize(TARGET_MP4) / (1024 * 1024)
webp_size_mb = os.path.getsize(TARGET_WEBP) / (1024 * 1024)
print(f"Output files:\n - {TARGET_MP4} ({mp4_size_mb:.2f} MB, duration ~{n_frames/fps:.1f}s)\n - {TARGET_WEBP} ({webp_size_mb:.2f} MB)")
