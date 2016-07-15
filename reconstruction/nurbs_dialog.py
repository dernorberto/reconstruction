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
			setMaximum: 7
			setTickInterval: 1
			valueChanged.connect: app.runget



		QtGui.QLabel:
			setText:"v "

		QtGui.QLineEdit:
			setText:"1"
			id: 'v'

		QtGui.QDial:
			setValue: 30
			id: 'vd'
			setMinimum: 0
			setMaximum: 5
			setTickInterval: 1
			valueChanged.connect: app.runget


		QtGui.QLabel:
			setText:"height "

		QtGui.QLineEdit:
			setText:"10"
			id: 'h'

		QtGui.QDial:
			setValue: 0
			setMinimum: -100
			setMaximum: 100
			id: 'hd'
			valueChanged.connect: app.modh

		QtGui.QLabel:
			setText:"weight "

		QtGui.QLineEdit:
			setText:"10"
			id: 'w'

		QtGui.QDial:
			setValue: 1
			setMinimum: 1
			setMaximum: 20
			id: 'wd'
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

		QtGui.QPushButton:
			setText: "edit selected pole"
			clicked.connect: app.getselection


'''


class MyApp(object):

	def getselection(self):
		s=Gui.Selection.getSelection()
		print s[0].Label
		se=Gui.Selection.getSelectionEx()
		ss=se[0]
		
		sn=ss.SubElementNames
		print sn
		# ('Vertex32',)
		polnr=int(sn[0][6:])
		print ("pole ", polnr)
		
		uc=self.obj.Object.nNodes_v
		vc=self.obj.Object.nNodes_u


		u=(polnr-1) % vc
		v=(polnr-1) / vc
		print ("u,v",u,v)
		self.root.ids['vd'].setValue(v)
		self.root.ids['ud'].setValue(u)
		self.run()
		
		

	def upp(self):
		u=int(self.root.ids['ud'].value())
		u += 1
		uc=self.obj.Object.nNodes_u
		vc=self.obj.Object.nNodes_v

		if u >=uc : u=0
		self.root.ids['u'].setText(str(u+1))
		self.root.ids['ud'].setValue(u)
		self.run()

	def vpp(self):
		v=int(self.root.ids['vd'].value())
		v += 1
		uc=self.obj.Object.nNodes_u
		vc=self.obj.Object.nNodes_v

		if v >=vc: v=0
		self.root.ids['v'].setText(str(v+1))
		self.root.ids['vd'].setValue(v)
		self.run()

	def umm(self):
		u=int(self.root.ids['ud'].value())
		u -= 1
		if u <0: u=self.obj.Object.nNodes_u-1
		self.root.ids['u'].setText(str(u+1))
		self.root.ids['ud'].setValue(u)
		self.run()

	def vmm(self):
		v=int(self.root.ids['vd'].value())
		v -= 1
		if v < 0: v= self.obj.Object.nNodes_v - 1
		self.root.ids['v'].setText(str(v+1))
		self.root.ids['vd'].setValue(v)
		self.run()

	def run2(self):
		try:
			if self.lock: return
		except: pass
		print "RUN2"
		if not self.root.ids['setmode'].isChecked():
			print "setze setmode"
			self.root.ids['setmode'].click()
			self.run()


	def run(self):
		try:
			s=App.ActiveDocument.Sphere
		except:
			s=App.ActiveDocument.addObject("Part::Sphere","Sphere")
		s.Radius=1
		s.ViewObject.ShapeColor=(1.0,1.0,0.0)

		g=self.obj.Object.Proxy.g
		u=int(self.root.ids['u'].text())
		v=int(self.root.ids['v'].text())

		print self.root.ids['h'].text()

		h=int(round(float(self.root.ids['h'].text())))

		u=int(self.root.ids['ud'].value())
		v=int(self.root.ids['vd'].value())
		h=int(round(self.root.ids['hd'].value()))
		w=int(round(self.root.ids['wd'].value()))
		
		
		self.root.ids['u'].setText(str(u+1))
		self.root.ids['v'].setText(str(v+1))
		self.root.ids['h'].setText(str(h))
		self.root.ids['w'].setText(str(w))

		print ("neue werte u,v ", u,v,"h,w",h,w)
#		movePoint(g,u,v,0,0,h)
		if  self.root.ids['setmode'].isChecked():
			print "AKTUALISIERE"
			self.obj.Object.Proxy.setpointZ(u,v,h,w)
			a=App.ActiveDocument.Nurbs
			a.polnumber=u+a.nNodes_u*v
			a.Height=h
			# self.root.ids['setmode'].click()
		else:
			self.get()

			h=g[v][u][2]
			print ("u,v,h",u,v,h)
			uc=self.obj.Object.nNodes_u
			vc=self.obj.Object.nNodes_v

			self.root.ids['hd'].setValue(h)

			self.root.ids['h'].setText(str(h))
			print "hole weight von ",((v)*uc+u,"uc,vc",uc,vc)
#			print self.obj.Object.weights
			w=self.obj.Object.weights[(v)*uc+u]
			self.root.ids['wd'].setValue(w)
#			self.root.ids['w'].setText(str(h))
			print ("hole  werte u,v ", u,v,"h,w",h,w)
			
			
		s.Placement.Base=FreeCAD.Vector(tuple(g[v][u]))

		try:
			ss=App.ActiveDocument.Shape
			ss.ViewObject.Transparency=90
		except:
			pass
		
		self.root.ids['setmode'].setChecked(False)


	def runget(self):
		print "start runget"
		self.lock=True
		try:
			s=App.ActiveDocument.Sphere
		except:
			s=App.ActiveDocument.addObject("Part::Sphere","Sphere")
		s.Radius=1
		s.ViewObject.ShapeColor=(1.0,1.0,0.0)

		g=self.obj.Object.Proxy.g
		u=int(self.root.ids['u'].text())
		v=int(self.root.ids['v'].text())

		print self.root.ids['h'].text()

		h=int(round(float(self.root.ids['h'].text())))

		u=int(self.root.ids['ud'].value())
		v=int(self.root.ids['vd'].value())
		h=int(round(self.root.ids['hd'].value()))
		w=int(round(self.root.ids['wd'].value()))
		
		
		self.root.ids['u'].setText(str(u+1))
		self.root.ids['v'].setText(str(v+1))
		self.root.ids['h'].setText(str(h))
		self.root.ids['w'].setText(str(w))

		print ("neue werte u,v ", u,v,"h,w",h,w)

		self.get()

		h=g[v][u][2]
		print ("u,v,h",u,v,h)
		uc=self.obj.Object.nNodes_u
		vc=self.obj.Object.nNodes_v

		self.root.ids['hd'].setValue(h)

		self.root.ids['h'].setText(str(h))
		print "hole weight von ",((v)*uc+u)
		print "hole weight von ",((v)*uc+u,"uc,vc",uc,vc)
		print self.obj.Object.weights
		w=self.obj.Object.weights[(v)*uc+u]
		self.root.ids['wd'].setValue(w)
#			self.root.ids['w'].setText(str(h))
		print ("hole  werte u,v ", u,v,"h,w",h,w)
		
		
		s.Placement.Base=FreeCAD.Vector(tuple(g[v][u]))

		try:
			ss=App.ActiveDocument.Shape
			ss.ViewObject.Transparency=90
		except:
			pass
		
		self.root.ids['setmode'].setChecked(False)
		self.lock=False
		print "runget fertig"


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
		return

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
	
	miki.ids['ud'].setMaximum(obj.Object.nNodes_u-1)
	miki.ids['vd'].setMaximum(obj.Object.nNodes_v-1)
	
	
	return miki

# mydialog(miki)
