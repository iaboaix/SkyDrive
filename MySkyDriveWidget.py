# -*- coding:utf-8 -*-
import os
from resource import source_rc
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QProgressBar, \
                            QHBoxLayout, QPushButton, QLabel, QApplication, \
                            QVBoxLayout, QWidget, QRubberBand, QMenu, QAction
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
        main_layout.setStretchFactor(self.select_type_widget, 2)
        main_layout.setStretchFactor(self.file_widget, 10)
        self.select_type_widget.setObjectName('select_type')


class FileWidget(QListWidget):

    upload_signal = pyqtSignal(list, str)
    def __init__(self, *args, **kwargs):
        super(FileWidget, self).__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.setFocusPolicy(Qt.NoFocus)
        self.setIconSize(QSize(180, 180))
        self.setViewMode(QListWidget.IconMode)
        # 隐藏横向滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 不能编辑
        self.setEditTriggers(self.NoEditTriggers)
        # 开启拖功能
        self.setDragEnabled(True)
        self.setDragDropMode(self.DragDrop)
        # 忽略放
        # self.setDefaultDropAction(Qt.IgnoreAction)
        # ****重要的一句（作用是可以单选，多选。Ctrl、Shift多选，可从空白位置框选）****
        # ****不能用ExtendedSelection,因为它可以在选中item后继续框选会和拖拽冲突****
        self.setSelectionMode(self.ContiguousSelection)
        # 设置从左到右、自动换行、依次排列
        self.setFlow(self.LeftToRight)
        self.setWrapping(True)
        self.setResizeMode(self.Adjust)
        # item的间隔
        self.setSpacing(30)
        # 橡皮筋(用于框选效果)
        self._rubberPos = None
        self._rubberBand = QRubberBand(QRubberBand.Rectangle, self)

    def list_file(self, file_list):
        for file in file_list.keys():
            file_type = os.path.splitext(file)[-1][1:]
            if file_list[file][0]:
                item = QListWidgetItem(QIcon(':/default/default_filetype/%s.png' % file_type), file)
            else:
                item = QListWidgetItem(QIcon(':/default/default_filetype/folder.png'), file)
            item.setSizeHint(QSize(200 ,200))
            self.addItem(item)
        item = QListWidgetItem(QIcon(':/default/default_pngs/add.png'), '添加文件')
        item.setSizeHint(QSize(200 ,200))
        self.addItem(item)

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
        if event.buttons() == Qt.RightButton and self.itemAt(event.pos()):
            menu = QMenu(self)
            menu_open = QAction(QIcon(':/default/default_icons/open_normal.ico'), '打开')
            menu_download = QAction(QIcon(':/default/default_icons/download_normal.ico'), '下载')
            menu_share = QAction(QIcon(':/default/default_icons/share_normal.ico'), '分享')
            menu_copy = QAction('复制')
            menu_cut = QAction('剪切')
            menu_move = QAction('移动到')
            menu_delete = QAction(QIcon(':/default/default_icons/delete_normal.ico'), '删除')
            menu_rename = QAction('重命名')
            menu_attribute = QAction('属性')

            menu.addAction(menu_open)
            menu.addAction(menu_download)
            menu.addAction(menu_share)
            menu.addAction(menu_copy)
            menu.addAction(menu_cut)
            menu.addAction(menu_move)
            menu.addAction(menu_delete)
            menu.addAction(menu_rename)
            menu.addAction(menu_attribute)

            menu.exec_(event.globalPos())
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
        except:
            target_folder = '根目录'
        self.upload_signal.emit(path_list, target_folder)
        print('用户拖拽', path_list, '到', target_folder)


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
        items = [QListWidgetItem(QIcon(url + 'recent_normal.ico'), '最近使用', self),
                 QListWidgetItem(QIcon(url + 'files_normal.ico'), '全部文件', self),
                 QListWidgetItem('\b\b\b\b图片', self),
                 QListWidgetItem('\b\b\b\b视频', self),
                 QListWidgetItem('\b\b\b\b文档', self),
                 QListWidgetItem('\b\b\b\b音乐', self),
                 QListWidgetItem('\b\b\b\b种子', self),
                 QListWidgetItem('\b\b\b\b其他', self),
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
    win = FileWidget()
    win.show()
    sys.exit(app.exec_())