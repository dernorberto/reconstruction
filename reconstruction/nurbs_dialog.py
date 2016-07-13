# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- nurbs editor -
#--
#-- microelly 2016 v 0.0
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

from say import *



layout='''
VerticalLayout:
		id:'main'

		QtGui.QLabel:
			setText:"***   N U R B S     E D I T O R   ***"
		QtGui.QLabel:

		QtGui.QCheckBox:
			id: 'setmode' 
			setText: 'Pole only'


		QtGui.QLabel:
			setText:"u "

		QtGui.QLineEdit:
			setText:"1"
			id: 'u'

		QtGui.QDial:
			setValue: 30
			id: 'ud'
			setMinimum: 0
			setMaximum: 3
			setTickInterval: 1
			valueChanged.connect: app.run



		QtGui.QLabel:
			setText:"v "

		QtGui.QLineEdit:
			setText:"1"
			id: 'v'

		QtGui.QDial:
			setValue: 30
			id: 'vd'
			setMinimum: 0
			setMaximum: 6
			setTickInterval: 1
			valueChanged.connect: app.run


		QtGui.QLabel:
			setText:"h "

		QtGui.QLineEdit:
			setText:"10"
			id: 'h'

		QtGui.QDial:
			setValue: 0
			setMinimum: -100
			setMaximum: 100
			id: 'hd'
			valueChanged.connect: app.modh


		QtGui.QPushButton:
			setText: "Commit values"
			clicked.connect: app.run2

		QtGui.QPushButton:
			setText: "Get object info for debug"
			clicked.connect: app.get

		QtGui.QPushButton:
			setText: "u++"
			clicked.connect: app.upp

		QtGui.QPushButton:
			setText: "u --"
			clicked.connect: app.umm

		QtGui.QPushButton:
			setText: "v++"
			clicked.connect: app.vpp


		QtGui.QPushButton:
			setText: "v --"
			clicked.connect: app.vmm


'''


class MyApp(object):

	def upp(self):
		u=int(self.root.ids['ud'].value())
		u += 1
		if u >3: u=0
		self.root.ids['u'].setText(str(u+1))
		self.root.ids['ud'].setValue(u)
		self.run()

	def vpp(self):
		v=int(self.root.ids['vd'].value())
		v += 1
		if v >6: v=0
		self.root.ids['v'].setText(str(v+1))
		self.root.ids['vd'].setValue(v)
		self.run()

	def umm(self):
		u=int(self.root.ids['ud'].value())
		u -= 1
		if u <0: u=3
		self.root.ids['u'].setText(str(u+1))
		self.root.ids['ud'].setValue(u)
		self.run()

	def vmm(self):
		v=int(self.root.ids['vd'].value())
		v -= 1
		if v < 0: v=6
		self.root.ids['v'].setText(str(v+1))
		self.root.ids['vd'].setValue(v)
		self.run()

	def run2(self):
		if not self.root.ids['setmode'].isChecked():
			self.root.ids['setmode'].click()
			self.run()


	def run(self):
		try:
			s=App.ActiveDocument.Sphere
		except:
			s=App.ActiveDocument.addObject("Part::Sphere","Sphere")
		s.Radius=1
		s.ViewObject.ShapeColor=(1.0,1.0,0.0)
		
		print "u,v"
		print self.root.ids['u'].text()
		print self.root.ids['v'].text()
		g=self.obj.Object.Proxy.g
		u=int(self.root.ids['u'].text())
		v=int(self.root.ids['v'].text())
		print "s"
		print self.root.ids['h'].text()

		h=int(round(float(self.root.ids['h'].text())))
		print "j"
		u=int(self.root.ids['ud'].value())
		v=int(self.root.ids['vd'].value())
		h=int(round(self.root.ids['hd'].value()))
		
		
		self.root.ids['u'].setText(str(u+1))
		self.root.ids['v'].setText(str(v+1))
		self.root.ids['h'].setText(str(h))
		print ("neue werte", u,v,h)
#		movePoint(g,u,v,0,0,h)
		if  self.root.ids['setmode'].isChecked():
			self.obj.Object.Proxy.setpointZ(u,v,h)
			a=App.ActiveDocument.Nurbs
			a.polnumber=u+a.nNodes_u*v
			a.Height=h
			self.root.ids['setmode'].click()
		else:
			self.get()
		
		s.Placement.Base=FreeCAD.Vector(tuple(g[v][u]))

		try:
			ss=App.ActiveDocument.Shape
			ss.ViewObject.Transparency=90
		except:
			pass


	def modh(self):
		u=int(self.root.ids['ud'].value())
		v=int(self.root.ids['vd'].value())
		h=int(round(self.root.ids['hd'].value()))
		self.root.ids['h'].setText(str(h))
		try:
			s=App.ActiveDocument.Sphere
		except:
			s=App.ActiveDocument.addObject("Part::Sphere","Sphere")
		s.Radius=1
		s.ViewObject.ShapeColor=(.0,1.0,0.0)
		s.Placement.Base.z=h
		self.run2()



	def get(self):

		print "get obj"
		print self.root
		print self.obj
		print self.obj.Object.Label

		print "shape .."
		print self.obj.Object.Proxy.g.shape





def mydialog(obj):

	import reconstruction.miki as miki
	reload(miki)

	app=MyApp()
	miki=miki.Miki()
	
	miki.app=app
	app.root=miki
	app.obj=obj

	miki.parse2(layout)
	miki.run(layout)
	
	return miki

# mydialog(miki)
