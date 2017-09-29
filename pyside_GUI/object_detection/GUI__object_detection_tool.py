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
        
        self.imagePath = ""
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
        pipe_gen_pixmap = QPixmap("[PATH_TO_BE_MODIFIED]/icon/pipe_gen.png")
        self.pipeGen.setPixmap(pipe_gen_pixmap)
        self.pipeGen.setFixedHeight(120)
        self.pipeGen.setFixedWidth(20)
        topPipeData.addWidget(self.pipeGen)

        topGenData = QVBoxLayout()

        self.runGenFree = QPushButton("")
        self.runGenFree.setIcon(QPixmap("[PATH_TO_BE_MODIFIED]/icon/Button-Play-icon.png"))
        self.runGenFree.setToolTip("Click to start producing your training record/sample.")
        self.runGenFree.clicked.connect(self.start_tf_sample_production)
        self.runGenFree.setFixedHeight(30)
        self.runGenFree.setFixedWidth(100)
        topGenData.addWidget(self.runGenFree)

        self.runGenBusy = QPushButton("")
        self.runGenBusy.setIcon(QPixmap("[PATH_TO_BE_MODIFIED]/icon/Actions-process-stop-icon.png"))
        self.runGenBusy.setToolTip("Click to stop producing your training record/sample.")
        self.runGenBusy.clicked.connect(self.stop_tf_sample_production)
        self.runGenBusy.setFixedHeight(30)
        self.runGenBusy.setFixedWidth(100)
        topGenData.addWidget(self.runGenBusy)
        self.runGenBusy.setVisible(False)

        self.runGenFreeFrame = QLabel()
        runGenFreePicture = QPixmap("[PATH_TO_BE_MODIFIED]/icon/factory_free.png")
        self.runGenFreeFrame.setPixmap(runGenFreePicture)
        topGenData.addWidget(self.runGenFreeFrame)

        self.runGenBusyFrame = QLabel()
        self.runGenBusyFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.runGenBusyFrame.setAlignment(Qt.AlignCenter)
        topGenData.addWidget(self.runGenBusyFrame)
        self.runGenBusyFrame.setVisible(False)
        runGenBusyGif = "[PATH_TO_BE_MODIFIED]/icon/factory_busy_animation.gif"
        self.runGenBusyMovie = QMovie(runGenBusyGif, QByteArray(), self) 
        self.runGenBusyMovie.setCacheMode(QMovie.CacheAll) 
        self.runGenBusyMovie.setSpeed(100) 
        self.runGenBusyFrame.setMovie(self.runGenBusyMovie) 
        self.runGenBusyMovie.start()
        self.runGenBusyMovie.stop()

        #self.runGenBusy = QPushButton("")
        #self.runGenBusy.setIcon(QPixmap("[PATH_TO_BE_MODIFIED]/icon/factory_busy.png"))
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
        training_pipe_pixmap = QPixmap("[PATH_TO_BE_MODIFIED]/icon/pipe_gen_v2.png")
        self.trainingPipe.setPixmap(training_pipe_pixmap)
        self.trainingPipe.setFixedHeight(150)
        self.trainingPipe.setFixedWidth(20)
        trainingPipeData.addWidget(self.trainingPipe)

        startTraining = QVBoxLayout()

        self.modelTrainingFree = QPushButton("")
        self.modelTrainingFree.setIcon(QPixmap("[PATH_TO_BE_MODIFIED]/icon/Button-Play-icon.png"))
        self.modelTrainingFree.setToolTip("Click to start training your model.")
        self.modelTrainingFree.clicked.connect(self.start_model_training)
        self.modelTrainingFree.setFixedHeight(30)
        self.modelTrainingFree.setFixedWidth(100)
        startTraining.addWidget(self.modelTrainingFree)

        self.modelTrainingBusy = QPushButton("")
        self.modelTrainingBusy.setIcon(QPixmap("[PATH_TO_BE_MODIFIED]/icon/Actions-process-stop-icon.png"))
        self.modelTrainingBusy.setToolTip("Click to stop training your model.")
        self.modelTrainingBusy.clicked.connect(self.stop_model_training)
        self.modelTrainingBusy.setFixedHeight(30)
        self.modelTrainingBusy.setFixedWidth(100)
        startTraining.addWidget(self.modelTrainingBusy)
        self.modelTrainingBusy.setVisible(False)

        self.modelTrainingFreeFrame = QLabel()
        modelTrainingFreePicture = QPixmap("[PATH_TO_BE_MODIFIED]/icon/spongebob_model.png")
        self.modelTrainingFreeFrame.setPixmap(modelTrainingFreePicture)
        startTraining.addWidget(self.modelTrainingFreeFrame)

        self.modelTrainingBusyFrame = QLabel()
        self.modelTrainingBusyFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.modelTrainingBusyFrame.setAlignment(Qt.AlignCenter)
        startTraining.addWidget(self.modelTrainingBusyFrame)
        self.modelTrainingBusyFrame.setVisible(False)
        modelTrainingBusyGif = "[PATH_TO_BE_MODIFIED]/icon/spongebob_work.gif"
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
    
    def load_annotation(self):
        """
        loading annotation file
        """
        FD = QFileDialog(self,"Load Text File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.ExistingFile)
        FD.setLabelText(QFileDialog.Accept, "Load")
        FD.setNameFilters(["TXT file (*.txt)"])
        if FD.exec_():
            self.annotationPath.setText(str(FD.selectedFiles()[0]))

    def load_label_map_for_sampling(self):
        """
        loading label map file for sampling
        """
        FD = QFileDialog(self,"Load pb-Text File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.ExistingFile)
        FD.setLabelText(QFileDialog.Accept, "Load")
        FD.setNameFilters(["PBTXT file (*.pbtxt)"])
        if FD.exec_():
            self.mapTextForGen.setText(str(FD.selectedFiles()[0]))

    def load_image_directory(self):
        """
        loading image directory
        """
        FD = QFileDialog(self,"Load Directory...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.Directory)
        FD.setOption(QFileDialog.ShowDirsOnly)
        FD.setLabelText(QFileDialog.Accept, "Load")
        if FD.exec_():
            self.imagePath.setText(str(FD.selectedFiles()[0]))

    def start_tf_sample_production(self):
        """
        starting Tensorflow sample generator
        """
        #check setting
        if not os.path.isfile(self.annotationPath.text()):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: Your annotation file is not valid or doesn't exist.")
            msgBox.exec_()
            self.annotationPath.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
        else:
            self.annotationPath.setStyleSheet("")

        if not os.path.isfile(self.mapTextForGen.text()):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: Your label map file is not valid or doesn't exist.")
            msgBox.exec_()
            self.mapTextForGen.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
        else:
            self.mapTextForGen.setStyleSheet("")

        if not os.path.isdir(self.imagePath.text()):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: Your input image directory is not valid or doesn't exist.")
            msgBox.exec_()
            self.imagePath.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
        else:
            self.imagePath.setStyleSheet("")

        self.jobMsg.runMessage.clear()
        self.jobMsg.errorMessage.clear()
        self.widget_control('sampling')

        self.jobMsg.APM.Popen("python2.7 [PATH_TO_BE_MODIFIED]/TFRecord_generator.py "\
                              +self.annotationPath.text()+" "+self.mapTextForGen.text()+" "+self.imagePath.text(), \
                              shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stop_tf_sample_production(self):
        """
        stopping Tensorflow sample generator
        """
        exit_msg = os.system('[PATH_TO_BE_MODIFIED]/kill_jobs.csh TFRecord_generator.py')
        time.sleep(5)
        if exit_msg:
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Information)
            msgBox.setText('All sample-production jobs are killed.')
            msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Information)
            msgBox.setText('There is no any sample-production job.')
            msgBox.exec_()

        # widget control
        self.widget_control("idle")

    def load_label_map_for_modeling(self):
        """
        loading label map file for modeling
        """
        FD = QFileDialog(self,"Load pb-Text File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.ExistingFile)
        FD.setLabelText(QFileDialog.Accept, "Load")
        FD.setNameFilters(["PBTXT file (*.pbtxt)"])
        if FD.exec_():
            self.mapTextForMod.setText(str(FD.selectedFiles()[0]))

    def load_pretrained_model(self):
        """
        loading pretrained model (fintune checkpoint)
        """
        FD = QFileDialog(self,"Load Model File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.ExistingFile)
        FD.setLabelText(QFileDialog.Accept, "Load")
        FD.setNameFilters(["CKPT file (*.ckpt*.data*)"])
        if FD.exec_():
            list_pretrained_text = str(FD.selectedFiles()[0]).strip().split('/')
            self.pretrainedModel.setText('/'.join(x for x in list_pretrained_text[:-1])+'/'+\
                                         list_pretrained_text[-1].split('.')[0]+'.'+\
                                         list_pretrained_text[-1].split('.')[1])

    def load_training_data(self):
        """
        loading training data set
        """
        FD = QFileDialog(self,"Load Data/Record File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.ExistingFile)
        FD.setLabelText(QFileDialog.Accept, "Load")
        FD.setNameFilters(["record file (*.record)"])
        if FD.exec_():
            self.trainingData.setText(str(FD.selectedFiles()[0]))

    def start_model_training(self):
        """
        starting model training
        """
        #check setting
        try:
            if not float(self.minImageDimText.text()).is_integer():
                msgBox = QMessageBox()
                msgBox.setIcon(msgBox.Critical)
                msgBox.setText("Error: You must assign an integer number to 'Min. pixel' of your input image(s).")
                msgBox.exec_()
                self.minImageDimText.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
                return
            else:
                self.minImageDimText.setStyleSheet("")
        except:
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: You must assign an integer number to 'Min. pixel' of your input image(s).")
            msgBox.exec_()
            self.minImageDimText.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
            
        try:
            if not float(self.maxImageDimText.text()).is_integer():
                msgBox = QMessageBox()
                msgBox.setIcon(msgBox.Critical)
                msgBox.setText("Error: You must assign an integer number to 'Max. pixel' of your input image(s).")
                msgBox.exec_()
                self.maxImageDimText.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
                return
            else:
                self.maxImageDimText.setStyleSheet("")
        except:
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: You must assign an integer number to 'Max. pixel' of your input image(s).")
            msgBox.exec_()
            self.maxImageDimText.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return

        if not os.path.isfile(self.mapTextForMod.text()):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: Your label map file is not valid or doesn't exist.")
            msgBox.exec_()
            self.mapTextForMod.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
        else:
            self.mapTextForMod.setStyleSheet("")

        if not os.path.isfile(self.pretrainedModel.text()+'.data-00000-of-00001') or\
           not os.path.isfile(self.pretrainedModel.text()+'.index') or\
           not os.path.isfile(self.pretrainedModel.text()+'.meta'):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: Your pretrained model is not valid or doesn't exist.\n"+\
                           "           The input text must end in 'model.ckpt' or 'model.ckpt-[DIGITS]'\n"+\
                           "           There are three files: *.ckpt.data-00000-of-00001, *.ckpt.index\n"+\
                           "           and *.ckpt.meta.")
            msgBox.exec_()
            self.pretrainedModel.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
        else:
            self.pretrainedModel.setStyleSheet("")

        if not os.path.isfile(self.trainingData.text()):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: Your input traing sample is not valid or doesn't exist.")
            msgBox.exec_()
            self.trainingData.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
        else:
            self.trainingData.setStyleSheet("")

        if self.outputModelPath.text().strip() == "":
            self.outputModelPath.setText("train_"+time.strftime("%Y%m%d%H%M%S", time.localtime()))
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Warning)
            msgBox.setText("Warning: Since you don't assign an directory path of output. The system \n"+\
                           "              automatically create an output directory '"+self.outputModelPath.text()+"'\n"+\
                           "              under your current working directory.")
            msgBox.exec_()
            os.system('mkdir '+self.outputModelPath.text())
        elif not os.path.isdir(self.outputModelPath.text()):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Warning)
            msgBox.setText("Warning: The output directory you assign is not valid or doesn't exist.\n"+\
                           "                 It will be automatically created by system.")
            msgBox.exec_()
            os.system('mkdir '+self.outputModelPath.text())
        else:
            if os.listdir(self.outputModelPath.text()) != []:
                msgBox = QMessageBox()
                msgBox.setIcon(msgBox.Warning)
                msgBox.setText("Warning: The output directory you assign is not empty. Please make\n"+\
                               "                 sure everything in it is unnecessary. You can backup\n"+\
                               "                 it/them before you click 'OK'. If it contains some models,\n"+\
                               "                 the training process will restore parameters from the last\n"+\
                               "                 model in that directory.\n"+\
                               "                 Model training will directly start after you click 'OK'.")
                msgBox.exec_()    

        self.jobMsg.runMessage.clear()
        self.jobMsg.errorMessage.clear()
        self.widget_control('modeling')
        self.check_num_of_classes_modeling()
        self.produce_model_config()

        # python2.7 -i, where the option '-i' is necessary. 
        # then we can have normal standard output message and error message
        self.jobMsg.APM.Popen("python2.7 -i [PATH_TO_BE_MODIFIED]/train.py "+\
                              "--logtostdout "+\
                              "--pipeline_config_path="+self.outputModelPath.text()+"/faster_resnet_101.config "+\
                              "--train_dir="+self.outputModelPath.text()\
                              , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def produce_model_config(self):
        """
        producing the configure file of model
        """
        file_template = open('[PATH_TO_BE_MODIFIED]/faster_resnet_101_template.config', 'r')
        file_output   = open(self.outputModelPath.text()+'/faster_resnet_101.config', 'w')

        for line in file_template.readlines():
            if '[NUM_CLASSES]' in line.strip():
                file_output.write('    num_classes: '+str(self.num_classes)+'\n')
            elif '[MIN_DIMENSION]' in line.strip():
                file_output.write('        min_dimension: '+self.minImageDimText.text()+'\n')
            elif '[MAX_DIMENSION]' in line.strip():
                file_output.write('        max_dimension: '+self.maxImageDimText.text()+'\n')
            elif '[FINE_TUNE_CHECKPOINT]' in line.strip():
                file_output.write('  fine_tune_checkpoint: "'+self.pretrainedModel.text()+'"\n')
            elif '[TRAIN_INPUT_PATH]' in line.strip():
                file_output.write('    input_path: "'+self.trainingData.text()+'"\n')
            elif '[EVAL_INPUT_PATH]' in line.strip():
                file_output.write('    input_path: "[PATH_TO_BE_MODIFIED]/val.record"\n')
            elif '[LABEL_MAP_PATH]' in line.strip():
                file_output.write('  label_map_path: "'+self.mapTextForMod.text()+'"\n')
            else:
                file_output.write(line)

        file_template.close()
        file_output.close()

        msgBox = QMessageBox()
        msgBox.setIcon(msgBox.Information)
        msgBox.setText("A config file 'faster_resnet_101.config' is automatically \n"+
                       "created under directory '"+self.outputModelPath.text()+"'.\n"+
                       "Please don't delete it. You still need it for exporting your\n"+
                       "final model for inference.")
        msgBox.exec_()

    def check_num_of_classes_modeling(self):
        """
        checking the number of classes listed in label map for modeling
        """
        file_map = open(self.mapTextForMod.text(), 'r')

        self.num_classes = 0
        for line in file_map.readlines():
            if 'item' in line.strip() and 'name' not in line.strip():
                self.num_classes += 1

    def stop_model_training(self):
        """
        stopping model training
        """
        exit_msg = os.system('[PATH_TO_BE_MODIFIED]/kill_jobs.csh train.py '+self.outputModelPath.text())
        time.sleep(5)
        if exit_msg:
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Information)
            msgBox.setText('Your model-training job is stopped.')
            msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Information)
            msgBox.setText('There is no any model-training job.')
            msgBox.exec_()

        # widget control
        self.widget_control("idle")

    def widget_control(self, current_job):
        """
        controling widgets among different jobs
        """
        if current_job == 'sampling':
            self.loadAnnotation.setEnabled(False)
            self.annotationPath.setEnabled(False)
            self.loadMapForGen.setEnabled(False)
            self.mapTextForGen.setEnabled(False)
            self.loadImage.setEnabled(False)
            self.imagePath.setEnabled(False)
            self.runGenFree.setVisible(False)
            self.runGenBusy.setVisible(True)
            self.runGenFreeFrame.setVisible(False)
            self.runGenBusyFrame.setVisible(True)
            self.runGenBusyMovie.start()
            self.modelTrainingFree.setEnabled(False)
            self.modelTrainingBusy.setEnabled(False)
            self.modelTrainingFreeFrame.setEnabled(False)
            self.modelTrainingBusyFrame.setEnabled(False)
        elif current_job == 'modeling':
            self.runGenFree.setEnabled(False)
            self.runGenBusy.setEnabled(False)
            self.runGenFreeFrame.setEnabled(False)
            self.runGenBusyFrame.setEnabled(False)
            self.minImageDimText.setEnabled(False)
            self.maxImageDimText.setEnabled(False)
            self.mapTextForMod.setEnabled(False)
            self.loadMapForMod.setEnabled(False)
            self.pretrainedModel.setEnabled(False)
            self.loadPretrainedModel.setEnabled(False)
            self.trainingData.setEnabled(False)
            self.loadTrainingData.setEnabled(False)
            self.outputModelPath.setEnabled(False)
            self.modelTrainingFree.setVisible(False)
            self.modelTrainingBusy.setVisible(True)
            self.modelTrainingFreeFrame.setVisible(False)
            self.modelTrainingBusyFrame.setVisible(True)
            self.modelTrainingBusyMovie.start()
        elif current_job == 'idle':
            self.loadAnnotation.setEnabled(True)
            self.annotationPath.setEnabled(True)
            self.loadMapForGen.setEnabled(True)
            self.mapTextForGen.setEnabled(True)
            self.loadImage.setEnabled(True)
            self.imagePath.setEnabled(True)
            self.runGenFree.setEnabled(True)
            self.runGenBusy.setEnabled(True)
            self.runGenFreeFrame.setEnabled(True)
            self.runGenBusyFrame.setEnabled(True)
            self.runGenFree.setVisible(True)
            self.runGenBusy.setVisible(False)
            self.runGenFreeFrame.setVisible(True)
            self.runGenBusyFrame.setVisible(False)
            self.runGenBusyMovie.stop()
            self.minImageDimText.setEnabled(True)
            self.maxImageDimText.setEnabled(True)
            self.mapTextForMod.setEnabled(True)
            self.loadMapForMod.setEnabled(True)
            self.pretrainedModel.setEnabled(True)
            self.loadPretrainedModel.setEnabled(True)
            self.trainingData.setEnabled(True)
            self.loadTrainingData.setEnabled(True)
            self.outputModelPath.setEnabled(True)
            self.modelTrainingFree.setEnabled(True)
            self.modelTrainingBusy.setEnabled(True)
            self.modelTrainingFreeFrame.setEnabled(True)
            self.modelTrainingBusyFrame.setEnabled(True)
            self.modelTrainingFree.setVisible(True)
            self.modelTrainingBusy.setVisible(False)
            self.modelTrainingFreeFrame.setVisible(True)
            self.modelTrainingBusyFrame.setVisible(False)
            self.modelTrainingBusyMovie.stop()

