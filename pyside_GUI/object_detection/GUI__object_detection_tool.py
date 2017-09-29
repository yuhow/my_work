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


#=============================================================#
#------------------  ObjectDetectionWidget  ------------------#
#=============================================================#
class ObjectDetectionWidget(QWidget):
    def __init__(self, parent = None):
        super(ObjectDetectionWidget, self).__init__(parent = parent)
        self.parent = parent

        self.num_classes = 0
        self.onlyInt = QIntValidator()

        objectDetectionAreaLayout = QVBoxLayout()

        objectDetectionMainLayout = QVBoxLayout()
        objectDetectionMainLayout.setAlignment(Qt.AlignCenter)
        objectDetectionMainLayout.setContentsMargins(5,5,5,5)

        objectDetection_widget = QWidget()
        objectDetection_widget.setLayout(objectDetectionMainLayout)

        self.detectionData = QGroupBox("TF sample generator")
        self.training = QGroupBox("Object-detection model training")

        self.scrollAreaSetup = QScrollArea()
        self.scrollAreaSetup.setWidget(objectDetection_widget)
        self.scrollAreaSetup.setWidgetResizable(True)

        #---- TF data generator ----#
        data_layout = QHBoxLayout()

        topData = QGridLayout()

        self.annotationLabel = QLabel("annotation")
        self.annotationLabel.setFixedWidth(80)
        topData.addWidget(self.annotationLabel, 0, 0)
        self.annotationPath = QLineEdit()
        self.annotationPath.setAlignment(Qt.AlignLeft)
        self.annotationPath.setText("")
        self.annotationPath.setFixedWidth(400)
        self.annotationPath.setToolTip("Load an annotation file for producing training record/sample.")
        topData.addWidget(self.annotationPath, 0, 1)
        self.loadAnnotation = QPushButton("load annotation")
        self.loadAnnotation.clicked.connect(self.load_annotation)
        self.loadAnnotation.setFixedWidth(100)
        topData.addWidget(self.loadAnnotation, 0, 2)

        self.mapLabelForGen = QLabel("label map")
        self.mapLabelForGen.setFixedWidth(80)
        topData.addWidget(self.mapLabelForGen, 1, 0)
        self.mapTextForGen = QLineEdit()
        self.mapTextForGen.setAlignment(Qt.AlignLeft)
        self.mapTextForGen.setText("")
        self.mapTextForGen.setFixedWidth(400)
        self.mapTextForGen.setToolTip("Load a label map for producing training record/sample.")
        topData.addWidget(self.mapTextForGen, 1, 1)
        self.loadMapForGen = QPushButton("load map")
        self.loadMapForGen.clicked.connect(self.load_label_map_for_sampling)
        self.loadMapForGen.setFixedWidth(100)
        topData.addWidget(self.loadMapForGen, 1, 2)

        self.imageLabel = QLabel("image path")
        self.imageLabel.setFixedWidth(80)
        topData.addWidget(self.imageLabel, 2, 0)
        self.imagePath = QLineEdit()
        self.imagePath.setAlignment(Qt.AlignLeft)
        self.imagePath.setText("")
        self.imagePath.setFixedWidth(400)
        self.imagePath.setToolTip("Give a directory path of your input image(s)")
        topData.addWidget(self.imagePath, 2, 1)
        self.loadImage = QPushButton("load image")
        self.loadImage.clicked.connect(self.load_image_directory)
        self.loadImage.setFixedWidth(100)
        topData.addWidget(self.loadImage, 2, 2)

        topPipeData = QVBoxLayout()

        self.pipeGen = QLabel()
        pipe_gen_pixmap = QPixmap("icon/pipe_gen_small.png")
        self.pipeGen.setPixmap(pipe_gen_pixmap)
        self.pipeGen.setFixedHeight(120)
        self.pipeGen.setFixedWidth(20)
        topPipeData.addWidget(self.pipeGen)

        topGenData = QVBoxLayout()

        self.runGenFree = QPushButton("")
        self.runGenFree.setIcon(QPixmap("icon/Button-Play-icon_small.png"))
        self.runGenFree.setToolTip("Click to start producing your training record/sample.")
        self.runGenFree.clicked.connect(self.start_tf_sample_production)
        self.runGenFree.setFixedHeight(30)
        self.runGenFree.setFixedWidth(100)
        topGenData.addWidget(self.runGenFree)

        self.runGenBusy = QPushButton("")
        self.runGenBusy.setIcon(QPixmap("icon/Actions-process-stop-icon_small.png"))
        self.runGenBusy.setToolTip("Click to stop producing your training record/sample.")
        self.runGenBusy.clicked.connect(self.stop_tf_sample_production)
        self.runGenBusy.setFixedHeight(30)
        self.runGenBusy.setFixedWidth(100)
        topGenData.addWidget(self.runGenBusy)
        self.runGenBusy.setVisible(False)

        self.runGenFreeFrame = QLabel()
        runGenFreePicture = QPixmap("icon/factory_off_small.png")
        self.runGenFreeFrame.setPixmap(runGenFreePicture)
        topGenData.addWidget(self.runGenFreeFrame)

        self.runGenBusyFrame = QLabel()
        self.runGenBusyFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.runGenBusyFrame.setAlignment(Qt.AlignCenter)
        topGenData.addWidget(self.runGenBusyFrame)
        self.runGenBusyFrame.setVisible(False)
        runGenBusyGif = "icon/factory_on_animation_small.gif"
        self.runGenBusyMovie = QMovie(runGenBusyGif, QByteArray(), self) 
        self.runGenBusyMovie.setCacheMode(QMovie.CacheAll) 
        self.runGenBusyMovie.setSpeed(100) 
        self.runGenBusyFrame.setMovie(self.runGenBusyMovie) 
        self.runGenBusyMovie.start()
        self.runGenBusyMovie.stop()

        #self.runGenBusy = QPushButton("")
        #self.runGenBusy.setIcon(QPixmap("icon/factory_on_small.png"))
        #self.runGenBusy.setIconSize(QSize(90, 90))
        #self.runGenBusy.setFixedHeight(100)
        #self.runGenBusy.setFixedWidth(100)
        #topGenData.addWidget(self.runGenBusy)
        #self.runGenBusy.setVisible(False)

        data_layout.addLayout(topData)
        data_layout.addLayout(topPipeData)
        data_layout.addLayout(topGenData)

        self.detectionData.setLayout(data_layout)

        #---- model training ----#
        training_layout = QHBoxLayout()

        training_sublayout = QVBoxLayout()
        training_sublayout.setAlignment(Qt.AlignLeft)

        training_sublayout_top = QGridLayout()
        training_sublayout_bottom = QGridLayout()

        self.minImageDim = QLabel("Min. pixel")
        self.minImageDim.setFixedWidth(55)
        training_sublayout_top.addWidget(self.minImageDim, 0, 0)
        self.minImageDimText = QLineEdit()
        self.minImageDimText.setAlignment(Qt.AlignCenter)
        self.minImageDimText.setText("")
        self.minImageDimText.setValidator(self.onlyInt)
        self.minImageDimText.setToolTip("Give a minimum number of pixel of your input image(s).")
        self.minImageDimText.setFixedWidth(50)
        training_sublayout_top.addWidget(self.minImageDimText, 0, 1)

        self.dummy1_training_sublayout_top = QLabel("")
        self.dummy1_training_sublayout_top.setFixedWidth(0)
        training_sublayout_top.addWidget(self.dummy1_training_sublayout_top, 0, 2)

        self.maxImageDim = QLabel("Max. pixel")
        self.maxImageDim.setFixedWidth(55)
        training_sublayout_top.addWidget(self.maxImageDim, 0, 3)
        self.maxImageDimText = QLineEdit()
        self.maxImageDimText.setAlignment(Qt.AlignCenter)
        self.maxImageDimText.setText("")
        self.maxImageDimText.setValidator(self.onlyInt)
        self.maxImageDimText.setToolTip("Give a maximum number of pixel of your input image(s).")
        self.maxImageDimText.setFixedWidth(50)
        training_sublayout_top.addWidget(self.maxImageDimText, 0, 4)

        self.dummy2_training_sublayout_top = QLabel("")
        self.dummy2_training_sublayout_top.setFixedWidth(340)
        training_sublayout_top.addWidget(self.dummy2_training_sublayout_top, 0, 5)

        self.mapLabelForMod = QLabel("label map")
        self.mapLabelForMod.setFixedWidth(80)
        training_sublayout_bottom.addWidget(self.mapLabelForMod, 0, 0)
        self.mapTextForMod = QLineEdit()
        self.mapTextForMod.setAlignment(Qt.AlignLeft)
        self.mapTextForMod.setText("")
        self.mapTextForMod.setFixedWidth(400)
        self.mapTextForMod.setToolTip("Load a label map for modeling. If should be noted this label map has to\n"+
                                      "be consistent with the one you used for producing training record/sample.")
        training_sublayout_bottom.addWidget(self.mapTextForMod, 0, 1)
        self.loadMapForMod = QPushButton("load map")
        self.loadMapForMod.clicked.connect(self.load_label_map_for_modeling)
        self.loadMapForMod.setFixedWidth(100)
        training_sublayout_bottom.addWidget(self.loadMapForMod, 0, 2)

        self.pretrainedModelLabel = QLabel("pretrained")
        self.pretrainedModelLabel.setFixedWidth(80)
        training_sublayout_bottom.addWidget(self.pretrainedModelLabel, 1, 0)
        self.pretrainedModel = QLineEdit()
        self.pretrainedModel.setAlignment(Qt.AlignLeft)
        self.pretrainedModel.setText("model.ckpt")
        self.pretrainedModel.setFixedWidth(400)
        self.pretrainedModel.setToolTip("Load a pretrained model for fine-tuning.\n"+\
                                        "This can significantly decrease the time of modeling.")
        training_sublayout_bottom.addWidget(self.pretrainedModel, 1, 1)
        self.loadPretrainedModel = QPushButton("load model")
        self.loadPretrainedModel.clicked.connect(self.load_pretrained_model)
        self.loadPretrainedModel.setFixedWidth(100)
        training_sublayout_bottom.addWidget(self.loadPretrainedModel, 1, 2)

        self.trainingDataLabel = QLabel("training data")
        self.trainingDataLabel.setFixedWidth(80)
        training_sublayout_bottom.addWidget(self.trainingDataLabel, 2, 0)
        self.trainingData = QLineEdit()
        self.trainingData.setAlignment(Qt.AlignLeft)
        self.trainingData.setText("")
        self.trainingData.setFixedWidth(400)
        self.trainingData.setToolTip("The training record produced by TF sample generator.")
        training_sublayout_bottom.addWidget(self.trainingData, 2, 1)
        self.loadTrainingData = QPushButton("load data")
        self.loadTrainingData.clicked.connect(self.load_training_data)
        self.loadTrainingData.setFixedWidth(100)
        training_sublayout_bottom.addWidget(self.loadTrainingData, 2, 2)

        self.outputModelPathLabel = QLabel("output Dir.")
        self.outputModelPathLabel.setFixedWidth(80)
        training_sublayout_bottom.addWidget(self.outputModelPathLabel, 3, 0)
        self.outputModelPath = QLineEdit()
        self.outputModelPath.setAlignment(Qt.AlignLeft)
        self.outputModelPath.setText("")
        self.outputModelPath.setFixedWidth(400)
        self.outputModelPath.setToolTip("Give a name of directory where you want to store your training results.\n"+\
                                        "If this directory doesn't exist, the system will create it automatically.")
        training_sublayout_bottom.addWidget(self.outputModelPath, 3, 1)

        trainingPipeData = QVBoxLayout()

        self.trainingPipe = QLabel()
        training_pipe_pixmap = QPixmap("icon/pipe_gen_v2_small.png")
        self.trainingPipe.setPixmap(training_pipe_pixmap)
        self.trainingPipe.setFixedHeight(150)
        self.trainingPipe.setFixedWidth(20)
        trainingPipeData.addWidget(self.trainingPipe)

        startTraining = QVBoxLayout()

        self.modelTrainingFree = QPushButton("")
        self.modelTrainingFree.setIcon(QPixmap("icon/Button-Play-icon_small.png"))
        self.modelTrainingFree.setToolTip("Click to start training your model.")
        self.modelTrainingFree.clicked.connect(self.start_model_training)
        self.modelTrainingFree.setFixedHeight(30)
        self.modelTrainingFree.setFixedWidth(100)
        startTraining.addWidget(self.modelTrainingFree)

        self.modelTrainingBusy = QPushButton("")
        self.modelTrainingBusy.setIcon(QPixmap("icon/Actions-process-stop-icon_small.png"))
        self.modelTrainingBusy.setToolTip("Click to stop training your model.")
        self.modelTrainingBusy.clicked.connect(self.stop_model_training)
        self.modelTrainingBusy.setFixedHeight(30)
        self.modelTrainingBusy.setFixedWidth(100)
        startTraining.addWidget(self.modelTrainingBusy)
        self.modelTrainingBusy.setVisible(False)

        self.modelTrainingFreeFrame = QLabel()
        modelTrainingFreePicture = QPixmap("icon/spongebob_model_small.png")
        self.modelTrainingFreeFrame.setPixmap(modelTrainingFreePicture)
        startTraining.addWidget(self.modelTrainingFreeFrame)

        self.modelTrainingBusyFrame = QLabel()
        self.modelTrainingBusyFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.modelTrainingBusyFrame.setAlignment(Qt.AlignCenter)
        startTraining.addWidget(self.modelTrainingBusyFrame)
        self.modelTrainingBusyFrame.setVisible(False)
        modelTrainingBusyGif = "icon/spongebob_work_small.gif"
        self.modelTrainingBusyMovie = QMovie(modelTrainingBusyGif, QByteArray(), self) 
        self.modelTrainingBusyMovie.setCacheMode(QMovie.CacheAll) 
        self.modelTrainingBusyMovie.setSpeed(100) 
        self.modelTrainingBusyFrame.setMovie(self.modelTrainingBusyMovie) 
        self.modelTrainingBusyMovie.start()
        self.modelTrainingBusyMovie.stop()

        training_sublayout.addLayout(training_sublayout_top)
        training_sublayout.addLayout(training_sublayout_bottom)

        training_layout.addLayout(training_sublayout)
        training_layout.addLayout(trainingPipeData)
        training_layout.addLayout(startTraining)

        self.training.setLayout(training_layout)


        #---- job message ----#
        self.jobMsg = ModelingRunMsgWidget(self)

        #-------------------------------------------------#

        objectDetectionMainLayout.addWidget(self.detectionData)
        objectDetectionMainLayout.addWidget(self.training)
        objectDetectionMainLayout.addWidget(self.jobMsg)

        objectDetectionMainLayout.addStretch()
        objectDetectionAreaLayout.addWidget(self.scrollAreaSetup)        
        self.setLayout(objectDetectionAreaLayout)

    #=====================================================#
    #=====================================================#

