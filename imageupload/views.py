#coding=UTF-8
import keras
from django.shortcuts import render
from .form import UploadImageForm
from .models import Image

from extract_cnn import RESnet
import h5py
import os, sys

import numpy as np
import PIL.Image as image  # 加载pil的包
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import cv2



def index(request):
    """imgs upload"""
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            picture = Image(photo=request.FILES['image'])
            picture.save()

            dict = imageclassify(picture)
            return render(request, 'show.html', {'picture': picture, 'dict': dict})

    else:
        form = UploadImageForm()

    return render(request, 'index.html', {'form': form})


def store_pic(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            picture = Image(photo=request.FILES['image'])
            picture.save()
    return render(request, 'index.html',{'form': form})

def get_imlist(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]


'''
 Extract features and index the images
'''

def extract_feat():

    db = "binary"
    img_list = get_imlist(db)


    feats = []
    names = []

    model = RESnet()

    for i, img_path in enumerate(img_list):
        norm_feat = model.extract_feat(img_path)
        # print "This is norm_feat of %d" %(i+1)
        # print norm_feat

        img_name = os.path.split(img_path)[1]
        feats.append(norm_feat)
        names.append(img_name)

        #print "extracting feature from image No. %d , %d images in total" % ((i + 1), len(img_list))

    feats = np.array(feats)
    # directory for storing extracted features
    output = "featureTes.h5"
    # print output

    h5f = h5py.File(output, 'w')
    h5f.create_dataset('dataset_1', data=feats)
    h5f.create_dataset('dataset_2', data=names)
    h5f.close()

    return 0

def processData(filePath):
    f = open(filePath, 'rb')  # 以二进制读取文件
    data = []
    img = image.open(f)  # 返回图片的像素值
    m, n = img.size  # 返回图片的大小
    for i in range(m):
        for j in range(n):
            x, y, z = img.getpixel((i, j))
            data.append([x / 256.0, y / 256.0, z / 256.0])
    f.close()
    return np.mat(data), m, n

#for root, dirs, files in os.walk('./database')：
    #for file in files:
    #    print(file)

def process_pic():
    imgData, row, col = processData('./database/'+file)

    # 图像分割-Kmeans聚类
    label = KMeans(n_clusters=3).fit_predict(imgData)  # 图片聚成3类
    label = label.reshape([row, col])
    pic_new = image.new("L", (row, col))
    for i in range(row):  # 根据所属类别给图片添加灰度
        for j in range(col):
            pic_new.putpixel((i, j), int(256 / (label[i][j] + 1)))
    pic_new.save("./result/k-means/"+file, "JPEG")

    # 图像增强-二值化
    img = cv2.imread('./result/k-means/'+file)

    GrayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh1=cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY)
    ret,thresh2=cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY_INV)

    plt.savefig('./result/binary/'+file)

    return 0

def imageclassify(picture):
    keras.backend.clear_session()

    h5f = h5py.File('imageupload/featureR_binary.h5', 'r')
    feats = h5f['dataset_1'][:]
    imgNames = h5f['dataset_2'][:]
    h5f.close()

    pic_name=picture.photo.name
    #pic = pic_name[0:6]

    queryDir = './binary-1/%s' % (pic_name) #+ ".jpg"

    # 初始化模型
    model = RESnet()

    # 抽取图片特征
    queryVec = model.extract_feat(queryDir)

    #计算相似度
    scores = np.dot(queryVec, feats.T)
    rank_ID = np.argsort(scores)[::-1]
    rank_score = scores[rank_ID]

    # 选择前n相似度图片
    maxres =3
    imlist = [imgNames[index] for i,index in enumerate(rank_ID[1:maxres+1])]

    dict = []
    for i in range(0,3):
        dict.append([imlist[i],rank_score[i+1]])

    return dict












