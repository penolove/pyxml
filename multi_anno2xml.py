
from lxml import etree
import sys
import cv2
import math
import glob

cur_ind=0
outfileID=len(glob.glob("JPEGImages/*.jpg"))


def img2xml(path,objects,shape,scale=1):
    root = etree.Element("annotation")
    folder = etree.SubElement(root, "folder")
    filename = etree.SubElement(root, "filename")
    source = etree.SubElement(root, "source")
    databases = etree.SubElement(source, "database")

    folder.text = "VOC2007"
    filename.text = str(path).zfill(6)
    databases.text = "FDDB"

    size = etree.SubElement(root, "size")
    width = etree.SubElement(size,"width")
    height = etree.SubElement(size,"height")
    depth = etree.SubElement(size,"depth")
    depth.text = str(shape[2])
    width.text = str(shape[1])
    height.text = str(shape[0])

    obj_count=0
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
        xmin_ = int(min(wid)/scale)
        xmax_ = int(max(wid)/scale)
        ymin_ = int(min(hei)/scale)
        ymax_ = int(max(hei)/scale)
        
        # check if out of box
        if(xmin_ >0 and ymin_>0 and xmax_<shape[1] and ymax_<shape[0] \
            and (xmax_-xmin_)+(ymax_-ymin_)>=20):
            obj_count+=1
            object_=etree.SubElement(root, "object")
            name=etree.SubElement(object_, "name")
            name.text="face"
            pose=etree.SubElement(object_, "pose")
            pose.text="Unspecified"
            truncated=etree.SubElement(object_, "truncated")
            truncated.text="0"
            difficult=etree.SubElement(object_, "difficult")
            difficult.text="0"
            # bndbox
            bndbox=etree.SubElement(object_, "bndbox")
            xmin=etree.SubElement(bndbox,"xmin")
            ymin=etree.SubElement(bndbox,"ymin")
            xmax=etree.SubElement(bndbox,"xmax")
            ymax=etree.SubElement(bndbox,"ymax")
            xmin.text = str(xmin_)
            ymin.text = str(ymin_)
            xmax.text = str(xmax_)
            ymax.text = str(ymax_)
    if obj_count>0:
        et = etree.ElementTree(root)
        et.write("Annotations/"+path+".xml", pretty_print=True)
        return True
    else: 
        return False

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
            wh.append([xmax-xmin,ymax-ymin])
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
    while (cur_ind<len(image_with_target)):
        path_img = '../'+image_with_target[cur_ind]+'.jpg'
        img = cv2.imread(path_img) 
        cur_ind+=1
        len_obj=int(image_with_target[cur_ind])
        cur_ind+=1
        objects=image_with_target[cur_ind:cur_ind+len_obj]
        cur_ind+=len_obj
        path=str(outfileID).zfill(6)
        if(img2xml(path,objects,img.shape)):
            cv2.imwrite("JPEGImages/"+path+".jpg", img)
            outfileID+=1
            path=str(outfileID).zfill(6)
            if(img2xml(path,objects,img.shape,2.0)):
                small = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
                cv2.imwrite("JPEGImages/"+path+".jpg", small)
                outfileID+=1
                path=str(outfileID).zfill(6)
                if(img2xml(path,objects,img.shape,3.0)):
                    small = cv2.resize(img, (0,0), fx=1/3.0, fy=1/3.0) 
                    cv2.imwrite("JPEGImages/"+path+".jpg", small)
                    outfileID+=1
