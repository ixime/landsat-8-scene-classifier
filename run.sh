#!/bin/sh

if [ -z "$EEROW" ]
then
    echo "row is empty"; exit 1
else
    echo $EEROW
fi
if [ -z "$EEPATH" ]
then
    echo "path is empty"; exit 1
else
    echo $EEPATH
fi
if [ -z "$EEDATE" ]
then
    echo "date is empty"; exit 1
else
    echo $EEDATE
fi
if [ -z "$NDVI" ]
then
    NDVI="FALSE"
else
    echo $NDVI
fi
if [ -z "$CLASSIFY" ]
then
    CLASSIFY="True"
else
    echo $CLASSIFY
fi
if [ -z "$NESTIMATORS" ]
then
    NESTIMATORS="10"
else
    echo $NESTIMATORS
fi
if [ -z "$VALIDATE" ]
then
    VALIDATE="False"
else
    echo $VALIDATE
fi
python 01-download/download.py --row $EEROW --path $EEPATH --date $EEDATE
./01-download/uncompress.sh
python 02-classification/random_forest.py --ndvi $NDVI --classify $CLASSIFY --n_estimators $NESTIMATORS --validate $VALIDATE


