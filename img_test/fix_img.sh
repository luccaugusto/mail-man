#!/bin/sh
# see https://imagemagick.org/Usage/distorts/#barrel
magick bbwf.png -virtual-pixel white -distort Barrel "0.0 0.0 -0.05 1.0 54 40" A.png
