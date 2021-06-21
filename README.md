![](./example-outputs/row540__ocean1old.png)

## Usage

Built for python 3.9.2.

If it does not work for your older python version, it might be enough to just comment out all print statements containing `=}`.

Assumes the frames are image files containing a single number in the filename, which is used for sorting them.

### Direct Usage

```bash
python main.py v -i"N:\Temp\videodir" -r400 -o ".\example-outputs"
```

or

```
python main.py visualize --inputdir "N:\Temp\videodir" --row 400 --outputdir ".\example-outputs"
```

#### Usage

```bash
#: python main.py v -h
usage: main.py visualise [-h] -i INPUTPATH [-o OUTPUTPATH] [-r R] [-n MODELNAME]
                         [-b FIRST_FILENAME] [-e LAST_FILENAME] [-s STRIDE]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTPATH, --inputdir INPUTPATH
                        Path to the directory containing the numbered frames
  -o OUTPUTPATH, --outputdir OUTPUTPATH
                        Path to the directory where the output should be saved in. (default:
                        directly in ./outputs relative to main.py)
  -r R, --row R         Row to visualize change of. (default: middle row)
  -n MODELNAME, --name MODELNAME
                        Postfix with MODELNAME will be added to generated files.
  -b FIRST_FILENAME, --start FIRST_FILENAME, --begin FIRST_FILENAME
                        Any files before this filename will be ignored.
  -e LAST_FILENAME, --end LAST_FILENAME
                        Any files after this filename will be ignored.
  -s STRIDE, --stride STRIDE
                        How many frames to skip in each step. (default 1)
```



### Custom Quick Usage

Mainly for my own repeated usage for visualizing the results of multiple models:

1. Specify the `BASEPATH` variable in the script to a place where directories exist like

   ```
   {basepath}/{modelname}/video{vid}/clip{clip}/
   ```

2. Modify the `the_dict` in `forallmodels` to map your `modelname`s to your model's directory. The `modelname` will be used for further displaying, file naming, and interaction.

3. ```bash
   python main.py r -v1 -c0 -r200
   # runs the visualization of all specified modelname's video1 clip0 on row 200
   # specifying row is optional
   # synonymous:
   python main.py runall --video 1 --clip 0 --row 200
   ```

#### Usage

```bash
#: python main.py r -h
usage: main.py runall [-h] -v V -c C [-r R]

optional arguments:
  -h, --help       show this help message and exit
  -v V, --video V  Number of the video
  -c C, --clip C   Number of the clip
  -r R, --row R    Which row. Default is the middle row.
```

## Examples

### Ocean 1

![](./example-outputs/row540__ocean1.png)

```bash
# get a video
youtube-dl https://www.youtube.com/watch?v=Mci4m-6WoyM -f bestvideo 
# split it into frames
ffmpeg -i Under\ The\ SEA\ 4K\ Underwater\ Wonders\ +\ Amazing\ Music\ -\ Coral\ Reefs\ \&\ Colorful\ Sea\ Life\ in\ UHD\ 🐟\ 🌊\ 🐠\ \[Mci4m-6WoyM\].webm frame%05d.png
# move the video file out of the way, it would confuse the script
mv Under\ The\ SEA\ 4K\ Underwater\ Wonders\ +\ Amazing\ Music\ -\ Coral\ Reefs\ \&\ Colorful\ Sea\ Life\ in\ UHD\ 🐟\ 🌊\ 🐠\ \[Mci4m-6WoyM\].webm ../video.webm
# take every frame (-s1) from the input directory (-i "N:\Temp\ocean") 
# that lies between(inclusive) the frame00001.png (-b) and the frame00600.png (-e)
# and save
# to the output directory (-o ".\example-outputs") an image file that shows
# how the middle row (omission of -r ROWNUMBER) changed over time
# with filename postfixed with ocean1 (-n)
python main.py v -i "N:\Temp\ocean" -n ocean1 -o ".\example-outputs" -b frame00001.png -e frame00600.png -s 1
main() finished row=540 for naming_postfix='ocean1'
```

This runs a while.

### Ocean 2

![](./example-outputs/row240__ocean2.png)

Same video, but this time with lower resolution, so it's faster.

```bash
# get video
youtube-dl https://www.youtube.com/watch?v=Mci4m-6WoyM -f 'bestvideo[height<=480]'
# this time we limit the threads to avoid the cpu being used at 100%
ffmpeg -threads 2 -i Under\ The\ SEA\ 4K\ Underwater\ Wonders\ +\ Amazing\ Music\ -\ Coral\ Reefs\ \&\ Colorful\ Sea\ Life\ in\ UHD\ 🐟\ 🌊\ 🐠\ \[Mci4m-6WoyM\].webm frame%05d.png
# we could also delete the video now, instead of moving it away
rm Under\ The\ SEA\ 4K\ Underwater\ Wonders\ +\ Amazing\ Music\ -\ Coral\ Reefs\ \&\ Colorful\ Sea\ Life\ in\ UHD\ 🐟\ 🌊\ 🐠\ \[Mci4m-6WoyM\].webm

# run the visualizer again, this time we want a square image.
# according to the output of the youtube-dl command, we've actually got a 854x480 video although we said the height should be at most 480 ??!
# so we make sure the range contains 480 frames I guess.
# I want to start at frame 12519.png and thus stop at frame 12999.png 
# because I'm still using a stride of 1.
python main.py v -i "N:\Temp\ocean2" -n ocean2 -o ".\example-outputs" -b frame12519.png -e frame12999.png -s 1
```



## Gallery

### Ocean 3

The below images all used the video here as source material:

> https://www.youtube.com/watch?v=Mci4m-6WoyM

![](./example-outputs/row540__oceana.png)

![](./example-outputs/row750__ocean1.png)

![row240__ocean2a](README.assets/row240__ocean2a.png)

![row240__ocean2e](README.assets/row240__ocean2e.png)

![row240__ocean2c](README.assets/row240__ocean2c.png)

![row240__ocean2b](README.assets/row240__ocean2b.png)

![row240__ocean2d](README.assets/row240__ocean2d.png)

also have a look at `row540__oceanb.png` which is too long for nice displaying in this readme, but should be found [here](./example-outputs/row540__oceanb.png).

### Fire

The following images use the video material from here:

> Video by **[Motion Places - Free Stock Video](https://www.pexels.com/@motion-places-free-stock-video-701499?utm_content=attributionCopyText&utm_medium=referral&utm_source=pexels)** from **[Pexels](https://www.pexels.com/photo/burning-firewood-1535674/?utm_content=attributionCopyText&utm_medium=referral&utm_source=pexels)**
>
> https://www.pexels.com/video/burning-firewood-1535674/

![row540__fireA](README.assets/row540__fireA.png)

![row1000__fireB](README.assets/row1000__fireB.png)

![row1__fireB](README.assets/row1__fireB.png)

