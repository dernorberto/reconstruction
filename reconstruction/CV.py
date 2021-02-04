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
import importlib
App=FreeCAD
Gui=FreeCADGui

import Draft


#----------------------------------------------------

class _EditWidget(QtGui.QWidget):
	'''double clicked dialog''' 
	def __init__(self, dialer,obj,menu,noclose,*args):
		QtGui.QWidget.__init__(self, *args)
		obj.widget=self
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.vollabel =QtGui.QLabel( "<b>"+obj.Object.Label+"</b>") 

		if dialer:
			dial = QtGui.QDial()
			dial.setNotchesVisible(True)
			self.dial=dial
			dial.setMaximum(100)
			dial.valueChanged.connect(obj.dialer);

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.vollabel)

		for m in menu:
			bt=QtGui.QPushButton(m[0])
			bt.clicked.connect(m[1])
			layout.addWidget(bt)

		if dialer:
			layout.addWidget(dial)

		if not noclose:
			self.pushButton02 = QtGui.QPushButton("close")
			self.pushButton02.clicked.connect(self.hide)
			layout.addWidget(self.pushButton02)

		self.setLayout(layout)
		try:
			self.setWindowTitle(obj.Object.target.Label)
		except:
			pass


class EditWidget(_EditWidget):
	def __init__(self, obj,menu,noclose,*args):
		_EditWidget.__init__(self, True, obj,menu,noclose,*args)

class EditNoDialWidget(_EditWidget):
	def __init__(self, obj,menu,noclose,*args):
		_EditWidget.__init__(self, False, obj,menu,noclose,*args)



#-----------------------------------------------------


from . import cv2
import numpy as np

import time

class _CV(object):

	def __init__(self,obj,icon='/icons/animation.png'):
		obj.Proxy = self
		self.Type = self.__class__.__name__
		self.obj2 = obj
		self.Lock=False
		self.Changed=False
		_ViewProviderCV(obj.ViewObject,icon) 


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

	def execute(self,obj):
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

class _ViewProviderCV():
 
	def __init__(self,vobj,icon='/icons/icon1.svg'):
		print("viewwproergrger")
		self.iconpath = icon
		print(self.iconpath)
		self.Object = vobj.Object
		vobj.Proxy = self
		self.cmenu=[]
		self.emenu=[]

		self.vers=__vers__
 
	def getIcon(self):
		return self.iconpath

	def attach(self,vobj):
		self.cmenu=[]
		self.emenu=[]
		self.Object = vobj.Object
		#icon='/icons/animation.png'
		#self.iconpath = __dir__ + icon

	def anims(self):
		return [['forward',self.animforward],['backward',self.animbackward],['ping pong',self.animpingpong]]

	def showVersion(self):
		cl=self.Object.Proxy.__class__.__name__
		PySide.QtGui.QMessageBox.information(None, "About ", "Animation" + cl +" Node\nVersion " + self.vers)

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
		print(anims)
		self.dialog=EditWidget(self,self.emenu + anims,False)
		self.dialog.show()

	def setEdit(self,vobj,mode=0):
		self.edit()
		return True

	def unsetEdit(self,vobj,mode=0):
		return False

	def doubleClicked(self,vobj):
		self.setEdit(vobj,1)

	def claimChildren(self):
		try:
			return self.Object.Group
		except:
			return None

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None

	def dialog(self,noclose=False):
		return EditWidget(self,self.emenu + self.anims(),noclose)

	def animforward(self):
		FreeCADGui.ActiveDocument.ActiveView.setAnimationEnabled(False)

	def animbackward(self):
		FreeCADGui.ActiveDocument.ActiveView.setAnimationEnabled(False)
		for i in range(101):
			self.obj2.time=float(100-i)/100
			FreeCAD.ActiveDocument.recompute()
			FreeCADGui.updateGui() 
			time.sleep(0.02)

	def animpingpong(self):
		print(self)
		print(self.Object)
		print(self.Object.Name)
		obj=self.Object
		img = cv2.imread(obj.imageFile)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		gray = np.float32(gray)
		dst = cv2.cornerHarris(gray,3,3,0.00001)
		dst = cv2.dilate(dst,None)
		img[dst>0.01*dst.max()]=[0,0,255]

		from matplotlib import pyplot as plt
		plt.subplot(121),plt.imshow(img,cmap = 'gray')
		plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
		plt.subplot(122),plt.imshow(dst,cmap = 'gray')
		plt.title('Corner Image'), plt.xticks([]), plt.yticks([])
		plt.show()


import reconstruction
importlib.reload (reconstruction.projectiontools)
from reconstruction.projectiontools import *

import reconstruction.miki as miki
importlib.reload(miki)

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

		QtGui.QSlider:
			id:'scalepoint'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: -100
			setMaximum: 100
			setTickInterval: 10
			setValue: 10
			setTickPosition: QtGui.QSlider.TicksBelow
			valueChanged.connect: app.create

		QtGui.QPushButton:
			id:'moveBtn'
			setText: "run a  testscript 2"
			clicked.connect: app.create
			setEnabled: False
'''

	def create(self):
		print("my app was running")
		print(self.obj)


def createCV(base=False):
	print("create CV ...")
	obj=FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython','Image')

	obj.addProperty('App::PropertyFile','imageFile',"base").imageFile='/home/thomas/Bilder/c1.png'
	obj.addProperty('App::PropertyLink','imageNode',"base")
	obj.addProperty('App::PropertyBool','imageFromNode',"base").imageFromNode=False
	obj.addProperty('App::PropertyBool','matplotlib',"base").matplotlib=False

	if not base:
		_CV(obj,'/icons/bounder.png')
		_ViewProviderCV(obj.ViewObject,__dir__+ '/icons/icon1.svg') 

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
	return createCV()





