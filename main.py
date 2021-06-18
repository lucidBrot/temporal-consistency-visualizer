#!/usr/bin/env python3
import os
import re
from PIL import Image
import numpy as np
from multiprocessing import Pool

### <Stash of Paths>
PROGRESSIVE_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\progressive_video1_clip2")
INTERLACED_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\interlaced_video1_clip2")
ex4a_v2_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\results_drdbnet_vimeo90k_ex4a-v2_832920")
yadif_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\results_yadif")
ex8a_v1_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\weighted_ex8a-v1")
ex10a_v1_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\weighted_ex10a-v1_275000")
ex9b_v1_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\weighted_ex9b-v1_250000")
### <Stash of Paths/>

THIS_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_OUTPUT_PATH = os.path.join(THIS_DIR_PATH, "outputs")
DEBUG = False
VERBOSE = True


def main( input_path, row = None, output_path = DEFAULT_OUTPUT_PATH, naming_postfix = "" ):
    """
        Args:
            input_path: Directory Path where all the input frames reside.
                        The frames are loaded only based on the number in the filename.

            row:        Which row to generate the figure for.
                        If `None`, a middle row is chosen.
    """
    # verify if input path exists
    if not os.path.isdir(input_path):
        raise FileNotFoundError(f"Input Directory does not exist: {input_path}")

    # fetch all frame filenames and verify they only contain one number
    listed_dir = os.listdir(input_path)
    unexpected_format_pattern = re.compile('\d\D\d')
    not_a_number_pattern = re.compile('\D')
    assert all([unexpected_format_pattern.match(x) is None for x in listed_dir]
                   ), "The frames are loaded in the order of ONLY the only number in the filename, ignoring all other characters. If you have multiple separate numbers, sorry, but that's not yet implemented."
    sorted_frame_filenames = sorted(listed_dir, key=lambda f: int(not_a_number_pattern.sub('', f)))
    if DEBUG:
        print(f"{sorted_frame_filenames=}")
    sorted_frame_paths = [ os.path.join(input_path, ff) for ff in sorted_frame_filenames ]

    # make sure output path exists
    os.makedirs(output_path, exist_ok=True)

    # compute the middle row index if it is not set
    if row is None:
        with Image.open(sorted_frame_paths[0]) as im:
            w, h = im.size
            row = h//2
            assert row >= 0 and row < h

    # prepare name of output file
    output_name = os.path.join(output_path, f"row{row}__{naming_postfix}.png")

    # setup is done, perform the work
    combine_frame_rows( frame_paths = sorted_frame_paths, row = row, output_name = output_name )

    if VERBOSE:
        print(f"main() finished {row=} for {naming_postfix=}")

def get_row( frame_path, row ):
    """
        get the row of one image as an array
    """
    with Image.open( frame_path ) as im:
        w, h = im.size
        try:
            imgrow = im.crop((0, row, 0+w, 1+row))
            return np.array(imgrow)

        except Exception as e:
            print(f"{frame_path}: {w=}, {h=}, {row=}")
            raise e

def work ( some_tuple ):
    frame_path, row = some_tuple
    return get_row( frame_path, row )

def combine_frame_rows( frame_paths, row, output_name, chunk_size = 200 ):
    """
        multiprocessing for speed
    """

    pool = Pool()
    # limit number of same time, to avoid memory issues
    for i in range(0, len(frame_paths), chunk_size):
        np_arrays = pool.map(work, [(xx, row) for xx in frame_paths[i : i + chunk_size]])

    np_arrays = np.squeeze(np.array(np_arrays), axis=1)
    if DEBUG:
        print(f"{np_arrays.shape=}")
        print(f"{np_arrays[0][0]}")

    # turn the list of rows into a numpy array, then that into an image
    combined_img = Image.fromarray(np_arrays)
    combined_img.save(output_name, "PNG")

# TODO:
# * build a collected image for comparing, automatically
# * run on more videoclips and rows


if __name__ == "__main__":
    row = 300
    main( input_path = PROGRESSIVE_VID1_CLIP2, row=row, naming_postfix = 'progressive' )
    main( input_path = INTERLACED_VID1_CLIP2,  row=row, naming_postfix = 'interlaced' )
    main( input_path = ex4a_v2_VID1_CLIP2,     row=row, naming_postfix = 'ex4-v2' )
    main( input_path = yadif_VID1_CLIP2,       row=row, naming_postfix = 'yadif' )
    main( input_path = ex8a_v1_VID1_CLIP2,     row=row, naming_postfix = 'ex8a-v1' )
    main( input_path = ex10a_v1_VID1_CLIP2,    row=row, naming_postfix = 'ex10a-v1' )
    main( input_path = ex9b_v1_VID1_CLIP2,     row=row, naming_postfix = 'ex9b-v1' )
