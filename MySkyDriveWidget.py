# -*- coding:utf-8 -*-

"""
@project: SkyDrive
@file: SkyDrive.py
@author: dangzhiteng
@email: 642212607@qq.com
@date: 2018-11-23
"""

import os
from Tools import get_pixmap
from resource import source_rc
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QProgressBar, \
                            QHBoxLayout, QPushButton, QLabel, QApplication, \
                            QVBoxLayout, QWidget, QRubberBand, QMenu, QAction, \
                            QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QColor, QDrag, QPainter, QCursor
from PyQt5.QtCore import Qt, QSize, QPoint, QRect, pyqtSignal

class MySkyDriveWidget(QWidget):

    def __init__(self):
        super(MySkyDriveWidget, self).__init__()
        main_layout = QHBoxLayout()
        self.select_type_widget = SelectTypeWidget()
        self.file_widget = FileWidget()
        main_layout.addWidget(self.select_type_widget)
        main_layout.addWidget(self.file_widget)
        self.setLayout(main_layout)
        main_layout.setStretchFactor(self.select_type_widget, 1)
        main_layout.setStretchFactor(self.file_widget, 5)
        self.select_type_widget.setObjectName('select_type')

        self.select_type_widget.itemClicked.connect(self.file_widget.filter_files)


class FileWidget(QListWidget):

    upload_signal = pyqtSignal(list, str)
    cd_folder_signal = pyqtSignal(str)
    def __init__(self):
        super(FileWidget, self).__init__()
        self.setAcceptDrops(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setIconSize(QSize(180, 180))
        self.setViewMode(QListWidget.IconMode)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setEditTriggers(self.NoEditTriggers)
        self.setDragEnabled(True)
        self.setDragDropMode(self.DragDrop)
        self.setSelectionMode(self.ContiguousSelection)
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        self.setSpacing(30)
        self._rubberPos = None
        self._rubberBand = QRubberBand(QRubberBand.Rectangle, self)

        self.brief_menu = QMenu(self)
        self.menu_open = QAction(QIcon(':/default/default_icons/open_normal.ico'), '打开')
        self.menu_download = QAction(QIcon(':/default/default_icons/download_normal.ico'), '下载')
        self.menu_share = QAction(QIcon(':/default/default_icons/share_normal.ico'), '分享')
        # self.menu_copy = QAction('复制')
        self.menu_move = QAction('移动到')
        self.menu_delete = QAction(QIcon(':/default/default_icons/delete_normal.ico'), '删除')
        self.menu_rename = QAction('重命名')
        self.menu_attribute = QAction('属性')
        self.brief_menu.addAction(self.menu_open)
        self.brief_menu.addSeparator()
        self.brief_menu.addAction(self.menu_download)
        self.brief_menu.addAction(self.menu_share)
        self.brief_menu.addSeparator()
        # self.brief_menu.addAction(self.menu_copy)
        self.brief_menu.addAction(self.menu_move)
        self.brief_menu.addSeparator()
        self.brief_menu.addAction(self.menu_delete)
        self.brief_menu.addAction(self.menu_rename)
        self.brief_menu.addAction(self.menu_attribute)

        self.extend_menu = QMenu(self)
        self.menu_upload = QAction(QIcon(':/default/default_icons/upload.ico'), '上传')
        self.menu_new_folder = QAction('新建文件夹')
        self.menu_refresh = QAction(QIcon(':/default/default_icons/refresh.ico'), '刷新')
        # menu_look = QAction('查看')
        # menu_sort_mode = QAction('排序方式')

        self.extend_menu.addAction(self.menu_upload)
        self.extend_menu.addAction(self.menu_new_folder)
        self.extend_menu.addSeparator()
        self.extend_menu.addAction(self.menu_refresh)
        # menu.addAction(menu_look)
        # menu.addAction(menu_sort_mode)

        self.itemDoubleClicked.connect(self.cd_folder)

    def list_file(self, file_list):
        self.clear()
        self.file_list = file_list
        for file in file_list.keys():
            self.file_list[file].append(os.path.splitext(file)[-1][1:])
            pixmap = get_pixmap(file, file_list[file][0])
            item = QListWidgetItem(QIcon(pixmap), file)
            item = QListWidgetItem(QIcon(pixmap), file)
            item.setSizeHint(QSize(200 ,200))
            self.addItem(item)
        self.add1item = QListWidgetItem(QIcon(':/default/default_pngs/add.png'), '添加文件')
        self.add1item.setSizeHint(QSize(200 ,200))
        self.addItem(self.add1item)

    def filter_file(self, type_list):
        self.clear()
        for file in self.file_list.keys():
            if self.file_list[file][4] not in type_list:
                continue
            pixmap = get_pixmap(file, self.file_list[file][0])
            item = QListWidgetItem(QIcon(pixmap), file)
            item = QListWidgetItem(QIcon(pixmap), file)
            item.setSizeHint(QSize(200 ,200))
            self.addItem(item)
        item = QListWidgetItem(QIcon(':/default/default_pngs/add.png'), '添加文件')
        item.setSizeHint(QSize(200 ,200))
        self.addItem(item)

    def filter_files(self, type_item):
        type_text = type_item.text().strip()
        if type_text == '全部文件':
            self.list_file(self.file_list)
        elif type_text == '图片':
            self.filter_file(['png', 'jpg', 'jpeg', 'bmp', 'gif', 'jpeg2000', 'tiff'])
        elif type_text == '视频':
            self.filter_file(['avi', 'mp4', 'mov', 'rmvb'])
        elif type_text == '文档':
            self.filter_file(['txt', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf'])
        elif type_text == '音乐':
            self.filter_file(['mp3', 'wav','flac'])
        elif type_text == '种子':
            self.filter_file(['bt'])
        elif type_text == '其他':
            pass        
        elif type_text == '隐藏空间':
            pass
        elif type_text == '我的分享':
            pass
        elif type_text == '回收站':
            pass

    def handle_action(self, select_type):
        if select_type == '打开':
            self.cd_folder()
        elif select_type == '下载':
            self.download([item.text() for item in self.selectedItems()])
        elif select_type == '分享':
            self.share([item.text() for item in self.selectedItems()])
        # elif select_type == '复制':
        #     pass
        elif select_type == '移动到':
            # 弹出选择框，选择目标文件夹
            pass
        elif select_type == '删除':
            self.delete(self.currentItem.text())
        elif select_type == '重命名':
            pass
            # 记录原始文件名
            # 设置当前item可编辑
            # 编辑完成出发更改槽，将原文件名和当前文件名发出
        elif select_type == '属性':
            pass
            # 弹出属性框
            # 先显示属性框，显示现有属性
            # 开启线程，获取其他属性
        elif select_type == '上传':
            self.upload()
            # 调用QFileDialog，选择文件上传
        elif select_type == '新建文件夹':
            # 新增名为新建文件夹的item，index为0，设置可编辑
            # setFlags(Qt::ItemIsEnabled|Qt::ItemIsEditable)
            # 编辑完成，发出新建信号
            # 设置不可编辑
            self.create_folder(self.item(0).text())
        elif select_type == '刷新':
            self.refresh_signal.emit()

    def cd_folder(self):
        self.cd_folder_signal.emit(self.currentItem().text())

    def download_files(self, file_list):
        self.download_signal.emit(file_list)

    def share(self, file_list):
        self.share_signal.emit(file_list)

    def move(self, file_source, file_target):
        pass

    def delete(self, file_list):
        self.delete_signal.emit(file_list)

    def rename(self, source_name, target_name):
        self.rename_sigan.emit(source_name, target_name)

    def attribute(self, file_name):
        self.attribute_signal.emit(file_name)

    def upload(self):
        file_list, ok = QFileDialog.getOpenFileNames(self, "多文件选择", "C:/", "All Files (*)")
        print(file_list)
        # self.upload_signal.emit(file_list)

    # 实现拖拽的时候预览效果图
    # 这里演示拼接所有的item截图(也可以自己写算法实现堆叠效果)
    def startDrag(self, supportedActions):
        items = self.selectedItems()
        drag = QDrag(self)
        mimeData = self.mimeData(items)
        # 由于QMimeData只能设置image、urls、str、bytes等等不方便
        # 这里添加一个额外的属性直接把item放进去,后面可以根据item取出数据
        mimeData.setProperty('myItems', items)
        drag.setMimeData(mimeData)
        pixmap = QPixmap(self.viewport().visibleRegion().boundingRect().size())
        pixmap.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        for item in items:
            rect = self.visualRect(self.indexFromItem(item))
            painter.drawPixmap(rect, self.viewport().grab(rect))
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(self.viewport().mapFromGlobal(QCursor.pos()))
        drag.exec_(supportedActions)

    def mousePressEvent(self, event):
        super(FileWidget, self).mousePressEvent(event)
        if event.buttons() == Qt.RightButton:
            file_item = self.itemAt(event.pos())
            if file_item:
                select_type = self.brief_menu.exec_(event.globalPos())
            else:
                select_type = self.extend_menu.exec_(event.globalPos())
            if select_type is not None:
                self.handle_action(select_type.text())
            else:
                print('右键菜单执行，但用户未选中。')
            return
        if event.buttons() != Qt.LeftButton or self.itemAt(event.pos()):
            return
        self._rubberPos = event.pos()
        self._rubberBand.setGeometry(QRect(self._rubberPos, QSize()))
        self._rubberBand.show()

    def mouseReleaseEvent(self, event):
        # 列表框点击释放事件,用于隐藏框选工具
        super(FileWidget, self).mouseReleaseEvent(event)
        self._rubberPos = None
        self._rubberBand.hide()

    def mouseMoveEvent(self, event):
        # 列表框鼠标移动事件,用于设置框选工具的矩形范围
        super(FileWidget, self).mouseMoveEvent(event)
        if self._rubberPos:
            pos = event.pos()
            lx, ly = self._rubberPos.x(), self._rubberPos.y()
            rx, ry = pos.x(), pos.y()
            size = QSize(abs(rx - lx), abs(ry - ly))
            self._rubberBand.setGeometry(
                QRect(QPoint(min(lx, rx), min(ly, ry)), size))

    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        path_list = [url.toLocalFile() for url in event.mimeData().urls()]
        try:
            target_folder = self.itemAt(event.pos()).text()
            if self.file_list[target_folder][0]:
                target_folder = ''
        except:
            target_folder = ''
        self.upload_signal.emit(path_list, target_folder)
        print('用户意图上传', path_list, '到', target_folder)


class SelectTypeWidget(QListWidget):

    def __init__(self):
        super(SelectTypeWidget, self).__init__()
        self.setViewMode(QListWidget.ListMode)
        self.setFlow(QListWidget.TopToBottom)
        self.setFocusPolicy(Qt.NoFocus)

        main_layout = QVBoxLayout()
        self.capacity_bar = QProgressBar()
        # 测试
        self.capacity_bar.setValue(30)
        capacity_layout = QHBoxLayout()
        # 测试
        self.capacity_info = QLabel('30G/100G')
        self.expand_capacity = QPushButton()
        capacity_layout.addWidget(self.capacity_info)
        capacity_layout.addStretch()
        capacity_layout.addWidget(self.expand_capacity)
        main_layout.addStretch()
        main_layout.addWidget(self.capacity_bar)
        main_layout.addLayout(capacity_layout)
        self.setLayout(main_layout)

        self.make_items()
        self.expand_capacity.setCursor(QCursor(Qt.PointingHandCursor))
        self.expand_capacity.setText('扩容')

    def make_items(self):
        url = ':/default/default_icons/'
        items = [QListWidgetItem(QIcon(url + 'files_normal.ico'), '全部文件', self),
                 QListWidgetItem('     图片', self),
                 QListWidgetItem('     视频', self),
                 QListWidgetItem('     文档', self),
                 QListWidgetItem('     音乐', self),
                 QListWidgetItem('     种子', self),
                 QListWidgetItem('     其他', self),
                 QListWidgetItem(QIcon(url + 'hide_space_normal.ico'), '隐藏空间', self),
                 QListWidgetItem(QIcon(url + 'share_normal.ico'), '我的分享', self),
                 QListWidgetItem(QIcon(url + 'trash_normal.ico'), '回收站')]
        for item in items:
            item.setSizeHint(QSize(100, 80))
            self.addItem(item)


if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MySkyDriveWidget()
    win.show()
    sys.exit(app.exec_())