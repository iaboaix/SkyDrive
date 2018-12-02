import os
from resource import source_rc
from PyQt5.QtGui import QPixmap

def get_pixmap(filename, isfile):
    if isfile:
        filetype = os.path.splitext(filename)[-1][1:]
        if filetype in ['txt']:
            return QPixmap(':/default/default_filetype/txt.png')
        elif filetype in ['ppt']:
            return QPixmap(':/default/default_filetype/ppt.png')
        elif filetype in ['doc', 'docx']:
            return QPixmap(':/default/default_filetype/docx.png')
        elif filetype in ['xls', 'xlsx']:
            return QPixmap(':/default/default_filetype/xlsx.png')
        elif filetype in ['png', 'jpg', 'jpeg']:
            return QPixmap(':/default/default_filetype/jpg.png')
        elif filetype in ['pdf']:
            return QPixmap(':/default/default_filetype/pdf.png')
        elif filetype in ['mp3']:
            return QPixmap(':/default/default_filetype/mp3.png')
        elif filetype in ['py']:
            return QPixmap(':/default/default_filetype/py.png')
        elif filetype in ['zip', 'rar', '7z']:
            return QPixmap(':/default/default_filetype/zip.png')
        elif filetype in ['link']:
            return QPixmap(':/default/default_filetype/zip.png')
        else:
            return QPixmap(':/default/default_filetype/unknown.png')
    else:
        return QPixmap(':/default/default_filetype/folder.png')

