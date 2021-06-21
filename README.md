### Direct Usage



### Custom Quick Usage

Mainly for my own repeated usage:

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