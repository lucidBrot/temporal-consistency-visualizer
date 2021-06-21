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

