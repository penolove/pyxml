
from lxml import etree
import sys
import cv2
import math
import glob
import csv

cur_ind=0
outfileID=len(glob.glob("JPEGImages/*.jpg"))



def face_box_wh(path,objects,shape):
    obj_count=0
    wh=list()
    for obj in objects:
        #object
        obj=[float(i) for i in obj.split()]
        #the smallest circumscribed parallelogram
        #[link] https://github.com/nouiz/lisa_emotiw/blob/master/emotiw/common/datasets/faces/FDDB.py
        maj_rad = obj[0]
        min_rad = obj[1]
        angle = obj[2]
        xcenter = obj[3]
        ycenter = obj[4]
        cosin = math.cos(math.radians(-angle))
        sin = math.sin(math.radians(-angle))

        x1 = cosin * (-min_rad) - sin * (-maj_rad) + xcenter
        y1 = sin * (-min_rad) + cosin * (-maj_rad) + ycenter
        x2 = cosin * (min_rad) - sin * (-maj_rad) + xcenter
        y2 = sin * (min_rad) + cosin * (-maj_rad) + ycenter
        x3 = cosin * (min_rad) - sin * (maj_rad) + xcenter
        y3 = sin * (min_rad) + cosin * (maj_rad) + ycenter
        x4 = cosin * (-min_rad) - sin * (maj_rad) + xcenter
        y4 = sin * (-min_rad) + cosin * (maj_rad) + ycenter
        wid=[x1,x2,x3,x4]
        hei=[y1,y2,y3,y4]
        xmin_ = int(min(wid))
        xmax_ = int(max(wid))
        ymin_ = int(min(hei))
        ymax_ = int(max(hei))
        
        # check if out of box
        if(xmin_ >0 and ymin_>0 and xmax_<shape[1] and ymax_<shape[0]):
            obj_count+=1
            wh.append([xmax_-xmin_,ymax_-ymin_])
    if obj_count>0:
        return wh
    else: 
        return list()



if __name__=="__main__":
    # you need to modify the path_img below
    # and the FDDB-fold-were assign by your own
    elliFold='FDDB-folds/'
    if len(sys.argv) < 2:
        ellipseList='FDDB-fold-01-ellipseList.txt'
    elif len(sys.argv)==2:
        ellipseList=sys.argv[1]
    else:
        print "usage : python example.py [ellipseList]"
    current_file=open(elliFold+ellipseList,'r')
    image_with_target=[i.replace('\n','') for i in current_file.readlines()]
    total_wh=list()
    while (cur_ind<len(image_with_target)):
        path_img = '../'+image_with_target[cur_ind]+'.jpg'
        img = cv2.imread(path_img) 
        cur_ind+=1
        len_obj=int(image_with_target[cur_ind])
        cur_ind+=1
        objects=image_with_target[cur_ind:cur_ind+len_obj]
        cur_ind+=len_obj
        path=str(outfileID).zfill(6)
        temp_whbx=face_box_wh(path,objects,img.shape)
        if(len(face_box_wh(path,objects,img.shape))>0):
            total_wh.extend(temp_whbx)

    with open("output.csv", "wb") as f:
         writer = csv.writer(f)
         writer.writerows(total_wh)

