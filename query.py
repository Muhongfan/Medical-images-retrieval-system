# -*- coding: utf-8 -*-
from extract_cnn import RESnet

import numpy as np
import h5py

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-query", required = True,
	help = "Path to query which contains image to be queried")
#ap.add_argument("-index", required = True,
#	help = "Path to index")
ap.add_argument("-result", required = True,
	help = "Path for output retrieved images")
args = vars(ap.parse_args())


# read in indexed images' feature vectors and corresponding image names
#h5f = h5py.File(args["index"],'r')

h5f = h5py.File('featureRES.h5','r')
feats = h5f['dataset_1'][:]
imgNames = h5f['dataset_2'][:]
h5f.close()


"""
 img name - for its extraction
"""
queryDir = "./database"+"/"+"0000"+args["query"]+".jpg"

# show query image
queryImg = mpimg.imread(queryDir)
plt.title("Query Image")
plt.imshow(queryImg)
plt.show()

# init RESnet model
model = RESnet()

# extract query image's feature, compute simlarity score and sort
queryVec = model.extract_feat(queryDir)



scores = np.dot(queryVec, feats.T)
rank_ID = np.argsort(scores)[::-1]
rank_score = scores[rank_ID]
#print model.weight



print rank_ID
print rank_score


# number of top retrieved images to show
maxres = 3
imlist = [imgNames[index] for i,index in enumerate(rank_ID[1:maxres+1])]


print "top %d images in order are: " %maxres, imlist
#, model.predict()
 


"""

# show top #maxres retrieved result one by one
for i,im in enumerate(imlist):
    image = mpimg.imread(args["result"]+"/"+im)
    plt.title("search output %d" %(i+1))
    plt.imshow(image)
    plt.show()
"""