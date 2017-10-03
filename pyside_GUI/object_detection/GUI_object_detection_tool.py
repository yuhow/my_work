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
            self.parent.modelPrediction.setEnabled(False)
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
            self.parent.modelPrediction.setEnabled(False)
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
            self.parent.modelPrediction.setEnabled(True)


#=============================================================#
#------------------  ModelPredictionWidget  ------------------#
#=============================================================#
class ModelPredictionWidget(QWidget):
    def __init__(self, parent = None):
        super(ModelPredictionWidget, self).__init__(parent = parent)
        self.parent = parent

        self.num_classes = 0

        modelPredictionAreaLayout = QVBoxLayout()

        modelPredictionMainLayout = QVBoxLayout()
        modelPredictionMainLayout.setAlignment(Qt.AlignCenter)
        modelPredictionMainLayout.setContentsMargins(5,5,5,5)

        modelPrediction_widget = QWidget()
        modelPrediction_widget.setLayout(modelPredictionMainLayout)

        self.exportGraph = QGroupBox("Export inference graph")
        self.predicting = QGroupBox("Object-detection model predicting")

        self.scrollAreaSetup = QScrollArea()
        self.scrollAreaSetup.setWidget(modelPrediction_widget)
        self.scrollAreaSetup.setWidgetResizable(True)

        #---- exporting graph ----#
        export_layout = QHBoxLayout()

        topDataExport = QGridLayout()

        self.modelPathLabel = QLabel("model path")
        self.modelPathLabel.setFixedWidth(80)
        topDataExport.addWidget(self.modelPathLabel, 0, 0)
        self.modelPath = QLineEdit()
        self.modelPath.setAlignment(Qt.AlignLeft)
        self.modelPath.setText("")
        self.modelPath.setFixedWidth(400)
        self.modelPath.setToolTip("A trained model which will be exported for inference.")
        topDataExport.addWidget(self.modelPath, 0, 1)
        self.loadModel = QPushButton("load model")
        self.loadModel.clicked.connect(self.load_trained_model)
        self.loadModel.setFixedWidth(100)
        topDataExport.addWidget(self.loadModel, 0, 2)

        self.modelConfigPathLabel = QLabel("config path")
        self.modelConfigPathLabel.setFixedWidth(80)
        topDataExport.addWidget(self.modelConfigPathLabel, 1, 0)
        self.modelConfigPath = QLineEdit()
        self.modelConfigPath.setAlignment(Qt.AlignLeft)
        self.modelConfigPath.setText("")
        self.modelConfigPath.setFixedWidth(400)
        self.modelConfigPath.setToolTip("Load the config file of your trained model.\n"+\
                                        "It exists usually in the directory of training output.")
        topDataExport.addWidget(self.modelConfigPath, 1, 1)
        self.loadModelConfig = QPushButton("load config")
        self.loadModelConfig.clicked.connect(self.load_model_config)
        self.loadModelConfig.setFixedWidth(100)
        topDataExport.addWidget(self.loadModelConfig, 1, 2)

        self.inferenceGraphPathLabel = QLabel("graph path")
        self.inferenceGraphPathLabel.setFixedWidth(80)
        topDataExport.addWidget(self.inferenceGraphPathLabel, 2, 0)
        self.inferenceGraphPath = QLineEdit()
        self.inferenceGraphPath.setAlignment(Qt.AlignLeft)
        self.inferenceGraphPath.setText("[YOUR_OUTPUT_INFERENCE_GRAPH].pb")
        self.inferenceGraphPath.setPlaceholderText("[YOUR_OUTPUT_INFERENCE_GRAPH].pb")
        self.inferenceGraphPath.setFixedWidth(400)
        self.inferenceGraphPath.setToolTip("Give a name for your output inference graph.")
        topDataExport.addWidget(self.inferenceGraphPath, 2, 1)

        topPipeExport = QVBoxLayout()

        self.pipeExport = QLabel()
        pipe_gen_pixmap = QPixmap("[PATH_TO_BE_MODIFIED]/icon/pipe_gen.png")
        self.pipeExport.setPixmap(pipe_gen_pixmap)
        self.pipeExport.setFixedHeight(120)
        self.pipeExport.setFixedWidth(20)
        topPipeExport.addWidget(self.pipeExport)

        topExport = QVBoxLayout()

        self.runExportFree = QPushButton("")
        self.runExportFree.setIcon(QPixmap("[PATH_TO_BE_MODIFIED]/icon/Button-Play-icon.png"))
        self.runExportFree.setToolTip("Click to start producing your training record/sample.")
        self.runExportFree.clicked.connect(self.start_export_inference_graph)
        self.runExportFree.setFixedHeight(30)
        self.runExportFree.setFixedWidth(100)
        topExport.addWidget(self.runExportFree)

        self.runExportBusy = QPushButton("")
        self.runExportBusy.setIcon(QPixmap("[PATH_TO_BE_MODIFIED]/icon/Actions-process-stop-icon.png"))
        self.runExportBusy.setToolTip("Click to stop producing your training record/sample.")
        self.runExportBusy.clicked.connect(self.stop_export_inference_graph)
        self.runExportBusy.setFixedHeight(30)
        self.runExportBusy.setFixedWidth(100)
        topExport.addWidget(self.runExportBusy)
        self.runExportBusy.setVisible(False)

        self.runExportFreeFrame = QLabel()
        runExportFreePicture = QPixmap("[PATH_TO_BE_MODIFIED]/icon/spongebob_export.png")
        self.runExportFreeFrame.setPixmap(runExportFreePicture)
        topExport.addWidget(self.runExportFreeFrame)

        self.runExportBusyFrame = QLabel()
        self.runExportBusyFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.runExportBusyFrame.setAlignment(Qt.AlignCenter)
        topExport.addWidget(self.runExportBusyFrame)
        self.runExportBusyFrame.setVisible(False)
        runExportBusyGif = "[PATH_TO_BE_MODIFIED]/icon/export.gif"
        self.runExportBusyMovie = QMovie(runExportBusyGif, QByteArray(), self) 
        self.runExportBusyMovie.setCacheMode(QMovie.CacheAll) 
        self.runExportBusyMovie.setSpeed(100) 
        self.runExportBusyFrame.setMovie(self.runExportBusyMovie) 
        self.runExportBusyMovie.start()
        self.runExportBusyMovie.stop()

        export_layout.addLayout(topDataExport)
        export_layout.addLayout(topPipeExport)
        export_layout.addLayout(topExport)

        self.exportGraph.setLayout(export_layout)

        #---- model predicting ----#
        predicting_layout = QHBoxLayout()

        predicting_sublayout = QVBoxLayout()
        predicting_sublayout.setAlignment(Qt.AlignLeft)

        predicting_sublayout_top = QGridLayout()
        predicting_sublayout_bottom = QGridLayout()

        self.isShowingImageChecked = QCheckBox("display image")
        self.isShowingImageChecked.setCheckState(Qt.Unchecked)
        self.isShowingImageChecked.setToolTip("check this option if you want to display image(s) simultaneously, default is 'OFF'\n"+
                                              "It should be noted that image result is shown one after one. We recommended you to\n"+
                                              "check this option when you have few images and really need to check your result(s)\n"+
                                              "instantaneously. Without checking this option, all results will still be saved under\n"+
                                              "your current working directory.")
        predicting_sublayout_top.addWidget(self.isShowingImageChecked, 0, 0)

        self.isGrayScaleChecked = QCheckBox("gray scale")
        self.isGrayScaleChecked.setCheckState(Qt.Checked)
        self.isGrayScaleChecked.setToolTip("Check this option if your image(s) is/are in gray scale, default is 'ON'")
        predicting_sublayout_top.addWidget(self.isGrayScaleChecked, 1, 0)

        self.inferenceGraphLabel = QLabel("TF graph")
        self.inferenceGraphLabel.setFixedWidth(80)
        predicting_sublayout_bottom.addWidget(self.inferenceGraphLabel, 0, 0)
        self.inferenceGraph = QLineEdit()
        self.inferenceGraph.setAlignment(Qt.AlignLeft)
        self.inferenceGraph.setText("")
        self.inferenceGraph.setFixedWidth(400)
        self.inferenceGraph.setToolTip("Load an inference graph for object detection.")
        predicting_sublayout_bottom.addWidget(self.inferenceGraph, 0, 1)
        self.loadinferenceGraph = QPushButton("load graph")
        self.loadinferenceGraph.clicked.connect(self.load_inference_graph)
        self.loadinferenceGraph.setFixedWidth(100)
        predicting_sublayout_bottom.addWidget(self.loadinferenceGraph, 0, 2)

        self.mapLabelForPred = QLabel("label map")
        self.mapLabelForPred.setFixedWidth(80)
        predicting_sublayout_bottom.addWidget(self.mapLabelForPred, 1, 0)
        self.mapTextForPred = QLineEdit()
        self.mapTextForPred.setAlignment(Qt.AlignLeft)
        self.mapTextForPred.setText("")
        self.mapTextForPred.setFixedWidth(400)
        self.mapTextForPred.setToolTip("Load a label map for predicting. If should be noted this label map has to\n"+
                                       "be consistent with the one used for producing training record/sample,\n"+
                                       "model-training and exporting inference graph.")
        predicting_sublayout_bottom.addWidget(self.mapTextForPred, 1, 1)
        self.loadMapForPred = QPushButton("load map")
        self.loadMapForPred.clicked.connect(self.load_label_map_for_predicting)
        self.loadMapForPred.setFixedWidth(100)
        predicting_sublayout_bottom.addWidget(self.loadMapForPred, 1, 2)

        self.predictingDataLabel = QLabel("image list")
        self.predictingDataLabel.setFixedWidth(80)
        predicting_sublayout_bottom.addWidget(self.predictingDataLabel, 2, 0)
        self.predictingData = QLineEdit()
        self.predictingData.setAlignment(Qt.AlignLeft)
        self.predictingData.setText("")
        self.predictingData.setFixedWidth(400)
        self.predictingData.setToolTip("Load a list of input image data for object detection.\n"+
                                       "Full path of input images should be listed line by line.")
        predicting_sublayout_bottom.addWidget(self.predictingData, 2, 1)
        self.loadPredictingData = QPushButton("load data")
        self.loadPredictingData.clicked.connect(self.load_predicting_data_list)
        self.loadPredictingData.setFixedWidth(100)
        predicting_sublayout_bottom.addWidget(self.loadPredictingData, 2, 2)

        predictingPipeData = QVBoxLayout()

        self.predictingPipe = QLabel()
        predicting_pipe_pixmap = QPixmap("[PATH_TO_BE_MODIFIED]/icon/pipe_gen_v2.png")
        self.predictingPipe.setPixmap(predicting_pipe_pixmap)
        self.predictingPipe.setFixedHeight(150)
        self.predictingPipe.setFixedWidth(20)
        predictingPipeData.addWidget(self.predictingPipe)

        startPredicting = QVBoxLayout()

        self.modelPredictingFree = QPushButton("")
        self.modelPredictingFree.setIcon(QPixmap("[PATH_TO_BE_MODIFIED]/icon/Button-Play-icon.png"))
        self.modelPredictingFree.setToolTip("Click to start training your model.")
        self.modelPredictingFree.clicked.connect(self.start_model_predicting)
        self.modelPredictingFree.setFixedHeight(30)
        self.modelPredictingFree.setFixedWidth(100)
        startPredicting.addWidget(self.modelPredictingFree)

        self.modelPredictingBusy = QPushButton("")
        self.modelPredictingBusy.setIcon(QPixmap("[PATH_TO_BE_MODIFIED]/icon/Actions-process-stop-icon.png"))
        self.modelPredictingBusy.setToolTip("Click to stop training your model.")
        self.modelPredictingBusy.clicked.connect(self.stop_model_predicting)
        self.modelPredictingBusy.setFixedHeight(30)
        self.modelPredictingBusy.setFixedWidth(100)
        startPredicting.addWidget(self.modelPredictingBusy)
        self.modelPredictingBusy.setVisible(False)

        self.modelPredictingFreeFrame = QLabel()
        modelPredictingFreePicture = QPixmap("[PATH_TO_BE_MODIFIED]/icon/spongebob_present.png")
        self.modelPredictingFreeFrame.setPixmap(modelPredictingFreePicture)
        startPredicting.addWidget(self.modelPredictingFreeFrame)

        self.modelPredictingBusyFrame = QLabel()
        self.modelPredictingBusyFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.modelPredictingBusyFrame.setAlignment(Qt.AlignCenter)
        startPredicting.addWidget(self.modelPredictingBusyFrame)
        self.modelPredictingBusyFrame.setVisible(False)
        modelPredictingBusyGif = "[PATH_TO_BE_MODIFIED]/icon/spongebob_magic.gif"
        self.modelPredictingBusyMovie = QMovie(modelPredictingBusyGif, QByteArray(), self) 
        self.modelPredictingBusyMovie.setCacheMode(QMovie.CacheAll) 
        self.modelPredictingBusyMovie.setSpeed(100) 
        self.modelPredictingBusyFrame.setMovie(self.modelPredictingBusyMovie) 
        self.modelPredictingBusyMovie.start()
        self.modelPredictingBusyMovie.stop()

        predicting_sublayout.addLayout(predicting_sublayout_top)
        predicting_sublayout.addLayout(predicting_sublayout_bottom)

        predicting_layout.addLayout(predicting_sublayout)
        predicting_layout.addLayout(predictingPipeData)
        predicting_layout.addLayout(startPredicting)

        self.predicting.setLayout(predicting_layout)


        #---- job message ----#
        self.jobMsg = ModelingRunMsgWidget(self)

        #-------------------------------------------------#

        modelPredictionMainLayout.addWidget(self.exportGraph)
        modelPredictionMainLayout.addWidget(self.predicting)
        modelPredictionMainLayout.addWidget(self.jobMsg)

        modelPredictionMainLayout.addStretch()
        modelPredictionAreaLayout.addWidget(self.scrollAreaSetup)        
        self.setLayout(modelPredictionAreaLayout)

    #=====================================================#
    #=====================================================#

    def load_trained_model(self):
        """
        loading trained model for exporting as an inference graph
        """
        FD = QFileDialog(self,"Load Model File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.ExistingFile)
        FD.setLabelText(QFileDialog.Accept, "Load")
        FD.setNameFilters(["CKPT file (*.ckpt*.data*)"])
        if FD.exec_():
            list_trained_text = str(FD.selectedFiles()[0]).strip().split('/')
            self.modelPath.setText('/'.join(x for x in list_trained_text[:-1])+'/'+\
                                   list_trained_text[-1].split('.')[0]+'.'+\
                                   list_trained_text[-1].split('.')[1])

    def load_model_config(self):
        """
        loading the config file of your trained model
        """
        FD = QFileDialog(self,"Load Text File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.ExistingFile)
        FD.setLabelText(QFileDialog.Accept, "Load")
        FD.setNameFilters(["CONFIG file (*.config)"])
        if FD.exec_():
            self.modelConfigPath.setText(str(FD.selectedFiles()[0]))

    def start_export_inference_graph(self):
        """
        starting to export inference graph of trained model
        """
        #check setting
        if not os.path.isfile(self.modelPath.text()+'.data-00000-of-00001') or\
           not os.path.isfile(self.modelPath.text()+'.index') or\
           not os.path.isfile(self.modelPath.text()+'.meta'):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: Your input model is not valid or doesn't exist.\n"+\
                           "           The input text must end in 'model.ckpt' or 'model.ckpt-[DIGITS]'\n"+\
                           "           There are three files: *.ckpt.data-00000-of-00001, *.ckpt.index\n"+\
                           "           and *.ckpt.meta.")
            msgBox.exec_()
            self.modelPath.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
        else:
            self.modelPath.setStyleSheet("")

        if not os.path.isfile(self.modelConfigPath.text()):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: Your config file is not valid or doesn't exist.")
            msgBox.exec_()
            self.modelConfigPath.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
        else:
            self.modelConfigPath.setStyleSheet("")

        if os.path.isfile(self.inferenceGraphPath.text()):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Warning)
            msgBox.setText("Warning: The output graph you assign already exists. Please make\n"+\
                           "                 sure you want to overwrite it anyway. \n"+\
                           "                 Exporting will be directly started after you click 'OK'.")
            msgBox.exec_()

        self.jobMsg.runMessage.clear()
        self.jobMsg.errorMessage.clear()
        self.widget_control('exporting')

        self.jobMsg.APM.Popen("python2.7 [PATH_TO_BE_MODIFIED]/export_inference_graph.py "\
                              +"--input_type image_tensor "\
                              +"--pipeline_config_path "+self.modelConfigPath.text()+" "\
                              +"--checkpoint_path "+self.modelPath.text()+" "\
                              +"--inference_graph_path "+self.inferenceGraphPath.text(), \
                              shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stop_export_inference_graph(self):
        """
        stopping exporting inference graph
        """
        exit_msg = os.system('[PATH_TO_BE_MODIFIED]/kill_jobs.csh export_inference_graph.py')
        time.sleep(5)
        if exit_msg:
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Information)
            msgBox.setText('Your exporting job is stopped.')
            msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Information)
            msgBox.setText('There is no any exporting job.')
            msgBox.exec_()

        # widget control
        self.widget_control("idle")

    def load_label_map_for_predicting(self):
        """
        loading label map file for predicting
        """
        FD = QFileDialog(self,"Load pb-Text File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.ExistingFile)
        FD.setLabelText(QFileDialog.Accept, "Load")
        FD.setNameFilters(["PBTXT file (*.pbtxt)"])
        if FD.exec_():
            self.mapTextForPred.setText(str(FD.selectedFiles()[0]))

    def load_inference_graph(self):
        """
        loading inference graph for predicting
        """
        FD = QFileDialog(self,"Load pb File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.ExistingFile)
        FD.setLabelText(QFileDialog.Accept, "Load")
        FD.setNameFilters(["PB file (*.pb)"])
        if FD.exec_():
            self.inferenceGraph.setText(str(FD.selectedFiles()[0]))

    def load_predicting_data_list(self):
        """
        loading a list of image data as input for predicting
        """
        FD = QFileDialog(self,"Load Text File...",directory="./")
        FD.setAcceptMode(QFileDialog.AcceptOpen)
        FD.setFileMode(QFileDialog.ExistingFile)
        FD.setLabelText(QFileDialog.Accept, "Load")
        FD.setNameFilters(["TXT file (*.txt)"])
        if FD.exec_():
            self.predictingData.setText(str(FD.selectedFiles()[0]))

    def start_model_predicting(self):
        """
        starting to detecting object(s) from input image(s) 
        """
        #check setting
        if not os.path.isfile(self.inferenceGraph.text()):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: Your input graph is not valid or doesn't exist.")
            msgBox.exec_()
            self.inferenceGraph.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
        else:
            self.inferenceGraph.setStyleSheet("")

        if not os.path.isfile(self.mapTextForPred.text()):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: Your label map file is not valid or doesn't exist.")
            msgBox.exec_()
            self.mapTextForPred.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
        else:
            self.mapTextForPred.setStyleSheet("")

        if not os.path.isfile(self.predictingData.text()):
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Critical)
            msgBox.setText("Error: The list file (.txt) of your input image data is not valid or doesn't exist.")
            msgBox.exec_()
            self.predictingData.setStyleSheet("QLineEdit {background-color: rgb(255, 0, 0)}")
            return
        else:
            self.predictingData.setStyleSheet("")

        self.jobMsg.runMessage.clear()
        self.jobMsg.errorMessage.clear()
        self.widget_control('predicting')
        self.check_num_of_classes_predicting()

        if self.isShowingImageChecked.isChecked():
            display = 1
        else:
            display = 0

        if self.isGrayScaleChecked.isChecked():
            gray_scale = 1
        else:
            gray_scale = 0

        self.jobMsg.APM.Popen("python2.7 [PATH_TO_BE_MODIFIED]/start_object_detection.py "\
                              +self.inferenceGraph.text()+" "\
                              +self.mapTextForPred.text()+" "\
                              +str(self.num_classes)+" "\
                              +self.predictingData.text()+" "\
                              +str(display)+" "\
                              +str(gray_scale),
                              shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stop_model_predicting(self):
        """
        stopping detecting object(s) process
        """
        exit_msg = os.system('[PATH_TO_BE_MODIFIED]/kill_jobs.csh start_object_detection.py')
        time.sleep(5)
        if exit_msg:
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Information)
            msgBox.setText('Your object-detection job is stopped.')
            msgBox.exec_()
        else:
            msgBox = QMessageBox()
            msgBox.setIcon(msgBox.Information)
            msgBox.setText('There is no any object-detection job.')
            msgBox.exec_()

        # widget control
        self.widget_control("idle")

    def check_num_of_classes_predicting(self):
        """
        checking the number of classes listed in label map for predicting
        """
        file_map = open(self.mapTextForPred.text(), 'r')

        self.num_classes = 0
        for line in file_map.readlines():
            if 'item' in line.strip() and 'name' not in line.strip():
                self.num_classes += 1

    def widget_control(self, current_job):
        """
        controling widgets among different jobs
        """
        if current_job == 'exporting':
            self.modelPath.setEnabled(False)
            self.loadModel.setEnabled(False)
            self.modelConfigPath.setEnabled(False)
            self.loadModelConfig.setEnabled(False)
            self.inferenceGraphPath.setEnabled(False)
            self.runExportFree.setEnabled(False)
            self.runExportBusy.setEnabled(True)
            self.runExportFree.setVisible(False)
            self.runExportBusy.setVisible(True)
            self.runExportFreeFrame.setVisible(False)
            self.runExportBusyFrame.setVisible(True)
            self.runExportBusyMovie.start()
            self.modelPredictingFree.setEnabled(False)
            self.modelPredictingBusy.setEnabled(False)
            self.parent.objectDetection.setEnabled(False)
        elif current_job == 'predicting':
            self.runExportFree.setEnabled(False)
            self.runExportBusy.setEnabled(False)
            self.isShowingImageChecked.setEnabled(False)
            self.isGrayScaleChecked.setEnabled(False)
            self.inferenceGraph.setEnabled(False)
            self.loadinferenceGraph.setEnabled(False)
            self.mapTextForPred.setEnabled(False)
            self.loadMapForPred.setEnabled(False)
            self.predictingData.setEnabled(False) 
            self.loadPredictingData.setEnabled(False)
            self.runExportFree.setEnabled(False)
            self.modelPredictingFree.setEnabled(False)
            self.modelPredictingBusy.setEnabled(True)
            self.modelPredictingFree.setVisible(False)
            self.modelPredictingBusy.setVisible(True)
            self.modelPredictingFreeFrame.setVisible(False)
            self.modelPredictingBusyFrame.setVisible(True)
            self.modelPredictingBusyMovie.start()
            self.parent.objectDetection.setEnabled(False)
        elif current_job == 'idle':
            self.modelPath.setEnabled(True)
            self.loadModel.setEnabled(True)
            self.modelConfigPath.setEnabled(True)
            self.loadModelConfig.setEnabled(True)
            self.inferenceGraphPath.setEnabled(True)
            self.runExportFree.setEnabled(True)
            self.runExportBusy.setEnabled(False)
            self.runExportFree.setVisible(True)
            self.runExportBusy.setVisible(False)
            self.runExportFreeFrame.setVisible(True)
            self.runExportBusyFrame.setVisible(False)
            self.runExportBusyMovie.stop()
            self.isShowingImageChecked.setEnabled(True)
            self.isGrayScaleChecked.setEnabled(True)
            self.inferenceGraph.setEnabled(True)
            self.loadinferenceGraph.setEnabled(True)
            self.mapTextForPred.setEnabled(True)
            self.loadMapForPred.setEnabled(True)
            self.predictingData.setEnabled(True) 
            self.loadPredictingData.setEnabled(True)
            self.modelPredictingFree.setEnabled(True)
            self.modelPredictingBusy.setEnabled(False)
            self.modelPredictingFree.setVisible(True)
            self.modelPredictingBusy.setVisible(False)
            self.modelPredictingFreeFrame.setVisible(True)
            self.modelPredictingBusyFrame.setVisible(False)
            self.modelPredictingBusyMovie.stop()
            self.parent.objectDetection.setEnabled(True)


#=====================================================#
#-------------------  HelpWidget  --------------------#
#=====================================================#
class HelpWidget(QWidget):
    def __init__(self, parent = None):
        super(HelpWidget, self).__init__(parent = parent)
        self.parent = parent

        helpAreaLayout = QVBoxLayout()

        helpMainLayout = QVBoxLayout()
        helpMainLayout.setAlignment(Qt.AlignCenter)
        helpMainLayout.setContentsMargins(5,5,5,5)

        help_widget = QWidget()
        help_widget.setLayout(helpMainLayout)
        self.helpGroup = QGroupBox("")
        self.helpGroup.resize(718, 300)
        #self.helpGroup.setMinimumHeight(830)

        self.scrollAreaSetup = QScrollArea()
        self.scrollAreaSetup.setWidget(help_widget)
        self.scrollAreaSetup.setWidgetResizable(True)

        helpGroup_layout = QVBoxLayout()

        region_one_helper = QHBoxLayout()

        self.announceLabel = QLabel('AFK is basically a general object-detection tool')
        self.dummyLabel = QLabel('')
        helpGroup_layout.addWidget(self.announceLabel)
        helpGroup_layout.addWidget(self.dummyLabel)

        self.loadLabelMapTxt = QPushButton("open template of label map")
        self.loadLabelMapTxt.clicked.connect(self.open_template_of_label_map)
        self.loadLabelMapTxt.setFixedWidth(200)
        region_one_helper.addWidget(self.loadLabelMapTxt)

        region_one_helper.addStretch()
        helpGroup_layout.addLayout(region_one_helper)

        self.helpGroup.setLayout(helpGroup_layout)
        
        #-------------------------------------------------#

        helpMainLayout.addWidget(self.helpGroup)

        helpMainLayout.addStretch()
        helpAreaLayout.addWidget(self.scrollAreaSetup)        
        self.setLayout(helpAreaLayout)

    #=====================================================#
    #=====================================================#

    def open_template_of_label_map(self):
        """
        viewing a template file of label map
        """
        os.system('gvim [PATH_TO_BE_MODIFIED]/label_map_template.pbtxt')


#===========================================================#
#-------------------  CustomizedWidget  --------------------#
#===========================================================#
class Canvas(FigureCanvas):
    def __init__(self, parent):
        self.figure = plt.figure(linewidth = 1, edgecolor='gray')
        FigureCanvas.__init__(self,self.figure)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class ClickableLabel(QLabel):
    clicked = Signal(str)

    def __init__(self, parent = None):
        super(ClickableLabel, self).__init__(parent = parent)

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())


class ModelingRunMsgWidget(QWidget):
    def __init__(self, parent = None):
        super(ModelingRunMsgWidget, self).__init__(parent = parent)
        self.parent = parent
        runMsg_layout = QVBoxLayout()
        runInformation= QGroupBox("Information")
        messageLayout = QVBoxLayout()

        self.runMessage = QTextEdit()
        self.errorMessage = QTextEdit()
        self.runMessage.setReadOnly(True)
        self.errorMessage.setReadOnly(True)
        self.runMessage.setMinimumHeight(100)
        self.errorMessage.setMinimumHeight(80)
        self.runMessage.setMaximumHeight(200)
        self.errorMessage.setMaximumHeight(150)

        self.APM = AsyncProcessMonitor()
        self.APM.stdout.connect(self.stdout_treatment)
        self.APM.stderr.connect(self.stderr_treatment)
        self.APM.finished.connect(self.next_treatment)
        messageLayout.addWidget(self.APM)
        runMs = QLabel("Running Message:")
        errorMs = QLabel("Error/Warning Message:")
        messageLayout.addWidget(runMs)
        messageLayout.addWidget(self.runMessage)
        messageLayout.addWidget(errorMs)
        messageLayout.addWidget(self.errorMessage)
        runInformation.setLayout(messageLayout)

        runMsg_layout.addWidget(runInformation)
        self.setLayout(runMsg_layout)

    def stdout_treatment(self, stdout):
        """
        standard output message
        """
        self.runMessage.append(stdout)

    def next_treatment(self):
        """
        treatment after completing the mission
        """
        self.parent.widget_control('idle')

    def stderr_treatment(self, stderr):
        """
        standard error message
        """
        self.errorMessage.append(stderr)


#=====================================================#
#-------------------  MainWindow  --------------------#
#=====================================================# 

class MainWindow(QMainWindow):
    def __init__(self, parent_object = None, option = None):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Object Detection")
        self.resize(785, 920)
        self.setMinimumSize(500,700)
        self.tool = ToolTab(self)
        self.setCentralWidget(self.tool)

        self.parent_object = parent_object

        #self.show()


##=====================================================#
#def main():
#    app = QApplication(sys.argv)
#    main = MainWindow()
#    sys.exit(app.exec_())                       # excute main interface
#
#if __name__ == "__main__":
#    main()

