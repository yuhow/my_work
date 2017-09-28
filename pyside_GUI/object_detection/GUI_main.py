from __future__ import division
import sys, os, copy
from PySide.QtCore import *
from PySide.QtGui import *      # import QWidget
import re
import commands
import numpy as np

import random
import math
import itertools

import GUI_object_detection_tool as gui_od

import argparse
import time
import datetime

import getpass

#=====================================================#
#--------------------  ToolTab  ----------------------#
#=====================================================#
class ToolTab(QTabWidget):
    def __init__(self, parent = None):
        super(ToolTab, self).__init__(parent)

        self.object_detection_tool = gui_od.MainWindow(self)
        self.addTab(self.object_detection_tool, "Assistant Feature Keeper")

        self.currentChanged.connect(self.setTabTitle)
        self.setTabTitle()

    def setTabTitle(self):
        cindex = self.currentIndex()
        for i in range(self.count()):
            if i == cindex:
                self.tabBar().setTabTextColor(i, "blue")
            else:
                self.tabBar().setTabTextColor(i, "black")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Platform of Tensorflow Toolkits")
#        self.resize(785, 920)
#        self.setMinimumSize(500,700)
        self.setFixedSize(785, 920)
        self.tool = ToolTab(self)
        self.setCentralWidget(self.tool)

#        self.show()

    def closeEvent(self, event):
        result = QMessageBox.question(self,
                                      "Confirm Exit...",
                                      "Are you sure you want to exit ?",
                                      QMessageBox.Yes | QMessageBox.No)
        event.ignore()

        if result == QMessageBox.Yes:
            event.accept()


#=====================================================#

def main():
    # arguments
    parser = argparse.ArgumentParser()

    # type of process: A, B, C...
    #parser.add_argument('-p', '--process',  type=str, help="Type of PROCESS, which currently can be 'A', 'B', 'C'. The default is 'A'.")

    # sub-setting
    #parser.add_argument('-c',   '--cfg',     type=str, help="CFG is your job configuration file. The default is 'job_setting.cfg'.")

    # the other setting
    parser.add_argument('--no-preface',  action='store_true', help="disable splash screen in the starting stage")

    args = parser.parse_args()

    # GUI application
    app = QApplication([])
    #app = QApplication(sys.argv)
    app.setStyle("cleanlooks")

    img_splash = QPixmap("[PROJECT_ROOT_DIR]/icon/PTT_splash.png")
    splash_PTT = QSplashScreen(img_splash)
    #splash_PTT.setWindowFlags(splash_PTT.windowFlags() | Qt.WindowStaysOnTopHint)
    splash_PTT.setMask(img_splash.mask())

    if not args.no_preface:
        splash_PTT.show()
        time.sleep(3)  # this can be modified in the future

    ps_window = QDialog()
    ps_window.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
    #ps_window.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint | Qt.CustomizeWindowHint)
    #ps_window.resize(450, 300)
    ps_window.setFixedSize(450, 300)
    #ps_window.setWindowTitle('')

    plotListMainLayout = QVBoxLayout()
    plotListMainLayout.setAlignment(Qt.AlignLeft)
    plotListMainLayout.setContentsMargins(5,5,5,5)

    ps_window.setLayout(plotListMainLayout)
    plotListLabel = QLabel("                 LICENSED APPLICATION END USER LICENSE AGREEMENT")
    plotListMainLayout.addWidget(plotListLabel)

    plotList_widget = QWidget()
    plotList_layout = QVBoxLayout()
    plotList_layout.addStretch()
    plotList_layout.setAlignment(Qt.AlignCenter)
    plotList_layout.setContentsMargins(5,5,5,5)
    plotList_widget.setLayout(plotList_layout)

    allAnnotationContent = QTextEdit()
    readme = open('[PROJECT_ROOT_DIR]/AGREEMENT.txt', 'r')
    for line in readme.readlines():
        allAnnotationContent.append(line.rstrip('\n'))
    allAnnotationContent.setReadOnly(True)
    plotList_layout.addWidget(allAnnotationContent)

    ps_window.scrollAreaSetup = QScrollArea()
    ps_window.scrollAreaSetup.setWidget(plotList_widget)
    ps_window.scrollAreaSetup.setWidgetResizable(True)

    plotListMainLayout.addWidget(ps_window.scrollAreaSetup)
    plotListMainLayout.addStretch()

    ps_button_widget = QWidget()
    ps_button_layout = QHBoxLayout()
    ps_button_widget.setLayout(ps_button_layout)
    ps_selected_ok = QPushButton('agree')
    ps_selected_ok.setFixedWidth(100)
    ps_selected_ok.clicked.connect(ps_window.accept)
    ps_selected_no = QPushButton('disagree')
    ps_selected_no.setFixedWidth(100)
    ps_selected_no.clicked.connect(ps_window.reject)

    ps_button_layout.addWidget(ps_selected_ok)
    ps_button_layout.addWidget(ps_selected_no)

    plotListMainLayout.addWidget(ps_button_widget)

    if ps_window.exec_() == QDialog.Accepted:
        pass
    else:
        return

    ps_window.deleteLater()

    main = MainWindow()
    main.show()

    splash_PTT.finish(main)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
