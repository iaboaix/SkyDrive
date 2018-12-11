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
from Tools import get_size
from resource import source_rc
from AttributeWidget import AttributeWidget
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QProgressBar, \
                            QHBoxLayout, QPushButton, QLabel, QApplication, \
                            QVBoxLayout, QWidget, QRubberBand, QMenu, QAction, \
                            QFileDialog, QLineEdit, QMessageBox, QGroupBox, \
                            QTextEdit, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap, QColor, QDrag, QPainter, QCursor
from PyQt5.QtCore import Qt, QSize, QPoint, QRect, pyqtSignal

class MySkyDriveWidget(QWidget):

    cur_path = ''
    upload_signal = pyqtSignal(list, str)
    request_down_signal = pyqtSignal(list)
    download_signal = pyqtSignal(list)
    cd_folder_signal = pyqtSignal(str)
    delete_signal = pyqtSignal(list)
    rename_signal = pyqtSignal(str, str)
    mkdir_signal = pyqtSignal(str)
    share_signal = pyqtSignal(list)

    def __init__(self):
        super(MySkyDriveWidget, self).__init__()
        self.factor = self.__width__ = QApplication.desktop().screenGeometry().width()/100
        # 工具栏
        tool_layout = QHBoxLayout()
        self.back_button = QPushButton('返回', clicked=self.back)
        self.upload_button = QPushButton('上传', clicked=self.upload)
        self.download_button = QPushButton('下载', clicked=self.request_down_files)
        self.share_button = QPushButton('分享', clicked=self.show_not_developed)
        self.delete_button = QPushButton('删除', clicked=self.delete)
        self.mkdir_button = QPushButton('新建文件夹', clicked=self.create_folder)
        self.move_button = QPushButton('移动', clicked=self.show_not_developed)
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
        # 接受托拽、 忽略放
        self.list_widget.setDragEnabled(True)
        self.list_widget.setDragDropMode(QListWidget.DragOnly)
        self.list_widget.setDefaultDropAction(Qt.IgnoreAction)

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
        self.list_widget.itemDoubleClicked.connect(self.double_click_item)
        self.list_widget.itemClicked.connect(self.check_is_upload)
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
            list_item.setSizeHint(QSize(self.factor * 8, self.factor * 8))
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, widget_item)
        add_file_widget = FileItem(QPixmap(':/default/default_pngs/add.png'), '添加文件', False)
        add_file_item = QListWidgetItem()
        add_file_item.setSizeHint(QSize(self.factor * 8, self.factor * 8))
        add_file_item.setFlags(add_file_item.flags() & ~Qt.ItemIsSelectable)
        self.list_widget.addItem(add_file_item)
        self.list_widget.setItemWidget(add_file_item, add_file_widget)

    def filter_file(self, type_list):
        self.list_widget.clear()
        for file in self.file_list.keys():
            if self.file_list[file][4] not in type_list:
                continue
            pixmap = get_pixmap(file, self.file_list[file][0])
            widget_item = FileItem(pixmap, file, self.file_list[file][0])
            widget_item.rename_signal.connect(self.rename)
            list_item = QListWidgetItem()
            list_item.setSizeHint(QSize(self.factor * 8, self.factor * 8))
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, widget_item)
        add_file_widget = FileItem(QPixmap(':/default/default_pngs/add.png'), '添加文件', False)
        add_file_item = QListWidgetItem()
        add_file_item.setSizeHint(QSize(self.factor * 8, self.factor * 8))
        # add_file_item.setFlags(add_file_item.flags() & ~Qt.ItemIsEnabled & ~Qt.ItemIsSelectable)
        add_file_item.setFlags(add_file_item.flags() & ~Qt.ItemIsSelectable)
        self.list_widget.addItem(add_file_item)
        self.list_widget.setItemWidget(add_file_item, add_file_widget)

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
            self.show_not_developed()
        elif type_text == '我的分享':
            self.show_not_developed()
        elif type_text == '回收站':
            self.show_not_developed()

    def handle_action(self, select_type):
        if select_type == '打开':
            self.double_click_item()
        elif select_type == '下载':
            self.request_down_files()
        elif select_type == '分享':
            self.share([item.text() for item in self.list_widget.selectedItems()])
        # elif select_type == '复制':
        #     pass
        elif select_type == '移动到':
            # 弹出选择框，选择目标文件夹
            self.show_not_developed()
        elif select_type == '删除':
            self.delete()
        elif select_type == '重命名':
            self.select_name()
        elif select_type == '属性':
            # 弹出属性框
            self.show_attribute()
        elif select_type == '上传':
            self.upload()
            # 调用QFileDialog，选择文件上传
        elif select_type == '新建文件夹':
            self.create_folder()
        elif select_type == '刷新':
            self.cd_folder()

    def show_not_developed(self):
        QMessageBox.information(self, '提示', '此项功能正在加紧开发中...')

    def show_attribute(self):
        file_name = self.list_widget.itemWidget(self.list_widget.currentItem()).file_name
        self.attribute = AttributeWidget(file_name, self.file_list[file_name], '我的网盘/' + self.cur_path)
        self.attribute.show()

    def select_name(self):
        item = self.list_widget.itemWidget(self.list_widget.currentItem()).file_name_line
        item.setFocus(Qt.MouseFocusReason)
        item.selectAll()

    def check_is_upload(self):
        item_name = self.list_widget.itemWidget(self.list_widget.currentItem()).file_name
        if item_name == '添加文件':
            self.upload()
            return

    def double_click_item(self):
        item_name = self.list_widget.itemWidget(self.list_widget.currentItem()).file_name
        if not self.file_list[item_name][0]:
            self.cd_folder(item_name)
        else:
            self.tip = QLabel(item_name + '已加入下载列表...', self.list_widget)
            # 此处应有提示框
            self.download_signal.emit([[item_name, self.file_list[item_name][3]]])

    def back(self):
        self.cur_path = os.path.split(self.cur_path)[0]
        self.cd_folder()

    def cd_folder(self, folder_name=''):
        if len(folder_name) != 0:
            self.cur_path = os.path.join(self.cur_path, folder_name)
        self.cd_folder_signal.emit(self.cur_path)

    def request_down_files(self):
        request_list = []
        add_list = []
        for item in self.list_widget.selectedItems():
            cur_item = self.list_widget.itemWidget(item)
            file_name = cur_item.file_name
            if cur_item.file_type:
                add_list.append([os.path.join(self.cur_path, file_name), self.file_list[file_name][3]])
            else:
                request_list.append(os.path.join(self.cur_path, file_name))
        self.download_signal.emit(add_list)
        if len(request_list) != 0:
            self.request_down_signal.emit(request_list)

    def share(self, file_list):
        self.share_signal.emit(file_list)
        self.show_not_developed()

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
        list_item.setSizeHint(QSize(self.factor * 8, self.factor * 8))
        widget_item = FileItem(get_pixmap('', False), folder_name, False)
        self.list_widget.insertItem(0, list_item)
        self.list_widget.setItemWidget(list_item, widget_item)
        self.mkdir_signal.emit(os.path.join(self.cur_path, folder_name))
        self.cd_folder()

    def move(self, file_source, file_target):
        pass

    def delete(self):
        file_list = []
        for item in self.list_widget.selectedItems():
            cur_item = self.list_widget.itemWidget(item)
            file_list.append([os.path.join(self.cur_path, cur_item.file_name), cur_item.file_type])
        print('用户删除', file_list)
        self.delete_signal.emit(file_list)
        self.cd_folder()

    def rename(self, source_name, target_name):
        self.rename_signal.emit(source_name, target_name)

    def attribute(self, file_name):
        self.attribute_signal.emit(file_name)

    def upload(self):
        file_list, ok = QFileDialog.getOpenFileNames(self, "多文件选择", "C:/", "All Files (*)")
        if ok:
            self.upload_signal.emit(file_list, self.cur_path)
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
        target_path = os.path.join(self.cur_path, target_folder)
        self.upload_signal.emit(path_list, target_path)
        print('用户意图上传', path_list, '到', target_folder if len(target_folder) != 0 else '当前目录')


    def set_size(self, info):
        self.select_type_widget.capacity_bar.setValue(info['USEDSIZE'] / (info['TOTALSIZE']*1024**3) * 100)
        self.select_type_widget.capacity_info.setText(\
        get_size(info['USEDSIZE']) + '/' + str(info['TOTALSIZE']) + 'GB')

    def set_notice_and_sharecode(self, notice, share_code):
        print('SHARECODE:', share_code)
        self.select_type_widget.text_edit.setText('    ' + notice)


class MyListWidget(QListWidget):
    menu_signal = pyqtSignal()
    def __init__(self):
        super(MyListWidget, self).__init__()
        # 避免产生虚线
        self.setFocusPolicy(Qt.NoFocus)
        # 设置查看模式（IconMode / ListMode）
        self.setViewMode(QListWidget.IconMode)
        # 设置选择 单选/多选等
        self.setSelectionMode(QListWidget.ContiguousSelection)
        self.setFlow(QListWidget.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(QListWidget.Adjust)
        self.setSpacing(30)


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
            pos = event.pos()
            lx, ly = self._rubberPos.x(), self._rubberPos.y()
            rx, ry = pos.x(), pos.y()
            size = QSize(abs(rx - lx), abs(ry - ly))
            self._rubberBand.setGeometry(
                QRect(QPoint(min(lx, rx), min(ly, ry)), size))

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


class FileItem(QWidget):

    rename_signal = pyqtSignal(str, str)
    def __init__(self, file_img, file_name, file_type):
        super(FileItem, self).__init__()
        self.file_name = file_name
        self.file_type = file_type

        file_image = QLabel()
        file_image.setPixmap(file_img)
        file_image.setAlignment(Qt.AlignCenter)
        self.file_name_line = QLineEdit(file_name)
        self.file_name_line.setContextMenuPolicy(Qt.NoContextMenu)
        self.file_name_line.setAlignment(Qt.AlignCenter)
        self.file_name_line.setFrame(False)

        main_layout = QVBoxLayout()
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
        self.factor = QApplication.desktop().screenGeometry().width()/100
        self.setViewMode(QListWidget.ListMode)
        self.setFlow(QListWidget.TopToBottom)
        self.setFocusPolicy(Qt.NoFocus)

        self.notice = QGroupBox('今日公告')
        self.notice.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout = QHBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)
        self.notice.setLayout(layout)

        capacity_layout = QHBoxLayout()
        self.capacity_bar = QProgressBar()
        self.capacity_info = QLabel()
        self.expand_capacity = QPushButton()
        capacity_layout.addWidget(self.capacity_info)
        capacity_layout.addStretch()
        capacity_layout.addWidget(self.expand_capacity)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.setSpacing(1)
        main_layout.addStretch()
        main_layout.addWidget(self.notice)
        main_layout.addWidget(self.capacity_bar)
        main_layout.addLayout(capacity_layout)
        self.setLayout(main_layout)

        self.make_items()
        self.expand_capacity.setCursor(QCursor(Qt.PointingHandCursor))
        self.expand_capacity.setText('扩容')
        self.notice.setFixedHeight(self.factor * 12)

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
            item.setSizeHint(QSize(self.factor * 3, self.factor * 2.5))
            self.addItem(item)


if __name__ == '__main__':
    import sys
    import qdarkstyle
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MySkyDriveWidget()
    win.show()
    sys.exit(app.exec_())