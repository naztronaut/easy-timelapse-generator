"""
Author: Nazmus Nasir and ChatGPT
Script Name: Easy Timelapse Generator
Website: https://www.Naztronomy.com
YouTube: https://www.youtube.com/Naztronomy

Description:
This script takes all the image files in a user-defined directory and turns them into a timelapse MP4 file.
The user can define the frames per second (FPS) and the output resolution (720p, 1080p, 2K, 4K).

Supported Image File Types:
- JPEG (.jpg, .jpeg)
- PNG (.png)
- Canon RAW (.cr2)
- Canon RAW 3 (.cr3)

Dependencies:
- Python 3.x
- OpenCV
- rawpy

Usage:
1. Place your image files in a directory.
2. Run the script and follow the prompts to specify the directory, output file name, FPS, and resolution.

"""

import cv2
import os
import rawpy
import numpy as np

def create_timelapse(directory, output_file, fps=30, resolution='1080p'):
    image_files = sorted([f for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.cr2', '.cr3'))])
    total_images = len(image_files)

    # Check if any image files are found in the directory
    if not total_images:
        print("No image files found in the directory.")
        return

    # Define the available resolution options
    resolution_options = {
        '720p': (1280, 720),
        '1080p': (1920, 1080),
        '2K': (2560, 1440),
        '4K': (3840, 2160)
    }

    # Validate and get the selected resolution
    if resolution not in resolution_options:
        print("Invalid resolution option. Supported options: 720p, 1080p, 2K, 4K.")
        return
    width, height = resolution_options[resolution]

    # Create the video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec (other options: XVID, MJPG, etc.)
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Iterate through each image file and write it to the video
    progress_counter = 0
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)

        # Check if the image file is a raw file
        if image_file.lower().endswith('.cr2') or image_file.lower().endswith('.cr3'):
            # Read the raw file using rawpy
            raw = rawpy.imread(image_path)

            # Convert the raw image to RGB
            rgb = raw.postprocess()

            # Resize the RGB image to match the desired resolution
            rgb = cv2.resize(rgb, (width, height))

            # Convert the RGB image to BGR (compatible with OpenCV)
            image = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

        else:
            # Read non-raw image files using OpenCV
            image = cv2.imread(image_path)

            # Resize the image to match the desired resolution
            image = cv2.resize(image, (width, height))

        # Write the image to the video
        video_writer.write(image)

        # Update progress counter and calculate percentage
        progress_counter += 1
        progress = (progress_counter / total_images) * 100

        # Print status update every 10% progress
        if progress_counter % (total_images // 10) == 0:
            print(f"Progress: {progress:.1f}%")

    # Release the video writer
    video_writer.release()
    print(f"Time-lapse video created: {output_file}")

# User-defined parameters
directory = input("Enter the directory path containing the image files: ")
output_file = input("Enter the output file name (e.g., output.mp4): ")
fps = int(input("Enter the frames per second (e.g., 30): "))
resolution = input("Enter the desired resolution (720p, 1080p, 2K, 4K): ")

# Create the time-lapse video
create_timelapse(directory, output_file, fps, resolution)
