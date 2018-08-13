#!/bin/bash
#=============================================================================
#File: uncompress.sh
#Usage: ./uncompress.sh
#Description: Extract GeoTIFF files of 2, 3, 4 and 5 bands (blue, green,
#			  red and infrared) from a tar.gz file in the current directory.
#			  The compressed file is removed after the files are extracted.
#=============================================================================
tar -xzvf *.tar.gz -C data --wildcards "*B2.TIF" "*B3.TIF" "*B4.TIF" "*B5.TIF"
rm *.tar.gz
echo "Raster files extracted and tar.gz file removed successfully"
