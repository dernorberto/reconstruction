# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- reconstruction workbench
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

__vers__="13.03.2016  0.1"
__dir__='/home/thomas/.FreeCAD/Mod/reconstruction'


import sympy
from sympy import Point3D,Plane

import PySide
from PySide import QtCore, QtGui

import FreeCAD,FreeCADGui

from . import cv2
import numpy as np


import reconstruction
import importlib
importlib.reload (reconstruction.projectiontools)
from reconstruction.projectiontools import *
from reconstruction.CV import _CV, _ViewProviderCV, createCV
importlib.reload(reconstruction.CV )

import reconstruction.miki as miki
importlib.reload(miki)


class _CV_cornerharris(_CV):

	def __init__(self,obj,icon='/icons/animation.png'):
		_CV.__init__(self,obj,icon)
		_ViewProviderCV_cornerharris(obj.ViewObject,icon)

	def execute(self,obj):
		obj.ViewObject.Proxy.animpingpong()
		return

class _ViewProviderCV_cornerharris(_ViewProviderCV):
	
	def __init__(self,vobj,icon):
		_ViewProviderCV.__init__(self,vobj,icon)

	def showVersion(self):
		cl=self.Object.Proxy.__class__.__name__
		PySide.QtGui.QMessageBox.information(None, "About ",  cl  +"_\nVersion " + __vers__)

	def edit(self):
		_ViewProviderCV.edit(self)
		self.animpingpong()

	def animpingpong(self):
		obj=self.Object
		img=None
		if not obj.imageFromNode:
			img = cv2.imread(obj.imageFile)
		else:
			img = obj.imageNode.ViewObject.Proxy.img.copy()

		print((obj.blockSize,obj.ksize,obj.k))
		try:
			gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			gray = np.float32(gray)
			print("normale")
		except:
			im2=cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
			gray = cv2.cvtColor(im2,cv2.COLOR_RGB2GRAY)
			print("except")

		dst = cv2.cornerHarris(gray,obj.blockSize,obj.ksize*2+1,obj.k/10000)
		dst = cv2.dilate(dst,None)

		img[dst>0.01*dst.max()]=[0,0,255]

		dst2=img.copy()
		dst2[dst<0.01*dst.max()]=[255,255,255]
		dst2[dst>0.01*dst.max()]=[0,0,255]

		if not obj.matplotlib:
			cv2.imshow(obj.Label,img)
		else:
			from matplotlib import pyplot as plt
			plt.subplot(121),plt.imshow(img,cmap = 'gray')
			plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
			plt.subplot(122),plt.imshow(dst2,cmap = 'gray')
			plt.title('Corner Image'), plt.xticks([]), plt.yticks([])
			plt.show()

		self.img=img


s6='''
VerticalLayout:
		id:'main'

		QtGui.QLabel:
			setText:"***     O P E N   C V     ***"
		QtGui.QLabel:

		QtGui.QLabel:
			setText:"***    Harris Corner Detection  ***"
		QtGui.QLabel:

		QtGui.QLabel:
			id:'blockSizeLabel'
			setText:"BlockSize"

		QtGui.QSlider:
			id:'blockSize'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 10
#			setTickInterval: 10
			setValue: 2
			setTickPosition: QtGui.QSlider.TicksBelow
			valueChanged.connect: app.change

		QtGui.QLabel:
			id:'ksizeLabel'
			setText:"ksize"

		QtGui.QSlider:
			id:'ksize'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 15
			setValue: 1
# site *2 +1  --> 3
			setTickPosition: QtGui.QSlider.TicksBelow
			valueChanged.connect: app.change

		QtGui.QLabel:
			id:'kLabel'
			setText:"k"

		QtGui.QSlider:
			id:'k'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 10000
			setValue: 1
# val/10000
			valueChanged.connect: app.change

		QtGui.QPushButton:
			id:'moveBtn'
			setText: "update view"
			clicked.connect: app.create
			setEnabled: False
'''


class MyApp(object):

	def create(self):
		self.obj.Proxy.execute(self.obj)

	def change(self):
		print("changed")
		self.obj.k=self.root.ids['k'].value()
		self.obj.ksize=self.root.ids['ksize'].value()
		self.obj.blockSize=self.root.ids['blockSize'].value()

		self.root.ids['kLabel'].setText("k " + str(round((0.0+self.obj.k)/10000,5)))
		self.root.ids['ksizeLabel'].setText("ksize " + str(self.obj.ksize*2+1))
		self.root.ids['blockSizeLabel'].setText("blockSize " + str(self.obj.blockSize))

		self.obj.Proxy.execute(self.obj)


def createCV_cornerharris():
	print("create CV  cornerharris ... 2")
	obj= createCV(True)
	obj.Label='Harris'

	obj.addProperty('App::PropertyInteger','blockSize',"cornerHarris").blockSize=2
	obj.addProperty('App::PropertyInteger','ksize',"cornerHarris").ksize=3
	obj.addProperty('App::PropertyFloat','k',"cornerHarris").k=1.0

	_CV_cornerharris(obj,__dir__+ '/icons/icon2.svg')
	miki2=miki.Miki2(MyApp,s6,obj)

	return obj

def run():
	 return createCV_cornerharris()
