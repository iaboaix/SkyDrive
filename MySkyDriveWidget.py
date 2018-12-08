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
                            QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QColor, QDrag, QPainter, QCursor
from PyQt5.QtCore import Qt, QSize, QPoint, QRect, pyqtSignal

class MySkyDriveWidget(QWidget):

    cur_path = ''
    upload_signal = pyqtSignal(list, str)
    cd_folder_signal = pyqtSignal(str)
    delete_signal = pyqtSignal(list)
    refresh_signal = pyqtSignal()
    rename_signal = pyqtSignal(str, str)
    mkdir_signal = pyqtSignal(str)

    def __init__(self):
        super(MySkyDriveWidget, self).__init__()
        # 工具栏
        tool_layout = QHBoxLayout()
        self.back_button = QPushButton('返回')
        self.upload_button = QPushButton('上传')
        self.download_button = QPushButton('下载')
        self.share_button = QPushButton('分享')
        self.delete_button = QPushButton('删除')
        self.mkdir_button = QPushButton('新建文件夹')
        self.move_button = QPushButton('移动')
        tool_layout.addWidget(self.back_button)
        tool_layout.addWidget(self.upload_button)
        tool_layout.addWidget(self.download_button)
        tool_layout.addWidget(self.share_button)
        tool_layout.addWidget(self.delete_button)
        tool_layout.addWidget(self.mkdir_button)
        tool_layout.addWidget(self.move_button)

        self.setAcceptDrops(True)
        # 显示QListWidgetItem
        self.list_widget = MyListWidget()
        # 接受拖放、可拖拽
        self.list_widget.setAcceptDrops(True)
        self.list_widget.setDragEnabled(True)
        self.list_widget.setDragDropMode(QListWidget.DragDrop)
        # 避免产生虚线
        self.list_widget.setFocusPolicy(Qt.NoFocus)
        # 设置大小
        self.list_widget.setIconSize(QSize(180, 180))
        # 设置查看模式（IconMode / ListMode）
        self.list_widget.setViewMode(QListWidget.IconMode)
        # 设置选择 单选/多选等
        self.list_widget.setSelectionMode(QListWidget.ContiguousSelection)
        self.list_widget.setFlow(QListWidget.LeftToRight)
        self.list_widget.setWrapping(True)
        self.list_widget.setResizeMode(QListWidget.Adjust)
        self.list_widget.setSpacing(30)
        # 鼠标穿透
        # self.list_widget.setAttribute(Qt.WA_TranslucentBackground, True)

        self.file_widget_layout = QVBoxLayout()
        self.file_widget_layout.addLayout(tool_layout)
        self.file_widget_layout.addWidget(self.list_widget)

        main_layout = QHBoxLayout()
        self.select_type_widget = SelectTypeWidget()
        main_layout.addWidget(self.select_type_widget)
        main_layout.addLayout(self.file_widget_layout)
        main_layout.setStretchFactor(self.select_type_widget, 1)
        main_layout.setStretchFactor(self.file_widget_layout, 5)
        self.setLayout(main_layout)

        # 定义一个右键文件或者文件夹的菜单
        self.brief_menu = QMenu(self)
        self.menu_open = QAction(QIcon(':/default/default_icons/open_normal.ico'), '打开')
        self.menu_download = QAction(QIcon(':/default/default_icons/download_normal.ico'), '下载')
        self.menu_share = QAction(QIcon(':/default/default_icons/share_normal.ico'), '分享')
        self.menu_move = QAction('移动到')
        self.menu_delete = QAction(QIcon(':/default/default_icons/delete_normal.ico'), '删除')
        self.menu_rename = QAction('重命名')
        self.menu_attribute = QAction('属性')
        self.brief_menu.addAction(self.menu_open)
        self.brief_menu.addSeparator()
        self.brief_menu.addAction(self.menu_download)
        self.brief_menu.addAction(self.menu_share)
        self.brief_menu.addSeparator()
        self.brief_menu.addAction(self.menu_move)
        self.brief_menu.addSeparator()
        self.brief_menu.addAction(self.menu_delete)
        self.brief_menu.addAction(self.menu_rename)
        self.brief_menu.addAction(self.menu_attribute)

        # 定义一个右键空白区域的菜单
        self.extend_menu = QMenu(self)
        self.menu_upload = QAction(QIcon(':/default/default_icons/upload.ico'), '上传')
        self.menu_new_folder = QAction('新建文件夹')
        self.menu_refresh = QAction(QIcon(':/default/default_icons/refresh.ico'), '刷新')
        self.extend_menu.addAction(self.menu_upload)
        self.extend_menu.addAction(self.menu_new_folder)
        self.extend_menu.addSeparator()
        self.extend_menu.addAction(self.menu_refresh)

        # 信号连接槽函数
        self.list_widget.itemDoubleClicked.connect(self.cd_folder)
        self.select_type_widget.itemClicked.connect(self.filter_files)
        self.list_widget.menu_signal.connect(self.show_menu)

        self.select_type_widget.setObjectName('select_type')


    def list_file(self, file_list):
        self.list_widget.clear()
        self.file_list = file_list
        for file in file_list.keys():
            self.file_list[file].append(os.path.splitext(file)[-1][1:])
            pixmap = get_pixmap(file, file_list[file][0])
            widget_item = FileItem(pixmap, file, file_list[file][0])
            widget_item.rename_signal.connect(self.rename)
            list_item = QListWidgetItem()
            list_item.setSizeHint(QSize(200, 200))
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, widget_item)
        widget_item = FileItem(QPixmap(':/default/default_pngs/add.png'), '添加文件', False)
        list_item = QListWidgetItem()
        list_item.setSizeHint(QSize(200, 200))
        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, widget_item)


    def filter_file(self, type_list):
        self.list_widget.clear()
        for file in self.file_list.keys():
            if self.file_list[file][4] not in type_list:
                continue
            pixmap = get_pixmap(file, self.file_list[file][0])
            item = QListWidgetItem(QIcon(pixmap), file)
            item = QListWidgetItem(QIcon(pixmap), file)
            item.setSizeHint(QSize(200 ,200))
            self.list_widget.addItem(item)
        widget_item = FileItem(QPixmap(':/default/default_pngs/add.png'), '添加文件', False)
        list_item = QListWidgetItem()
        list_item.setSizeHint(QSize(200, 200))
        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, widget_item)


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
            self.download([item.text() for item in self.list_widget.selectedItems()])
        elif select_type == '分享':
            self.share([item.text() for item in self.list_widget.selectedItems()])
        # elif select_type == '复制':
        #     pass
        elif select_type == '移动到':
            # 弹出选择框，选择目标文件夹
            pass
        elif select_type == '删除':
            self.delete()
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
            self.create_folder()
        elif select_type == '刷新':
            self.refresh_signal.emit()

    def cd_folder(self):
        self.cd_folder_signal.emit(self.itemWidget(self.list_widget.currentItem()).file_name)

    def download_files(self, file_list):
        self.download_signal.emit(file_list)

    def share(self, file_list):
        self.share_signal.emit(file_list)

    def create_folder(self):
        folder_name = '新建文件夹'
        if '新建文件夹' not in self.file_list:
            pass
        else:
            index = 1
            while True:
                folder_name = '新建文件夹({})'.format(index)
                index += 1
                if folder_name not in self.file_list:
                    break
        list_item = QListWidgetItem()
        list_item.setSizeHint(QSize(200, 200))
        widget_item = FileItem(get_pixmap('', False), folder_name, False)
        self.list_widget.insertItem(0, list_item)
        self.list_widget.setItemWidget(list_item, widget_item)
        self.mkdir_signal.emit(folder_name)

    def move(self, file_source, file_target):
        pass

    def delete(self):
        file_list = []
        for item in self.list_widget.selectedItems():
            cur_item = self.list_widget.itemWidget(item)
            file_list.append([cur_item.file_name, cur_item.file_type])
        print('用户删除', file_list)
        self.delete_signal.emit(file_list)

    def rename(self, source_name, target_name):
        self.rename_signal.emit(source_name, target_name)

    def attribute(self, file_name):
        self.attribute_signal.emit(file_name)

    def upload(self):
        file_list, ok = QFileDialog.getOpenFileNames(self, "多文件选择", "C:/", "All Files (*)")
        if ok:
            print(file_list)
            # 右键上传，默认上传至当前目录下。因此，target=''
            self.upload_signal.emit(file_list, '')
        else:
            print('用户打开上传文件框，并未选择文件。')


    def show_menu(self):
        file_item = self.list_widget.itemAt(self.list_widget.mapFromGlobal(QCursor.pos()))
        if file_item:
            select_type = self.brief_menu.exec_(QCursor.pos())
        else:
            select_type = self.extend_menu.exec_(QCursor.pos())
        if select_type is not None:
            self.handle_action(select_type.text())
        else:
            print('右键菜单执行，但用户未选中。')
        return

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
            target_folder = self.list_widget.itemAt(event.pos()).text()
            if self.file_list[target_folder][0]:
                target_folder = ''
        except:
            target_folder = ''
        self.upload_signal.emit(path_list, target_folder)
        print('用户意图上传', path_list, '到', target_folder if len(target_folder) != 0 else '当前目录')


class MyListWidget(QListWidget):
    menu_signal = pyqtSignal()
    def __init__(self):
        super(MyListWidget, self).__init__()
        # 左键矩形选择框
        self._rubberPos = None
        self._rubberBand = QRubberBand(QRubberBand.Rectangle, self)

    def mousePressEvent(self, event):
        super(MyListWidget, self).mousePressEvent(event)
        if event.buttons() == Qt.RightButton:
            self.menu_signal.emit()
            event.accept()
        else:
            event.ignore()

    def mouseReleaseEvent(self, event):
        # 列表框点击释放事件,用于隐藏框选工具
        super(MyListWidget, self).mouseReleaseEvent(event)
        self._rubberPos = None
        self._rubberBand.hide()

    def mouseMoveEvent(self, event):
        # 列表框鼠标移动事件,用于设置框选工具的矩形范围
        super(MyListWidget, self).mouseMoveEvent(event)
        if self._rubberPos:
            pos = self.mapFromGlobal(event.pos())
            lx, ly = self._rubberPos.x(), self._rubberPos.y()
            rx, ry = pos.x(), pos.y()
            size = QSize(abs(rx - lx), abs(ry - ly))
            self._rubberBand.setGeometry(
                QRect(QPoint(min(lx, rx), min(ly, ry)), size))


class FileItem(QWidget):

    rename_signal = pyqtSignal(str, str)
    def __init__(self, file_img, file_name, file_type):
        super(FileItem, self).__init__()
        self.file_name = file_name
        self.file_type = file_type
        main_layout = QVBoxLayout()
        file_image = QLabel()
        file_image.setPixmap(file_img)
        file_image.setAlignment(Qt.AlignCenter)
        self.file_name_line = QLineEdit(file_name)
        self.file_name_line.setAlignment(Qt.AlignCenter)
        self.file_name_line.setFrame(False)
        main_layout.addWidget(file_image)
        main_layout.addWidget(self.file_name_line)
        self.setLayout(main_layout)

        self.file_name_line.editingFinished.connect(self.rename)

        self.file_name_line.setObjectName('transparent')
        file_image.setObjectName('transparent')

    def rename(self):
        cur_name = self.file_name_line.text()
        if self.file_name != cur_name and len(cur_name) != 0:
            self.rename_signal.emit(self.file_name, cur_name)
            self.file_name = cur_name
        elif len(cur_name) == 0:
            QMessageBox.warning(self, 'warning', '文件/文件夹名不能为空！')


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