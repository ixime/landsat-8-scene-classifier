# USGS Landsat 8 Scene Classification with Random Forest

This repository contains a docker for downloading one Landsat 8 OLI/TIRS C1 Level-1 GeoTIFF raster through the USGS/EROS API and for training, classifying and/or validating it using the random forest algorithm.  

For simplicity we use only the 2, 3, 4 and 5 bands during training.  

For better results it is possible to add the Normalized difference vegetation index (NDVI) as an extra feature for classification.  

## More information

### NDVI

The Normalized difference vegetation index is an indicator used for global vegetation monitoring. It is calculated based on the reflection in the red and near-infrared band from green vegetation which is higher than from clouds, water, rocks and soil.
It is obtained according:
```
NDVI = (NIR - RED) / (NIR + RED)
```

### Dealing with unbalanced data for random forest

Unbalanced data is a common problem in classification. It can be tackled in different ways. Among them there are two common approaches:

* Assign a high cost to missclasification of the minority incorporating class weights  
* Down-sampling majority classes ot over-sampling minority classes  

However, for simplicity this approaches were not implemented here.

## Requirements

* docker

## Installation

1. Clone or download this repository

2. Save the training GeoTIFF `training.tif` inside the `data` directory  

3. Register in [USGS](https://earthexplorer.usgs.gov/)  

4. Write the username and password in the `.env` file inside the `01-download` directory and change its permissions  
```
chmod 600 .env
```  

5. Build the docker from dockerfile  

```
docker build --tag usgs-landsat-8-classifier:0.1 --tag usgs-landsat-8-classifier:latest .
```
## Deploy

Run the docker  
NOTE 1: In the following command add values to the environment variables i.e. EEDATE, EEROW, etc.   
NOTE 2: The variables EEPATH, EEROW and EEDATE begin with EE to differentiate PATH from the PATH variable. They correspond to the row, path and date of the raster that is going to be downloaded.  
NOTE 3: The variable NESTIMATORS corresponds to the number of trees in the forest. If this environment variable is not added, the default value is 10.  
NOTE 4: NDVI indicates if the extra feature from NDVI is going to be added for training. CLASSIFY indicates if the classified raster `classification.tif` is going to be generated and VALIDATE if 5 fold cross validation is going to be performed. In case cross validation is performed, the accuracy will be showed in terminal. If these environment variables are not added, then they are not performed.  
NOTE 5: NDATA is the amount of data it is going to use for training and cross validation. If this environment variable is not added, all available data is used.  
```
docker run -it --env EEPATH=<value> --env EEROW=<value> --env EEDATE=<YYYY-MM-DD> --env NDVI=<bool> --env CLASSIFY=<bool> --env NESTIMATORS=<value> --env VALIDATE=<bool> --env NDATA=<value> --volume=`pwd`/data:/workspace/data --rm usgs-landsat-8-classifier
```
When it ends, if generated, the classified raster `classification.tif` and the model pickle  will be in the `data` directory.  

