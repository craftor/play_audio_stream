# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
import sys
import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMainWindow, QAction, qApp 
from PyQt5.QtWidgets import QApplication, QCheckBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QTableWidget,QFrame,QAbstractItemView, QTableWidgetItem, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread, pyqtSignal

from Ui_main import Ui_Dialog

from scan import NmapScan

import subprocess
import paramiko
import datetime
import time

VERSION = 2.1

# 扫描局域网的线程
class ScanThread(QThread):
    # 使用信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    finishSignal = pyqtSignal(list)
    # 带参数示例
    def __init__(self, parent=None):
        super(ScanThread, self).__init__(parent)
        self.scan = NmapScan()

    def run(self):
        ip_list = self.scan.get_all_host()
        self.finishSignal.emit(ip_list)

# 更新ip的线程
class UpdateThread(QThread):
    finishSignal = pyqtSignal(str)
    def __init__(self, ip_list, parent=None):
        super(UpdateThread, self).__init__(parent)

        self.scan = NmapScan()
        self.ip_list = ip_list

    def run(self):
        self.scan.update_all(self.ip_list)
        self.finishSignal.emit("IP更新完成")

class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)

        # nmap扫描器
        self.scan = NmapScan()

        # 版本号
        title = "树莓派改IP小工具(for天立泰) v" + str(VERSION)
        self.setWindowTitle(title)

        # 初始化表格
        self.init_table()
        self.lines = []

    def log_print(self, str):
        """
        带时间日期的打印信息输出
        """
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
        msg = otherStyleTime + " - " + str
        self.textEdit.append(msg)

    def init_table(self):
        """
        初始化Table
        """
        self.tableWidget.setColumnCount(5)##设置表格一共有五列
        self.tableWidget.setHorizontalHeaderLabels(['原IP','新IP', '是否更新', 'Mac','Host'])#设置表头文字
        self.tableWidget.horizontalHeader().setSectionsClickable(False) #可以禁止点击表头的列
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

    def add_line(self, ip, mac, host):
        """
        增加一行
        """
        row = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row + 1)
        self.tableWidget.setItem(row,0,QTableWidgetItem(ip))
        self.tableWidget.setItem(row,1,QTableWidgetItem(ip))
        self.tableWidget.setItem(row,3,QTableWidgetItem(mac))
        self.tableWidget.setItem(row,4,QTableWidgetItem(host))

        ck = QCheckBox()
        h = QVBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(ck)
        w = QWidget()
        w.setLayout(h)
        self.tableWidget.setCellWidget(row,2,w)

        self.lines.append([ip, ip, ck, mac, host])

    def refresh_list(self, ip_list):
        """
        刷新IP List
        """
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        for row in ip_list:
            # 找出 Pi 主机
            if self.scan.check_pi(row[1], row[2]):
                self.add_line(row[0], row[1], row[2])
        self.log_print("扫描完成")
        self.pushButton_Refresh.setEnabled(True)

    def get_ip_list_to_update(self):
        """
        获取需要更新的IP list
        """
        ip_list = []
        for row in self.lines:
            try:
                if row[2].isChecked():
                    ip_list.append([row[0], row[1]])
            except Exception:
                pass
        return ip_list

    def update_all_finish(self, msg):
        """
        更新后的操作
        """
        self.pushButton_UpdateAll.setEnabled(True)
        self.log_print(msg)

    @pyqtSlot()
    def on_pushButton_ClearLog_clicked(self):
        """
        清空日志
        """
        self.textEdit.setText("")
    
    @pyqtSlot()
    def on_pushButton_Refresh_clicked(self):
        """
        刷新IP List
        """
        self.pushButton_Refresh.setEnabled(False)
        self.log_print("正在扫描局域网，请稍等...")
        self.tk1 = ScanThread()
        self.tk1.finishSignal.connect(self.refresh_list)
        self.tk1.start()

    @pyqtSlot()
    def on_pushButton_UpdateAll_clicked(self):
        """
        更新所有IP
        """
        self.pushButton_UpdateAll.setEnabled(False)
        self.log_print("正在更新IP，请稍等...")
        ip_list = self.get_ip_list_to_update()
        self.tk2 = UpdateThread(ip_list)
        self.tk2.finishSignal.connect(self.update_all_finish)
        self.tk2.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Dialog()
    main.show()
    sys.exit(app.exec_())
    
