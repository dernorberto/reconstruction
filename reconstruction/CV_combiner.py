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


class _CV_combiner(_CV):

	def __init__(self,obj,icon='/icons/animation.png'):
		_CV.__init__(self,obj,icon)
		_ViewProviderCV_combiner(obj.ViewObject,icon)

	def execute(self,obj):
		obj.ViewObject.Proxy.animpingpong()
		return

class _ViewProviderCV_combiner(_ViewProviderCV):
	
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
		
		res=None
		for t in obj.OutList:
			print(t.Label)
			img=t.ViewObject.Proxy.img.copy()
			if res==None:
				res=img.copy()
			else:
				#rr=cv2.subtract(res,img)
				#rr=cv2.add(res,img)
				
				aw=0.0+float(obj.aWeight)/100
				bw=0.0+float(obj.bWeight)/100
				print(aw)
				print(bw)
				if obj.aInverse:
					# b umsetzen
					ret, mask = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
					img=cv2.bitwise_not(mask)
				rr=cv2.addWeighted(res,aw,img,bw,0)
				res=rr
		#b,g,r = cv2.split(res)
		cv2.imshow(obj.Label,res)
		#cv2.imshow(obj.Label +" b",b)
		#cv2.imshow(obj.Label + " g",g)
		#cv2.imshow(obj.Label + " r",r)

		res=img
		
		if not obj.matplotlib:
			cv2.imshow(obj.Label,img)
		else:
			from matplotlib import pyplot as plt
			# plt.subplot(121),
			plt.imshow(img,cmap = 'gray')
			plt.title(obj.Label), plt.xticks([]), plt.yticks([])
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


s6='''
VerticalLayout:
		id:'main'

		QtGui.QLabel:
			setText:"***     O P E N   C V     ***"
		QtGui.QLabel:

		QtGui.QLabel:
			setText:"***    Combiner  ***"
		QtGui.QLabel:


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


def createCV_combiner():
	print("create CV  combiner ... 2")
	obj= createCV(True)
	obj.Label='Combiner'

	obj.addProperty('App::PropertyInteger','aWeight',"combiner").aWeight=80
	obj.addProperty('App::PropertyInteger','bWeight',"combiner").bWeight=20

	obj.addProperty('App::PropertyBool','aInverse',"combiner").aInverse=False

	obj.addProperty('App::PropertyInteger','ksize',"combiner").ksize=3
	obj.addProperty('App::PropertyFloat','k',"combiner").k=1.0

	_CV_combiner(obj,__dir__+ '/icons/icon2.svg')
	miki2=miki.Miki2(MyApp,s6,obj)

	return obj

def run():
	 return createCV_combiner()
