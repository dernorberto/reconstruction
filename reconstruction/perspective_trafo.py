
import FreeCADGui as Gui
import FreeCAD,Part,Sketcher,Draft
App=FreeCAD

import PySide
from PySide import  QtGui,QtCore

import numpy as np
import random, time, os
from pivy import coin
import PIL


def find_coeffs(pa, pb):
	''' coeeffs for a perspective transfo of 2D-quadrangle pa to pb '''
	matrix = []
	for p1, p2 in zip(pa, pb):
		matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
		matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

	A = np.matrix(matrix, dtype=np.float)
	B = np.array(pb).reshape(8)

	res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
	return np.array(res).reshape(8)



def addTextureImage(obj,fn,color=(1.0,1.0,1.0),transparency=0):
	rootnode = obj.ViewObject.RootNode
	cl=rootnode.getChildren()

	try:
		cl[1].filename.getValue()
		rootnode.removeChild(1) 
	except:
		pass
		# print "no image to delete"

	tex =  coin.SoTexture2()
	tex.filename = str(fn)
	rootnode.insertChild(tex,1)
	obj.ViewObject.Transparency=transparency
	obj.ViewObject.ShapeColor=color


def runwid(text):
	w=QtGui.QWidget()
	w.setStyleSheet("QLabel { color: rgb(255, 0, 0); font-size: 20px; background-color: rgba(255, 255, 100, 100); border: 1px solid rgba(188, 188, 188, 250); }")
	w.setGeometry(800, 400, 10, 10)

	box = QtGui.QVBoxLayout()
	w.setLayout(box)
	w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

	l=QtGui.QLabel(text)
	box.addWidget(l)
	return w


def runw(window):

	window.rw=runwid("Running ...<br>load the image and create the projections")
	window.rw.show()
	window.hide()

	fn=window.anz.text()
	FreeCAD.ParamGet('User parameter:Plugins/reconstruction').SetString("Document",fn)

	bn=os.path.basename(fn)
	dn=os.path.dirname(fn)

	# load the image
	try: im = PIL.Image.open(fn)
	except:
		window.rw=runwid("Error loading file " + fn)
		window.show()
		window.rw.show()
		return

	sx,sy=im.size

	# load the image
	if App.ActiveDocument==None:
		App.ActiveDocument=App.newDocument("Unnamed")
		App.setActiveDocument("Unnamed")

	try: obj=App.ActiveDocument.Plane
	except: 
		obj=App.ActiveDocument.addObject("Part::Plane","Plane")
		App.ActiveDocument.recompute()
	obj.Label=bn

	obj.Length=sx
	obj.Width=sy

	addTextureImage(obj,fn)


	#set up the projection infrastructure
	try: obj2=App.ActiveDocument.Plane001
	except: 
		obj2=App.ActiveDocument.addObject("Part::Plane","Plane001")
		App.ActiveDocument.recompute()
	obj2.Label="Landscape Trafo "  + bn
	m=obj2.ViewObject.ShapeMaterial
	m.DiffuseColor=(0.0,0.0,0.0,0.0)
	m.EmissiveColor=(0.0,1.0,1.0,0.0)
	

	try: obj3=App.ActiveDocument.Plane002
	except: 
		obj3=App.ActiveDocument.addObject("Part::Plane","Plane002")
		App.ActiveDocument.recompute()
	obj3.Label="Portrait Trafo "  + bn
	m=obj3.ViewObject.ShapeMaterial
	m.DiffuseColor=(0.0,0.0,1.0,1.0)
	m.EmissiveColor=(1.0,1.0,0.0,1.0)
	

	try:
		sk=App.ActiveDocument.Sketch
		geo=sk.Geometry
	except:
		sk = App.ActiveDocument.addObject('Sketcher::SketchObject','Sketch')
		sk.addGeometry(Part.LineSegment(App.Vector(0,0,0),
			App.Vector(sx,0,0)),False)
		App.ActiveDocument.recompute()

		sk.addGeometry(Part.LineSegment(App.Vector(sx,0,0),
			App.Vector(sx,sy,0)),False)
		App.ActiveDocument.recompute()
		sk.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 

		sk.addGeometry(Part.LineSegment(App.Vector(sx,sy,0),
			App.Vector(0,sy,0)),False)
		App.ActiveDocument.recompute()
		sk.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 

		sk.addGeometry(Part.LineSegment(App.Vector(-100,100,0),
			App.Vector(-100,-100,0)),False)
		App.ActiveDocument.recompute()
		sk.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		sk.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.recompute()
		geo=App.ActiveDocument.Sketch.Geometry

	sk.Label="Border for " + bn
	sk.ViewObject.LineColor=(1.0,0.0,0.0)
	sk.ViewObject.LineWidth=5
	
	pa=[(geo[i].StartPoint.x,sy-geo[i].StartPoint.y) for i in [0,1,3,2]]

	#size of the results
	a=3000
	b=2000

	#border offset
	try: r=int(window.off.text())
	except:
		print("cannot convert offset value")
		window.off.setText('0')
		r=0

	pb=[(r, r), (a-r, r), (r,b-r), (a-r,b-r)]
	
	M=find_coeffs(pb, pa)

	ima=im.transform((a, b), PIL.Image.PERSPECTIVE, M,
			PIL.Image.BICUBIC)

	im2=ima.transpose(PIL.Image.FLIP_TOP_BOTTOM)

	a3,b3=b,a
	im3=ima.transpose(PIL.Image.ROTATE_90)
 

	rotpos=window.rotpos.isChecked()

	if rotpos and window.rotneg.isChecked():
		window.rotneg.click()

	rotneg=window.rotneg.isChecked()

	if (rotpos or rotneg) and window.rot180.isChecked():
		window.rot180.click()

	rot180=window.rot180.isChecked()

	if rotpos:
		im3=im3.transpose(PIL.Image.ROTATE_90)
		im2=im2.transpose(PIL.Image.ROTATE_270)

	if rotneg:
		im3=im3.transpose(PIL.Image.ROTATE_270)
		im2=im2.transpose(PIL.Image.ROTATE_90)

	if rot180:
		im3=im3.transpose(PIL.Image.ROTATE_180)
		im2=im2.transpose(PIL.Image.ROTATE_180)


	# save the images into the sdame directory dn with profixes
	fn2=dn+'/_land_'+ bn
	im2.save(fn2)

	fn3=dn+'/_port_'+ bn
	im3.save(fn3)

	FreeCAD.Console.PrintMessage( "\nSave images as " + fn2+" "+fn3)

	obj2.Placement.Base.x=sx+50
	obj2.Length=a
	obj2.Width=b
	addTextureImage(obj2,fn2)
	App.ActiveDocument.recompute()


	obj3.Placement.Base.x=sx+a+100
	obj3.Length=a3
	obj3.Width=b3
	addTextureImage(obj3,fn3)
	App.ActiveDocument.recompute()
	Gui.SendMsgToActiveView("ViewFit")

	# geht noch nicht #?
	obj3.ViewObject.ShapeMaterial.DiffuseColor=(0.0,0.0,0.0,0.0)
	obj3.ViewObject.ShapeMaterial.EmissiveColor=(1.0,1.0,0.0,1.)
	obj2.ViewObject.ShapeMaterial.DiffuseColor=(0.0,0.0,0.0,0.0)
	obj2.ViewObject.ShapeMaterial.EmissiveColor=(.0,1.0,1.0,1.)

	print("colors")
	print(obj3.ViewObject.ShapeMaterial.DiffuseColor)




	for ob in [obj, obj2,obj3]:
		ob.ViewObject.Selectable = False

	
	window.show()
	window.rw.hide()





# dialog template



def run2(window):

	anz=int(window.anz.text())
	print(anz)

	print(window.r.isChecked())

	window.r.hide()
	window.hide()


def dialog(fn):

	w=QtGui.QWidget()

	box = QtGui.QVBoxLayout()
	w.setLayout(box)
	w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

	l=QtGui.QLabel("Path to Image" )
	box.addWidget(l)
	w.anz = QtGui.QLineEdit()
	w.anz.setText(fn)
	box.addWidget(w.anz)

	loff=QtGui.QLabel("Offset Border" )
	box.addWidget(loff)
	w.off = QtGui.QLineEdit()
	w.off.setText("100")
	box.addWidget(w.off)

	w.rotpos=QtGui.QCheckBox("Rot +90")
	box.addWidget(w.rotpos)

	w.rotneg=QtGui.QCheckBox("Rot -90")
	box.addWidget(w.rotneg)

	w.rot180=QtGui.QCheckBox("Rot 180")
	box.addWidget(w.rot180)



	w.r=QtGui.QPushButton("run")
	box.addWidget(w.r)
	w.r.pressed.connect(lambda :runw(w))

	w.show()
	return w



def run():
	fn=FreeCAD.ParamGet('User parameter:Plugins/reconstruction').GetString("Document",'/tmp/xyz.png')
	FreeCAD.t=dialog(fn)


