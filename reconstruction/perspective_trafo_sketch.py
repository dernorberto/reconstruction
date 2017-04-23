
import FreeCADGui as Gui
import FreeCAD,Part,Sketcher
App=FreeCAD

import Draft
import numpy as np

import PySide
from PySide import  QtGui,QtCore


import numpy as np
import random
from pivy import coin
import time

import cv2
import numpy as np
import scipy
import scipy.cluster
import scipy.cluster.vq 


#-------------------








#----------------------------------------------------------------


def showborders(shx):
	pass

	lines=FreeCAD.ll

	plines=[]
	dl=[]
	al=[]
	for x1,y1,x2,y2 in lines:
		p1=FreeCAD.Vector(x1,y1,0)
		p2=FreeCAD.Vector(x2,y2,0)
		#plines.append(Part.makePolygon([p1,p2]))

	#	pts += [FreeCAD.Vector(x,y,0),FreeCAD.Vector(x+y,y-x,0)]
		d=FreeCAD.Vector().projectToLine(p1+1000000*(p2-p1),p2+1000000*(p1-p2))

		plines.append(Part.makePolygon([p1+2000*(p2-p1).normalize(),p2+2000*(p1-p2).normalize()]))

		d=d*(-1)
		#plines.append(Part.makePolygon(FreeCAD.Vector(),p1+d]))

		alpha=np.arctan2(x2-x1,y2-y1)
		print (round(d.Length,1),round(alpha/np.pi*180,1))
		dl.append(d.Length)
		al.append(alpha)

	import matplotlib as ml
	import matplotlib.pyplot as plt
	import scipy
	import scipy.cluster
	import scipy.cluster.vq 
	

	plt.plot(dl,al,'x')
	#plt.show()

	# Part.show(Part.Compound(plines))

	#from scipy.cluster.vq import kmeans,vq
	# idee von http://glowingpython.blogspot.de/2012/04/k-means-clustering-with-scipy.html

	data=np.array([dl,al]).swapaxes(0,1)

	# computing K-Means with K = 2 (2 clusters)
	cs=4
	centroids,_ = scipy.cluster.vq.kmeans(data,cs)
	# assign each sample to a cluster
	idx,_ = scipy.cluster.vq.vq(data,centroids)

	# some plotting using numpy's logical indexing

	# some plotting using numpy's logical indexing
	plt.plot(
		data[idx==0,0],data[idx==0,1],'Dy',
		data[idx==1,0],data[idx==1,1],'Dc',
		data[idx==2,0],data[idx==2,1],'Db',
		data[idx==3,0],data[idx==3,1],'Dg'
	 )


	plt.plot(centroids[:,0],centroids[:,1],'or',markersize=8)
	plt.show()

	import Draft

	#shy=1536

	goodlines=[1]*len(data)

	for pp in [0,0,1]:
		for cn in range(cs):
			print ("cn",cn)
			xxs=[]
			yys=[]
			tns=[]
			lls=[]
			for i,c in enumerate(idx):
				if not goodlines[i]: continue
				if c==cn:
					#print data[i]
					print (lines[i],data[i,1],data[i,0])
					x1,y1,x2,y2=lines[i]
					#print (np.tan(data[i,1]),(0.0+x1-x2)/(y1-y2))
					xxs += [x1,x2]
					yys += [y1,y2]
					tns += [data[i,1]]
					lls += [i]
			l=len(xxs)
			xm=sum(xxs)/l
			ym=sum(yys)/l
			dm=sum(tns)/len(tns)
			for i in lls:
				print ("------",i,data[i,1]-dm)
				if abs(data[i,1]-dm)>0.5:
					goodlines[i]=0
			print (xm,ym,dm)
			if pp:
				b=FreeCAD.Vector(xm,-ym+shx,20)
				bd=FreeCAD.Vector(1000*np.sin(dm),-1000*np.cos(dm),20)
				d=Draft.makeWire([b+bd,b-bd])










def genpics(w=None,fn=None):

	if w <>None:
		print "genpics ..."
		lo=w.th1.value()
		up=w.th2.value()
		fn=w.fn
		debug=w.debugf.isChecked()

	else:
		lo=100
		up=250
		debug=False

	if lo>up: lo,up=up,lo

	# graubild
	print ("fn",fn)
	imgg = cv2.imread(fn,0)
	imgg.shape


	img = cv2.imread(fn)

	img.shape

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


	# filten bereich in hsv
	# http://docs.opencv.org/3.2.0/df/d9d/tutorial_py_colorspaces.html


	gx=180
	gy=120

	#b=cv2.inRange(b,lo,up)

	h=hsv[:,:,0]
	s=hsv[:,:,1]
	v=hsv[:,:,0]
	h=cv2.resize(h, (gx, gy)) 
	s=cv2.resize(s, (gx, gy)) 
	v=cv2.resize(v, (gx, gy)) 

	h=cv2.inRange(h,lo,up)
	s=cv2.inRange(s,lo,up)
	v=cv2.inRange(v,lo,up)

	cv2.imwrite('/tmp/h.png',h)
	cv2.imwrite('/tmp/s.png',s)
	cv2.imwrite('/tmp/v.png',v)

	if debug:
		cv2.imshow('h',h)
		cv2.imshow('s',s)
		cv2.imshow('v',v)



	r=img[:,:,0]
	g=img[:,:,1]
	b=img[:,:,2]
	r=cv2.resize(r, (gx, gy)) 
	g=cv2.resize(g, (gx, gy)) 
	b=cv2.resize(b, (gx, gy)) 


	r=cv2.inRange(r,lo,up)
	g=cv2.inRange(g,lo,up)
	b=cv2.inRange(b,lo,up)

	cv2.imwrite('/tmp/r.png',r)
	cv2.imwrite('/tmp/g.png',g)
	cv2.imwrite('/tmp/b.png',b)

	if debug:
		cv2.imshow('r',r)
		cv2.imshow('g',g)
		cv2.imshow('b',b)


	#b2=cv2.inRange(b,120,255)
	#cv2.imshow('b2',b2)
	#cv2.imwrite('/tmp/b2.png',b2)

	if w<>None:
		fn='/tmp/b.png'
		myPixmap = QtGui.QPixmap(fn)
		w.lb.setPixmap(myPixmap)

		fn='/tmp/g.png'
		myPixmap = QtGui.QPixmap(fn)
		w.lg.setPixmap(myPixmap)

		fn='/tmp/r.png'
		myPixmap = QtGui.QPixmap(fn)
		w.lr.setPixmap(myPixmap)


		fn='/tmp/h.png'
		myPixmap = QtGui.QPixmap(fn)
		w.lh.setPixmap(myPixmap)

		fn='/tmp/s.png'
		myPixmap = QtGui.QPixmap(fn)
		w.ls.setPixmap(myPixmap)

		fn='/tmp/v.png'
		myPixmap = QtGui.QPixmap(fn)
		w.lv.setPixmap(myPixmap)


		genresult(w,w.fn,w.ths.value(),w.mode)
		fn='/tmp/result.png'
		myPixmap = QtGui.QPixmap(fn)
		w.result.setPixmap(myPixmap)
		print "done"




# siehe http://c4dnetwork.com/board/threads/81548-Schnittpunkt-zwischen-zwei-Strahlen
def RayIntersection(p0, d0, p1, d1):
	"""
	p0 -> Ortvektor erster Strahl / Position vector of first ray
	d0 -> Richtungsvektor erster Strahl / Direction vector of first ray
	p1 -> Ortvektor zweiter Strahl / Position vector of second ray
	d1 -> Richtungsvektor zweiter Strahl / Direction vector of second ray
	"""
	if d0 == FreeCAD.Vector(0,0,0) or d1 == FreeCAD.Vector(0,0,0): return None

	k1 = int((d0.x+0.00001)/(d1.x+0.00001)+0.00005)
	k2 = int((d0.y+0.00001)/(d1.y+0.00001)+0.00005)
	k3 = int((d0.z+0.00001)/(d1.z+0.00001)+0.00005)
	if k1 == k2 == k3: return None


	a = d0.x*(p1.x-p0.x) + d0.y*(p1.y-p0.y) + d0.z*(p1.z-p0.z)
	b = d1.x*(p1.x-p0.x) + d1.y*(p1.y-p0.y) + d1.z*(p1.z-p0.z)
	c = d0.x**2 + d0.y**2 + d0.z**2
	d = d1.x**2 + d1.y**2 + d1.z**2
	e = d1.x*d0.x + d1.y*d0.y + d1.z*d0.z
	try:
		s = ((a * -d) + (e * b)) / ((c * -d) + e**2)
		t = (b - s*e)/-d
	except:
		print "Schnittpunkt fehler fuer"
		print p0
		print d0
		print p1
		print d1
		return None

#	print (p0 + s*d0 - (p1 + t*d1))
	return p0 + s*d0


'''
p0=FreeCAD.Vector(10,0,0)
p1=FreeCAD.Vector(20,0,0)
d0=FreeCAD.Vector(1,1,0)
d1=FreeCAD.Vector(-1,2,0)
 
 
res=  RayIntersection(p0, d0, p1, d1)
print res
'''


def genresult(w=None,fn='/home/thomas/Bilder/bp_325.png',s=150,mode='grey'):
	import cv2
	import numpy as np
	fn=FreeCAD.ParamGet('User parameter:Plugins/reconstruction').GetString("Document")
	print ("genresult",fn)
	fcupd=w<>None and w.computef.isChecked()
	debug=w<>None and w.debugf.isChecked()
	
	'''
	fn='/home/thomas/Dokumente/freecad_buch/b244_perspective_transform.py/Prozessmodell.jpg'
	fn='/home/thomas/Bilder/122_PANA/P1220700.JPG'
	fn='/home/thomas/Bilder/122_PANA/P1220701.JPG'
	fn='/home/thomas/Bilder/122_PANA/P1220702.JPG'
	fn='/home/thomas/Bilder/122_PANA/P1220703.JPG'
	#fn=
	'''
	img = cv2.imread(fn,0)
	imgr = cv2.imread(fn)
	try:
		imgr = cv2.cvtColor(imgr,cv2.COLOR_GRAY2RGB)
	except: pass
	hsv = cv2.cvtColor(imgr, cv2.COLOR_BGR2HSV)


	print imgr.shape
	shx,shy,_t= imgr.shape
	# img ist sw

	im3=cv2.resize(img, (800, 800)) 
	if debug: cv2.imshow("image",im3)


	print ("berechne img2 nach mode",mode)
	# schwellwert 110
	img2=img
	
	
	if mode=='grey': img2=img
	elif mode=='r':	img2=imgr[:,:,0]
	elif mode=='g':	img2=imgr[:,:,1]
	elif mode=='b':	img2=imgr[:,:,2]
	elif mode=='h':	img2=hsv[:,:,0]
	elif mode=='s':	img2=hsv[:,:,1]
	elif mode=='v':	img2=hsv[:,:,2]

	img2=(img2>s)*240
	img2=np.array(img2,dtype=np.uint8)

	ks=50
	kernel = np.ones((ks,ks),np.uint8)

	closing =img2

	closing = cv2.morphologyEx(img2, cv2.MORPH_CLOSE, kernel)
	closing = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)


	edges = cv2.Canny(closing,100,200)
	print ("size edges",edges.shape)

	t=np.where(edges == 255)      

	pts=[]
	for i in range(len(t[0])):
		pts.append(FreeCAD.Vector(t[0][i],t[1][i],0))

	print "hah"
	edges2 = cv2.cvtColor(edges,cv2.COLOR_GRAY2RGB)
	edges2 *= 0

	#lines = cv2.HoughLinesP(edges,1,np.pi/180,100, minLineLength = 20, maxLineGap = 100)[0]
	lines = cv2.HoughLinesP(edges,1,np.pi/180,100, minLineLength = 20, maxLineGap = 20)[0]


	if lines<>None:
		print "huhu"
#		print lines
		FreeCAD.ll=np.array(lines)
		ll=np.array(lines).swapaxes(0,1)
		
#		print ll[0]
#		xm=0.5*(ll[0].mean()+ll[2].mean())
#		ym=0.5*(ll[1].mean()+ll[3].mean())

		for x1,y1,x2,y2 in lines:        
			cv2.line(edges2,(x1,y1),(x2,y2),(0,255,255,255),1)

		for x1,y1,x2,y2 in lines:        
			cv2.line(imgr,(x1,y1),(x2,y2),(0,255,255,255),15)
			cv2.line(imgr,(x1,y1),(x2,y2),(0,0,255,255),5)

		print "directionsa "
		dirs=[]
		plines=[]
		xm=0
		ym=0
		for x1,y1,x2,y2 in lines:
			p1=FreeCAD.Vector(x1,-y1+shx,10)
			p2=FreeCAD.Vector(x2,-y2+shx,10)

			plines.append(Part.makePolygon([p1,p2]))

#			pts += [FreeCAD.Vector(x,y,0),FreeCAD.Vector(x+y,y-x,0)]
			d=FreeCAD.Vector().projectToLine(p1+1000000*(p2-p1),p2+1000000*(p1-p2))
			alpha=np.arctan2(x2-x1,y2-y1)
			print (round(d.Length,1),round(alpha/np.pi*180,1))
			#d.normalize()
			#print (d.normalize(),(p1-p2).normalize())
			dirs.append([round(d.Length,1),round(alpha/np.pi*180,1)])
			FreeCAD.dirs=dirs

		p1=FreeCAD.Vector(0,0,10)
		p2=FreeCAD.Vector(shy,shx,10)
		plines.append(Part.makePolygon([p1,p2]))
		if fcupd:
			Part.show(Part.Compound(plines))
			App.ActiveDocument.ActiveObject.Label="dir 345 obhj"
			App.ActiveDocument.ActiveObject.ViewObject.LineColor=(1.0,0.,0.)

	print "b"

	# schnittpunkte berechnen
	if lines<>None:
		maxx,maxy=img.shape
		apts=[FreeCAD.Vector(x1,y1,0) for x1,y1,x2,y2 in lines]
		dirs=[FreeCAD.Vector(x2-x1,y2-y1,0) for x1,y1,x2,y2 in lines]

		ptsq=[]
		for i,h in enumerate(apts):
			for j in range(i):
				p=RayIntersection(apts[i], dirs[i], apts[j], dirs[j])
				if p<>None:
					if p.x>-maxx and p.x<2*maxx and  p.y>-maxy and p.y<2*maxy:
						ptsq.append(FreeCAD.Vector(p[0],1500-p[1],0))
						print p

		import Points
		FreeCAD.ptsq=ptsq
		if fcupd:
			Points.show(Points.Points(ptsq))
			App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(1.0,0.,0.)
			App.ActiveDocument.ActiveObject.ViewObject.PointSize=5

		print "hone"


		# define criteria and apply kmeans()
		'''
		Z=[[p.x,p.y,0] for p in ptsq]
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 3.0)
		Z2=np.float32(Z)
		ret,label,center=cv2.kmeans(Z2, 4, criteria, 10, 0)
		ptsc=[FreeCAD.Vector(p) for p in center]
		Points.show(Points.Points(ptsc))
		App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(1.0,0.,0.)
		App.ActiveDocument.ActiveObject.ViewObject.PointSize=10

		print ret
		print label
		print "center"
		print center
		'''


		import Points

		dist={}
		# ptsq=FreeCAD.ptsq
		for i,p in enumerate(ptsq):
			ds=0
			for j,q in enumerate(ptsq):
				if i<>j:
					ds += 1.0/(1+(p-q).Length)
			print ds
			dist[i]=ds

		vs=dist.values()
		vs.sort()


		its=[i for i in dist if dist[i] in vs[-70:-1]]
		cpis=[ptsq[i] for i in its]
		if fcupd:
			Points.show(Points.Points(cpis))
			App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(1.0,1.,0.)
			App.ActiveDocument.ActiveObject.ViewObject.PointSize=12



	edges3=cv2.resize(edges2, (800, 800)) 
	if debug: cv2.imshow("cont",edges3)
	

	imgr=cv2.resize(imgr, (640, 480)) 
	if debug: cv2.imshow("imgr",imgr)
	cv2.imwrite('/tmp/result.png',imgr)


	if w<>None and w.computef.isChecked():
		showborders(shx)

	return
	if 0:
		import Points
		Points.show(Points.Points(pts))


		ctn=np.array([[p.x,p.y] for p in pts],dtype=np.float32)
		ch=cv2.convexHull(np.array(ctn))

		ptsc=[FreeCAD.Vector(c[0,0],c[0,1],0) for c in ch]

		import Draft
		Draft.makeWire(ptsc,closed=True)



def mode(w,m):
	w.mode=m
	print ("mode",w.mode,w.fn)
	genpics(w)





def dialog(fn):

	gx=180
	gy=120


	w=QtGui.QWidget()
	w.fn=fn
	w.mode='grey'
	w.progress=lambda a,b:progress(w,a,b)

	w.i=100

	box = QtGui.QVBoxLayout()
	
	box = QtGui.QGridLayout()
	box.setSpacing(10)

	#	grid.addWidget(title, 1, 0)
	#	grid.addWidget(titleEdit, 1, 1,1,3)


	w.setLayout(box)
	w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

#	l=QtGui.QLabel("Anzahl" )
#	box.addWidget(l)
#	w.anz = QtGui.QLineEdit()
#	w.anz.setText('3')
#	box.addWidget(w.anz)

	w.btn_stop=QtGui.QPushButton("run")
	box.addWidget(w.btn_stop,0,0)
	w.btn_stop.pressed.connect(lambda:genpics(w))

	w.btn_clean=QtGui.QPushButton("clean")
	box.addWidget(w.btn_clean,0,5)
	w.btn_stop.pressed.connect(lambda:genpics(w))

	w.computef=QtGui.QCheckBox("Update Sketch")
	box.addWidget(w.computef,0,1)

	w.debugf=QtGui.QCheckBox("Debug on")
	box.addWidget(w.debugf,0,2)
	# w.debugf.click()



	w.btn_b=QtGui.QPushButton("b")
	w.btn_b.pressed.connect(lambda :mode(w,'b'))
	box.addWidget(w.btn_b,1,0)
	w.lb= QtGui.QLabel("huhu")
	fn='/tmp/b.png'
	myPixmap = QtGui.QPixmap(fn)
	myScaledPixmap = myPixmap.scaled(PySide.QtCore.QSize(gx,gy))#, Qt.KeepAspectRatio)
	w.lb.setPixmap(myScaledPixmap)
	box.addWidget(w.lb,2,0)


	w.btn_g=QtGui.QPushButton("g")
	w.btn_g.pressed.connect(lambda :mode(w,'g'))
	box.addWidget(w.btn_g,3,0)
	w.lg= QtGui.QLabel("huhu")
	fn='/tmp/g.png'
	myPixmap = QtGui.QPixmap(fn)
	myScaledPixmap = myPixmap.scaled(PySide.QtCore.QSize(gx,gy))#, Qt.KeepAspectRatio)
	w.lg.setPixmap(myScaledPixmap)
	box.addWidget(w.lg,4,0)

	w.btn_r=QtGui.QPushButton("r")
	w.btn_r.pressed.connect(lambda :mode(w,'r'))
	box.addWidget(w.btn_r,5,0)
	w.lr= QtGui.QLabel("huhu")
	fn='/tmp/r.png'
	myPixmap = QtGui.QPixmap(fn)
	myScaledPixmap = myPixmap.scaled(PySide.QtCore.QSize(gx,gy))#, Qt.KeepAspectRatio)
	w.lr.setPixmap(myScaledPixmap)
	box.addWidget(w.lr,6,0)


	w.btn_h=QtGui.QPushButton("h")
	w.btn_h.pressed.connect(lambda :mode(w,'h'))
	box.addWidget(w.btn_h,1,1)
	w.lh= QtGui.QLabel("huhu")
	fn='/tmp/h.png'
	myPixmap = QtGui.QPixmap(fn)
	myScaledPixmap = myPixmap.scaled(PySide.QtCore.QSize(gx,gy))#, Qt.KeepAspectRatio)
	w.lh.setPixmap(myScaledPixmap)
	box.addWidget(w.lh,2,1)

	w.btn_s=QtGui.QPushButton("s")
	w.btn_s.pressed.connect(lambda :mode(w,'s'))
	box.addWidget(w.btn_s,3,1)
	w.ls= QtGui.QLabel("huhu")
	fn='/tmp/s.png'
	myPixmap = QtGui.QPixmap(fn)
	myScaledPixmap = myPixmap.scaled(PySide.QtCore.QSize(gx,gy))#, Qt.KeepAspectRatio)
	w.ls.setPixmap(myScaledPixmap)
	box.addWidget(w.ls,4,1)

	w.btn_v=QtGui.QPushButton("v")
	w.btn_v.pressed.connect(lambda :mode(w,'v'))
	box.addWidget(w.btn_v,5,1)
	w.lv= QtGui.QLabel("huhu")
	fn='/tmp/v.png'
	myPixmap = QtGui.QPixmap(fn)
	myScaledPixmap = myPixmap.scaled(PySide.QtCore.QSize(gx,gy))#, Qt.KeepAspectRatio)
	w.lv.setPixmap(myScaledPixmap)
	box.addWidget(w.lv,6,1)


	w.lo= QtGui.QLabel("low threshold")
	box.addWidget(w.lo,1,2)
	w.th1 = QtGui.QSlider(QtCore.Qt.Horizontal)
	w.th1.setValue(100)
	w.th1.setMaximum(255)
	w.th1.setMinimum(0)
	box.addWidget(w.th1,2,2)

	w.th1.valueChanged.connect(lambda :genpics(w))

	w.up= QtGui.QLabel("high threshold")
	box.addWidget(w.up,3,2)

	w.th2 = QtGui.QSlider(QtCore.Qt.Horizontal)
	w.th2.setValue(200)
	w.th2.setMaximum(255)
	w.th2.setMinimum(0)
	box.addWidget(w.th2,4,2)
	w.th2.valueChanged.connect(lambda :genpics(w))

	w.sl= QtGui.QLabel("param s")
	box.addWidget(w.sl,5,2)

	w.ths = QtGui.QSlider(QtCore.Qt.Horizontal)
	w.ths.setValue(160)
	w.ths.setMaximum(255)
	w.ths.setMinimum(0)
	box.addWidget(w.ths,6,2)
	w.ths.valueChanged.connect(lambda :genpics(w))



	#ergebnis
	label= QtGui.QLabel("huhu")
	# hier ein angfangsbilde erzeugen !!
#	fn='/tmp/b.png'
#	fn='/home/thomas/Bilder/bp_338.png'
	fn=w.fn
	myPixmap = QtGui.QPixmap(fn)
	print label.size()
	myScaledPixmap = myPixmap.scaled(label.size())#, Qt.KeepAspectRatio)
	#myScaledPixmap = myPixmap.scaled(PySide.QtCore.QSize(gx,gy))#, Qt.KeepAspectRatio)
	label.setPixmap(myScaledPixmap)
	w.result=label
	box.addWidget(w.result,1,4,6,2)

	w.show()
	genpics(w)
	return w


def run():
	fna='/home/thomas/Bilder/122_PANA/P1220703.JPG'
	fna=FreeCAD.ParamGet('User parameter:Plugins/reconstruction').GetString("Document",fna)
	genpics(None,fna)
	dialog(fna)



