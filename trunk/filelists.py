#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elementtree.ElementTree as ET


#fileHandle = open ( 'yepp.txt','r' )
#mstring=fileHandle.read()
#fileHandle.close()
root = ET.ElementTree('yepp.txt')
#ET.fromstring(mstring)
#ET.dump(root)
lst = root.findall("Direcory/File")
print len(lst)
for item in lst:
    print item.attrib["Size"]

