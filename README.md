# this is a example for transform FDDB ellipse infomation
# to bbox (xml)

you need to download the files(dataset) of FDDB
http://vis-www.cs.umass.edu/fddb/

Translate ellipseList to annotation xml files:

```
python anno2xml.py [ellipseList]
```

list file were put in FDDB-folds 
(e.g. FDDB-fold-01-ellipseList.txt)
there are 01~10 ellipselist

the Annotations and JPGE will be fill with files
(adding new by index)

the avg w,h for FDDB face is:
(97.4,144.6)

| w         | h           | 
| ------------- |:-------------:| 
| 37.8       | 54.05 | 
| 80.8      | 120.0      | 
| 127.0 | 189.5      | 
| 198.41 | 296.33      | 

![alt tag](https://raw.githubusercontent.com/penolove/pyxml/master/FDDBwh.png)
