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
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle

np.random.seed(29123)

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
        """Perform the classification and/or cross validation"""
        def loadData(args):
            """Load the 2, 3, 4, and 5 raster bands and the training data. 
            Adding a feature from the NDVI to the raster bands is optional

            Args:
                args (obj): Arguments from argparse

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

        def preprocessData(raster, sample, args):
            """Set same size for raster and sample and take out pixels where there is no data
            in one of them. If n_data is equal or less than zero, it returns n_data values.
            
            Args:
                raster (obj): Raster in Numpy ndarray
                sample (obj): Sample in Numpy ndarray
                args (obj): arguments from argparse

            Returns:
                obj: X in Numpy ndarray
                obj: y in Numpy ndarray
            """
            rastertr = raster[slice(0,sample.shape[0]),slice(0,sample.shape[1]),:]
            X = rastertr[sample > 0,:]
            y = sample[sample > 0]

            y = y[X[...,0] > 0]
            X = X[X[...,0] > 0,:]

            slices = np.arange(y.shape[0])
            np.random.shuffle(slices)
            X_shuf = X[slices,:]
            y_shuf = y[slices]
            if args.n_data <= 0:
                X = X_shuf
                y = y_shuf
            else:
                X = X_shuf[:args.n_data,:]
                y = y_shuf[:args.n_data]
            
            return X, y

        def getPrediction(raster, X, y, args):
            """Train and classify raster and save the prediction as GeoTIFF in the data directory
            
            Args:
                raster (obj): Raster in Numpy ndarray
                X (obj): Sample in Numpy ndarray
                y (obj): Sample in Numpy ndarray
                args (obj): arguments from argparse
            """
            X_train, X_val, y_train, y_val = train_test_split(X, y, random_state=1273483)
            rf.fit(X_train,y_train)
            print("Model trained successfully")
            raster = np.nan_to_num(raster)
            prediction = rf.predict(raster.reshape(raster.shape[0]*raster.shape[1],raster.shape[2]))
            print("Accuracy: {}".format(metrics.accuracy_score(y_val, prediction)))
            print(metrics.classification_report(prediction, y_val))
            prediction = prediction.reshape(raster[...,0].shape)
            with rasterio.open(self.datadir + self.bandname + '2.TIF') as src:
                profile = src.profile.copy()
            profile.update(
                dtype=rasterio.uint8,
                count=1,
                compress='lzw')
            with rasterio.open(self.datadir + self.classificationfilename, 'w', **profile) as dst:
                dst.write(prediction, 1)
            print("Raster classified successfully")
            with open(self.datadir + "model_n{}_pt{}.pkl".format(args.n_estimators,args.n_data), "wb") as f:
                pickle.dump(rf, f)
            print("Model saved successfully")


        parser = argparse.ArgumentParser()
        parser.add_argument("--ndvi", help="add ndvi as new feature", action="store_true")
        parser.add_argument("--classify", help="classify scene", action="store_true")
        parser.add_argument("--n_estimators", help="number of estimators for random forrest classifier", required=True, type=int)
        parser.add_argument("--n_data", help="number of pixels for training", required=True, type=int)
        parser.add_argument("--validate", help="validate with 5 fold cross validation", action="store_true")
        args = parser.parse_args()

        raster, sample = loadData(args)

        X, y = preprocessData(raster, sample, args)

        rf = RandomForestClassifier(n_estimators = args.n_estimators)

        if args.validate:
            scores = cross_val_score(rf, X, y, cv=5)
            print("5 fold cross validation:")
            print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std()))

        if args.classify:
            getPrediction(raster, X, y, args)



if __name__ == "__main__":
    clf = Classification()
    clf.run()
