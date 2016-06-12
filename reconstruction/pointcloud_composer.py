import FreeCAD,FreeCADGui
import  Part
from pivy.coin import *
 
from PySide import QtCore
from PySide.QtGui import QApplication, QCursor 


import reconstruction
#reload (reconstruction.projectiontools)
#from reconstruction.projectiontools import *

import reconstruction.miki as miki
reload(miki)

import numpy as np
import time, random

App=FreeCAD
Gui=FreeCADGui


class _Composer():

	def __init__(self,obj):
		obj.Proxy = self
		self.obj=obj

	def execute(self,obj):
		print ("ich bin execute")
		if obj.updateOnChange:
			run_transform2(self.obj)

	def run(self):
		run_transform2(self.obj)
		App.activeDocument().recompute()
		Gui.updateGui()



def _createComposer():

		scaler=1000
		obj=FreeCAD.ActiveDocument.addObject('Part::FeaturePython','My_PointCloudComposer')

		obj.addProperty('App::PropertyLink','pointcloudA',"Point Clouds")
		obj.addProperty('App::PropertyLink','pointcloudB',"Point Clouds")
		obj.addProperty('App::PropertyLink','pointcloudC',"Point Clouds")

		obj.addProperty('App::PropertyBool','predefinedFormula',"Compose Details")
		obj.addProperty('App::PropertyString','expressionFormula',"Compose Details")
		obj.addProperty('App::PropertyEnumeration','selectedFormula',"Compose Details")
		obj.selectedFormula=["2*A #scale A","A>B # A above B","A+B # add the heights","(A>1)*(A<2)*B # map Interval" ,"(A>2)*10","10*sin(B)"]
		obj.addProperty('App::PropertyBool','updateOnChange',"Compose Details").updateOnChange=False
		
		obj.addProperty('App::PropertyVector','minBoundBox',"Bound Box").minBoundBox=FreeCAD.Vector(-20,20,100)
		obj.addProperty('App::PropertyVector','maxBoundBox',"Bound Box").maxBoundBox=FreeCAD.Vector(-20,20,100)

		obj.ViewObject.Proxy=object()
		obj.ViewObject.PointColor=(1.0,1.0,0.0)
		obj.ViewObject.PointSize=2

		_Composer(obj)
		return obj





import Points
import random
import matplotlib.pyplot as plt

def createPointset(grid,extend):
	(xmin,xmax,ymin,ymax)=extend
	pts=[]


	for ix in range(grid.shape[0]):
		for iy in range(grid.shape[1]):
			if not np.isnan(grid[ix,iy]) and grid[ix,iy]<>0:
				pts.append(FreeCAD.Vector(xmin+(0.0+(xmax-xmin)*ix)/400,ymin+(0.0+(ymax-ymin)*iy)/400,grid[ix,iy]))
				# pts.append(FreeCAD.Vector(ymin+(0.0+(ymax-ymin)*iy)/400,xmin+(0.0+(xmax-xmin)*ix)/400,grid[ix,iy]))
				
				# pts.append(FreeCAD.Vector(ymin+(0.0+(ymax-ymin)*iy)/200,xmin+(0.0+(xmax-xmin)*ix)/200,grid[ix,iy]))
	print pts
	pout=Points.Points(pts)
	return pout




def transformPointCloud2(cmd,string,extend,showmatplot=False):

	pout=createPointset(cmd.T,extend)
	Points.show(pout)
	
	result=App.ActiveDocument.ActiveObject
	result.ViewObject.hide()
	
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
	App.ActiveDocument.ActiveObject.Label=string
	#App.activeDocument().recompute()
	#Gui.updateGui()

	if showmatplot:
		plt.imshow(cmd, origin='lower')
		plt.title('data for ' + string)
		plt.gca().get_xaxis().set_visible(False)
		plt.gca().get_yaxis().set_visible(False)
		plt.colorbar()
		plt.show()
	s=[]
	for  p in pout.Points:
		shape = Part.Vertex(p)
		s.append(shape)
	comp=Part.makeCompound(s)
	#Part.show(comp)
	#result2=App.ActiveDocument.ActiveObject.Shape
	result2=comp
	return result,result2

def getGriddata(x,y,z,extend):
	''' data x,y,z and boundbox  to print '''
	(xmin,xmax,ymin,ymax)=extend

	grid_y, grid_x = np.mgrid[xmin:xmax:(xmax-xmin)*10j, ymin:ymax:(ymax-ymin)*10j]

	points=[]
	for i in range(x.shape[0]):
		## points.append([x[i],y[i]])
		points.append([y[i],x[i]])

	values=z

	# see http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html
	from scipy.interpolate import griddata
#	grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
#	grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
	grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')

	return grid_z2


def run_transform2(composer):

	extend=(-20,20,-20,20)

	if composer.pointcloudA<>None:
		ya=np.array([p.x for p in composer.pointcloudA.Points.Points])
		xa=np.array([p.y for p in composer.pointcloudA.Points.Points])
		za=np.array([p.z for p in composer.pointcloudA.Points.Points])
		A=getGriddata(xa,ya,za,extend)
		#A=getGriddata(ya,xa,za,extend)
		print "okay"
	if composer.pointcloudB<>None:
		ya=np.array([p.x for p in composer.pointcloudB.Points.Points])
		xa=np.array([p.y for p in composer.pointcloudB.Points.Points])
		za=np.array([p.z for p in composer.pointcloudB.Points.Points])
		B=getGriddata(xa,ya,za,extend)
		#B=getGriddata(ya,xa,za,extend)
	if composer.pointcloudC<>None:
		xa=np.array([p.x for p in composer.pointcloudC.Points.Points])
		ya=np.array([p.y for p in composer.pointcloudC.Points.Points])
		za=np.array([p.z for p in composer.pointcloudC.Points.Points])
		C=getGriddata(xa,ya,za,extend)

	from numpy import *
	if composer.predefinedFormula:
		cmd=eval(composer.selectedFormula)
		title=composer.selectedFormula
	else:
		cmd=eval(composer.expressionFormula)
		title=composer.expressionFormula
	result,result2=transformPointCloud2(cmd,title,extend)
	
	composer.Shape=result2

	





s6='''
VerticalLayout:
		id:'main'
#		setFixedHeight: 900
#		setFixedWidth: 730
#		setFixedWidth: 700
		move:  PySide.QtCore.QPoint(3000,100)

		QtGui.QLabel:
			setText:"***     C O M P O S E     P O I N T  C L O U D S     ***"



		QtGui.QLabel:
			setText:"Formula with A,B,C as the names of the pointclouds"

		QtGui.QLabel:

		QtGui.QLabel:
		QtGui.QLineEdit:
			setText:"3*A +2*B"
			id: 'bl'
		
		QtGui.QLabel:
		QtGui.QLabel:
			id:'gridcountlabel'
			setText:"Number of Grid lines"

		QtGui.QSlider:
			id:'gridcount'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 9
#			setTickInterval: 500
			setValue: 6
#			setTickPosition: QtGui.QSlider.TicksBothSides
# 			valueChanged.connect: app.creategrid

		QtGui.QCheckBox:
			id: 'measuringpoints' 
			setText: 'show elevation grid'
#			setChecked: True
#			clicked.connect: app.showmode


		QtGui.QPushButton:
			setText: "create/update point cloud"
			clicked.connect: app.recomputePointCloud

		QtGui.QPushButton:
			setText: "close"
			clicked.connect: app.close


'''


class MyApp(object):

	def create(self):
		self.ob=_createPerspective()

	def recomputePointCloud(self):
		print "recompute cloud ...."

	def close(self):
		pass


def run():
	global miki
	app=MyApp()
	miki2=miki.Miki()
	miki2.app=app
	app.root=miki2
	miki2.run(s6)
	app.create()

#createPerspective()
