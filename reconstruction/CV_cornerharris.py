# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- reconstruction workbench
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

__vers__="13.03.2016  0.0"
__dir__='/home/thomas/.FreeCAD/Mod/reconstruction'


import sympy
from sympy import Point3D,Plane

import PySide
from PySide import QtCore, QtGui


import FreeCAD,FreeCADGui
App=FreeCAD
Gui=FreeCADGui

import Draft


from reconstruction.CV import _CV, _ViewProviderCV




import cv2
import numpy as np

import time

class _CV_cornerharris(_CV):

	def __init__(self,obj,icon='/icons/animation.png'):
		print "init cv cornerharris "
		obj.Proxy = self
		self.Type = self.__class__.__name__
		self.obj2 = obj
		self.Lock=False
		self.Changed=False
		_ViewProviderCV_cornerharris(obj.ViewObject,icon) 


	def initPlacement(self,tp):
		self.obj.initPlace=tp
		self.obj.obj2.Placement=tp

	def initialize(self):
		sayd("initialize ...")
	
	def getObject(self,name):
		if  isinstance(name,str):
#			obj=FreeCAD.ActiveDocument.getObject(name)
			objl=App.ActiveDocument.getObjectsByLabel(name)
			obj=objl[0]
			sayd('obj found')
		else:
			obj=name
		sayd(obj)
		return obj

	def toInitialPlacement(self):
		self.obj.obj2.Placement=self.obj.initPlace
	def setIntervall(self,s,e):
		self.obj.start=s
		self.obj.end=e
	def step(self,now):
		sayd("Step" + str(now))
	def stepsub(self,now):
		say("runsub ...")
		say(self)
		FreeCAD.yy=self
		g=self.obj2.Group
		#say(g)
		for sob in g:
				FreeCAD.ty=sob
				say(sob.Label)
				sob.Proxy.step(now)
		
	def move(self,vec=FreeCAD.Vector(0,0,0)):
		FreeCAD.uu=self
		say("move " + str(self.obj2.Label) + " vector=" +str(vec))

	def rot(self,angle=0):
		FreeCAD.uu=self
		say("rotate " + str(self.obj2.Label) + " angle=" +str(angle))


	def execute(self,obj):
		obj.ViewObject.Proxy.animpingpong()
		return




	def attach(self,vobj):
		self.Object = vobj.Object

	def claimChildren(self):
		return self.Object.Group

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None

	def onDocumentRestored(self, fp):
		say(["onDocumentRestored",fp])

class _ViewProviderCV_cornerharris(_ViewProviderCV):
 
	def __init__(self,vobj,icon='/icons/icon1.svg'):
		print "view provider emo startet"
		self.iconpath = icon
		print self.iconpath
		self.Object = vobj.Object
		self.cmenu=[]
		self.emenu=[]
		self.Object = vobj.Object

		vobj.Proxy = self
		self.vers=__vers__
		# obj.Proxy = self
		self.Type = "_Viewpoint"
#		_ViewProviderCV_cornerharris(obj.ViewObject,icon) 
 

	def showVersion(self):
		cl=self.Object.Proxy.__class__.__name__
		PySide.QtGui.QMessageBox.information(None, "About ", "CV cornerharris" + cl +" Node\nVersion " + self.vers)

	def setupContextMenu(self, obj, menu):
		cl=self.Object.Proxy.__class__.__name__
		action = menu.addAction("About " + cl)
		action.triggered.connect(self.showVersion)

		action = menu.addAction("Edit ...")
		action.triggered.connect(self.edit)

		for m in self.cmenu + self.anims():
			action = menu.addAction(m[0])
			action.triggered.connect(m[1])

	def edit(self):
		anims=self.anims()
		print anims
		self.dialog=EditWidget(self,self.emenu + anims,False)
		self.dialog.show()
		self.animpingpong()

	def animpingpong(self):
		obj=self.Object
		img=None
		if not obj.imageFromNode:
			img = cv2.imread(obj.imageFile)
		else:
			print "copy image ..."
			img = obj.imageNode.ViewObject.Proxy.img.copy()
			print "cpied"
		
		print " loaded"
		print (obj.blockSize,obj.ksize,obj.k)
		try:
			gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			#gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			gray = np.float32(gray)
			print "normale"
		except:
			im2=cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
			gray = cv2.cvtColor(im2,cv2.COLOR_RGB2GRAY)
			print "except"

		# dst = cv2.cornerHarris(gray,3,3,0.00001)
		dst = cv2.cornerHarris(gray,obj.blockSize,obj.ksize*2+1,obj.k/10000)
		dst = cv2.dilate(dst,None)
		img[dst>0.01*dst.max()]=[0,0,255]
		if True:
			print "zeige"
			cv2.imshow(obj.Label,img)
			print "gezeigt"
		else:
			from matplotlib import pyplot as plt
			plt.subplot(121),plt.imshow(img,cmap = 'gray')
			plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
			plt.subplot(122),plt.imshow(dst,cmap = 'gray')
			plt.title('Corner Image'), plt.xticks([]), plt.yticks([])
			plt.show()
		print "fertig"
		self.img=img


import reconstruction
reload (reconstruction.projectiontools)
from reconstruction.projectiontools import *

import reconstruction.miki as miki
reload(miki)

class MyApp(object):


	s6='''
VerticalLayout:
		id:'main'
#		setFixedHeight: 900
#		setFixedWidth: 700
		move:  PySide.QtCore.QPoint(3000,100)

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
#			setTickPosition: QtGui.QSlider.TicksBelow
			valueChanged.connect: app.change


		QtGui.QLabel:
			id:'ksizeLabel'
			setText:"BlockSize"

		QtGui.QSlider:
			id:'ksize'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 15
#			setTickInterval: 10
			setValue: 1
# site *2 +1  --> 3
#			setTickPosition: QtGui.QSlider.TicksBelow
			valueChanged.connect: app.change


		QtGui.QLabel:
			id:'kLabel'
			setText:"k"

		QtGui.QSlider:
			id:'k'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 10000
#			setTickInterval: 10
			setValue: 1
# val/10000
#			setTickPosition: QtGui.QSlider.TicksBelow


		QtGui.QPushButton:
			id:'moveBtn'
			setText: "update view"
			clicked.connect: app.create
			setEnabled: False
'''

	def create(self):
		print "my app was running"
		print self.obj
		self.obj.Proxy.execute(self.obj)
		


	def change(self):
		print "changed"
		self.obj.k=self.root.ids['k'].value()
		self.obj.ksize=self.root.ids['ksize'].value()
		self.obj.ksize=self.root.ids['blockSize'].value()
		self.obj.Proxy.execute(self.obj)
		self.root.ids['kLabel'].setText("k " + str(round(self.obj.k/10000,5)))
		self.root.ids['ksizeLabel'].setText("ksize " + str(self.obj.ksize*2+1))
		self.root.ids['blockSizeLabel'].setText("blockSize " + str(self.obj.blockSize))
		

		
		pass

def createCV_cornerharris():
	print "create CV  cornerharris ..."
	obj=FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython','Harris')
	obj.addProperty('App::PropertyFile','imageFile',"base").imageFile='/home/thomas/Bilder/c1.png'
	obj.addProperty('App::PropertyLink','imageNode',"base")
	obj.addProperty('App::PropertyBool','imageFromNode',"base").imageFromNode=False
	
	obj.addProperty('App::PropertyInteger','blockSize',"cornerHarris").blockSize=2
	obj.addProperty('App::PropertyInteger','ksize',"cornerHarris").ksize=3
	obj.addProperty('App::PropertyFloat','k',"cornerHarris").k=1.0

	_CV_cornerharris(obj,'/icons/bounder.png')
	_ViewProviderCV_cornerharris(obj.ViewObject,__dir__+ '/icons/icon2.svg') 

	app=MyApp()
	miki2=miki.Miki()
	miki2.app=app
	app.root=miki2
	app.obj=obj

	obj.ViewObject.Proxy.cmenu.append(["Dialog",lambda:miki2.run(MyApp.s6)])
	obj.ViewObject.Proxy.edit= lambda:miki2.run(MyApp.s6)
	return obj


#
#  derived classes
#


def run():
	 return createCV_cornerharris()






