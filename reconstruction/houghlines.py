# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- hough line finder
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import cv2
import numpy as np
from matplotlib import pyplot as plt

import PySide
from PySide import QtCore, QtGui, QtSvg
import Part,Draft

f='/home/thomas/Dokumente/freecad_buch/b186_image_processing_opencv/P1210191.JPG'
# f='/home/thomas/Dokumente/freecad_buch/b186_image_processing_opencv/bn_454.png'

scaler=1000

def fclinev2(x1,y1,x2,y2):
	v=FreeCAD.Vector(float(x1)*scaler,float(y1)*scaler,0)
	v2=FreeCAD.Vector(float(x2)*scaler,float(y2)*scaler,0)
	l=Part.makeLine(v,v2)
	return l

def main(filename,canny1=100,canny2=200,rho=1,theta=1, threshold=10, minLineLength =25, maxLineGap =10,
			showimage=False,showimagewithlines=False,newDocument=True):
# def main(f):
	f=filename
	im = cv2.imread(f)
	gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,canny1,canny2)

	xsize=len(im[0])
	ysize=len(im)

#image, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]])
	lines = cv2.HoughLinesP(edges,1,np.pi/180*theta,threshold, minLineLength = minLineLength, maxLineGap = maxLineGap)
#	lines = cv2.HoughLinesP(edges,1,np.pi/180,10, minLineLength = 25, maxLineGap = 10)
	#lines = cv2.HoughLinesP(edges,1,np.pi/2,2)[0]

	k=0
	fclines=[]

	for l in lines:
		k += 1
		[[x1,y1,x2,y2]] = l       
		fl=fclinev2(x1,-y1,x2,-y2)
		fclines.append(fl)
		#print (x1,y1,x2,y2)
		a=cv2.line(im,(x1,y1),(x2,y2),(0,255,255),2)

	c=Part.makeCompound(fclines)
	c.Placement.Base=FreeCAD.Vector(-xsize/2*scaler,ysize/2*scaler,0)
	if newDocument:
		d=App.newDocument("HoughLines")
#		App.setActiveDocument("Unnamed1")
#		App.ActiveDocument=d
#		Gui.ActiveDocument=Gui.getDocument("Unnamed1")
		
	Part.show(c)

	cv2.imwrite('/tmp/out.png',im)

	import Image, ImageGui
	#ImageGui.open(unicode("/tmp/out.png","utf-8"))

	if showimage:
		fimg=App.activeDocument().addObject('Image::ImagePlane','Image 2')
		fimg.Label=f
		fimg.ImageFile = f
		fimg.XSize = xsize*scaler
		fimg.YSize = ysize*scaler
		fimg.Placement.Base.z=-5

	if showimagewithlines:
		fimg=App.activeDocument().addObject('Image::ImagePlane','Image with Houghlines')
		fimg.ImageFile = '/tmp/out.png'
		fimg.XSize = xsize*scaler
		fimg.YSize = ysize*scaler
		fimg.Placement.Base.z=-10
		FreeCADGui.SendMsgToActiveView("ViewFit")

	print ("lines:",k)



s6='''
VerticalLayout:
		id:'main'
		setFixedHeight: 900
		setFixedWidth: 730
		setFixedWidth: 700
		move:  PySide.QtCore.QPoint(3000,100)

		QtGui.QLabel:
			setText:"***   C O M P U T E   H O U G H   L I N E S   F O R   A N   I M A G E   ***"
		QtGui.QLabel:
		QtGui.QLineEdit:
			setText:"/home/thomas/Bilder/houghlines/P1210172.JPG"
			id: 'bl'

		QtGui.QPushButton:
			setText: "Get Image Filename"
			clicked.connect: app.getfn

		QtGui.QLabel:
			setText:"Scale"
		QtGui.QLabel:
		QtGui.QSlider:
			id:'scaler'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 2000
			setTickInterval: 100
			setValue: 500
			setTickPosition: QtGui.QSlider.TicksBelow

		QtGui.QLabel:
#		QtGui.QCheckBox:
#			id: 'elevation' 
#			setText: 'Process Elevation Data'

		QtGui.QLabel:
			setText:"C a n n y   E d g e   gradient   0 - 400"
		QtGui.QLabel:
		QtGui.QSlider:
			id:'canny1'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 400
			setTickInterval: 10
			setValue: 100
			setTickPosition: QtGui.QSlider.TicksBelow
		QtGui.QSlider:
			id:'canny2'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 400
			setTickInterval: 10
			setValue: 200
			

		QtGui.QLabel:
		QtGui.QLabel:
			setText:"p r o b a b i l i s t i c   H o u g h   t r a n s f o r m "
		QtGui.QLabel:

		QtGui.QLabel:
			setText:"rho = Distance resolution of the accumulator in pixels"
		QtGui.QSlider:
			id:'rho'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 100
			setTickInterval: 10
			setValue: 25
			setTickPosition: QtGui.QSlider.TicksBothSides

		QtGui.QLabel:
			setText:"theta = Angle resolution of the accumulator in Degree."
		QtGui.QSlider:
			id:'theta'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 180
			setTickInterval: 10
			setValue: 1
			setTickPosition: QtGui.QSlider.TicksBothSides

		QtGui.QLabel:
			setText:"threshold = Accumulator threshold parameter. Only those lines are returned that get enough votes."
		QtGui.QSlider:
			id:'threshold'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 100
			setTickInterval: 10
			setValue: 10
			setTickPosition: QtGui.QSlider.TicksBothSides

		QtGui.QLabel:
			setText:"minLineLength = Minimum line length. Line segments shorter than that are rejected."
		QtGui.QSlider:
			id:'minLineLength'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 100
			setTickInterval: 10
			setValue: 25
			setTickPosition: QtGui.QSlider.TicksBothSides

		QtGui.QLabel:
			setText:"maxLineGap = Maximum allowed gap between points on the same line to link them."
		QtGui.QSlider:
			id:'maxLineGap'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 100
			setTickInterval: 10
			setValue: 10
			setTickPosition: QtGui.QSlider.TicksBothSides

	QtGui.QLabel:
	QtGui.QLabel:
			setText:"O U T P U T:"
			id: "status"

		QtGui.QCheckBox:
			id: 'showimage' 
			setText: 'Show Image'

		QtGui.QCheckBox:
			id: 'showimagewithlines' 
			setText: 'Show Image with Lines'

		QtGui.QCheckBox:
			id: 'newDocument' 
			setText: 'create new Document'
			setChecked: True


		QtGui.QPushButton:
			setText: "Run values"
			clicked.connect: app.run

'''

import FreeCAD,FreeCADGui

class MyApp(object):

	def run(self):
		print "run app"
		filename=self.root.ids['bl'].text()
		#main(s.text())
		main(
		filename,
		self.root.ids['canny1'].value(),
		self.root.ids['canny2'].value(),
		self.root.ids['rho'].value(),
		self.root.ids['theta'].value(),
		self.root.ids['threshold'].value(),
		self.root.ids['minLineLength'].value(),
		self.root.ids['maxLineGap'].value(),
		self.root.ids['showimage'].isChecked(),
		self.root.ids['showimagewithlines'].isChecked(),
		self.root.ids['newDocument'].isChecked(),
		)
		# main(filename,canny1=100,canny2=200,rho=1,theta=1, threshold=10, minLineLength =25, maxLineGap =10)


	def getfn(self):
		fileName = QtGui.QFileDialog.getOpenFileName(None,u"Open File",u"/home/thomas/Bilder/houghlines",u"Images (*.png *.xpm *.jpg)");
		print fileName
		s=self.root.ids['bl']
		s.setText(fileName[0])


#def findHoughLines():

def run():
	
	print "huhu"
	app=MyApp()

	import geodat
	import geodat.miki as miki
	reload(miki)

	miki=miki.Miki()
	miki.app=app
	app.root=miki

	miki.parse2(s6)
	miki.run(s6)



#findHoughLines()
