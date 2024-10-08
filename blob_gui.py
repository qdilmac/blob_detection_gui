"""
Blob Detection GUI
Gerekli sliderlara sahip olacak
3 farklı video feed içerecek
15/19/2024 21.19 @qdilmac - Mustafa Osman Dilmaç
"""

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QThread, Signal)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QMainWindow,
    QSizePolicy, QSlider, QStatusBar, QWidget)
import numpy as np
import cv2
import sys
import threading

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 840)
        MainWindow.setStyleSheet(u"background-color: rgb(30, 99, 115);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(150, 20, 131, 16))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.original_vf = QLabel(self.centralwidget)
        self.original_vf.setObjectName(u"original_vf")
        self.original_vf.setGeometry(QRect(30, 50, 391, 281))
        self.masked_vf = QLabel(self.centralwidget)
        self.masked_vf.setObjectName(u"masked_vf")
        self.masked_vf.setGeometry(QRect(30, 380, 391, 281))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(160, 350, 131, 16))
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.blob_vf = QLabel(self.centralwidget)
        self.blob_vf.setObjectName(u"blob_vf")
        self.blob_vf.setGeometry(QRect(460, 50, 391, 281))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(590, 20, 131, 16))
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignCenter)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(880, 30, 381, 761))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.groupBox.setFont(font1)
        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(20, 30, 341, 221))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.groupBox_2.setFont(font2)
        self.lowerhue_slider = QSlider(self.groupBox_2)
        self.lowerhue_slider.setObjectName(u"lowerhue_slider")
        self.lowerhue_slider.setGeometry(QRect(90, 30, 211, 21))
        self.lowerhue_slider.setMaximum(179)
        self.lowerhue_slider.setOrientation(Qt.Horizontal)
        self.lowerhue_slider.setTickPosition(QSlider.NoTicks)
        self.upperhue_slider = QSlider(self.groupBox_2)
        self.upperhue_slider.setObjectName(u"upperhue_slider")
        self.upperhue_slider.setGeometry(QRect(90, 60, 211, 21))
        self.upperhue_slider.setMaximum(179)
        self.upperhue_slider.setOrientation(Qt.Horizontal)
        self.upperhue_slider.setTickPosition(QSlider.NoTicks)
        self.lowersat_slider = QSlider(self.groupBox_2)
        self.lowersat_slider.setObjectName(u"lowersat_slider")
        self.lowersat_slider.setGeometry(QRect(90, 90, 211, 21))
        self.lowersat_slider.setMaximum(255)
        self.lowersat_slider.setOrientation(Qt.Horizontal)
        self.lowersat_slider.setTickPosition(QSlider.NoTicks)
        self.uppersat_slider = QSlider(self.groupBox_2)
        self.uppersat_slider.setObjectName(u"uppersat_slider")
        self.uppersat_slider.setGeometry(QRect(90, 120, 211, 21))
        self.uppersat_slider.setMaximum(255)
        self.uppersat_slider.setOrientation(Qt.Horizontal)
        self.uppersat_slider.setTickPosition(QSlider.NoTicks)
        self.upperval_slider = QSlider(self.groupBox_2)
        self.upperval_slider.setObjectName(u"upperval_slider")
        self.upperval_slider.setGeometry(QRect(90, 180, 211, 21))
        self.upperval_slider.setMaximum(255)
        self.upperval_slider.setOrientation(Qt.Horizontal)
        self.upperval_slider.setTickPosition(QSlider.NoTicks)
        self.lowerval_slider = QSlider(self.groupBox_2)
        self.lowerval_slider.setObjectName(u"lowerval_slider")
        self.lowerval_slider.setGeometry(QRect(90, 150, 211, 21))
        self.lowerval_slider.setMaximum(255)
        self.lowerval_slider.setOrientation(Qt.Horizontal)
        self.lowerval_slider.setTickPosition(QSlider.NoTicks)
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 30, 71, 20))
        font3 = QFont()
        font3.setBold(True)
        self.label_2.setFont(font3)
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 60, 71, 20))
        self.label_3.setFont(font3)
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 90, 71, 20))
        self.label_5.setFont(font3)
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 120, 71, 20))
        self.label_7.setFont(font3)
        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 150, 71, 20))
        self.label_8.setFont(font3)
        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 180, 71, 20))
        self.label_9.setFont(font3)
        self.groupBox_3 = QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(20, 270, 341, 101))
        self.groupBox_3.setFont(font2)
        self.erosion_slider = QSlider(self.groupBox_3)
        self.erosion_slider.setObjectName(u"erosion_slider")
        self.erosion_slider.setGeometry(QRect(90, 30, 211, 21))
        self.erosion_slider.setMaximum(10)
        self.erosion_slider.setOrientation(Qt.Horizontal)
        self.erosion_slider.setTickPosition(QSlider.NoTicks)
        self.dilation_slider = QSlider(self.groupBox_3)
        self.dilation_slider.setObjectName(u"dilation_slider")
        self.dilation_slider.setGeometry(QRect(90, 60, 211, 21))
        self.dilation_slider.setMaximum(10)
        self.dilation_slider.setOrientation(Qt.Horizontal)
        self.dilation_slider.setTickPosition(QSlider.NoTicks)
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(10, 30, 71, 20))
        self.label_10.setFont(font3)
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 60, 71, 20))
        self.label_11.setFont(font3)
        self.groupBox_4 = QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(20, 390, 341, 121))
        self.groupBox_4.setFont(font2)
        self.mincontour_slider = QSlider(self.groupBox_4)
        self.mincontour_slider.setObjectName(u"mincontour_slider")
        self.mincontour_slider.setGeometry(QRect(90, 30, 211, 21))
        self.mincontour_slider.setMinimum(100)
        self.mincontour_slider.setMaximum(5000)
        self.mincontour_slider.setOrientation(Qt.Horizontal)
        self.mincontour_slider.setTickPosition(QSlider.NoTicks)
        self.maxcontour_slider = QSlider(self.groupBox_4)
        self.maxcontour_slider.setObjectName(u"maxcontour_slider")
        self.maxcontour_slider.setGeometry(QRect(90, 60, 211, 21))
        self.maxcontour_slider.setMinimum(5000)
        self.maxcontour_slider.setMaximum(30000)
        self.maxcontour_slider.setOrientation(Qt.Horizontal)
        self.maxcontour_slider.setTickPosition(QSlider.NoTicks)
        self.radius_slider = QSlider(self.groupBox_4)
        self.radius_slider.setObjectName(u"radius_slider")
        self.radius_slider.setGeometry(QRect(90, 90, 211, 21))
        self.radius_slider.setMaximum(100)
        self.radius_slider.setOrientation(Qt.Horizontal)
        self.radius_slider.setTickPosition(QSlider.NoTicks)
        self.label_12 = QLabel(self.groupBox_4)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 30, 71, 20))
        self.label_12.setFont(font3)
        self.label_13 = QLabel(self.groupBox_4)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 60, 71, 20))
        self.label_13.setFont(font3)
        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(10, 90, 71, 20))
        self.label_14.setFont(font3)
        self.groupBox_5 = QGroupBox(self.groupBox)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(20, 520, 341, 221))
        self.groupBox_5.setFont(font2)
        self.label_20 = QLabel(self.groupBox_5)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(10, 120, 71, 20))
        self.label_20.setFont(font3)
        self.label_17 = QLabel(self.groupBox_5)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(10, 60, 71, 20))
        self.label_17.setFont(font3)
        self.label_18 = QLabel(self.groupBox_5)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(10, 90, 71, 20))
        self.label_18.setFont(font3)
        self.label_19 = QLabel(self.groupBox_5)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(10, 180, 71, 20))
        self.label_19.setFont(font3)
        self.label_15 = QLabel(self.groupBox_5)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(10, 30, 71, 20))
        self.label_15.setFont(font3)
        self.label_16 = QLabel(self.groupBox_5)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(10, 150, 71, 20))
        self.label_16.setFont(font3)
        self.label_21 = QLabel(self.groupBox_5)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(170, 60, 71, 20))
        self.label_21.setFont(font3)
        self.label_22 = QLabel(self.groupBox_5)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(170, 30, 71, 20))
        self.label_22.setFont(font3)
        self.label_23 = QLabel(self.groupBox_5)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QRect(170, 150, 71, 20))
        self.label_23.setFont(font3)
        self.label_24 = QLabel(self.groupBox_5)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(170, 90, 71, 20))
        self.label_24.setFont(font3)
        self.label_25 = QLabel(self.groupBox_5)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(170, 120, 71, 20))
        self.label_25.setFont(font3)
        self.lowerhue_valuelabel = QLabel(self.groupBox_5)
        self.lowerhue_valuelabel.setObjectName(u"lowerhue_valuelabel")
        self.lowerhue_valuelabel.setGeometry(QRect(100, 30, 49, 21))
        self.upperhue_valuelabel = QLabel(self.groupBox_5)
        self.upperhue_valuelabel.setObjectName(u"upperhue_valuelabel")
        self.upperhue_valuelabel.setGeometry(QRect(100, 60, 49, 21))
        self.lowersat_valuelabel = QLabel(self.groupBox_5)
        self.lowersat_valuelabel.setObjectName(u"lowersat_valuelabel")
        self.lowersat_valuelabel.setGeometry(QRect(100, 90, 49, 21))
        self.uppersat_valuelabel = QLabel(self.groupBox_5)
        self.uppersat_valuelabel.setObjectName(u"uppersat_valuelabel")
        self.uppersat_valuelabel.setGeometry(QRect(100, 120, 49, 21))
        self.lowerval_valuelabel = QLabel(self.groupBox_5)
        self.lowerval_valuelabel.setObjectName(u"lowerval_valuelabel")
        self.lowerval_valuelabel.setGeometry(QRect(100, 150, 49, 21))
        self.upperval_valuelabel = QLabel(self.groupBox_5)
        self.upperval_valuelabel.setObjectName(u"upperval_valuelabel")
        self.upperval_valuelabel.setGeometry(QRect(100, 180, 49, 21))
        self.erosion_valuelabel = QLabel(self.groupBox_5)
        self.erosion_valuelabel.setObjectName(u"erosion_valuelabel")
        self.erosion_valuelabel.setGeometry(QRect(260, 30, 49, 21))
        self.dilation_valuelabel = QLabel(self.groupBox_5)
        self.dilation_valuelabel.setObjectName(u"dilation_valuelabel")
        self.dilation_valuelabel.setGeometry(QRect(260, 60, 49, 21))
        self.mincontour_valuelabel = QLabel(self.groupBox_5)
        self.mincontour_valuelabel.setObjectName(u"mincontour_valuelabel")
        self.mincontour_valuelabel.setGeometry(QRect(260, 90, 49, 21))
        self.maxcontour_valuelabel = QLabel(self.groupBox_5)
        self.maxcontour_valuelabel.setObjectName(u"maxcontour_valuelabel")
        self.maxcontour_valuelabel.setGeometry(QRect(260, 120, 49, 21))
        self.radius_valuelabel = QLabel(self.groupBox_5)
        self.radius_valuelabel.setObjectName(u"radius_valuelabel")
        self.radius_valuelabel.setGeometry(QRect(260, 150, 49, 21))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi
    
        # -> Slider değerlerini alıp değer label'larına yazdırma
        self.lowerhue_slider.valueChanged.connect(self.lowerhue_valuelabel.setNum)
        self.upperhue_slider.valueChanged.connect(self.upperhue_valuelabel.setNum)
        self.lowersat_slider.valueChanged.connect(self.lowersat_valuelabel.setNum)
        self.uppersat_slider.valueChanged.connect(self.uppersat_valuelabel.setNum)
        self.lowerval_slider.valueChanged.connect(self.lowerval_valuelabel.setNum)
        self.upperval_slider.valueChanged.connect(self.upperval_valuelabel.setNum)
        self.erosion_slider.valueChanged.connect(self.erosion_valuelabel.setNum)
        self.dilation_slider.valueChanged.connect(self.dilation_valuelabel.setNum)
        self.mincontour_slider.valueChanged.connect(self.mincontour_valuelabel.setNum)
        self.maxcontour_slider.valueChanged.connect(self.maxcontour_valuelabel.setNum)
        self.radius_slider.valueChanged.connect(self.radius_valuelabel.setNum)
        
        # -> Video thread'i başlatma
        self.videothread = video_thread(self.lowerhue_slider.value(), self.upperhue_slider.value(), self.lowersat_slider.value(),
                                   self.uppersat_slider.value(), self.lowerval_slider.value(), self.upperval_slider.value(),
                                   self.erosion_slider.value(), self.dilation_slider.value(), self.mincontour_slider.value(),
                                   self.maxcontour_slider.value(), self.radius_slider.value())
        
        self.videothread.pixmapOriginal.connect(self.update_original)
        self.videothread.pixmapMasked.connect(self.update_masked)
        self.videothread.pixmapBlob.connect(self.update_blob)
        self.videothread.start()
        
        # -> Slider değerlerini thread içerisinde güncelleme
        self.lowerhue_slider.valueChanged.connect(self.update_video_thread_params)
        self.upperhue_slider.valueChanged.connect(self.update_video_thread_params)
        self.lowersat_slider.valueChanged.connect(self.update_video_thread_params)
        self.uppersat_slider.valueChanged.connect(self.update_video_thread_params)
        self.lowerval_slider.valueChanged.connect(self.update_video_thread_params)
        self.upperval_slider.valueChanged.connect(self.update_video_thread_params)
        self.erosion_slider.valueChanged.connect(self.update_video_thread_params)
        self.dilation_slider.valueChanged.connect(self.update_video_thread_params)
        self.mincontour_slider.valueChanged.connect(self.update_video_thread_params)
        self.maxcontour_slider.valueChanged.connect(self.update_video_thread_params)
        self.radius_slider.valueChanged.connect(self.update_video_thread_params)

    def update_video_thread_params(self):
        self.videothread.set_parameters(self.lowerhue_slider.value(), self.upperhue_slider.value(), self.lowersat_slider.value(),
                                        self.uppersat_slider.value(), self.lowerval_slider.value(), self.upperval_slider.value(),
                                        self.erosion_slider.value(), self.dilation_slider.value(), self.mincontour_slider.value(),
                                        self.maxcontour_slider.value(), self.radius_slider.value())

        
    def update_original(self, image):
        self.original_vf.setPixmap(QPixmap.fromImage(image))
        
    def update_masked(self, image):
        self.masked_vf.setPixmap(QPixmap.fromImage(image))
    
    def update_blob(self, image):
        self.blob_vf.setPixmap(QPixmap.fromImage(image))

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Original Video Feed", None))
        self.original_vf.setText("")
        self.masked_vf.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Masked Video", None))
        self.blob_vf.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Blob Detection", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Sliders", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"HSV", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Lower Hue", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Upper Hue", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Lower Sat.", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Upper Sat.", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Lower Value", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Upper Value", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Erosion - Dilation", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Erosion", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Dilation", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Contour - Radius (Circle)", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Min Contour", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Max Contour", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Radius", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Current Values", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Upper Sat.", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Upper Hue", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Lower Sat.", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Upper Value", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Lower Hue", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Lower Value", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Dilation", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Erosion", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Radius", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Min Contour", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Max Contour", None))
        self.lowerhue_valuelabel.setText(QCoreApplication.translate("MainWindow", u"NaN", None))
        self.upperhue_valuelabel.setText(QCoreApplication.translate("MainWindow", u"NaN", None))
        self.lowersat_valuelabel.setText(QCoreApplication.translate("MainWindow", u"NaN", None))
        self.uppersat_valuelabel.setText(QCoreApplication.translate("MainWindow", u"NaN", None))
        self.lowerval_valuelabel.setText(QCoreApplication.translate("MainWindow", u"NaN", None))
        self.upperval_valuelabel.setText(QCoreApplication.translate("MainWindow", u"NaN", None))
        self.erosion_valuelabel.setText(QCoreApplication.translate("MainWindow", u"NaN", None))
        self.dilation_valuelabel.setText(QCoreApplication.translate("MainWindow", u"NaN", None))
        self.mincontour_valuelabel.setText(QCoreApplication.translate("MainWindow", u"NaN", None))
        self.maxcontour_valuelabel.setText(QCoreApplication.translate("MainWindow", u"NaN", None))
        self.radius_valuelabel.setText(QCoreApplication.translate("MainWindow", u"NaN", None))
    # retranslateUi
    
# -> Kameradan görüntü alıp üç farklı <isim>_vf QLabel'ına yazdıracak olan thread, blob detection işlemlerini vs de yapacak
class video_thread(QThread):
    pixmapOriginal = Signal(QImage)
    pixmapMasked = Signal(QImage)
    pixmapBlob = Signal(QImage)
    
    def __init__(self, lower_hue, upper_hue, lower_sat, upper_sat, lower_val, upper_val, erosion, dilation, min_contour, max_contour, radius):
        super().__init__()
        # -> initial parametreleri fonksiyon çağırarak set et
        self.set_parameters(lower_hue, upper_hue, lower_sat, upper_sat, lower_val, upper_val, erosion, dilation, min_contour, max_contour, radius)

    def set_parameters(self, lower_hue, upper_hue, lower_sat, upper_sat, lower_val, upper_val, erosion, dilation, min_contour, max_contour, radius):
        self.lower_hue = lower_hue
        self.upper_hue = upper_hue
        self.lower_sat = lower_sat
        self.upper_sat = upper_sat
        self.lower_val = lower_val
        self.upper_val = upper_val
        self.erosion = erosion
        self.dilation = dilation
        self.min_contour = min_contour
        self.max_contour = max_contour
        self.radius = radius
        # -> debug, açık istemiyorsan yorum satırına al
        print(f"Parametreler Güncellendi: {self.lower_hue}, {self.upper_hue}, {self.lower_sat}, {self.upper_sat}, {self.lower_val}, {self.upper_val}, {self.erosion}, {self.dilation}, {self.min_contour}, {self.max_contour}, {self.radius}")
        
    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Kamera açılamadı")
            return
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue

            # -> Orijinal video feed'i QLabel'a yazdırma
            original_vf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            original_vf = cv2.resize(original_vf, (391, 281))
            original_vf_qt = QImage(original_vf, original_vf.shape[1], original_vf.shape[0], original_vf.strides[0], QImage.Format_RGB888)
            self.pixmapOriginal.emit(original_vf_qt)

            # -> Orijinal görüntüyü HSV'ye dönüştürme ve maskeleme
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower = np.array([self.lower_hue, self.lower_sat, self.lower_val])
            upper = np.array([self.upper_hue, self.upper_sat, self.upper_val])
            mask = cv2.inRange(hsv, lower, upper)

            # -> Gaussian blur, erosion, dilation işlemleri -> maskeyi daha net hâle getirmek için
            blurred_mask = cv2.GaussianBlur(mask, (5, 5), 0)

            kernel = np.ones((5, 5), np.uint8)
            eroded_mask = cv2.erode(blurred_mask, kernel, iterations=self.erosion)
            dilated_mask = cv2.dilate(eroded_mask, kernel, iterations=self.dilation)

            # -> Maskeleme sonucunu QLabel'a yazdırma
            masked_vf = cv2.bitwise_and(frame, frame, mask=dilated_mask)
            masked_vf = cv2.cvtColor(masked_vf, cv2.COLOR_BGR2RGB)
            masked_vf = cv2.resize(masked_vf, (391, 281))
            masked_vf_qt = QImage(masked_vf, masked_vf.shape[1], masked_vf.shape[0], masked_vf.strides[0], QImage.Format_RGB888)
            self.pixmapMasked.emit(masked_vf_qt)

            # -> Contour detection ve blob detection
            contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if self.min_contour < area < self.max_contour:
                    perimeter = cv2.arcLength(cnt, True)
                    if perimeter == 0:
                        continue
                    circularity = 4 * np.pi * (area / (perimeter ** 2))

                    # -> belirlenen yuvarlaklık oranı aralığında bir blob tespit edildiyse
                    if 0.7 < circularity <= 1.2:
                        (x, y), r = cv2.minEnclosingCircle(cnt)
                        center = (int(x), int(y))
                        r = int(r)

                        # -> belirlenen yarıçap aralığında bir blob tespit edildiyse
                        frame = cv2.circle(frame, center, r, (0, 255, 0), 2)
                        frame = cv2.rectangle(frame, (int(x - r), int(y - r)), (int(x + r), int(y + r)), (255, 0, 0), 2)
                        
                        # -> opsiyonel: blob'un contour'unu çizdirme
                        cv2.drawContours(frame, [cnt], -1, (0, 0, 255), 2)

            # -> Blob detection sonucunu QLabel'a yazdırma
            blob_vf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            blob_vf = cv2.resize(blob_vf, (391, 281))
            blob_vf_qt = QImage(blob_vf, blob_vf.shape[1], blob_vf.shape[0], blob_vf.strides[0], QImage.Format_RGB888)
            self.pixmapBlob.emit(blob_vf_qt)
    
    def stop(self):
        self.quit()
        self.wait()
    
def main():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()