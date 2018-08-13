"""
USGS Landsat 8 Scene Classification
02 Classification
Train and perform classification and/or validation with random forest algorithm 
for classification of a satellite GeoTIFF raster from Landsat 8. The data can be 
downloaded from USGS/EROS. Adding a feature by calculating the normalized difference
vegetation index (NDVI) is optional.
"""
import argparse
import os
import math
import rasterio
import re
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score


class Classification:
    """Random forest Classifier for a satellite GeoTIFF raster"""
    def __init__(self):
        """
        Args:
            bandname (str): Part of the band namefile
            datadir (str): Directory where the data is stored
            trainingfilename (str): training filename
            classificationfilename (str): prediction filename  
        """
        self.bandname = [fi[:-5] for fi in os.listdir('data') if fi.lower().endswith('b2.tif')][0]
        self.datadir = 'data/'
        self.trainingfilename = 'training.tif'
        self.classificationfilename = 'classification.tif'

    def run(self):
        """Perform the classification and/or validation"""
        def loadData(args):
            """Load the 2, 3, 4, and 5 raster bands and the training data. 
            Adding a feature from the NDVI to the raster bands is optional

            Args:
                args (obj): Arguments for argparse

            Returns:
                obj: Raster in Numpy ndarray
                obj: Sample in Numpy ndarray
            """
            lst = [] 
            for i in range(2,6):
                with rasterio.open(self.datadir + self.bandname + str(i) + '.TIF') as src:
                    lst.append(src.read(1))

            if args.ndvi:
                ndvi = getndvi(lst)
                lst.append(ndvi)
                print("Added NDVI feature successfully")

            with rasterio.open(self.datadir + self.trainingfilename) as src:
                sample = src.read(1)

            raster = np.stack(lst, axis=2)
            return raster, sample

        def getndvi(lst):
            """Calculate NDVI from 4th and 5th bands

            Args:
                lst (obj): List with bands in Numpy ndarray

            Returns:
                obj: NDVI in Numpy ndarray
            """
            RED = lst[2]
            NIR = lst[3]
            ndvi = NIR - RED / (NIR + RED)
            return ndvi

        def preprocessData(raster, sample):
            """Set same size for raster and sample and take out pixels where there is no data
            in one of them 
            
            Args:
                raster (obj): Raster in Numpy ndarray
                sample (obj): Sample in Numpy ndarray

            Returns:
                obj: X in Numpy ndarray
                obj: Y in Numpy ndarray
            """
            rastertr = raster[slice(0,sample.shape[0]),slice(0,sample.shape[1]),:]
            X = rastertr[sample > 0,:]
            Y = sample[sample > 0]

            Y = Y[X[...,0] > 0]
            X = X[X[...,0] > 0,:]
            
            return X, Y

        def getPrediction(raster, X, Y):
            """Train and classify raster and save the prediction as GeoTIFF in the data directory
            
            Args:
                raster (obj): Raster in Numpy ndarray
                X (obj): Sample in Numpy ndarray
                Y (obj): Sample in Numpy ndarray
            """
            rfp = rf.fit(X,Y)
            prediction = rfp.predict(raster.reshape(raster.shape[0]*raster.shape[1],raster.shape[2]))
            prediction = prediction.reshape(raster[...,0].shape)

            with rasterio.open(self.datadir + self.bandname + '2.TIF') as src:
                profile = src.profile.copy()
            profile.update(
                dtype=rasterio.uint8,
                count=1,
                compress='lzw')
            with rasterio.open(self.datadir + self.classificationfilename, 'w', **profile) as dst:
                dst.write(prediction, 1)


        parser = argparse.ArgumentParser()
        parser.add_argument("--ndvi", help="row of scene", required=False, default=False, type=bool)
        parser.add_argument("--classify", help="classify scene", required=False, default=True, type=bool)
        parser.add_argument("--n_estimators", help="number of estimators for random forrest classifier", required=False, default=10, type=int)
        parser.add_argument("--validate", help="validate with 5 fold cross validation", required=False, default=False, type=bool)
        args = parser.parse_args()
        raster, sample = loadData(args)
        X, Y = preprocessData(raster, sample)

        rf = RandomForestClassifier(n_estimators = args.n_estimators)

        if args.classify:
            getPrediction(raster, X, Y)
            print("raster classified successfully")

        if args.validate:
            scores = cross_val_score(rf, X, Y, cv=5)
            print("5 fold cross validation:")
            print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std()))




if __name__ == "__main__":
    cl = Classification()
    cl.run()
