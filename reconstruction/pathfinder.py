# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- reconstruction workbench
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

from say import *

import cv2

import reconstruction.mpl
reload(reconstruction.mpl)


# import cProfile

def context(ed,x,y):
	''' calculate the context of a point'''

	if ed[x,y]==0:
		return [0,0]
	try:
		plus=ed[x+1,y]+ed[x,y+1]+ed[x-1,y]+ed[x,y-1]
		cross=ed[x+1,y+1]+ed[x-1,y-1]+ed[x-1,y+1]+ed[x+1,y-1]
		ivals = 2*ed[x+1,y]+ed[x,y+1]+64*ed[x-1,y]+128*ed[x,y-1]
		ivals += 4*ed[x+1,y+1] + 32*ed[x-1,y-1] + 16*ed[x-1,y+1] + 8*ed[x+1,y-1]
	except: 
		plus=0
		cross=0
		ivals=0

	return [plus + cross,ivals]

colortab=[
	[255,255,255], # 0
	[0,255,255], # 1
	[0,255,0], # 2
	[255,0,255], # 3
	[0,255,255], # 4
	[0,0,255], # 5
	[0,0,255], # 6
	[0,0,255], # 7
	[0,0,255] # 8
]


def run(ed,cimg,ed2,showPics=True):

	startpts=[]; dreier=[]; vieler=[]

	l,w=ed.shape
	counts=[0,0,0,0,0,0,0,0,0,0]

	for x in range(l):
		for y in range(w):
			[ix,ivals] =context(ed,x,y)
			if ix==1:
				startpts.append([x,y])
			elif ix==3:
				dreier.append((x,y))
			elif ix>=4:
				vieler.append((x,y))
			counts[ix] += 1
			cimg[x,y]=colortab[ix]
			if ix<5:
				ed2[x,y]=ix*40
			else:
				ed2[x,y]=255
	print counts

	if showPics: cv2.imshow('context image',cimg)

	return [startpts,dreier,vieler]

# colorate the points
def colvieler(vieler,cimg):
	for p in vieler:
		x=p[0]
		y=p[1]
		cv2.circle(cimg,(y,x),4,(255,0,0),-1)

def coldreier(dreier,cimg):
	for p in dreier:
		x=p[0]
		y=p[1]
		cv2.circle(cimg,(y,x),2,(255,0,255),-1)

def colstart(startpts,cimg):
	for p in startpts:
		x=p[0]
		y=p[1]
		cv2.circle(cimg,(y,x),2,(0,255,255),-1)



def runpath(ed,x,y):
	''' find path starting at x,y '''

	path=[(x,y)]
	fin=False

	while not fin:
		fin=True
		for p in [(x+1,y),(x+1,y+1),(x+1,y-1),(x,y+1),(x,y-1),(x-1,y),(x-1,y-1),(x-1,y-1)]:
			if p not in path and ed[p[1]][p[0]]>0:
				ed[p[1]][p[0]]=0
				path.append(p)
				fin=False
				x,y = p[0],p[1]
				break

	return path


def findpathlist(ed,showPics=True):
	''' generate list of pathes '''

	pathlist=[]
	w,l=ed.shape

	for x in range(l):
		for y in range(w):
			if ed[y][x] : 
				path=runpath(ed,x,y)
				if len(path)>4:
					if showPics:
						cv2.imshow('remaining points',ed)
						cv2.waitKey(1)
					Gui.updateGui()
				pathlist.append(path)

	return  pathlist


def xylist(pa):
	''' convert pointlist to coord lists for matplot'''
	x=[]
	y=[]
	for p in pa:
		x.append(p[0])
		y.append(p[1])
	return [x,y]


def part(pa,i):

	points=[FreeCAD.Vector(p[0],p[1],i*10) for p in pa]
	pol=Part.makePolygon(points)
	Part.show(pol)
	t=App.ActiveDocument.ActiveObject
	Gui.updateGui()
	return t

'''
runnign mean
http://stackoverflow.com/questions/13728392/moving-average-or-running-mean

Fortunately, numpy includes a convolve function which we can use to speed things up. 
The running mean is equivalent to convolving x with a vector that is N long, 
with all members equal to 1/N. The numpy implementation of convolve includes 
the starting transient, so you have to remove the first N-1 points:

'''

def runningMeanFast(x, N):
    return np.convolve(x, np.ones((N,))/N)[(N-1):]


class PathFinder():

	def run(self,minPathPoints,showPics):

		try:
			img=self.img
		except:
			sayexc("kein image self.img")
			fn=self.fn
			img = cv2.imread(fn,0)

		edges = cv2.Canny(img,10,255)

		ed2=edges
		ed2 = 0*ed2


		ed= edges >0
		ed = 1* ed


		# classify the points 
		cimg = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
		[startpts,dreier,vieler]=run(ed,cimg,ed2,showPics)
		colvieler(vieler,cimg)
		coldreier(dreier,cimg)
		colstart(startpts,cimg)
		self.imgOut=cimg

		if showPics: cv2.imshow('Canny Edge Detection',ed2)


		pl=findpathlist(ed2,showPics)
		pl2=[]

		# draw a path map 
		mplw=reconstruction.mpl.MatplotlibWidget()

		print ("processed pathes ...")
		for i,pa in enumerate(pl):

			# skip the short pathes
			if len(pa)>minPathPoints:
				[xl,yl]=xylist(pa)
				yl=np.array(yl)
				mplw.plot(xl,-yl)
				print [i,len(pa)]
				pl2.append(pa)

		mplw.show()
		FreeCAD.mplw2=mplw

		sels=0
		for i,pa in enumerate(pl2):
			sels += 1
			t=part(pa,i)

		print (len(pl)," pathes found", sels," pathes selected")

		Gui.SendMsgToActiveView("ViewFit")
		Gui.activeDocument().activeView().viewBottom()
		Gui.SendMsgToActiveView("ViewFit")

		return pl2
