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
    NDVI=""
else
    if [ "$NDVI" = "True" ]
    then
        NDVI="--ndvi"
    else
        NDVI=""
    fi
fi
if [ -z "$CLASSIFY" ]
then
    CLASSIFY="--classify"
else
    if [ "$CLASSIFY" = "True" ]
    then
        CLASSIFY="--classify"
    else
        CLASSIFY=""
    fi
fi
if [ -z "$NESTIMATORS" ]
then
    NESTIMATORS="10"
else
    echo $NESTIMATORS
fi
if [ -z "$VALIDATE" ]
then
    VALIDATE=""
else
    if [ "$VALIDATE" = "True" ]
    then
        VALIDATE="--validate"
    else
        VALIDATE=""
    fi

fi
python 01-download/download.py --row $EEROW --path $EEPATH --date $EEDATE
./01-download/uncompress.sh
python 02-classification/random_forest-test.py $NDVI $CLASSIFY --n_estimators $NESTIMATORS $VALIDATE


