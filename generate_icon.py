# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generate_icon.py'
#
# Created: Fri Apr 21 10:35:41 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

import subprocess, os, codecs

images = os.listdir('./images')
f = open('images.qrc', 'wb+')
f.write(u'<!DOCTYPE RCC>\n<RCC version="1.0">\n<qresource>\n')

for item in images:
    f.write(u'<file alias="images/' + item + '">images/' + item + '</file>\n')

f.write(u'</qresource>\n</RCC>')
f.close()

pipe = subprocess.Popen(r'pyrcc4 -o images.py images.qrc', stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=0x08)
