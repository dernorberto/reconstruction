#: utf-8 -*-
#-------------------------------------------------
#-- reconstruction workbench
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

__vers__="30.05.2016  0.2"

import reconstruction.say
reload(reconstruction.say)
from reconstruction.say import *


try:
	__dir__ = os.path.dirname(os.path.dirname(__file__))
except:
	__dir__='/home/thomas/.FreeCAD/Mod/reconstruction'


import cv2

matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import reconstruction
import reconstruction.miki as miki
reload(miki)

import reconstruction.tools as tools
reload(reconstruction.tools)

import reconstruction.configuration as config
reload(reconstruction.configuration) 
modes=config.modes

import reconstruction.mpl
reload(reconstruction.mpl)

lasttime=0
countUpdater=0


def updater():
	''' recompute the active document but no faster than once per second'''

	global countUpdater
	global lasttime

	t=time.time()
	if t-lasttime<1: return

	if countUpdater>0:
		sayErr("counter to high - update canceled ")
		return

	countUpdater += 1
	try: App.ActiveDocument.recompute()
	except: sayexc()

	lasttime=t
	countUpdater -= 1


def recomputeData(obj):
	say("recompute by " + obj.Label)
	FreeCAD.ActiveDocument.recompute()
	say ("recompute done")


def getMainWindowByName(name,separateMainWindow):
	if not separateMainWindow:
		return FreeCAD.Gui.getMainWindow()

	toplevel2 = QtGui.qApp.topLevelWidgets()
	for i in toplevel2:
		if name == i.windowTitle():
			i.show()
			return i
		
	r=QtGui.QMainWindow()
	r.setWindowTitle(name)
	FreeCAD.r=r
	r.show()
	r.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
	return r


def dockit():

	separateMainWindow=False

	# anzeige als separates Hauoptfenster ...
	separateMainWindow=True

	w2=getMainWindowByName("Reconstruction Tools",separateMainWindow)

	for w in FreeCAD.w5:
		say(w.windowTitle())
		try:
			w2.addDockWidget(QtCore.Qt.TopDockWidgetArea, w)
			w.setAllowedAreas(QtCore.Qt. AllDockWidgetAreas)

		except:  
			sayexc()
			FreeCAD.w5=[]

	last=None
	for c in w2.children():
		if c.__class__.__name__ =='MyDockWidget':
			print c.windowTitle()
			if last <> None:
				w2.tabifyDockWidget(last, c)
			last=c


class CVGui(object):
	''' GUI  interface for CV nodes'''

	layout='''

VerticalLayout:
	setWindowTitle: '{0}'
	id:'main'
#	QtGui.QLabel:
#			setText:"***    My    C V    Dialog ***"

HorizontalLayout:
		id:'vela'
#		setFixedHeight: 500
#		setFixedWidth: 500
		resize: PySide.QtCore.QSize(400,300)
		setWindowTitle: '{1}'
#		move:  PySide.QtCore.QPoint(3000,100)
#		QtGui.QLabel:
#			setText:"***    My    C V    Image result  ***"

'''

	def edit(self):
		say("Edit .. (not implemented)")

	def resetZoom(self):
		self.obj.Proxy.markers=[]
		self.plot()
#------------------

	def cv2selector(self):
		say("CV2 selector ...")
		obj=self.obj
		say(obj)

		try:
			if obj.mode == 'ImageFile':
				say("File ...")
				say(obj.sourceFile)
				img = cv2.imread(obj.sourceFile)
			else:
				#img=obj.sourceObject.Proxy.img
				say("image geladn von sourceObject !!!!!!!!!!!!!!!!!")
				img=obj.Proxy.img
		except:
			sayexc()
		if img == None:
			img=cv2.imread(__dir__+'/icons/freek.png')

		obj.Proxy.img=img


		try: 
			if len(obj.Proxy.markers)>=2:
				say(obj.Proxy.markers)
				[x0,y0]=obj.Proxy.markers[0]
				[x1,y1]=obj.Proxy.markers[1]
				if x0 < x1: x0,x1 = x1,x0
				if y0 < y1: y0,y1 = y1,y0
				crop_img = img[y1:y0, x1:x0]
				cv2.imshow("crop image",crop_img)
				
				scaler=img.shape[0]//crop_img.shape[0]
				try:
					#img=cv2.resize(crop_img,(img.shape[1],img.shape[1]*crop_img.shape[0]//crop_img.shape[1]),interpolation = cv2.INTER_CUBIC)
					img=tools.resize(crop_img,400,800)
				except:
					sayexc()
		except:
			obj.Proxy.markers=[]

#				if event == cv2.EVENT_LBUTTONDBLCLK:

		if 1 :
			if not hasattr(obj.Proxy,'points'):
				obj.Proxy.points=[]
				obj.Proxy.selector=False



			img2=img

			def draw_mask(event,x,y,flags,param):
				radius=3
				if event == cv2.EVENT_LBUTTONDOWN:
					say("# !X mouse callback left down function" + str(event))
					img2=img.copy()
					R=10
					color=(255,0,0)
					cv2.circle(img2,(x,y),R,color,-1)
					dst = cv2.addWeighted(img,0.7,img2,0.3,0)
					cv2.imshow("image",dst)
					obj.Proxy.selector=True
					obj.Proxy.center=(x,y)
				if event == cv2.EVENT_LBUTTONUP:
					say("# !! mouse callback left up function" + str(event))
					obj.Proxy.selector=False
					img2=img.copy()
					color=(255,0,0)
					cv2.circle(img2,obj.Proxy.center,obj.Proxy.R,color,-1)
## rectangle mode
					cv2.rectangle(img2,obj.Proxy.center,obj.Proxy.point2,(255,255,0),-1)
					obj.Proxy.img=img2



				if  event == cv2.EVENT_MOUSEMOVE:
					if obj.Proxy.selector:
						say("# !XX! mouse callback move " + str(event))
						
						img2=img.copy()
						R=np.sqrt((obj.Proxy.center[0]-x)**2+(obj.Proxy.center[1]-y)**2)
						R=int(round(R))
						obj.Proxy.point2=(x,y)
						obj.Proxy.R=R
						color=(255,0,0)
						cv2.circle(img2,obj.Proxy.center,R,color,-1)
						
						cv2.rectangle(img2,obj.Proxy.center,(x,y),(255,255,0),-1)
						# http://opencvinpython.blogspot.de/2014/09/basic-drawing-examples-drawing-line-cv2.html
						
						dst = cv2.addWeighted(img,0.7,img2,0.3,0)
						cv2.imshow("image",dst)
						obj.Proxy.img=img2
				
				obj.touch()

			cv2.namedWindow('image')
			cv2.setMouseCallback('image',draw_mask)
			for [x,y,R] in obj.Proxy.points:
				if obj.invertMask: color=(255,255,255)
				else: color=(0,0,0)
				
				# mouse position as blue circle
				cv2.circle(img2,(x,y),R,color,-1)

		cv2.imshow('image',img)
		obj.touch()
		obj.Proxy.display=True


#------------------

	def plot(self):
		say("Plot ...")
		obj=self.obj
		say(obj)
		try:
			if obj.mode == 'ImageFile':
				say("File ...")
				say(obj.sourceFile)
				img = cv2.imread(obj.sourceFile)
			else:
				#img=obj.sourceObject.Proxy.img
				say("image geladn von sourceObject !!!!!!!!!!!!!!!!!")
				img=obj.Proxy.img
		except:
			sayexc()
		if img == None:
			img=cv2.imread(__dir__+'/icons/freek.png')

		try: 
			if len(obj.Proxy.markers)>=2:
				say(obj.Proxy.markers)
				[x0,y0]=obj.Proxy.markers[0]
				[x1,y1]=obj.Proxy.markers[1]
				if x0 < x1: x0,x1 = x1,x0
				if y0 < y1: y0,y1 = y1,y0
				crop_img = img[y1:y0, x1:x0]
				cv2.imshow("crop image",crop_img)
				
				scaler=img.shape[0]//crop_img.shape[0]
				try:
					#img=cv2.resize(crop_img,(img.shape[1],img.shape[1]*crop_img.shape[0]//crop_img.shape[1]),interpolation = cv2.INTER_CUBIC)
					img=tools.resize(crop_img,400,800)
				except:
					sayexc()
		except:
			obj.Proxy.markers=[]

		# mouse callback function
		# rectangle select by two mouse clicks #+# not finished
		if obj.mode == 'ImageFile':
			
			def draw_circle(event,x,y,flags,param):
				if event == cv2.EVENT_LBUTTONDBLCLK:
					obj.Proxy.markers=[]
					img = cv2.imread(obj.sourceFile)
					cv2.imshow('image',img)
					obj.Proxy.img=img

				if event == cv2.EVENT_LBUTTONDOWN:
					say("# !! mouse callback function" + str(event))
					say([x,y])
					img=obj.Proxy.img
					cv2.circle(img,(x,y),3,(255,0,0),-1)
					cv2.imshow('image',img)
					obj.Proxy.img=img
					obj.Proxy.markers.append([x,y])
					say("Markers ...")
					obj.Proxy.markers=obj.Proxy.markers[-2:]
					say(obj.Proxy.markers)

					if len(obj.Proxy.markers)>=2:
						say(obj.Proxy.markers)
						[x0,y0]=obj.Proxy.markers[0]
						[x1,y1]=obj.Proxy.markers[1]
						if x0 < x1: x0,x1 = x1,x0
						if y0 < y1: y0,y1 = y1,y0
						crop_img = img[y1:y0, x1:x0]
						cv2.imshow("crop image",crop_img)
						say("change IUmaege")
						obj.Proxy.img=crop_img


					obj.touch()


			cv2.namedWindow('image')
			cv2.setMouseCallback('image',draw_circle)

		if obj.mode == 'Mask':
			if not hasattr(obj.Proxy,'points'):
				obj.Proxy.points=[]
				obj.Proxy.selector=False

			img2=img

			def draw_mask(event,x,y,flags,param):
				if event == cv2.EVENT_LBUTTONDOWN:
					say("# !! mouse callback left down function" + str(event))
					obj.Proxy.selector=True
				if event == cv2.EVENT_LBUTTONUP:
					say("# !! mouse callback left up function" + str(event))
					obj.Proxy.selector=False
				if  event == cv2.EVENT_MOUSEMOVE:
					say("# !! mouse callback move " + str(event))
					say([x,y,flags])
					if obj.Proxy.selector:
						obj.Proxy.points.append([x,y,obj.radius])
					say(len(obj.Proxy.points))
					pp=[x,y,obj.radius]

					img2=img
					#img2=img.copy()

					for [x,y,R] in obj.Proxy.points:
						if obj.invertMask:
							color=(255,255,255)
						else:
							color=(0,0,0)
						cv2.circle(img2,(x,y),R,color,-1)

					img3=img2.copy()
					cv2.circle(img3,(pp[0],pp[1]),pp[2],(255,0,0),1)
					cv2.imshow("image",img3)

			cv2.namedWindow('image')
			cv2.setMouseCallback('image',draw_mask)
			for [x,y,R] in obj.Proxy.points:
				if obj.invertMask: color=(255,255,255)
				else: color=(0,0,0)
				
				# mouse position as blue circle
				cv2.circle(img2,(x,y),R,color,-1)
				cv2.imshow("image",img2)

			obj.Proxy.img=img

		cv2.imshow('image',img)

		obj.Proxy.img=img
		obj.touch()
		obj.Proxy.display=True

	def plot2(self,h=None,w=None):

		say("plot2  for -------" + self.obj.mode)
		
		try: self.root.ids['vela'].show()
		except: pass
		cv2.destroyWindow('image')

		# add/reset the mathplotlibwidget 
		try: self.mpl
		except: self.add_mplw("mplw")

		plt=self.mpl.figure
		plt.clf()

		obj=self.obj
		
		if obj.mode == 'ElevationGrid':
			say("elevatin grid")
			say(obj)
			say("plot to")
			say(plt)
			x=obj.Proxy.x
			y=obj.Proxy.y
			z=obj.Proxy.z
			zi=obj.Proxy.zi
			reconstruction.elevationgrid.showHeightMap(x,y,z,zi)
			return

		try:
			if obj.mode == 'ImageFile':
#				say("Image from File ..." + str(obj.sourceFile))
				try:
					img2 = cv2.imread(obj.sourceFile)
					img=obj.Proxy.img
				except:
					sayexc("error reading source because ...")
					say(obj)
					say(obj.Proxy)
					img = cv2.imread(obj.sourceFile)
			else:
				say("Image from Object ..." + str(obj.sourceObject.Label))
				try: img=obj.Proxy.img
				except: img=None
		except:
			sayexc()


		if img == None:
			img=cv2.imread(__dir__+'/icons/freek.png')
			obj.Proxy.img=img

		im_w = img.shape[0]
		im_h = img.shape[1]

		ks=3
		kernel = np.ones((ks,ks),np.uint8)
		dilation = cv2.dilate(img,kernel,iterations = 1)

		if 0: # das geth schon ...
			import matplotlib.pyplot as plt2
			obj.Proxy.dist_on_skel
			plt2.imshow(obj.Proxy.dist_on_skel, cmap=plt2.cm.spectral, interpolation='nearest')
			# plt.imshow(dist_on_skelw, cmap=plt.cm.PRGn, interpolation='nearest')
			plt2.show()
			say("okay 3")
		try:
			# fuer skelette umfaerben
			img=obj.Proxy.dist_on_skel
			say("skeleton image loaded")
		except:
			pass

		res=tools.resize(img,int(plt.bbox.ymax-plt.bbox.ymin),int(plt.bbox.xmax-plt.bbox.xmin))
		
		# plt.figimage(res, 0, 0, alpha=.75, zorder=2)
		
		import matplotlib.pyplot as plt2
		
		#res=cv2.cvtColor(res,cv2.COLOR_BGR2RGB)
		try:
			b,g,r = cv2.split(res)       # get b,g,r
			res = cv2.merge([r,g,b])
		except:
			pass
		##plt.figimage(res, 0, 0, alpha=.75, zorder=2)
		
		### -- fuer skelette 
		
		plt.figimage(res, 0,0,  cmap=plt2.cm.spectral, )
		self.mpl.draw()


	def showcolormap(self):
		import matplotlib.pyplot as plt
		obj=self.obj
		m=obj.Proxy.dist_on_skel
		#plt.imshow(m, cmap=plt.cm.spectral, interpolation='nearest')
		plt.imshow(m, cmap=plt.cm.PRGn, interpolation='nearest')
		plt.show()




	#
	# add special widgets
	#

	def add_mplw(self,idname):
		##self.mpl=MatplotlibWidget()
		
		self.mpl=reconstruction.mpl.MatplotlibWidget()
		self.root.ids[idname]=self.mpl
		try: self.root.ids['vela'].layout.addWidget(self.mpl)
		except: pass

		def onResize(obj,e,uk,vela):
			''' event handler for onResize of a matplotlib widget '''

			w=e.size().width()
			h=e.size().height()
			print(w,h)
			obj.plot2()
			uk(e)


		k=self.mpl.resizeEvent
		self.mpl.resizeEvent = lambda e:onResize(self,e,k,self.root.ids['vela'])



	def add_button(self,idname,label,method):
		bt=QtGui.QPushButton(label)
		if method <>None:
			bt.clicked.connect(method)
		else:
			bt.clicked.connect(lambda:sayErr("button "+ label +" clicked"))
		self.root.ids[idname]=bt
		self.root.ids['main'].layout.addWidget(bt)


	def run(self,dial):
		import time
		self.stop=False
		pos=dial.value()
		for i in range(pos,dial.maximum()):
			if self.stop: return
			dial.setValue(i)
			FreeCAD.Gui.updateGui()
			time.sleep(0.1)
		for i in range(0,pos):
			if self.stop: return
			dial.setValue(i)
			FreeCAD.Gui.updateGui()
			time.sleep(0.1)


	def stopme(self):
		self.stop=True

	def add_dialer2(self,idname,label,method,norun=False):
		dial = QtGui.QDial()
		dial.setNotchesVisible(True)
		self.dial=dial
		dial.setMaximum(255)
		m2= lambda: method(dial.value())
		dial.valueChanged.connect(m2)
		# dial.valueChanged.connect(updater)
		self.root.ids[idname]=dial

		lab=QtGui.QLabel(idname + '  '+'_' * (20-len(idname)))
		
		
		w=QtGui.QWidget()
		hbox = QtGui.QHBoxLayout()
		w.setLayout(hbox)
		
		#hbox.addStretch(1)
		
		edi = QtGui.QLineEdit()
		edi.setMaxLength(4)
		edi.setMaximumSize(50,40)
		edi.setText(label)
		
		if not norun:
			bt=QtGui.QPushButton("run")
			bt.clicked.connect(lambda:self.run(dial))

			self.stop=False
			bt2=QtGui.QPushButton("stop")
			bt2.clicked.connect(lambda:self.stopme())
		
		self.edi=edi
		edi.textChanged.connect(m2)
		dial.valueChanged.connect(lambda: edi.setText(str(dial.value())))
		edi.textChanged.connect(lambda:dial.setValue(int(edi.text())))
		# hbox.addStretch(1)
		hbox.addWidget(lab)
		hbox.addWidget(edi)
		hbox.addStretch(1)
		hbox.addWidget(dial)
		# hbox.addStretch(1)

		if not norun:
			hbox.addWidget(bt)
			hbox.addWidget(bt2)

		self.root.ids['main'].layout.addWidget(w)
		return dial

	def add_dialer(self,idname,label,method):
		dial=self.add_dialer2(idname,label,method)
		dial.valueChanged.connect(updater)


	def add_dialernr(self,idname,label,method):
		# dialier without run 
		dial=self.add_dialer2(idname,label,method,norun=True)
		dial.valueChanged.connect(updater)


	def add_slider(self,idname,label,method):
		dial = QtGui.QSlider()
		dial.setOrientation(PySide.QtCore.Qt.Orientation.Horizontal)
		dial.setMinimum(1)
		dial.setMaximum(40)
		dial.setTickInterval(1)
		dial.setValue(2)
		dial.setTickPosition(QtGui.QSlider.TicksBothSides)

		self.dial=dial
		dial.setMaximum(255)
		m2= lambda: method(dial.value())
		dial.valueChanged.connect(m2)
		self.root.ids[idname]=dial

		lab=QtGui.QLabel(idname)

		w=QtGui.QWidget()
		hbox = QtGui.QVBoxLayout()
		w.setLayout(hbox)
		hbox.addStretch(1)
		hbox.addWidget(lab)
		hbox.addWidget(dial)

		self.root.ids['main'].layout.addWidget(w)


	def add_lineEdit(self,idname,label,method):
		dial = QtGui.QLineEdit()
		dial.setText(label)
		self.dial=dial
		m2= lambda: method(dial.text())
		dial.textChanged.connect(m2)
		self.root.ids[idname]=dial
		lab=QtGui.QLabel(idname)

		w=QtGui.QWidget()
		hbox = QtGui.QHBoxLayout()
		w.setLayout(hbox)

		#hbox.addStretch(1)
		hbox.addWidget(lab)
		hbox.addWidget(dial)

		self.root.ids['main'].layout.addWidget(w)


	def add_checkBox(self,idname,label,method):
		dial = QtGui.QCheckBox()
		dial.setText(idname)
		self.dial=dial
		m2= lambda: method(dial.isChecked())
		dial.clicked.connect(m2)
		self.root.ids[idname]=dial

		l=self.root.ids['main'].layout
		l.addWidget(dial)


	def add_widget(self,idname,widgetclassname,p2w,w2p):
		### x=self.obj.getPropertyByName(idname)
		f=lambda ww: setattr(self.obj,idname,p2w(ww))
		if widgetclassname=='dialer2':
			self.add_dialer2(idname,widgetclassname +  " xx for "  +  idname ,f)
		if widgetclassname=='dialernr':
			self.add_dialernr(idname,widgetclassname +  " xx for "  +  idname ,f)
		if widgetclassname=='dialer':
			self.add_dialer(idname,widgetclassname +  " xx for "  +  idname ,f)
		if widgetclassname=='slider':
			self.add_slider(idname,widgetclassname +  " xx for "  +  idname ,f)
		if widgetclassname=='lineEdit':
			self.add_lineEdit(idname,widgetclassname +  " xx for "  +  idname ,f)
		if widgetclassname=='checkBox':
			self.add_checkBox(idname,widgetclassname +  " xx for "  +  idname ,f)
		if widgetclassname=='button':
			f=None
			self.add_button(idname,idname ,f)


	def updateDialog(self):
#		sayErr("updateDialog " + str(self.obj.Label))
		widgets=config.configMode[self.obj.mode]['widgets']
		for w in widgets:
			wid = None
			try:
				wid=self.root.ids[w['id']]
				wic=w['params'][0]
				if wic == 'button': 
					pass
					continue

				val=self.obj.getPropertyByName(w['id'])
				# say ([w,val,wic])
				if wic == 'lineEdit': wid.setText(val)
				if wic == 'slider': wid.setValue(val)
				if wic == 'dialer': 
					wid.setValue(val)
					if len(w['params'])>=3:
						wid.setMinimum(w['params'][1])
						wid.setMaximum(w['params'][2])
				if wic == 'dialer2': wid.setValue(val)
				if wic == 'dialernr': wid.setValue(val)
				if wic == 'checkBox': 
					if val: wid.setCheckState(QtCore.Qt.Checked)
					else: wid.setCheckState(QtCore.Qt.Unchecked)
			except: 
				# hier fhelrhandling einbauen
				if wid <> None: sayexc()


	#
	# customize generic dialog
	#

	def close(self):
		''' clos dialog and view'''
		
		self.root.ids['main'].hide()
		self.root.ids['vela'].hide()

	def snapshot(self):
		Gui.activeDocument().activeView().saveImage('/home/thomas/Schreibtisch/screen.png',563,442,'Current')
		self.obj.touch()
		FreeCAD.ActiveDocument.recompute()

	def snapshotImg(self):
		cv2.imwrite('/tmp/'+self.obj.Label+'.png',self.obj.Proxy.img)

	def modDialog(self):
		FreeCAD.ActiveDocument.recompute()

		try: t=config.configMode[self.obj.mode]
		except: sayexc("modDialog Mode no mode " + self.obj.mode)

		for w in config.configMode[self.obj.mode]['widgets']:
			self.add_widget(w['id'],w['params'][0],w['p2w'],w['w2p'])

		self.updateDialog()

		if self.obj.mode ==  'ElevationGrid' :
			self.add_button("resetdata","Elevation Grid",lambda:run_elevationgrid(self.obj,self))
			btsok=True

		btsok=False
		if self.obj.mode ==  'HoughLinesPost' :
			self.add_button("resetdata","HoughLines Post processing",lambda:tools.run_HoughLinesPost(self.obj,self))
			btsok=True

		if self.obj.mode ==  'Pathes' :
			self.add_button("resetdata","Pathes generater",lambda:run_pathes(self.obj,self))
			btsok=True

		if self.obj.mode ==  'PathAnalyzer' :
			self.add_button("resetdata","Detect Pathes in the Image",lambda:run_pathfinder(self.obj,self))
			self.add_button("resetdata","Analyse Path (and create exact Wire)",lambda:run_pathanalyzer(self.obj,self,True,self.obj.createWire))
			self.add_button("updateimage","Update Image",self.plot2)
			btsok=True

		if not btsok:
			self.add_button("updateimage","Update Image",self.plot2)

			if self.obj.mode ==  'ImageFile' :
##				self.add_button("showimage","Select Subrectangle V0",self.plot)
				pass
			elif self.obj.mode ==  'Mask' :
				self.add_button("showimage","Set Mask",self.plot)
			else:
				self.add_button("showimage","Show Image in separate Window",self.plot)

			self.add_button("showimage","Simple Subimage Selector V1",self.cv2selector)
##			self.add_button("showimage","Show Color Map in separate Window",self.showcolormap)
			self.add_button("resetdata","Recompute Data",lambda:recomputeData(self.obj))
			self.add_button("resetdata","Snapshot active 3D View",self.snapshot)
			self.add_button("resetdata","Snapshot Image",self.snapshotImg)
			

##		if self.obj.mode ==  'ImageFile' :
##			self.add_button("showimagex","Reset Zoom",self.resetZoom)

		self.add_button("resetdata","close",self.close)

		# example access to a widget
		#self.root.ids['resetdata'].hide()
		#self.root.ids['vela'].hide()

		# update layout
		try:
			self.root.ids['main'].layout.setStretchFactor(self.mpl, 1)
		except: pass
		self.plot2()

def run_elevationgrid(obj=None,app=None):

	import reconstruction.elevationgrid
	reload(reconstruction.elevationgrid)
	say(obj.Label)
	say(obj)
	say(app)
	[x,y,z,zi]=reconstruction.elevationgrid.createElevationGrid('thin_plate')

	if obj:
		obj.Proxy.x=x
		obj.Proxy.y=y
		obj.Proxy.z=z
		obj.Proxy.zi=zi


def run_pathfinder (obj,app):
	''' find pathes(connected pointsets) in an image'''

	import reconstruction.pathfinder
	reload(reconstruction.pathfinder)

	# load a image and calculate the pathlist pl2
	pf=reconstruction.pathfinder.PathFinder()
	pf.fn=obj.sourceObject.sourceFile

	try: pf.img=obj.sourceObject.Proxy.img
	except: pass
	
	pl2=pf.run(obj.minPathPoints,obj.showPics,obj)
	obj.Proxy.pl2=pl2
	obj.Proxy.img=pf.imgOut

	say("done/found")


def run_pathanalyzer(obj,app=None,forcereload=True,createFC=False):
	''' split path into intervals '''
	
	import reconstruction.pathanalyser
	if forcereload: reload(reconstruction.pathanalyser)
	
	if app <> None:
		FreeCAD.app=app

	try: obj.Proxy.pl2
	except:
		sayexc("no data - run FindPathes first")
		errorDialog("no data - run FindPathes first")
		return

	try: widget=obj.Proxy.analyzer
	except: widget=None

	hideApprox=obj.hideApproximation

	if obj.pathSelection: # process selected path
		analyzer=reconstruction.pathanalyser.runsel(obj.N,obj.Threshold,widget,createFC,obj)
	elif obj.pathId==-1: # process pathObject
		analyzer=reconstruction.pathanalyser.runobj(obj.pathObject,obj.N,obj.Threshold,widget,createFC,obj)
	else: # process object by index number
		analyzer=reconstruction.pathanalyser.run(obj.Proxy.pl2,obj.pathId,obj.N,obj.Threshold,widget,createFC,obj)

	obj.Proxy.analyzer=analyzer
	return


def run_pathes(obj,app):

	try:
		pathes=obj.sourceObject.Proxy.pathes
	except:
		sayexc("sourceObject has no pathes, use dummy data")
		pathes=[
				[[0,0,0],[100,0,0],[100,150,0]],
				[[-50,-50,0],[100,0,0],[100,50,0]],
				[[-50,-150,0],[200,0,0],[100,50,0]],
				[[0,0,0],[100,60,0],[100,350,0]],
				[[-50,-50,0],[100,60,0],[100,350,0]],
				[[-50,-150,0],[200,60,0],[100,350,0]],
			]
	pathes=np.array(pathes)
	n=pathes.shape[0]

	color=eval("iter(cm."+obj.modelColor+"(np.linspace(0,1,n)))")

	colors=[]
	for i in range(n):
		c=next(color)
		colors.append((c[0],c[1],c[2]))

	ix=0

	for path in pathes:
		ps=[]
		for p in path:
			fp=FreeCAD.Vector(p[0],p[1],0)
			ps.append(fp)
		pp=Part.makePolygon(ps)
		oname=obj.pathname+"_"+str(ix)
		a=FreeCAD.ActiveDocument.getObject(oname)
		if a == None:
			a=FreeCAD.ActiveDocument.addObject("Part::Feature",oname)
		a.Shape=pp
		wv=a.ViewObject
		wv.LineColor=colors[ix]
		ix += 1
		say(ps)


#-----------------------
# anzupassende Methoden
#-----------------------




def changeMode(obj,mode):
	''' create, hide/unhide the properties for mode'''

	try:
		if mode == 'ImageFile':
			obj.setEditorMode("sourceFile", 0)
			obj.setEditorMode("sourceObject", 2)
		else:
			obj.setEditorMode("sourceFile", 2)
			obj.setEditorMode("sourceObject", 0)
	except: pass

	try: t = config.configMode[obj.mode]
	except: 
		sayexc("change Mode no mode found for " + obj.mode)
		return

	props=config.configMode[obj.mode]['props']
	for p in props:
		pid,ptyp,pgroup,pval=p
		try: temp=obj.getPropertyByName(pid)
		except:
			obj.addProperty(ptyp,pid,pgroup)
			setattr(obj,pid,pval)


#
#  execute image processing
#


def execute_BlobDetector(proxy,obj):

	try: img=obj.sourceObject.Proxy.img.copy()
	except: img=cv2.imread(__dir__+'/icons/freek.png')

	im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	im=255-im
	im2 = img

	params = cv2.SimpleBlobDetector_Params()

	params.filterByArea = True
	params.minArea = obj.Area

	params.filterByConvexity = True
	params.minConvexity = obj.Convexity/200


	# Set up the detector with default parameters.
	detector = cv2.SimpleBlobDetector_create(params)
	
	# Detect blobs.
	keypoints = detector.detect(im)
	# Draw detected blobs as red circles.
	# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
	if not obj.showBlobs:
		im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		obj.Proxy.img = im_with_keypoints
		
		for k in keypoints:
			(x,y)=k.pt
			x=int(round(x))
			y=int(round(y))
#			cv2.circle(im,(x,y),4,0,5)
			cv2.circle(im,(x,y),4,255,5)
			cv2.circle(im,(x,y),4,0,5)
			im[y,x]=255
			im[y,x]=0
		obj.Proxy.img = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
		
	else:
		for k in keypoints:
			(x,y)=k.pt
			x=int(round(x))
			y=int(round(y))
			cv2.circle(im2,(x,y),4,(255,0,0),5)
			cv2.circle(im2,(x,y),4,(0,0,0),5)
			im2[y,x]=(255,0,0)
			im2[y,x]=(0,0,0)
		obj.Proxy.img = im2



def execute_CannyEdge(proxy,obj):
	''' create Canny Edge image with two parameters'''

	try: img=obj.sourceObject.Proxy.img.copy()
	except: img=cv2.imread(__dir__+'/icons/freek.png')

	edges = cv2.Canny(img,obj.minVal,obj.maxVal)
	obj.Proxy.img = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
	say(["Canny Edge image updated",obj.minVal,obj.maxVal])


def execute_Color(proxy,obj):

	try: img=obj.sourceObject.Proxy.img.copy()
	except: img=cv2.imread(__dir__+'/icons/freek.png')

	b,g,r = cv2.split(img)

	if obj.red:
		obj.Proxy.img = cv2.cvtColor(r, cv2.COLOR_GRAY2RGB)
	if obj.blue:
		obj.Proxy.img = cv2.cvtColor(b, cv2.COLOR_GRAY2RGB)
	if obj.green:
		obj.Proxy.img = cv2.cvtColor(255-g, cv2.COLOR_GRAY2RGB)

def execute_Mixer(proxy,obj):

	try: img1=obj.sourceObject.Proxy.img.copy()
	except: img1=cv2.imread(__dir__+'/icons/freek.png')

	try: img2=obj.source2Object.Proxy.img.copy()
	except: img2=cv2.imread(__dir__+'/icons/freek.png')

	s1='/home/thomas/Bilder/bn_900.png'
	s2='/home/thomas/Schreibtisch/quader2.png'

#	img1 = cv2.imread(s1)
#	img2 = cv2.imread(s2)

#	say("execute Mixer")
	if obj.flipOrder:
		img1, img2 =img2, img1
#	say(img1.shape)
#	say(img2.shape)

	if obj.inverse:
		img1=cv2.bitwise_not(img1)
	
	if obj.inverse2:
		img2=cv2.bitwise_not(img2)
	
	(h1,l1,z1)=img1.shape
	(h2,l2,z2)=img2.shape
	ofmax=max(obj.sourceOffsetX,obj.sourceOffsetY)

	h=max(h1,h2)
	l=max(l1,l2)
	nim1=np.zeros((h,l,3),np.uint8)
	nim2=np.zeros((h,l,3),np.uint8)

	try:
		img2 =img2 +img2

		gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
		ret, gb = cv2.threshold(gray,128,255,cv2.THRESH_BINARY)
		gb = cv2.bitwise_not(gb)
		res2=cv2.cvtColor(gb, cv2.COLOR_GRAY2BGR)

		
		if l1>l2:
			xoff22= (l1-l2)*obj.sourceOffsetX//200
			xoff11=0
		else:
			xoff11= (l2-l1)*obj.sourceOffsetX//200
			xoff22=0
		if h1>h2:
			yoff22= (h1-h2)*obj.sourceOffsetY//200
			yoff11=0
		else:
			yoff11= (h2-h1)*obj.sourceOffsetY//200
			yoff22=0

#		say("nims ..")
#		say(nim2.shape)
#		say(nim1.shape)
		nim2[0+yoff22:h2+yoff22, 0+xoff22:l2+xoff22] = img2
		nim1[0+yoff11:h1+yoff11, 0+xoff11:l1+xoff11 ] = img1
			

		w=0.5*obj.weight
		# say(w)
		if obj.modeMixer == 'addWeighted':
			nim=cv2.addWeighted(nim2,0.01*w,nim1,1.0-0.01*w,0)
		elif obj.modeMixer == 'add':
			nim=cv2.add(nim2,nim1)
		else:
			nim=cv2.subtract(nim2,nim1)

		if obj.zoom:
#			say("zoom")
			cv2.rectangle(nim,
					(l*obj.zoomX//200,h*obj.zoomY//200),
					(l*obj.zoomX//200 +(l-l*obj.zoomX//200)*obj.zoomX2//200,h*obj.zoomY//200 + (h-h*obj.zoomY//200)*obj.zoomY2//200),
					(255,0,0),2
				)
			
#		say("nim berechnet")

		# cv2.imshow('res',nim)
		obj.Proxy.img=nim
	except:
		sayexc()



def execute_Threshold(proxy,obj):

	try: img=obj.sourceObject.Proxy.img.copy()
	except: img=cv2.imread(__dir__+'/icons/freek.png')

	# img = cv2.imread('dave.jpg',0) ??
	img = cv2.medianBlur(img,5)
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


	if obj.globalThresholding:
		ret,th1 = cv2.threshold(img,obj.param1,obj.param2,cv2.THRESH_BINARY)
		obj.Proxy.img = cv2.cvtColor(th1, cv2.COLOR_GRAY2RGB)

	if obj.adaptiveMeanTresholding:
		th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
				cv2.THRESH_BINARY,11,2)
		obj.Proxy.img = cv2.cvtColor(th2, cv2.COLOR_GRAY2RGB)

	if obj.adaptiveGaussianThresholding:
		th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
			cv2.THRESH_BINARY,17,2)
		obj.Proxy.img = cv2.cvtColor(th3, cv2.COLOR_GRAY2RGB)

def execute_ColorSpace(proxy,obj):

	try: img=obj.sourceObject.Proxy.img.copy()
	except: img=cv2.imread(__dir__+'/icons/freek.png')
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	lower = np.array([max(obj.h1-obj.h2,0),max(obj.s1-obj.s2,0),max(obj.v1-obj.v2,0)])
	upper = np.array([min(obj.h1+obj.h2,255),min(obj.s1+obj.s2,255),min(obj.v1+obj.v2,255)])
	say("ee")
	say(lower)
	say(upper)

	mask = cv2.inRange(hsv, lower, upper)
	mask = cv2.inRange(img, lower, upper)

	res = cv2.bitwise_and(img,img, mask= mask)

	obj.Proxy.img=res



def execute_GoodFeaturesToTrack(proxy,obj):
	'''
	https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_shi_tomasi/py_shi_tomasi.html
	'''
	try: img=obj.sourceObject.Proxy.img.copy()
	except: img=cv2.imread(__dir__+'/icons/freek.png')

	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	corners = cv2.goodFeaturesToTrack(gray,obj.maxCorners,obj.qualityLevel,obj.minDistance)
	corners = np.int0(corners)

	for i in corners:
		x,y = i.ravel()
		cv2.circle(img,(x,y),3,255,-1)

	obj.Proxy.img = img

def execute_Morphing(proxy,obj):

	try: img=obj.sourceObject.Proxy.img.copy()
	except: img=cv2.imread(__dir__+'/icons/freek.png')

	ks=obj.kernel
	kernel = np.ones((ks,ks),np.uint8)
	if obj.filter == 'dilation':
		dilation = cv2.dilate(img,kernel,iterations = 1)
		img=dilation
	if obj.filter == 'erosion':
		dilation = cv2.erode(img,kernel,iterations = 1)
		img=dilation
	if obj.filter == 'opening':
		dilation = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
		img=dilation
	if obj.filter == 'closing':
		dilation = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
		img=dilation

	obj.Proxy.img = img



#
# property functions for HoughLines
#

def linelengths(self):
	''' helper function for hough lines '''
	lines=self.lines
	ds=[]
	for ll in lines:
		[l]=ll
		d=np.sqrt((l[0]-l[2])**2+(l[1]-l[3])**2)
		ds.append(d)
	ds=np.array(ds)
	return ds

def directions(self):
	''' helper function for hough lines '''
	ds=[]
	for ll in self.lines:
		[l]=ll
		d=np.arctan2((l[0]-l[2]),(l[1]-l[3]))*180.0/np.pi
		if d<0: d += 180
		ds.append(d)
	ds=np.array(ds)
	return ds

def execute_HoughLines(proxy,obj):
	''' find houghlines '''
	
	# parameter from obj
	canny1=obj.canny1
	canny2=obj.canny2
	rho=obj.rho
	theta=obj.theta
	threshold=obj.threshold
	minLineLength =obj.minLineLength
	maxLineGap =obj.maxLineGap

	# load the image
	try: img=obj.sourceObject.Proxy.img.copy()
	except: img=cv2.imread(__dir__+'/icons/freek.png')

	# find edges
	# naechst zwei zeilen koennen wahrscheinlich weg. #+#
	edges = cv2.Canny(img,canny1,canny2)
	obj.Proxy.img = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,canny1,canny2)
	xsize=img.shape[1]
	ysize=img.shape[0]

	# find lines
	lines = cv2.HoughLinesP(edges,1,np.pi/180*theta,threshold, minLineLength = minLineLength, maxLineGap = maxLineGap)

	k=0
	fclines=[]
	img = 0 *img

	for l in lines:
		k += 1
		[[x1,y1,x2,y2]] = l
		fl=tools.fcline(x1,-y1,x2,-y2)
		fclines.append(fl)       
		print (x1,y1,x2,y2)
		a=cv2.line(img,(x1,y1),(x2,y2),(0,255,0),1)

	# data for following nodes
	obj.Proxy.img=img
	obj.Proxy.fclines=fclines
	obj.Proxy.lines=lines

	# method for extra calculations
	obj.Proxy.__class__.linelengths=property(lambda self: linelengths(self))
	obj.Proxy.__class__.directions=property(lambda self: directions(self))


def execute_HoughLinesPost(proxy,obj):
	sayErr("execute_HoughLinesPost - does nothing - update by hand required")


def execute_ImageFile(proxy,obj):

	try: 
		img=cv2.imread(obj.sourceFile)
		if hasattr(obj.Proxy,"markers") and len(obj.Proxy.markers)>=2:
			[x0,y0]=obj.Proxy.markers[0]
			[x1,y1]=obj.Proxy.markers[1]
			if x0 < x1: x0,x1 = x1,x0
			if y0 < y1: y0,y1 = y1,y0
			crop_img = img[y1:y0, x1:x0]

			scaler=img.shape[0]//crop_img.shape[0]

			try:
				img=cv2.resize(crop_img,
						(img.shape[1],img.shape[1]*crop_img.shape[0]//crop_img.shape[1]),
						interpolation = cv2.INTER_CUBIC)
			except: sayexc()

		obj.Proxy.img=img


#---------------------
		# cv2 selector postprocessing
		if hasattr(obj.Proxy,"center"): 
			img2=img.copy()
			img2 = np.zeros(img.shape, np.uint8)
			color=(255,255,255)
			if obj.rectangleSelectMode:
				cv2.rectangle(img2,obj.Proxy.center,obj.Proxy.point2,color,-1)
			else:
				cv2.circle(img2,obj.Proxy.center,obj.Proxy.R,color,-1)

			img3 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
			if obj.invert: img=255-img
			res = cv2.bitwise_and(img,img,mask = img3)
			if obj.invert: res=255-res
			obj.Proxy.img=res
#---------------------



	except:
		sayexc()
		sayErr(__dir__+'/icons/freek.png')
		obj.Proxy.img=cv2.imread(__dir__+'/icons/freek.png')

	# subimage selection
	if obj.subX1>0 or obj.subY1>0:
		if obj.subY1 == 0: yy=img.shape[0]
		else: yy=obj.subY1

		if obj.subX1 == 0: xx=img.shape[1]
		else: xx=obj.subX1

		obj.Proxy.img=obj.Proxy.img[obj.subY0:obj.subY0+yy,obj.subX0:obj.subX0+xx]



def execute_Mask(proxy,obj):

	if obj.undo and hasattr(obj.Proxy,'points'): obj.Proxy.points=[]

	try: img=obj.sourceObject.Proxy.img.copy()
	except: 
		sayexc()
		img=cv2.imread(__dir__+'/icons/freek.png')

	# draw for every point a full circle
	if hasattr(obj.Proxy,'points'):
		for [x,y,R] in obj.Proxy.points:
			if obj.invertMask: color=(255,255,255)
			else: color=(0,0,0)
			cv2.circle(img,(x,y),R,color,-1)

	obj.Proxy.img=img


def execute_ElevationGrid(proxy,obj):
	say("no exe l2vation grid")
	# run_elevationgrid(obj,None)
	say("done")


def execute_HSV(proxy,obj):

	say("hsv ..")

	try: img=obj.sourceObject.Proxy.img.copy()
	except: img=cv2.imread(__dir__+'/icons/freek.png')

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	lower=np.array([obj.valueColor-obj.deltaColor,0,0])
	upper=np.array([obj.valueColor+obj.deltaColor,255,255])
	mask = cv2.inRange(hsv, lower, upper)

	res = cv2.bitwise_and(hsv,hsv, mask= mask)

	obj.Proxy.img=res




def execute_Invert(proxy,obj):

	say("invert ..")

	try: img=obj.sourceObject.Proxy.img.copy()
	except: img=cv2.imread(__dir__+'/icons/freek.png')

	imagem = 255-img
	obj.Proxy.img=imagem


def execute_Pathes(proxy,obj):
	say("execute pathes")
	try: 
		say("try peoxy.lock")
		if proxy.lock: return
	except:
		say("except proxy lock")
	proxy.lock=True
	run_pathes(obj,None)
	say("invert ..")
	proxy.lock=False


def execute_PathAnalyzer(proxy,obj):
	say("execute path  analyser")
	say([obj.N,obj.Threshold])
	try:
		say(len(obj.Proxy.pl2))
		run_pathanalyzer(obj,None,False,False)
	except:
		say("still no data to analyze")
	say("path analyse done")



'''
alte version

def execute_SkeletonV0(proxy,obj):
	say("skeleton ..")
	threshold=obj.threshold
	otsu=obj.otsu

	try: 
		img2=obj.sourceObject.Proxy.img
		img=img2.copy()
	except: 
		sayexc()
		img=cv2.imread(__dir__+'/icons/freek.png')

	img3 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	size = np.size(img3)
	skel = np.zeros(img3.shape,np.uint8)
	g = 255*np.ones(img3.shape,np.uint8)
	b = np.zeros(img3.shape,np.uint8)
	
	
	# flexibler
	if otsu:
		ret,img3 = cv2.threshold(img3, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 
	else:
		ret,img3 = cv2.threshold(img3,threshold,255,0)

	element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
	ks=2
	kernel = np.ones((ks,ks),np.uint8)
	done = False
	n=1000
	c=0
	while( not done):
		eroded = cv2.erode(img3,element)
		temp = cv2.dilate(eroded,element)
		temp = cv2.subtract(img3,temp)
		temp = (61*c%256)* temp  
		
		temp= cv2.dilate(temp,kernel,iterations = 1)
		
# 		say(c)
#		say(skel.shape)
#		say(temp.shape)
		skel = cv2.bitwise_or(skel,temp)
#		if c>0:
#			g = cv2.bitwise_or(g,temp)
#		if c>2:
#			b = cv2.bitwise_or(b,temp)
		c += 1
		
		hsv = cv2.merge((skel,g,g))
		bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
		cv2.imwrite("/tmp/hsv_skel_"+str(n)+".png", hsv)
		cv2.imwrite("/tmp/skel_"+str(n)+".png", skel)
		n += 1
		img3 = eroded.copy()

		s=cv2.countNonZero(img3)
		zeros = size - s
		if zeros==size:
			done = True

	say("skeleton done")

	hsv = cv2.merge((skel,g,g))
	bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

	#obj.Proxy.img=skel
	obj.Proxy.img=bgr

'''




def execute_Skeleton(proxy,obj):

	from skimage.morphology import medial_axis

	threshold=0.1*obj.threshold

	try: 
		img2=obj.sourceObject.Proxy.img
		img=img2.copy()
	except: 
		sayexc()
		img=cv2.imread(__dir__+'/icons/freek.png')

	data = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Compute the medial axis (skeleton) and the distance transform
	skel, distance = medial_axis(data, return_distance=True)

	# Distance to the background for pixels of the skeleton
	dist_on_skel = distance * skel

	# entferne ganz duenne linien
	dist_on_skelw =(dist_on_skel >= threshold)* distance

	say("size of the image ...")
	say(dist_on_skelw.shape)
#	skel = np.array(dist_on_skelw,np.uint8) 
	skel = np.array(dist_on_skelw *255/np.max(dist_on_skelw),np.uint8) 
	obj.Proxy.img=cv2.cvtColor(skel*100, cv2.COLOR_GRAY2BGR)
	obj.Proxy.dist_on_skel=dist_on_skelw


def execute_FatColor(proxy,obj):

	import matplotlib.pyplot as plt

	from skimage.morphology import medial_axis

	try: 
		img2=obj.sourceObject.Proxy.img
		img=img2.copy()
	except: 
		sayexc()
		img=cv2.imread(__dir__+'/icons/freek.png')

	lower = np.array([255,255,255])
	upper = np.array([255,255,255])

	mask = cv2.inRange(img, lower, upper)
	res = cv2.bitwise_and(img,img, mask= mask)

	ks=3
	kernel = np.ones((ks,ks),np.uint8)

	kernelPLUS=np.array([[0, 1, 0],
		   [1, 1, 1],
		   [0, 1, 0]], dtype=np.uint8)

	kernelCROSS=np.array([[1, 0,1],
		   [0, 1, 0],
		   [1, 0, 1]], dtype=np.uint8)

	dilation = cv2.dilate(res,kernel,iterations = 1)
	erode1 = cv2.erode(res,kernelPLUS,iterations = 1)
	erode2 = cv2.erode(res,kernelCROSS,iterations = 1)
	erode = cv2.erode(res,kernel,iterations = 1)
	res=dilation
	res=erode1 + erode2 

	dilation = cv2.dilate(res,kernel,iterations = 1)
	res=dilation

#	plt.imshow(res, cmap=plt.cm.PRGn, interpolation='nearest')
#	plt.show()

	obj.Proxy.img=res



#---------------------------------
class _CV(Animation._Actor):

	def __init__(self,obj):
		obj.Proxy = self
#		self.Type = self.__class__.__name__
#		self.obj2 = obj
		_ViewProviderCV(obj.ViewObject) 


	def execute(self,obj):

		# hidden objects are not executed
		if not obj.ViewObject.Visibility:
			sayW("NOT execute " + obj.mode +  " on " + obj.Label)
			return

		sayW("execute " + obj.mode +  " on " + obj.Label)
		exec("rc=execute_"+obj.mode+"(self,obj)")

		if obj.invert: self.img=255-self.img

		if rc <> None: say(("executed " + obj.mode + " rc=",rc))

		try:
			if obj.ViewObject.Proxy.edit <> None:
#				say("erzeuge dialig")
				try:
					zz=obj.ViewObject.Proxy.Object.Proxy.app.mpl
					obj.ViewObject.Proxy.Object.Proxy.app.plot2()
				except:
					obj.ViewObject.Proxy.createDialog()
					if obj.ViewObject.Proxy.hidden:
						obj.ViewObject.Proxy.edit()
					obj.ViewObject.Proxy.hidden=True
					obj.ViewObject.Proxy.Object.Proxy.app.plot2()
			else:
#				say("muss edit erzeugen")
				obj.ViewObject.Proxy.createDialog()
				if obj.ViewObject.Proxy.hidden:
					obj.ViewObject.Proxy.edit()
				obj.ViewObject.Proxy.hidden=True
				obj.ViewObject.Proxy.Object.Proxy.app.plot2()

		except:
			sayexc()

		obj.ViewObject.Proxy.Object.Proxy.app.updateDialog()
		return rc


	def onChanged(self,obj,prop):
		if prop == 'mode': changeMode(obj,obj.mode)

	@property
	# testcase for dynamic property, to call use 
	# App.ActiveDocument.My_ImageFile.Proxy.myprop
	# http://stackoverflow.com/questions/1325673/how-to-add-property-to-a-python-class-dynamically

	def myprop(self):
		say("myprop called")
		return "Return of MYPROP"



class _ViewProviderCV(Animation._ViewProviderActor):

	''' the gui for a CV node '''

	edit=None


	def __init__(self,vobj):
		self.attach(vobj)


	def attach(self,vobj):
		self.emenu=[]
		self.cmenu=[]
		self.Object = vobj.Object
		vobj.Proxy = self
		self.vers=__vers__
		self.hidden=True
		try: self.createDialog()
		except: sayexc()
		self.hidden=True


	def getIcon(self):
		return  __dir__+ '/icons/'+self.Object.mode+'.svg'

	def doubleClicked(self,vobj):
		self.edit2()


	def createDialog(self): 

		if self.hidden: self.hidden=False
		else: return

		app=CVGui()
		miki2=miki.Miki()
		miki2.app=app
		app.root=miki2
		app.obj=self.Object
		self.Object.Proxy.app=app

#		self.edit= lambda:miki2.run(CVGui.layout.format(
#				self.Object.Label+": "+self.Object.mode,
#				self.Object.Label+": "+self.Object.mode
#				),
#			app.modDialog)

		self.edit= lambda:miki2.run(CVGui.layout.format(
				self.Object.Label,
				self.Object.Label+": "+self.Object.mode
				),
			app.modDialog)


	def edit2(self):
		self.hidden=True
		self.createDialog()
		self.edit()
		dockit()


	def setupContextMenu(self, obj, menu):
		''' create the context menu''' 

		self.createDialog()

		try: t=config.configMode[self.Object.mode]
		except: sayexc("setupContextMenu no value for property mode " + self.Object.mode)

		cl=self.Object.Proxy.__class__.__name__
		action = menu.addAction("About " + cl)
		action.triggered.connect(self.showVersion)

		action = menu.addAction("Edit ... ")
		action.triggered.connect(self.edit2)

		action = menu.addAction("Show Image ...")
		action.triggered.connect(self.Object.Proxy.app.plot)

		action = menu.addAction("Update Image ...")
		action.triggered.connect(self.Object.Proxy.app.plot2)

		action = menu.addAction("Show colormap ...")
		action.triggered.connect(self.Object.Proxy.app.showcolormap)


	def setEdit(self,vobj,mode=0):
		if self.hidden:
			self.createDialog()
			self.edit()
			dockit()
			self.hidden=False
		FreeCAD.ActiveDocument.recompute()
		return True




def createCV(mode='ImageFile',label=None):
	''' create a new CV node '''

	if label == None: label = "My " + mode

	obj=FreeCAD.ActiveDocument.addObject('App::DocumentObjectGroupPython',label)
	obj.addProperty('App::PropertyLink','sourceObject',"Base")
	obj.addProperty('App::PropertyFile','sourceFile',"Base")
	obj.addProperty('App::PropertyEnumeration','mode',"Base").mode=modes
	obj.addProperty('App::PropertyBool','invert',"Base").invert=False
	
	#obj.addProperty('App::PropertyInteger','subX0',"Base").subX0=0
	#obj.addProperty('App::PropertyInteger','subX1',"Base").subX1=0
	#obj.addProperty('App::PropertyInteger','subY0',"Base").subY0=0
	#obj.addProperty('App::PropertyInteger','subY1',"Base").subY1=0
	
	obj.mode=mode
	changeMode(obj,obj.mode)
	_CV(obj)

	return obj
