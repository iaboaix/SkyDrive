# -*- coding:utf-8 -*-

"""
@project: SkyDrive
@file: SkyDrive.py
@author: dangzhiteng
@email: 642212607@qq.com
@date: 2018-11-23
"""

import os
from resource import source_rc
from PyQt5.QtGui import QPixmap

def get_pixmap(filename, isfile):
    if isfile:
        filetype = os.path.splitext(filename)[-1][1:].lower()
        if filetype in ['txt']:
            return QPixmap(':/default/default_filetype/txt.png')
        elif filetype in ['ppt', 'pptx']:
            return QPixmap(':/default/default_filetype/ppt.png')
        elif filetype in ['doc', 'docx']:
            return QPixmap(':/default/default_filetype/docx.png')
        elif filetype in ['xls', 'xlsx']:
            return QPixmap(':/default/default_filetype/xlsx.png')
        elif filetype in ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'jpeg2000', 'tiff']:
            return QPixmap(':/default/default_filetype/jpg.png')
        elif filetype in ['pdf']:
            return QPixmap(':/default/default_filetype/pdf.png')
        elif filetype in ['mp3', 'wav','flac']:
            return QPixmap(':/default/default_filetype/mp3.png')
        elif filetype in ['avi', 'mp4', 'mov', 'rmvb']:
            return QPixmap(':/default/default_filetype/avi.png')
        elif filetype in ['py']:
            return QPixmap(':/default/default_filetype/py.png')
        elif filetype in ['zip', 'rar', '7z']:
            return QPixmap(':/default/default_filetype/zip.png')
        elif filetype in ['link', 'html']:
            return QPixmap(':/default/default_filetype/link.png')
        elif filetype in ['exe']:
            return QPixmap(':/default/default_filetype/exe.png')
        elif filetype in ['apk']:
            return QPixmap(':/default/default_filetype/apk.png')
        else:
            return QPixmap(':/default/default_filetype/unknown.png')
    else:
        return QPixmap(':/default/default_filetype/folder.png')

