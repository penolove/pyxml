from random import shuffle
import glob

dirPath='../JPEGImages/'

fileID=glob.glob(dirPath+"*.jpg")

x=[i.split('/')[2].replace('.jpg','') for i in fileID]

shuffle(x)
trainRatio=0.8
trainSize=int(len(x)*trainRatio)

#train
f=open('Main/trianval.txt','w')
for i in x[:trainSize]:
    f.write(i+'\n')
f.close()

#test

f=open('Main/test.txt','w')
for i in x[trainSize:]:
    f.write(i+'\n')
f.close()

