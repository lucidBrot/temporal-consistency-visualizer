#!/usr/bin/env python3
import os
import re
from PIL import Image
import numpy as np
from multiprocessing import Pool
import argparse
import bisect

### <Stash of Paths>
PROGRESSIVE_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\progressive_video1_clip2")
INTERLACED_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\interlaced_video1_clip2")
ex4a_v2_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\results_drdbnet_vimeo90k_ex4a-v2_832920")
yadif_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\results_yadif")
ex8a_v1_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\weighted_ex8a-v1")
ex10a_v1_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\weighted_ex10a-v1_275000")
ex9b_v1_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\weighted_ex9b-v1_250000")
zhu_VID1_CLIP2 = os.path.normpath(r"N:\Temp\videos\video1_clip2\zhu")
BASEPATH = os.path.normpath(r"N:\Temp\videos\results")
### <Stash of Paths/>

THIS_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_OUTPUT_PATH = os.path.join(THIS_DIR_PATH, "outputs")
DEBUG = False
VERBOSE = True


def main( input_path, row = None, output_path = DEFAULT_OUTPUT_PATH, naming_postfix = "",
            first_filename = None, last_filename = None, stride = 1):
    """
        Args:
            input_path: Directory Path where all the input frames reside.
                        The frames are loaded only based on the number in the filename.

            row:        Which row to generate the figure for.
                        If `None`, a middle row is chosen.

            first_filename:         see below
            last_filename:      optional filters to only consider a certain range of frames.
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

    # make sure output path exists
    os.makedirs(output_path, exist_ok=True)

    # trim the list of filenames to the wished for range
    if stride is None:
        stride = 1
    if (not (first_filename is None and last_filename is None)) or stride != 1:
        first_index = 0 if first_filename is None else bisect.bisect_left(sorted_frame_filenames, first_filename)
        last_index = len(sorted_frame_filenames) if last_filename is None else bisect.bisect_left(sorted_frame_filenames, last_filename)
        sorted_frame_filenames = sorted_frame_filenames[first_index:last_index:stride]
        if VERBOSE:
            print(f"After applying the first_index/last_index/stride filters, {len(sorted_frame_filenames)} frames remain to be processed.")

    # prepare list of paths
    sorted_frame_paths = [ os.path.join(input_path, ff) for ff in sorted_frame_filenames ]

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
            arr = np.array(imgrow)
            return np.squeeze(arr, axis=0)

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
    np_arrays = list()
    for i in range(0, len(frame_paths), chunk_size):
        np_arrays_new = pool.map(work, [(xx, row) for xx in frame_paths[i : i + chunk_size]])
        np_arrays += np_arrays_new

    pool.close()
    pool.join()

    np_arrays = np.array(np_arrays)

    if DEBUG:
        print(f"{np_arrays.shape=}")
        print(f"{np_arrays[0][0]}")

    # turn the list of rows into a numpy array, then that into an image
    combined_img = Image.fromarray(np_arrays)
    combined_img.save(output_name, "PNG")

def forallmodels ( basepath, vid, clip, models = [], row = None ):
    """
        models:     A list of models to use, given the dict inside this function
                    where it is assumed that each path of the form
                    {basepath}/{the_dict[modelname]}/video{vid}/clip{clip}/ exists
    """
    # output directory with vid and clip name
    output_dir = os.path.join(DEFAULT_OUTPUT_PATH, f"video{vid}_clip{clip}")

    # dict with models and their paths
    the_dict = {
            'progressive': 'progressive',
            'interlaced': 'interlaced',
       }

    for model in models:
        assert model in the_dict.keys()

    for model in models:
        resdir = os.path.join(basepath, the_dict[model], f"video{vid}", f"clip{clip}")
        main ( input_path = resdir, row = row, naming_postfix = model, output_path = output_dir )

def runall ( vid, clip, row = None ):
    """
        To be called from the command line like
        python -c "import main as m; m.runall( vid = 5, clip = 0, row = 123 )"
        ... unless that requires that __file__ is set, perhaps?
    """
    models = [ 'progressive' ]
    forallmodels ( basepath = BASEPATH, vid = vid, clip = clip, row = row, models = models )

def argparse_runall ( args ):
    """
        wrapper function to avoid issue with argparse saying
        runall() missing 1 required positional argument: 'clip'
    """
    runall( args.vid, args.clip, args.row )

def argparse_main ( argz ):
    """
        wrapper function for argparse
    """
    # avoid unset values, use function's defaults instead
    argzz = vars(argz)
    args = { k: v for k, v in argzz.items() if v is not None and k != 'subcommand' and k != 'func' }
    main(**args)

def parse_args ():
    parser = argparse.ArgumentParser(description='Visualize temporal consistency as an image.')
    subparsers = parser.add_subparsers(dest = 'subcommand')

    # direct usage for just one video clip
    visualizer = subparsers.add_parser('visualise', aliases=['v', 'visualize'])
    visualizer.add_argument('-i', '--inputdir', type=str, metavar='INPUTPATH', required=True, dest='input_path', help="Path to the directory containing the numbered frames")
    visualizer.add_argument('-o', '--outputdir', type=str, metavar='OUTPUTPATH', required=False, dest='output_path', help="Path to the directory where the output should be saved in. (default: directly in ./outputs relative to main.py)", default=None)
    visualizer.add_argument('-r', '--row', type=int, metavar='R', default=None, help="Row to visualize change of. (default: middle row)", dest='row')
    visualizer.add_argument('-n', '--name', type=str, metavar='MODELNAME', default='', dest='naming_postfix', help="Postfix with MODELNAME will be added to generated files.")
    visualizer.add_argument('-b', '--start', '--begin', type=str, metavar='FIRST_FILENAME', default=None, dest='first_filename', help="Any files before this filename will be ignored.", required=False)
    visualizer.add_argument('-e', '--end', type=str, metavar='LAST_FILENAME', default=None, dest='last_filename', help="Any files after this filename will be ignored.", required=False)
    visualizer.add_argument('-s', '--stride', type=int, metavar='STRIDE', default=1, dest='stride', help="How many frames to skip in each step. (default 1)")
    visualizer.set_defaults(func=argparse_main)

    # used for my specific use case and format
    runaller   = subparsers.add_parser('runall', aliases=['r'])
    runaller.add_argument('-v', '--video', type=int, metavar='V', help="Number of the video", required=True, dest='vid')
    runaller.add_argument('-c', '--clip', type=int,  metavar='C', help="Number of the clip", required=True)
    runaller.add_argument('-r', '--row', type=int, default = None, metavar='R', help="Which row. Default is the middle row.", required=False)
    runaller.set_defaults(func=argparse_runall)

    parsing_failed = False
    args = parser.parse_args()

    if parsing_failed:
        parser.parse_args(['-h'])
    else:
        if args.subcommand is not None:
            #print(args)
            args.func(args)

if __name__ == "__main__":
    parse_args()
