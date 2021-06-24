#!/usr/bin/env python3
from PIL import Image
import numpy as np
import os
import tempfile
from main import main, DEFAULT_OUTPUT_PATH

def test_order ():
    """
        1. Builds frames that are all black first, and all yellow later

        2. Runs the visualizer on this video

        3. Assert manually that the lower half of the image is yellow
    """
    num_frames = 10
    yellow_frame = np.full((100, 100, 3), np.array([0xff, 0xff, 0])).astype(np.uint8)
    black_frame = np.full((100, 100, 3), np.array([0, 0, 0])).astype(np.uint8)

    with tempfile.TemporaryDirectory() as dirpath:
        for i in range(num_frames//2):
            img = Image.fromarray(black_frame)
            img.save(os.path.join(dirpath, f"frame{i}.png"), "PNG")
        for i in range(num_frames//2+1, num_frames):
            img = Image.fromarray(yellow_frame)
            img.save(os.path.join(dirpath, f"frame{i}.png"), "PNG")

        # run visualizer
        main( dirpath, row = None, output_path = os.path.join(DEFAULT_OUTPUT_PATH, "testing"), naming_postfix = "test_order",
            first_filename = None, last_filename = None, stride = 1)

def test_solid ():
    """
        1. Builds frames that are all black except for a green line on row 10

        2. Runs the visualizer on this video, once on row 10 and once on row 11

        3. Manually check that row10 results in a solid green picture, and
            row11 results in a solid black picture
    """
    num_frames = 20
    colored_frame = np.full((100, 100, 3), np.array([0, 0, 0])).astype(np.uint8)
    colored_frame[10, :] = np.array([0, 0xff, 0], dtype=np.uint8)

    with tempfile.TemporaryDirectory() as dirpath:
        for i in range(num_frames):
            img = Image.fromarray(colored_frame)
            img.save(os.path.join(dirpath, f"frame{i}.png"), "PNG")

        # run visualizer
        main( dirpath, row = 11, output_path = os.path.join(DEFAULT_OUTPUT_PATH, "testing"), naming_postfix = "test_solid_black")
        main( dirpath, row = 10, output_path = os.path.join(DEFAULT_OUTPUT_PATH, "testing"), naming_postfix = "test_solid_green")

if __name__ == "__main__":
    test_order()
    test_solid()
