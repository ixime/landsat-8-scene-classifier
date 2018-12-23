#!/bin/sh

if [ -z "$EEROW" ]
then
    echo "row is empty"; exit 1
else
    echo "row: $EEROW"
fi
if [ -z "$EEPATH" ]
then
    echo "path is empty"; exit 1
else
    echo "path: $EEPATH"
fi
if [ -z "$EEDATE" ]
then
    echo "date is empty"; exit 1
else
    echo "date: $EEDATE"
fi
if [ -z "$NDVI" ]
then
    NDVI=""
    echo "ndvi: False"
else
    if [ "$NDVI" = "True" ]
    then
        NDVI="--ndvi"
        echo "ndvi: True"
    else
        NDVI=""
        echo "ndvi: False"
    fi
fi
if [ -z "$CLASSIFY" ]
then
    CLASSIFY="--classify"
    echo "classify: True"
else
    if [ "$CLASSIFY" = "True" ]
    then
        CLASSIFY="--classify"
        echo "classify: True"
    else
        CLASSIFY=""
        echo "classify: False"
    fi
fi
if [ -z "$NESTIMATORS" ]
then
    NESTIMATORS="10"
    echo "n_estimators: 10"
else
    echo "n_estimators: $NESTIMATORS"
fi
if [ -z "$NDATA" ]
then
    NDATA="-1"
    echo "n_data: all"
else
    echo "n_data: $NDATA"
fi
if [ -z "$VALIDATE" ]
then
    VALIDATE=""
    echo "validate: False"
else
    if [ "$VALIDATE" = "True" ]
    then
        VALIDATE="--validate"
        echo "validate: True"
    else
        VALIDATE=""
        echo "validate: False"
    fi

fi
autopep8 --in-place --aggressive 01-download/download.py
python 01-download/download.py --row $EEROW --path $EEPATH --date $EEDATE
./01-download/uncompress.sh
autopep8 --in-place --aggressive 02-classification/random_forest.py
python 02-classification/random_forest.py $NDVI $CLASSIFY --n_estimators $NESTIMATORS $VALIDATE --n_data $NDATA

