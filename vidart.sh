#!/bin/bash
# This file is about turning a video into art

# initialize
VIDNAME=''
FRAMEDIR=''
OUTDIR=''
COMBINE_FLAG=1
TARGETVIDNAME=''

# TODO: handle taking begin and end flags and pass them on to the visualizer
# TODO: handle stride argument for skipping frames
# TODO: handle stride bash argument for skipping rows
# TODO: test this file
# TODO: find out which rows to loop over.

# Usage code block based off kenorb's https://stackoverflow.com/a/34531699/2550406
usage() { echo "$0 usage:" && grep " .)\ #" $0; exit 0; }
[ $# -eq 0 ] && usage
while getopts ":hdv:o:Ct:" arg; do
  case $arg in
    f) # Specify frames folder path that contains frame%05d.png
        FRAMEDIR="$OPTARG"
      ;;
    t) # Specify location of final output video (Path including video filename. Must exist.)
        TARGETVIDNAME="$OPTARG"
      ;;
    v) # Decompose video into frames.
      VIDNAME="${OPTARG}"
      ;;
    o) # Output Directory for visualizer
        OUTDIR="$OPTARG"
      ;;
    C) # Skip combining back to video format
        COMBINE_FLAG=0
      ;;
    s) # (Useless Option): Specify strength, either 45 or 90.
      strength=${OPTARG}
      [ $strength -eq 45 -o $strength -eq 90 ] \
        && echo "Strength is $strength." \
        || echo "Strength needs to be either 45 or 90, $strength found instead."
      ;;
    h | *) # Display help.
      usage
      exit 1
      ;;
  esac
done

if [ -z "$FRAMEDIR" ] ;
then
    echo "Frame Dir Path -f is required."
    usage
fi

if $COMBINE_FLAG ;
then
    if [ -z "$TARGETVIDNAME" ] ;
    then
        echo "Target Video Path missing (-t)."
        usage
    fi
fi

if [ -z "$OUTDIR" ] ;
then
    echo "Output Dir Path -o is required."
    usage
fi
mkdir -p "$OUTDIR"

# split video into frames if needed
if [ -n "$VIDNAME" ] ;
then
    echo "decomposing video..." ;
    ffmpeg -i "${VIDNAME}" "${FRAMEDIR}/frame%05d.png" ; 
    echo "done decomposing." ;
fi

# use framedir as input directory to temporal-consistency-visualizer
# which is normally used like:  
### python main.py v -i "N:\Temp\ocean" -n ocean1 -o ".\example-outputs" -b frame00001.png -e frame00600.png -s 1
# TODO: loop over all rows
FINAL_ROW=40
for ((ROW=0;ROW<=FINAL_ROW;ROW++)); do
    python main.py v -i "$FRAMEDIR" -o "$OUTPUTDIR" -r "$ROW"
done

# combine video again
if $COMBINE_FLAG ;
then
    # the -c:v means it copies, I think. should be faster but cannot use filters.
    # https://stackoverflow.com/a/37478183/2550406
    ffmpeg -framerate 30 -pattern_type glob -i "${OUTPUTDIR}"'*.png' -c:v libx264 "${TARGETVIDNAME}"
fi

