#--coding: utf-8 --
from __future__ import division
import sys, os, copy, getpass
import subprocess

from PySide.QtCore import *
from PySide.QtGui import *      # import QWidget

import re
import commands

from Asyncproc import AsyncProcessMonitor

import random
import math
import itertools

import matplotlib
matplotlib.rcParams['backend.qt4'] = 'PySide'

import datetime
import time

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.image as mpimg
import matplotlib.patches as patches

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
try:
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
except:
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import RectangleSelector
from numpy.compat import asbytes


#=====================================================#
#----------------------  APM  ------------------------#
#=====================================================#
class APM(AsyncProcessMonitor):
    def __init__(self, parent = None):
        super(APM, self).__init__(parent)


#=====================================================#
#--------------------  ToolTab  ----------------------#
#=====================================================#
class ToolTab(QTabWidget):
    def __init__(self, parent = None):
        super(ToolTab, self).__init__(parent = parent)
        self.parent = parent
        self.annotation = AnnotationWidget(self)
        self.addTab(self.annotation, "Annotation")
        self.objectDetection = ObjectDetectionWidget(self)
        self.addTab(self.objectDetection, "Modeling")
        self.modelPrediction = ModelPredictionWidget(self)
        self.addTab(self.modelPrediction, "Prediction")
        self.help = HelpWidget(self)
        self.addTab(self.help, "Help")
        self.currentChanged.connect(self.setTabTitle)
        self.setTabTitle()

    def setTabTitle(self):
        cindex = self.currentIndex()
        for i in range(self.count()):
            if i == cindex:
                self.tabBar().setTabTextColor(i, "blue")
            else:
                self.tabBar().setTabTextColor(i, "black")


#========================================================#
#------------------  AnnotationWidget  ------------------#
#========================================================#
class AnnotationWidget(QWidget):
    def __init__(self, parent = None):
        super(AnnotationWidget, self).__init__(parent = parent)
        self.parent = parent

        self.onlyInt = QIntValidator()

        annotationAreaLayout = QVBoxLayout()

        annotationMainLayout = QVBoxLayout()
        annotationMainLayout.setAlignment(Qt.AlignCenter)
        annotationMainLayout.setContentsMargins(5,5,5,5)

        annotation_widget = QWidget()
        annotation_widget.setLayout(annotationMainLayout)
        self.annoData = QGroupBox("Annotation assistant")
        self.annoData.resize(718, 830)
        self.annoData.setMinimumHeight(830)

        self.scrollAreaSetup = QScrollArea()
        self.scrollAreaSetup.setWidget(annotation_widget)
        self.scrollAreaSetup.setWidgetResizable(True)

        data_layout = QVBoxLayout()

        topData = QHBoxLayout()

        self.loadAnnoTxt = QPushButton("load file")
        self.loadAnnoTxt.clicked.connect(self.load_text_file)
        self.loadAnnoTxt.setFixedWidth(100)
        topData.addWidget(self.loadAnnoTxt)

        self.saveAnnoTxt = QPushButton("save file")
        self.saveAnnoTxt.clicked.connect(self.save_to_text_file)
        self.saveAnnoTxt.setFixedWidth(100)
        topData.addWidget(self.saveAnnoTxt)

        self.loadImage = QPushButton("load image")
        self.loadImage.clicked.connect(self.load_image)
        self.loadImage.setFixedWidth(100)
        topData.addWidget(self.loadImage)

        self.cleanImage = QPushButton("clean image")
        self.cleanImage.clicked.connect(self.clean_image)
        self.cleanImage.setFixedWidth(100)
        topData.addWidget(self.cleanImage)

        self.currentTagLabel = QLabel("                       current tag ID")
        topData.addWidget(self.currentTagLabel)
        self.currentTagText = QLineEdit()
        self.currentTagText.setText("")
        self.currentTagText.setValidator(self.onlyInt)
        self.currentTagText.setFixedWidth(150)
        topData.addWidget(self.currentTagText)

        topData.addStretch()
        data_layout.addLayout(topData)

        annotationFileLayout = QVBoxLayout()
        #self.allAnnotationContent = QPlainTextEdit()
        #self.allAnnotationContent.insertPlainText("")
        self.allAnnotationContent = QTextEdit()
        self.allAnnotationContent.append("")
        self.allAnnotationContent.setFixedSize(723,200)
        annotationFileLayout.addWidget(self.allAnnotationContent)
        self.annotationLineText = QLineEdit()
        self.annotationLineText.setAlignment(Qt.AlignLeft)
        self.annotationLineText.setText("")
        self.annotationLineText.setFixedSize(723,30)
        annotationFileLayout.addWidget(self.annotationLineText)
        data_layout.addLayout(annotationFileLayout)

        self.canvas = Canvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)
        fig = self.canvas.figure
        fig.clear()
        ax = fig.gca()

        toolbarLayout = QHBoxLayout()
        toolbarLayout.setAlignment(Qt.AlignCenter)

        toolbarLayout.addWidget(self.toolbar)
        data_layout.addLayout(toolbarLayout)

        data_layout.addWidget(self.canvas)
        self.annoData.setLayout(data_layout)
        
        #-------------------------------------------------#

        annotationMainLayout.addWidget(self.annoData)

        annotationMainLayout.addStretch()
        annotationAreaLayout.addWidget(self.scrollAreaSetup)        
        self.setLayout(annotationAreaLayout)

    #=====================================================#
    #=====================================================#

    def load_image(self):
        """
        loading image -> *.jpg
        """
        self.imagePath = ""

        FD = QFileDialog(self,"Load Image File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.ExistingFile)
        FD.setLabelText(QFileDialog.Accept, "Load")
        FD.setNameFilters(["JPEG image (*.jpg)"])
        if FD.exec_():
            self.imagePath = str(FD.selectedFiles()[0])

        if self.imagePath == "" or not os.path.isfile(self.imagePath):
            return

        if self.annotationLineText.text() != "" and len(self.annotationLineText.text().strip().split()) > 1:
            #self.allAnnotationContent.insertPlainText(self.annotationLineText.text()+"\n")
            #self.allAnnotationContent.append(self.annotationLineText.text()+"\n")
            self.allAnnotationContent.append(self.annotationLineText.text())

        self.annotationLineText.setText(self.imagePath.strip().split('/')[-1]+" ")

        self.canvas.figure.clear()
        self.genPicture()

    def clean_image(self): 
        """
        clean image
        """
        if self.imagePath == "":
            return

        #self.allAnnotationContent.insertPlainText("\n")
        self.imagePath = ""
        self.annotationLineText.setText("")
        self.canvas.figure.clear()
        self.canvas.draw()

    def load_text_file(self): 
        """
        loading an existing anootation text
        """
        FD = QFileDialog(self,"Load Text File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.ExistingFile)
        FD.setLabelText(QFileDialog.Accept, "Load")
        FD.setNameFilters(["TXT file (*.txt)"])
        if FD.exec_():
            self.annotationPath = str(FD.selectedFiles()[0])

            self.allAnnotationContent.clear()
            _file = open(self.annotationPath, 'r')
            for line in _file.readlines():
                self.allAnnotationContent.append(line.rstrip('\n'))

            _file.close()

    def save_to_text_file(self): 
        """
        saving current anootation text to a output file
        """
        FD = QFileDialog(self,"Save Text File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptSave)
        FD.setLabelText(QFileDialog.Accept, "Save")
        FD.setNameFilters(["TXT file (*.txt)"])
        FD.setDefaultSuffix('txt')
        if FD.exec_() == QFileDialog.Accepted:
            if self.annotationLineText.text() != "" and \
               len(self.annotationLineText.text().strip().split()) > 1:
                self.allAnnotationContent.append(self.annotationLineText.text())

            current_text = self.allAnnotationContent.toPlainText()
            if os.path.isfile(str(FD.selectedFiles()[0])):
                os.system('rm '+str(FD.selectedFiles()[0]))
                with open(str(FD.selectedFiles()[0]), 'w') as f:
                    f.write(current_text)
            else:
                with open(str(FD.selectedFiles()[0]), 'w') as f:
                    f.write(current_text)

    def line_select_callback(self, eclick, erelease):
        """
        eclick and erelease are the press and release events
        """
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        if self.currentTagText.text().strip() == "":
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Warning)
            msgBox.setText("Warning: You didn't give a tag ID for this annotation.")
            msgBox.exec_()
            self.currentTagText.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
        else:
            self.currentTagText.setStyleSheet("")
            
        rect = plt.Rectangle((min(x1,x2),min(y1,y2)), np.abs(x1-x2), np.abs(y1-y2), fill=False, edgecolor="red")
        self.ax.add_patch(rect)
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        self.annotationLineText.setText(self.annotationLineText.text()+str(int(x1))+" "+str(int(y1))+\
                                        " "+str(int(x2))+" "+str(int(y2))+" "+str(self.currentTagText.text())+" ")

        self.canvas.draw()

    def genPicture(self): 
        """
        show image
        """
        #ax = self.canvas.figure.add_subplot()
        fig = self.canvas.figure
        fig.clear()
        self.ax = fig.gca()

        img=mpimg.imread(self.imagePath)
        #img = img[::-1]
        plt.imshow(img, cmap='gray')

        rectprops = dict(facecolor = 'blue', edgecolor = 'black', alpha = 0.4, fill = True)
        self.rs = RectangleSelector(self.ax, self.line_select_callback,
                                    drawtype='box', rectprops = rectprops, 
                                    useblit=True,
                                    button=[1],  #use left button
                                    minspanx=5, minspany=5,
                                    spancoords='pixels')
        
        self.canvas.draw()

