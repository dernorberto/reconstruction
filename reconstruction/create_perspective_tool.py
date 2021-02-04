import FreeCAD,FreeCADGui
import FreeCADGui, Part
from pivy.coin import *
 
from PySide import QtCore
from PySide.QtGui import QApplication, QCursor 
import importlib

'''
import geodat
reload (geodat.projectiontools)
from geodat.projectiontools import *
import geodat
import geodat.miki as miki
reload(miki)
'''

import reconstruction
importlib.reload (reconstruction.projectiontools)
from reconstruction.projectiontools import *

import reconstruction.miki as miki
importlib.reload(miki)


import numpy as np
import time



# gefunden
# excel interface
# https://openpyxl.readthedocs.org/en/2.3.3/

# http://www.math.utah.edu/~treiberg/Perspect/Perspect.htm

class line:
	"this class will move a control point after the user clicked it and it destination place on screen"
	def __init__(self,dialog,size=10):
		peob=dialog.ob
		self.dialog=dialog
		docs().i()
		self.view = FreeCADGui.ActiveDocument.ActiveView
		self.view.viewTop()
		self.size=size
		self.stack = []
		self.callback = self.view.addEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(),self.getpoint)
		self.s=None
		self.peob=peob
		self.pepo=[peob.P0,peob.P1,peob.P2,peob.P3,peob.P4,peob.P5] #peob.P6,peob.P6]
#		QtGui.QApplication.setOverrideCursor(QCursor(QtCore.Qt.CrossCursor))

	def getpoint(self,event_cb):
		event = event_cb.getEvent()
		if event.getState() == SoMouseButtonEvent.DOWN:
			pos = event.getPosition()
			point = self.view.getPoint(pos[0],pos[1])
			if len(self.stack) == 0:
				nix=0
				mindist=1e+40
				for i in range(len(self.pepo)):
					if point.distanceToPoint(self.pepo[i])<mindist:
						nix=i
						mindist= point.distanceToPoint(self.pepo[i])
				nearest=self.pepo[nix]
				self.nix=nix
			point.z=0
			self.stack.append(point)
			if len(self.stack) == 2:
				if self.nix==0: self.peob.P0=self.stack[1]
				if self.nix==1: self.peob.P1=self.stack[1]
				if self.nix==2: self.peob.P2=self.stack[1]
				if self.nix==3: self.peob.P3=self.stack[1]
				if self.nix==4: self.peob.P4=self.stack[1]
				if self.nix==5: self.peob.P5=self.stack[1]
				if self.nix==6: self.peob.P6=self.stack[1]
				if self.nix==7: self.peob.P7=self.stack[1]
				draw(self.dialog,self.size)
				self.stack= []
#				QApplication.restoreOverrideCursor()
				self.view.removeEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(),self.callback)

	def finish(self):
		self.view.removeEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(),self.callback)



class leftpoint:
	"this class will register a point on the left surface by one mouse click"
	def __init__(self,dialog,mode='l',size=10):
		peob=dialog.ob
		self.mode=mode
		# self.leftmode=True
		self.dialog=dialog
		FreeCADGui.ActiveDocument=docs().gi()
		App.ActiveDocument=docs().i()
		self.view = FreeCADGui.ActiveDocument.ActiveView
		self.view.viewTop()
		self.size=size
		self.stack = []
		self.callback = self.view.addEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(),self.getpoint)
		self.s=None
		self.peob=peob
		self.pepo=[peob.P0,peob.P1,peob.P2,peob.P3,peob.P4,peob.P5] #peob.P6,peob.P6]
		
		grids=self.dialog.grids
		for grid in self.dialog.grids:
			grid.ViewObject.hide()
		if self.mode=='l':
			grids[0].ViewObject.show()
			grids[2].ViewObject.show()
		if self.mode=='r':
			grids[1].ViewObject.show()
			grids[3].ViewObject.show()
		if self.mode=='z':
			grids[4].ViewObject.show()
			grids[5].ViewObject.show()

		
#		QtGui.QApplication.setOverrideCursor(QCursor(QtCore.Qt.CrossCursor))



	def getpoint(self,event_cb):
		event = event_cb.getEvent()
		if event.getState() == SoMouseButtonEvent.DOWN:
			button=event.getButton()

			# process only left buttons 
			if button !=1: return



			pos = event.getPosition()
			point = self.view.getPoint(pos[0],pos[1])
			point.z=0


			self.view.removeEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(),self.callback)

			lines=[]
			p=Part.makeCircle(20,point)
			lines.append(p)
		###	lines.append(Part.makeLine(point,self.dialog.ob.zpol))

			pp=numpo(point)
			obj=self.dialog.ob
			p0=numpo(obj.P0)
#			p1=numpo(obj.P1)
			p2=numpo(obj.P2)
			p3=numpo(obj.P3)
			p4=numpo(obj.P4)
#			p5=numpo(obj.P5)
			lp=numpo(obj.lpol)
			rp=numpo(obj.rpol)
			zp=numpo(obj.zpol)
			
			
			[lp,rp,zp]=self.dialog.polset
			[p0,p2,p3,p4]=self.dialog.basepoints
			print("berechnung  basepoints")
			print(self.dialog.basepoints)
			
			
			# fehlerausgleich
#			try: 
#				sz1=schnittpunkt(p1,p2,p0,p3)
#				sz2=schnittpunkt(p4,p5,p0,p3)
#				
#				sz=np.array([(sz1[0]+sz2[0])/2,(sz1[1]+sz2[1])/2])
#				p5=schnittpunkt(p0,sr,sz,p4)
#				p1=schnittpunkt(p0,sl,sz,p2)
#				zp=zp
#			except: pass
			#-------------------------------------
			
			rval=0.0
			lval=0.0
			zval=0.0
			lrevpos=0.0
			rrevpos=0.0
			mylpv=FreeCAD.Vector()
			myrpv=FreeCAD.Vector()
			myzpv=FreeCAD.Vector()

			if self.mode=='l':
			###	lines.append(Part.makeLine(point,self.dialog.ob.lpol))
				ls=schnittpunkt(lp,pp,p0,zp)
				ls2=schnittpunkt(lp,pp,p2,zp)
				lines.append(Part.makeLine(vec(ls),vec(pp)))
				lval=perspos(pp,ls,ls2,lp)
				lval=round(lval,4)
				
				lval2=perspos(pp,ls2,ls,lp)
				lval2=round(lval2,4)
				print(("y lval lval2", lval,lval2))

				lls=ls
				lls2=ls2
				pos=np.sqrt(len2(ls,pp))

				ls=schnittpunkt(zp,pp,p0,lp)
				ls2=schnittpunkt(zp,pp,p3,lp)
				lines.append(Part.makeLine(vec(ls2),vec(pp)))
				zval=perspos(pp,ls2,ls,zp)
				zval=round(zval,4)

				zval2=perspos(pp,ls,ls2,zp)
				zval2=round(lval2,4)
				print(("zval zval2", zval,zval2))

				vls=ls
				vls2=ls2
				
				print("lval",lval)

			if self.mode=='r':
			###	lines.append(Part.makeLine(point,self.dialog.ob.lpol))
				ls=schnittpunkt(rp,pp,p0,zp)
				ls2=schnittpunkt(rp,pp,p4,zp)
				lines.append(Part.makeLine(vec(ls),vec(pp)))
				rval=perspos(pp,ls,ls2,rp)
				rval=round(rval,4)
				
				rval2=perspos(pp,ls2,ls,rp)
				rval2=round(rval2,4)
				print(("y rval ", rval,rval2))

				lls=ls
				lls2=ls2
				pos=np.sqrt(len2(ls,pp))

				ls=schnittpunkt(zp,pp,p0,rp)
				ls2=schnittpunkt(zp,pp,p3,rp)
				lines.append(Part.makeLine(vec(ls2),vec(pp)))
				zval=perspos(pp,ls2,ls,zp)
				zval=round(zval,4)

				zval2=perspos(pp,ls,ls2,zp)
				zval2=round(zval2,4)
				print(("zval zval2", zval,zval2))

				vls=ls
				vls2=ls2
				
				print("rval",rval)

			if self.mode=='z':
			###	lines.append(Part.makeLine(point,self.dialog.ob.lpol))

				ls=schnittpunkt(lp,pp,p3,rp)
				ls2=schnittpunkt(lp,pp,p2,rp)
				lines.append(Part.makeLine(vec(ls),vec(pp)))
				lines.append(Part.makeLine(vec(ls2),vec(pp)))
				lval=perspos(pp,ls,ls2,lp)
				lval=round(lval,4)
				
				lval2=perspos(pp,ls2,ls,lp)
				lval2=round(lval2,4)
				print(("y lval lval2", lval,lval2))


				ls=schnittpunkt(rp,pp,p3,lp)
				ls2=schnittpunkt(rp,pp,p4,lp)
				lines.append(Part.makeLine(vec(ls),vec(pp)))
				lines.append(Part.makeLine(vec(ls2),vec(pp)))
				rval=perspos(pp,ls,ls2,rp)
				rval=round(rval,4)
				
				rval2=perspos(pp,ls2,ls,rp)
				rval2=round(rval2,4)
				print(("y rval ", rval,rval2))





#-------------------------


			#create real point 
			sx=obj.length
			sy=obj.width
			sz=obj.height

			docs().run()
			if False:
				c=Part.makeCompound(lines)
				Part.show(c)
				App.ActiveDocument.ActiveObject.Label= "coord lines for " + str([str(-lval),str(rval),str(zval)])
				App.ActiveDocument.ActiveObject.ViewObject.LineColor=(.0,0.0,1.0)
				App.ActiveDocument.ActiveObject.ViewObject.LineWidth=5
				App.ActiveDocument.ActiveObject.ViewObject.PointColor=(1.0,0.0,1.0)
				App.ActiveDocument.ActiveObject.ViewObject.PointSize=10
				##App.ActiveDocument.ActiveObject.ViewObject.hide()
				tcl=App.ActiveDocument.ActiveObject
			
			
			#App.ActiveDocument.ActiveObject.Label=str([str(-lval),str(rval),str(zval)])
			#vo=App.ActiveDocument.ActiveObject.ViewObject
			#vo.PointSize=6
			#vo.PointColor=(1.0,0.3,0.0)

			d=docs()
			yp="LP"+str(time.time())
			mylp=createMP2(yp,docs().m(),FreeCAD.Vector(-lval*sx,rval*sy,zval*sz).add(self.dialog.mpos))
			mylp.Label=str([str(-lval),str(rval),str(zval)])
			print("-----------------------")
			print(("pos lval ",FreeCAD.Vector(-lval*sx,rval*sy,zval*sz)))
			print(("mpos",(self.dialog.mpos)))
			mylp.pos=FreeCAD.Vector(-lval*sx,rval*sy,zval*sz).add(self.dialog.mpos)
			print(("position",mylp.pos))
			
			mylpi=createMP2(yp,docs().i(),point)
			
			# mylpi.Label="MyLPI "+ str([str(-lval+self.dialog.mpos[0]/sx),str(rval+self.dialog.mpos[1]/sy),str(zval+self.dialog.mpos[3]/sz)])
			mylpi.Label=str([str(-lval),str(rval),str(zval)])
			mylpi.clickPoint=point
			mylpi.pos=mylp.pos
			mylpi.ViewObject.PointColor=(.0,1.0,1.0)
			mylpi.ViewObject.PointSize=10
			
			if self.mode=='l':
				lone=makeBase(lval+1,zval,lp,zp,p2,p0,p3)
				zone=makeBase(lval,zval+1,lp,zp,p2,p0,p3)
				rone=[0,0]
				sa=schnittpunkt(lp,pp,zp,p3)
				sb=schnittpunkt(sa,rp,zp,p4)
				sc=schnittpunkt(lp,sb,pp,rp)

			if self.mode=='r':
				zone=makeBase(rval,zval+1,rp,zp,p4,p0,p3)
				rone=makeBase(rval+1,zval,rp,zp,p4,p0,p3)
				lone=[0,0]
				sa=schnittpunkt(rp,pp,zp,p3)
				sb=schnittpunkt(sa,lp,zp,p2)
				sc=schnittpunkt(rp,sb,pp,lp)

			if self.mode=='z':
				# gheht noch nicht
				lone=makeBase(lval+1,rval,lp,zp,p2,p0,p3)
				rone=makeBase(rval+1,lval,rp,zp,p4,p0,p3)
				zone=[0,0]
				#lone=[0,0]
				#rone=[0,0]
#				sa=schnittpunkt(rp,pp,zp,p3)
#				sb=schnittpunkt(sa,lp,zp,p2)
#				sc=schnittpunkt(rp,sb,pp,lp)
				sc=[0,0]



			
			mylpi.lunit=vec(lone)
			mylpi.zunit=vec(zone)
			mylpi.runit=vec(rone)

			if self.mode=='l':
				mylpi.runit=vec(sc)
			if self.mode=='r':
				mylpi.lunit=vec(sc)
#			if self.mode=='z':
#				mylpi.zunit=vec(sc)



#			c=Part.makeCircle(10000,vec(sc))
#			Part.show(c)
			
			lines=[]
			
			if self.mode!='z':
				lines.append(Part.makeLine(point,vec(zone)))
				lines.append(Part.makeLine(point,vec(sc)))
			if self.mode=='l':
				lines.append(Part.makeLine(point,vec(lone)))
				#mylpi.runit=sc
			if self.mode=='r':
				lines.append(Part.makeLine(point,vec(rone)))
				#mylpi.lunit=sc

#			if self.mode=='z':
#				lines.append(Part.makeLine(point,vec(zone)))


#			lines.append(Part.makeLine(point,vec(lone)))
#			lines.append(Part.makeLine(point,vec(rone)))
#			lines.append(Part.makeLine(point,vec(zone)))

			if self.mode!='z':
				comp=Part.makeCompound(lines)
				Part.show(comp)
				App.ActiveDocument.ActiveObject.ViewObject.LineColor=(1.0,0.0,1.0)
				App.ActiveDocument.ActiveObject.ViewObject.LineWidth=10
				App.ActiveDocument.ActiveObject.ViewObject.PointColor=(.0,0.0,1.0)
				App.ActiveDocument.ActiveObject.ViewObject.PointSize=10
				##App.ActiveDocument.ActiveObject.ViewObject.hide()
				
				App.ActiveDocument.ActiveObject.Label= "axis cross " + str([str(-lval),str(rval),str(zval)])
				tax=App.ActiveDocument.ActiveObject

			if False:
				comp=Part.makeCompound([tax.Shape,tcl.Shape,mylpi.Shape])
				Part.show(comp)
				App.ActiveDocument.ActiveObject.Label="Helper for "+mylpi.Label
				App.ActiveDocument.ActiveObject.ViewObject.hide()
			
#			mylpi.lp=vec(lp)
#			mylpi.rp=vec(rp)
#			mylpi.zp=vec(zp)
			
#			mylpi.refLink=docs().i().getObject('P2')
#			mylpi.refName='P2'
#			mylpi.Shape=c
#			vo=App.ActiveDocument.ActiveObject.ViewObject
#			vo.PointSize=6
#			vo.PointColor=(1.0,0.3,0.0)
#			mylpi.lp=mylpv
#			mylpi.rp=myrpv
#			mylpi.zp=myzpv
			
#			c=Part.makeLine(mylpv,myzpv)
#			Part.show(c)

			
			

#			QApplication.restoreOverrideCursor()
			self.view.removeEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(),self.callback)


def _createPerspective():

		scaler=1000
		obj=FreeCAD.ActiveDocument.addObject('Part::FeaturePython','Perspective')
		obj.addProperty('App::PropertyVector','rpol',"1 vanishing")
		obj.addProperty('App::PropertyVector','lpol',"1 vanishing")
		obj.addProperty('App::PropertyVector','zpol',"1 vanishing")
		obj.addProperty('App::PropertyVector','base',"9 aux")
		obj.addProperty('App::PropertyLink','part',"9 aux")
		obj.addProperty('App::PropertyBool','showhorizon',"9 aux")
		obj.addProperty('App::PropertyBool','showhelper',"9 aux").showhelper=True

		for i in range(8):
			obj.addProperty('App::PropertyVector',"P"+str(i),"2 helper")

		obj.P0=FreeCAD.Vector(0,0,0)
		obj.P1=FreeCAD.Vector(-96.038*scaler,42.13*scaler,0)
		obj.P2=FreeCAD.Vector(-110*scaler,-100*scaler,0)
		obj.P3=FreeCAD.Vector(0,-200*scaler,0)
		obj.P4=FreeCAD.Vector(100*scaler,-100*scaler,0)
		obj.P5=FreeCAD.Vector(87.154*scaler,46.803*scaler,0)
		obj.P6=FreeCAD.Vector(0,100*scaler,0)
		obj.P7=FreeCAD.Vector(20*scaler,50*scaler,0)

		obj.addProperty('App::PropertyLink','basePoint',"9 aux")
		obj.addProperty('App::PropertyFloat','leftTop',"3 meassures")
		obj.addProperty('App::PropertyFloat','leftBottom',"3 meassures")
		obj.addProperty('App::PropertyFloat','rightTop',"3 meassures")
		obj.addProperty('App::PropertyFloat','rightBottom',"3 meassures")
		obj.addProperty('App::PropertyFloat','heightLeft',"3 meassures")
		obj.addProperty('App::PropertyFloat','heightRight',"3 meassures")
		obj.addProperty('App::PropertyFloat','heightCenter',"3 meassures")
		
		obj.addProperty('App::PropertyFloat','height',"4 size").height=7000
		obj.addProperty('App::PropertyFloat','length',"4 size").length=15000
		obj.addProperty('App::PropertyFloat','width',"4 size").width=20000

		obj.ViewObject.Proxy=object()
		return obj

def draw(dialog,size):
	obj=dialog.ob
	lines=[]
	if obj.showhelper:
		lines.append(Part.makeLine(obj.P0,obj.P1))
		lines.append(Part.makeLine(obj.P0,obj.P3))
		lines.append(Part.makeLine(obj.P0,obj.P5))
		
		lines.append(Part.makeLine(obj.P3,obj.P4))
		lines.append(Part.makeLine(obj.P4,obj.P5))
		
		lines.append(Part.makeLine(obj.P1,obj.P2))
		lines.append(Part.makeLine(obj.P2,obj.P3))
	
	p0=numpo(obj.P0)
	p1=numpo(obj.P1)
	p2=numpo(obj.P2)
	p3=numpo(obj.P3)
	p4=numpo(obj.P4)
	p5=numpo(obj.P5)
	
	
	d=docs()
	
	# punkte im image space/perspective/2D
	ip0=createMP2("P0",d.i(),obj.P0)
	ip0.type='IP'
	ip1=createMP2("P1",d.i(),obj.P1)
	ip1.type='IP'
	ip2=createMP2("P2",d.i(),obj.P2)
	ip2.type='IP'
	ip3=createMP2("P3",d.i(),obj.P3)
	ip3.type='IBP'
	obj.basePoint=ip3
	
	ip3.ViewObject.PointColor=(1.0,.0,.0)
	ip4=createMP2("P4",d.i(),obj.P4)
	ip4.type='IP'
	ip5=createMP2("P5",d.i(),obj.P5)
	ip5.type='IP'

	# punkte im model space/ortho/3D
	# hier koordinaten uaf lwh anpassen
	if False:
		mp0=createMP2("P0",d.m(),FreeCAD.Vector(0,0,obj.height))
		mp0.type='MP' 
		mp1=createMP2("P1",d.m(),FreeCAD.Vector(-obj.length,0,obj.height)) 
		mp1.type='MP' 
		mp2=createMP2("P2",d.m(),FreeCAD.Vector(-obj.length,0,0)) 
		mp2.type='MP' 
		mp3=createMP2("P3",d.m(),FreeCAD.Vector())
		mp3.type='MBP'
		mp3.ViewObject.PointColor=(1.0,.0,.0)
		mp4=createMP2("P4",d.m(),FreeCAD.Vector(0,obj.width,0))
		mp4.type='MP' 
		mp5=createMP2("P5",d.m(),FreeCAD.Vector(0,obj.width,obj.height))
		mp5.type='MP' 

	try: sr=schnittpunkt(p3,p4,p0,p5)
	except: sr=None
	try: sl=schnittpunkt(p3,p2,p0,p1)
	except: sl=None
	try: sz=schnittpunkt(p1,p2,p0,p3)
	except: sz=None


	# fehlerausgleich
	try: 
		sz1=schnittpunkt(p1,p2,p0,p3)
		sz2=schnittpunkt(p4,p5,p0,p3)
		
		sz=np.array([(sz1[0]+sz2[0])/2,(sz1[1]+sz2[1])/2])
		p5=schnittpunkt(p0,sr,sz,p4)
		p1=schnittpunkt(p0,sl,sz,p2)
	except: pass

	if obj.showhorizon:
		try:
			lines.append(Part.makeLine(vec(p4),vec(sr)))
			lines.append(Part.makeLine(vec(p5),vec(sr)))
			lines.append(Part.makeCircle(size,vec(sr)))
		except:
			pass

		try:
			lines.append(Part.makeLine(vec(p1),vec(sl)))
			lines.append(Part.makeLine(vec(p2),vec(sl)))
			lines.append(Part.makeCircle(size,vec(sl)))
		except:
			pass

		try:
			lines.append(Part.makeLine(vec(p0),vec(sz)))
			lines.append(Part.makeLine(vec(p1),vec(sz)))
			lines.append(Part.makeCircle(size,vec(sz)))
		except:
			pass

	if sr!=None: obj.rpol=vec(sr)
	if sl!=None: obj.lpol=vec(sl)
	if sz!=None: obj.zpol=vec(sz)

	docs().run()

	if dialog.root.ids['eyepoint'].isChecked():
		lines.append(Part.makeCircle(size,FreeCAD.Vector()))

	if dialog.root.ids['vanishing'].isChecked():
		lines.append(Part.makeLine(vec(sr),vec(sl)))
		lines.append(Part.makeLine(vec(sl),vec(sz)))
		lines.append(Part.makeLine(vec(sz),vec(sr)))

	if obj.part:
		App.ActiveDocument.removeObject(obj.part.Name)

	c=Part.makeCompound(lines)
	obj.Shape=c
	vo=obj.ViewObject
	vo.PointColor=(1.0,0.0,0.0)
	vo.PointSize=5
	vo.LineColor=(1.0,1.0,0.0)
	obj.Placement.Base.z=0.01

	d=docs()
	if False:
		# vertexes of the basebox
		createBaseBox(d.m(),obj.length,obj.width,obj.height)

	# a basebox placeholder
	bx=d.m().getObject('BaseBox')
	if bx==None:
		bx=d.m().addObject("Part::Box","BaseBox")
	bx.Width=obj.width
	bx.Length =obj.length
	bx.Height= obj.height
	bx.Placement.Base.x= -obj.length
	bx.ViewObject.Transparency=90
	print ("draw done")


s6='''
VerticalLayout:
		id:'main'
#		setFixedHeight: 900
#		setFixedWidth: 730
#		setFixedWidth: 700
		move:  PySide.QtCore.QPoint(3000,100)

		QtGui.QLabel:
			setText:"***     P E R S P E C T I V E     C R E A T O R     ***"
		QtGui.QLabel:


		QtGui.QLabel:
			setText:"Size of the Circles"

		QtGui.QSlider:
			id:'size'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 10000
			setTickInterval: 500
			setValue: 1000
			setTickPosition: QtGui.QSlider.TicksBothSides
			valueChanged.connect: app.resize

		QtGui.QLabel:
			id:'gridsizelabel'
			setText:"Size of Grid"

		QtGui.QSlider:
			id:'gridsize'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: 0
			setMaximum: 11
#			setTickInterval: 500
			setValue: 6
#			setTickPosition: QtGui.QSlider.TicksBothSides
			valueChanged.connect: app.creategrid

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
			valueChanged.connect: app.creategrid


		QtGui.QLabel:
		QtGui.QLabel:

		QtGui.QCheckBox:
			id: 'horizon' 
			setText: 'show horizon lines '
#			setChecked: True
			clicked.connect: app.showmode

		QtGui.QCheckBox:
			id: 'helper' 
			setText: 'show helper lines'
			setChecked: True
			clicked.connect: app.showmode

		QtGui.QCheckBox:
			id: 'vanishing' 
			setText: 'show vanishing points'
#			setChecked: True
			clicked.connect: app.showmode


		QtGui.QCheckBox:
			id: 'eyepoint' 
			setText: 'show eyepoint'
#			setChecked: True
			clicked.connect: app.showmode

		QtGui.QCheckBox:
			id: 'baseline' 
			setText: 'show baseline'
#			setChecked: True
			clicked.connect: app.showmode

		QtGui.QCheckBox:
			id: 'measuringpoints' 
			setText: 'show measuring points'
#			setChecked: True
			clicked.connect: app.showmode


		QtGui.QPushButton:
			id:'create'
			setText: "create or update Perspective"
			clicked.connect: app.create


		QtGui.QPushButton:
			id:'moveBtn'
			setText: "move Control Point"
			clicked.connect: app.line
			setEnabled: False

#		QtGui.QPushButton:
#			id:'stopBtn'
#			setText: "stop Moving"
#			clicked.connect: app.finish
#			setEnabled: False

		QtGui.QPushButton:
			setText: "create point on left face"
			clicked.connect: app.leftpoint

		QtGui.QPushButton:
			setText: "create point on right face"
			clicked.connect: app.rightpoint

		QtGui.QPushButton:
			setText: "create point on bottom face"
			clicked.connect: app.zenitpoint

		QtGui.QPushButton:
			setText: "create quadrangle by 4 points"
			clicked.connect: app.createface

		QtGui.QPushButton:
			setText: "create bounding rectangle"
			clicked.connect: app.createboundbox

		QtGui.QPushButton:
			setText: "toggle grid"
			clicked.connect: app.togglegrid


		QtGui.QPushButton:
			setText: "change base point"
			clicked.connect: app.changebasepoint

		QtGui.QPushButton:
			setText: "close"
			clicked.connect: app.close

		QtGui.QLabel:
			id:'scalepointlabel'
			setText:"Scale factor of the Axis cross"


		QtGui.QSlider:
			id:'scalepoint'
			setOrientation: PySide.QtCore.Qt.Orientation.Horizontal
			setMinimum: -100
			setMaximum: 100
			setTickInterval: 10
			setValue: 10
			setTickPosition: QtGui.QSlider.TicksBelow
			valueChanged.connect: app.scalepoint


		QtGui.QPushButton:
			setText: "reset Scale"
			clicked.connect: app.scalenorm

'''


class MyApp(object):

	def create(self):
		# genLabel("HUHU",[500,800])
		
		try:
			d=docs()
			d.run()
			print(App.ActiveDocument.Label)
			self.ob=App.ActiveDocument.Perspective
		except:
			self.ob=_createPerspective()
		self.mpos=FreeCAD.Vector(1,2,3)

		draw(self,self.root.ids['size'].value())
		self.line=None
		print("run app")
		self.root.ids['moveBtn'].setEnabled(True)
		self.root.ids['create'].setEnabled(False)
		draw(self,self.root.ids['size'].value())

		obj=self.ob
		p0=numpo(obj.P0)
		p2=numpo(obj.P2)
		p3=numpo(obj.P3)
		p4=numpo(obj.P4)

		lp=numpo(obj.lpol)
		rp=numpo(obj.rpol)
		zp=numpo(obj.zpol)
		
		
		docs().i()
		
		#genLabel("p0",p0)
		#genLabel("p2",p2)
		#genLabel("p4",p4)
		
		self.refpoint=FreeCAD.Vector()
		self.mpos=FreeCAD.Vector()

		
		self.polset=[lp,rp,zp]
		self.basepoints=[p0,p2,p3,p4]
		self.changebasepoint()
		

	def line(self):
		self.line=line(self,self.root.ids['size'].value())
		print(self.line)
		#self.root.ids['moveBtn'].setEnabled(False)
		# self.root.ids['stopBtn'].setEnabled(True)

	def leftpoint(self):
		leftpoint(self,'l')

	def rightpoint(self):
		l=leftpoint(self,'r')

	def zenitpoint(self):
		l=leftpoint(self,'z')


	def finish(self):
		print(self.line)
		if self.line:
			self.line.finish()
		self.line=None
		self.root.ids['moveBtn'].setEnabled(True)
		#self.root.ids['stopBtn'].setEnabled(False)

	def close(self):
		#if self.line:
		#	self.line.finish()
		self.root.ids['main'].hide()

	def resize(self):
		print("resize")
		try:
			print(self.root.ids['size'].value())
			print(self.line.size)
			self.line.size=self.root.ids['size'].value()
		except:
			pass
		draw(self,self.root.ids['size'].value())

	def showmode(self):
		print("showmode")
		self.ob.showhorizon=self.root.ids['horizon'].isChecked()
		self.ob.showhelper=self.root.ids['helper'].isChecked()
		self.ob.showhelper=self.root.ids['helper'].isChecked()
		draw(self,self.root.ids['size'].value())

	def createface(self):
		''' drawface on 4 point '''
		drawface()

	def createboundbox(self):
		''' draw rectangle on 2 points or more '''
		drawboundbox()


	def creategrid(self):
			''' create equidistant point set'''
			print("gridsize")
			print(self.root.ids['gridsize'].value())
			gs=self.root.ids['gridsize'].value()
			gstab=[ 0.01,0.02,0.05,0.1,1.0/6,0.2,1.0/3,0.5,1,2,5,10]
			self.root.ids['gridsizelabel'].setText("Relative distance of the grid lines : " +str(gstab[gs]))
			
			gc=self.root.ids['gridcount'].value()
			gctab=[ 1,3,4,5,8,10,12,15,20,25,30,50,100]
			self.root.ids['gridcountlabel'].setText("Count of the grid lines : " +str(gctab[gc]))
			
			self.grids=createGrids(self.polset,self.basepoints,self.refpoint,gstab[gs],gctab[gc])
			for g in self.grids:
#				if g.ViewObject.Visibility:
#					g.ViewObject.hide()
#					print g.Label
#				else:
					g.ViewObject.show()
#					print g.Label," !!"
			print("okay")

	def togglegrid(self):
			''' create equidistant point set'''
			for g in self.grids:
				if g.ViewObject.Visibility:
					g.ViewObject.hide()
					print(g.Label)
#				else:
#					g.ViewObject.show()
#					print g.Label," !!"
			print("okay")



	def changebasepoint(self):
		d=docs()
		d.i()

		obj=self.ob
		p0=numpo(obj.P0)
		p2=numpo(obj.P2)
		p3=numpo(obj.P3)
		p4=numpo(obj.P4)

		lp=numpo(obj.lpol)
		rp=numpo(obj.rpol)
		zp=numpo(obj.zpol)

		self.refpoint=FreeCAD.Vector()
		self.mpos=FreeCAD.Vector()
		try:
			print(" change Basepoint")
			print(" selected:")
			sel=Gui.Selection.getSelection()[0]
			print(sel.Label)
			if sel.Label in ['P0','P1','P2','P3','P4','P5']:
				print("nicht moegliche units noch nicht gesetzt, nutze P3 und breche ab")
				return
			p3=numpo(sel.base)
			p2=numpo(sel.lunit)
			p4=numpo(sel.runit)
			p0=numpo(sel.zunit)
			self.refpoint=sel.pos
			self.mpos=sel.pos
			print("3D pos:",self.mpos)
		except:
			pass

		self.polset=[lp,rp,zp]
		self.basepoints=[p0,p2,p3,p4]
		print("p3 ",p3)
		print("p2 ",p2)
		print("p4 ",p4)
		print("p0 ",p0)
		print("refpoint ", self.refpoint)
		self.creategrid()
		return

		# weitere idee fuer mehrfachauswahlen
		try:
			s=Gui.Selection.getSelectionEx()[0]
			s.Object
			print(s.Object.Label)
			print(s.PickedPoints)
			print() 
			s.SubElementNames # Vertex
			print(s.SubObjects[0]) # entsprichte PickedPoints[0]
		except:
			pass

	def scalepoint(self):
		print("scale")
		sels=Gui.Selection.getSelection()
		if sels == []: return
		sel=sels[0]
		print(sel.Label)
		name=sel.Label
		
		import re
		m = re.match(r"axis cross (.*)", name)
		if m:
			print("gefunden")
			name=m.group(1)
			print("gefunden", name)
			jj=App.ActiveDocument.getObjectsByLabel(name)
			print(jj)
			if len(jj) == 1:
				sel=jj[0]
			else: return
			print("verarbeite ",sel)
		
		docs().i()
		yy="axis cross "+name
		print(("!"+yy+"!"))
		obs=App.ActiveDocument.getObjectsByLabel("axis cross "+name)
		print(obs)
		if len(obs)>0:
			print("gefunden")
			print(obs[0])
			obj=obs[0]
			scaler=self.root.ids['scalepoint'].value()/10.0
			if scaler==0:
				scaler=0.1
			self.root.ids['scalepointlabel'].setText("Scale factor of the axis cross " + str(self.root.ids['scalepoint'].value()/10.0))
#			scaler=-1.0
			print("scaler value is ", scaler)
			lines=[]
			point=sel.clickPoint
			rone=sel.runit
			lone=sel.lunit
			zone=sel.zunit
			j=Part.makeLine(FreeCAD.Vector(),vec(rone).sub(point).multiply(scaler))
			#j.Placement.Base=point
			lines.append(j)
			#mylpi.lunit=sc
			j=Part.makeLine(FreeCAD.Vector(),vec(lone).sub(point).multiply(scaler))
			#j.Placement.Base=point
			lines.append(j)

			j=Part.makeLine(FreeCAD.Vector(),vec(zone).sub(point).multiply(scaler))
			#j.Placement.Base=point
			lines.append(j)
			print(lines)



			
			comp=Part.makeCompound(lines)
			comp.Placement.Base=point
			obj.Shape=comp
			App.ActiveDocument.recompute()

	def scalenorm(self):
			self.root.ids['scalepoint'].setValue(10)
			self.root.ids['scalepointlabel'].setText("Scale factor of the Axis cross " + str(self.root.ids['scalepoint'].value()/10))

#def createPerspective():

def run():
	global miki
	app=MyApp()
	miki2=miki.Miki()
	miki2.app=app
	app.root=miki2
	miki2.run(s6)
	app.create()

#createPerspective()
