# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- nurbs editor -
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

from say import *


layout='''
VerticalLayoutTab:
#VerticalLayout:
		id:'main'

#		QtGui.QLabel:
#			setText:"***   N U R B S     E D I T O R   ***"
#		QtGui.QLabel:

		QtGui.QCheckBox:
			id: 'polegrid' 
			setText: 'calculate PoleGrid'
			stateChanged.connect: app.calculatePoleGrid

		QtGui.QCheckBox:
			id: 'setmode' 
			setText: 'Pole only'
			setVisible: False

		QtGui.QCheckBox:
			id: 'relativemode' 
			setText: 'Height relative'
			stateChanged.connect: app.relativeMode
			setChecked: True

		QtGui.QLabel:
			setText:"Action "

		QtGui.QComboBox:
			id: 'actionmode'
			addItem: "change Height relative"
			addItem: "set absolute Height and Weight"
			addItem: "Add VLine"
			addItem: "Add ULine"
			addItem: "Elevate VLine"
			addItem: "Elevate ULine"
			addItem: "Elevate Rectangle"
			addItem: "Elevate Circle"
			currentIndexChanged.connect: app.setActionMode

		QtGui.QPushButton:
			id: "runbutton"
			setText: "Run Action"
			clicked.connect: app.run



		QtGui.QLabel:
			setText:"u "

		QtGui.QLineEdit:
			setText:"1"
			id: 'u'

		QtGui.QDial:
			setValue: 2
			id: 'ud'
			setMinimum: 1
			setMaximum: 7
			setTickInterval: 1
			valueChanged.connect: app.getDataFromNurbs


		QtGui.QLabel:
			setText:"v "

		QtGui.QLineEdit:
			setText:"1"
			id: 'v'

		QtGui.QDial:
			setValue: 2
			id: 'vd'
			setMinimum: 1
			setMaximum: 5
			setTickInterval: 1
			valueChanged.connect: app.getDataFromNurbs


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
			valueChanged.connect: app.modHeight

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
			valueChanged.connect: app.modHeight

#		QtGui.QPushButton:
#			setText: "Commit relative values"
#			id: 'updateRelative'
#			clicked.connect: app.updateRelative



#		QtGui.QPushButton:
#			setText: "Get object info for debug"
#			clicked.connect: app.getInfo

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

	def updateDialog(self):
		self.root.ids['ud'].setMaximum(self.obj.Object.nNodes_u-1)
		self.root.ids['vd'].setMaximum(self.obj.Object.nNodes_v-1)

	def setActionMode(self):
		print "set Action Mode"
		rc=self.root.ids['actionmode'].currentText()
		print rc
		if rc=="change Height relative":
			if not self.root.ids['relativemode'].isChecked():
				self.root.ids['relativemode'].click()
				self.getDataFromNurbs()
		if rc=="set absolute Height and Weight":
			if self.root.ids['relativemode'].isChecked():
				self.root.ids['relativemode'].click()
				self.getDataFromNurbs()
			self.root.ids['runbutton'].hide()
			return
		self.root.ids['runbutton'].show()



	def run(self):
		rc=self.root.ids['actionmode'].currentText()
		print rc
		if rc=='Add ULine':
			v=self.root.ids['vd'].value()
			self.obj.Object.Proxy.addUline(v,0.5)
			self.updateDialog()
			print "done"
			
			return
		if rc=='Add VLine':
			u=self.root.ids['ud'].value()
			self.obj.Object.Proxy.addVline(u,0.5)
			self.updateDialog()
			print "done"
			return
		if rc=="change Height relative":
			if not self.root.ids['relativemode'].isChecked():
				self.root.ids['relativemode'].click()
			self.updateRelative()
			return
		if rc=="set absolute Height and Weight":
			if self.root.ids['relativemode'].isChecked():
				self.root.ids['relativemode'].click()
			self.update()
			return
		if rc== "Elevate VLine":
			u=self.root.ids['ud'].value()
			h=int(round(self.root.ids['hd'].value()))
			self.obj.Object.Proxy.elevateVline(u,h)
			return
		if rc== "Elevate ULine":
			v=self.root.ids['vd'].value()
			h=int(round(self.root.ids['hd'].value()))
			self.obj.Object.Proxy.elevateUline(v,h)
			return

		if rc== "Elevate Rectangle":
			v=self.root.ids['vd'].value()
			u=self.root.ids['ud'].value()
			h=int(round(self.root.ids['hd'].value()))
			dv=2
			du=1
			self.obj.Object.Proxy.elevateRectangle(v,u,dv,du,h)
			return

		if rc== "Elevate Circle":
			v=self.root.ids['vd'].value()
			u=self.root.ids['ud'].value()
			h=int(round(self.root.ids['hd'].value()))
			r=2
			self.obj.Object.Proxy.elevateCircle2(v,u,r,h)
			return


		print "not implemented"

	def getselection(self):
		''' get pole from gui selection '''
		s=Gui.Selection.getSelection()
		print s[0].Label
		se=Gui.Selection.getSelectionEx()
		ss=se[0]

		sn=ss.SubElementNames
		# ('Vertex32',)
		polnr=int(sn[0][6:])
		print ("pole number ", polnr)

		uc=self.obj.Object.nNodes_v
		vc=self.obj.Object.nNodes_u

		u=(polnr-1) % vc
		v=(polnr-1) / vc
		self.root.ids['vd'].setValue(v)
		self.root.ids['ud'].setValue(u)
		self.setDataToNurbs()

	def relativeMode(self):
		print("RELATVE MODE")
		print self.root.ids['relativemode'].isChecked()
		if self.root.ids['relativemode'].isChecked():
			self.obj.Object.Proxy.gBase =  self.obj.Object.Proxy.g.copy()
			try: self.root.ids['updateRelative'].show()
			except: pass
		else:
			self.root.ids['updateRelative'].hide()
		print self.obj.Object.Proxy.gBase.shape
		print "set  relative"
 
	def calculatePoleGrid(self):
		self.obj.Object.Proxy.calculatePoleGrid=self.root.ids['polegrid'].isChecked()
 

	def upp(self):
		''' move pole selection u-axis up '''
		u=int(self.root.ids['ud'].value())
		u += 1
		uc=self.obj.Object.nNodes_u
		vc=self.obj.Object.nNodes_v

		if u >=uc : u=0
		self.root.ids['u'].setText(str(u+1))
		self.root.ids['ud'].setValue(u)
		self.setDataToNurbs()

	def vpp(self):
		v=int(self.root.ids['vd'].value())
		v += 1
		uc=self.obj.Object.nNodes_u
		vc=self.obj.Object.nNodes_v
		if v >=vc: v=0
		self.root.ids['v'].setText(str(v+1))
		self.root.ids['vd'].setValue(v)
		self.setDataToNurbs()

	def umm(self):
		u=int(self.root.ids['ud'].value())
		u -= 1
		if u <0: u=self.obj.Object.nNodes_u-1
		self.root.ids['u'].setText(str(u+1))
		self.root.ids['ud'].setValue(u)
		self.setDataToNurbs()

	def vmm(self):
		v=int(self.root.ids['vd'].value())
		v -= 1
		if v < 0: v= self.obj.Object.nNodes_v - 1
		self.root.ids['v'].setText(str(v+1))
		self.root.ids['vd'].setValue(v)
		self.setDataToNurbs()


	def update(self):
		''' setDataToNurbs for update '''
		try:
			# dont setDataToNurbs during a locked transaction
			if self.lock: return
		except: pass
		print "setDataToNurbs2"
		if not self.root.ids['setmode'].isChecked():
			print "setze setmode"
			self.root.ids['setmode'].click()
			self.setDataToNurbs()



	def updateRelative(self):
		''' setDataToNurbs for update '''
		try:
			# dont setDataToNurbs during a locked transaction
			if self.lock: return
		except: pass
		print "setDataToNurbs2"
		if not self.root.ids['setmode'].isChecked():
			print "setze setmode"
			self.root.ids['setmode'].click()
			self.setDataToNurbs(True)


#			id: 'updateRelative'
#			clicked.connect: app.updateRelative



	def setDataToNurbs(self,updateRelative=False):
		''' setDataToNurbs a change in the dialog for the nurbs '''
		
		# create the helper sphere
		try:
			s=App.ActiveDocument.Sphere
		except:
			s=App.ActiveDocument.addObject("Part::Sphere","Sphere")
		s.Radius=1
		s.ViewObject.ShapeColor=(1.0,1.0,0.0)
		s.ViewObject.PointColor=(1.0,1.0,0.0)
		s.ViewObject.PointSize=10
		App.activeDocument().recompute()


		g=self.obj.Object.Proxy.g

		# data from the input fields
#		u=int(self.root.ids['u'].text())
#		v=int(self.root.ids['v'].text())
#		h=int(round(float(self.root.ids['h'].text())))

		# data from the dialers
		u=int(self.root.ids['ud'].value())
		v=int(self.root.ids['vd'].value())
		h=int(round(self.root.ids['hd'].value()))
		w=int(round(self.root.ids['wd'].value()))

		# write dialer data to the input fields
		self.root.ids['u'].setText(str(u+1))
		self.root.ids['v'].setText(str(v+1))
		self.root.ids['h'].setText(str(h))
		self.root.ids['w'].setText(str(w))


		if  self.root.ids['setmode'].isChecked():
			print "AKTUALISIERE"
			if  self.root.ids['relativemode'].isChecked():
				print "set relative values ..."
				self.obj.Object.Proxy.setpointRelativeZ(u,v,h,w)
				if updateRelative:
					self.obj.Object.Proxy.setpointRelativeZ(u,v,h,w,updateRelative)
					self.root.ids['h'].setText(str(0))
					self.root.ids['hd'].setValue(0)

			else:
				print "set absoliute "
				self.obj.Object.Proxy.setpointZ(u,v,h,w)
		else:
			self.getInfo()
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


	def getDataFromNurbs(self):
		print "start getDataFromNurbs"
		self.lock=True
		try:
			s=App.ActiveDocument.Sphere
		except:
			s=App.ActiveDocument.addObject("Part::Sphere","Sphere")
		s.Radius=1
		s.ViewObject.ShapeColor=(1.0,1.0,0.0)
		s.ViewObject.PointColor=(1.0,1.0,0.0)
		s.ViewObject.PointSize=10
		App.activeDocument().recompute()

		g=self.obj.Object.Proxy.g

		u=int(self.root.ids['ud'].value())
		v=int(self.root.ids['vd'].value())

		self.root.ids['u'].setText(str(u+1))
		self.root.ids['v'].setText(str(v+1))

		h=g[v][u][2]

		uc=self.obj.Object.nNodes_u
		vc=self.obj.Object.nNodes_v
		if  self.root.ids['relativemode'].isChecked():
			self.root.ids['hd'].setValue(0)
			self.root.ids['h'].setText(str(0))
		else:
			self.root.ids['hd'].setValue(h)
			self.root.ids['h'].setText(str(h))
		
#		print "hole weight von ",((v)*uc+u)
#		print "hole weight von ",((v)*uc+u,"uc,vc",uc,vc)
#		print self.obj.Object.weights

		w=self.obj.Object.weights[(v)*uc+u]
		
		self.root.ids['wd'].setValue(w)
		self.root.ids['w'].setText(str(w))

		print ("hole  werte u,v ", u,v,"h,w",h,w)
		s.Placement.Base=FreeCAD.Vector(tuple(g[v][u]))

		try:
			ss=App.ActiveDocument.Shape
			ss.ViewObject.Transparency=90
		except:
			pass
		
		self.root.ids['setmode'].setChecked(False)
		self.lock=False
		print "getDataFromNurbs fertig"


	def modHeight(self):
		''' dialog has changed -> modify object '''
		u=int(self.root.ids['ud'].value())
		v=int(self.root.ids['vd'].value())
		h=int(round(self.root.ids['hd'].value()))

		try:
			s=App.ActiveDocument.Sphere
		except:
			s=App.ActiveDocument.addObject("Part::Sphere","Sphere")
		s.Radius=1
		s.ViewObject.ShapeColor=(.0,1.0,0.0)
		s.ViewObject.PointColor=(1.0,1.0,0.0)
		s.ViewObject.PointSize=10
		App.activeDocument().recompute()

		s.Placement.Base.z=h
		self.update()



	def getInfo(self):
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
	app.getDataFromNurbs()
	
	return miki

# mydialog(miki)
