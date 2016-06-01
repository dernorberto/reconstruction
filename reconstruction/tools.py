#
#  tools for reconstruction
#


import say
reload(say)
from say import *


import cv2

import reconstruction 
import reconstruction.dbscan
import reconstruction.smooth
reload(reconstruction.smooth)

import geodat
reload (geodat.projectiontools)
from geodat.projectiontools import *


def fcline(x1,y1,x2,y2,scaler=1000):
	''' create a Part shape line for 4 coords '''
	v=FreeCAD.Vector(float(x1)*scaler,float(y1)*scaler,0)
	v2=FreeCAD.Vector(float(x2)*scaler,float(y2)*scaler,0)
	l=Part.makeLine(v,v2)
	return l


def analyzeLines(lines):
	''' analyze direction and quality of lines given from houghlines as 4 tupel of coords '''

	arcs={}
	arclines={}
	for l in lines:
		[[x1,y1,x2,y2]] = l
		arc=np.arctan2(x1-x2,y1-y2)
		if arc < 0: arc += np.pi

		# normalize arc
		arc /= np.pi

		# length of the line as measure for quality: long lines are good lines
		lens=np.sqrt((x1-x2)**2+(y1-y2)**2)

		if 0: # length independent weight
			try: arcs[arc] += 1.0 
			except: arcs[arc] = 1.0
		else:
			try: arcs[arc] += lens
			except: arcs[arc] = lens

		# collect the lines
		try: arclines[arc].append(l)
		except: arclines[arc]=[l]

	# create ordered lists index k, weights ss
	ks=arcs.keys()
	ks.sort()
	ks=np.array(ks)
	ss=[arcs[k] for k in ks]
	ss=np.array(ss)

	return ks,ss,arcs,arclines




def showDirections(ks,ss,arcs,arclines,dw=2):
	''' display direction of the lines in a normalized diagramm'''

	# windows=['hamming', 'bartlett', 'blackman']
	w='hamming'
	wh=2

	# direction raw
	plt.plot(180*ks, 1.0*ss/np.max(ss))

	# directions smoothed
	ss=reconstruction.smooth.smooth(ss,8,w)
	ss2=ss[:ks.shape[0]]
	plt.plot(180*ks,1+ss[:ks.shape[0]]/np.max(ss))

	# gradient of the direction
	ss2grad=np.gradient(ss2)
	plt.plot(180*ks,wh+2+ss2grad/np.abs(np.max(ss2grad)))

	# 2nd derivative
	ss3grad=np.gradient(ss2grad)
	plt.plot(180*ks,wh+4+ss3grad/np.abs(np.max(ss3grad)))

	# a useful combination too
	plt.plot(180*ks,wh+6+0.25*(ss2grad/np.max(ss2grad)+ 3* ss3grad/np.max(ss3grad)))

	plt.grid(True)
	plt.show()

	# group lines to directions
	alllines=[]
	for i in range(ss2grad.shape[0]-1):
		vi=ss2grad[i]
		# look for arcs with relative maximum
		if ss2grad[i]>ss2grad[i-1] and ss2grad[i+1]<vi:
			print (round(ks[i],2),vi,i,'#')
			print arclines[ks[i]]
			lines=[]
			lines.append(arclines[ks[i]])
			# use neighbors arcs too
			df=True
			uf=True
			for d in range(dw):
				try:
					if ss2grad[i-d]>ss2grad[i-d-1] and df:
						lines.append(arclines[ks[i-d-1]])
					else:
						df=False
					if ss2grad[i+d]>ss2grad[i+d+1] and uf:
						lines.append(arclines[ks[i+d+1]])
					else:
						uf=False
				except:
					sayexc()
			alllines.append(lines)

	alllines=np.array(alllines)
	return alllines





def drawFC(alllines):
	''' visualize lines in FreeCAD 3D window '''

	allLines2=[]

	# draw the lines
	for lines in alllines:
		nplines=[]
		for ll in lines:
			for l in ll:
				print l
				[[x1,y1,x2,y2]] = l
				points=[FreeCAD.Vector(x1,-y1,0),FreeCAD.Vector(x2,-y2,0)]
				p1,p2 =np.array([x1,-y1]), np.array([x2,-y2])
				nplines.append([p1,p2])
				Draft.makeWire(points,closed=False,face=True,support=None)
		nplines=np.array(nplines)
		allLines2.append(nplines)

	allLines2=np.array(allLines2)

	# find the intersections of maybe parallel lines as vansishing point candidates 
	# and draw them as circle markers
	circles=[]
	for c in range(allLines2.shape[0]):
		nplines1=allLines2[c-1]
		nplines2=allLines2[c]

		for c1 in range(nplines1.shape[0]):
			l1=nplines1[c1]
			# random coloring
			c=(random.random(),random.random(),random.random())
			for c2 in range(nplines2.shape[0]):
					l2=nplines2[c2]
					try:
						s=schnittpunkt(l1[0],l1[1],l2[0],l2[1])
						pl=FreeCAD.Placement()
						circles.append(s)
						pl.Base=FreeCAD.Vector(s[0],s[1],0.0)
						Draft.makeCircle(radius=12,placement=pl,face=True,support=None)
						App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=c
						FreeCAD.ActiveDocument.recompute()
						Gui.updateGui()
					except:
						pass

	return circles


def drawErosion(circles):
	''' reduce the dataset of intersection points '''

	x=[]
	y=[]
	for c in circles:
		x.append(int(round(c[0])))
		y.append(int(round(c[1])))
	x=np.array(x)
	y=np.array(y)

	f=20
	bbox=[int(round(np.min(x)/f)),int(round(np.min(y)/f)),int(round(np.max(x)/f)),int(round(np.max(y)/f))]
	h=int(round(bbox[3]-bbox[1]))
	w=int(round(bbox[2]-bbox[0]))

	img = np.zeros((2*h,2*w,3), np.uint8)

	for c in circles:
		# draw the outer circle
		u,v=int(round(c[0]/f))-bbox[0],bbox[3]-int(round(c[1]/f))
		q=cv2.circle(img,(100+u,100+v),3,(0,255,0),3)

	kernel = np.ones((3,3),np.uint8)
	erosion = cv2.erode(img,kernel,iterations = 4)
	result=erosion

	#opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
	#result=opening

	yy=cv2.circle(img,(1500,500),50,(0,0,255),3)
	yy=cv2.imshow("erosion ",result)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()


	circles2=[]
	for ix in range(result.shape[0]):
		for iy in range(result.shape[1]):
			if max(erosion[ix][iy])> 0:
				circles2.append([iy,-ix])

	return circles2



def mkline(l):
	''' create a FreeCAD line from 4 coords '''

	s="line"
	for co in l: s += '_' + str(co)

	shapeobj=App.ActiveDocument.getObject(s)

	if shapeobj == None:
		myshape = Part.makeLine(FreeCAD.Vector(l[0],l[1],0.0),FreeCAD.Vector(l[2],l[3],0.0))
		doc=App.ActiveDocument
		shapeobj = doc.addObject("Part::Feature",s)
		shapeobj.Shape = myshape
		doc.recompute()

	return shapeobj



def createLines(lines,dirs):
	''' create FreeCAD lines for a list of 4-coords '''
	
	# create arc-index of lines
	arc2lines={}

	grp=App.ActiveDocument.addObject("App::DocumentObjectGroup","auxHoughlines")

	for c in range(len(lines)):
		[l] = lines[c] 
		arc=dirs[c]
		try: arc2lines[arc].append(l)
		except: arc2lines[arc]=[l]
		print (c,l,arc)

	# create lines with same direction in same color
	for arc in arc2lines:
		c=(random.random(),random.random(),random.random())
		for l in arc2lines[arc]:
			ll=mkline(l)
			ll.ViewObject.LineColor=c
			grp.addObject(ll)

	return arc2lines



# runme
def create_clusters(arc2lines,a,b,vobj):
	''' create clusters  '''

	ploton=False
	ploton=True
	dirs=arc2lines.keys()

	[xh,y]=np.histogram(dirs,180)
	zh=np.arange(180)


	if ploton:
		fig = vobj.mpl.figure
		fig.clf()

		ax=vobj.mpl.figure.add_subplot(111)
		
		ax.spines['top'].set_visible(False)
		ax.spines['right'].set_visible(False)
		ax.spines['bottom'].set_visible(False)
		ax.spines['left'].set_visible(False)

		ax.grid(True)
		ax.set_yticklabels([])
		
		# draw the histogram
		ax.plot(zh,1.0*xh/np.max(xh)*10)
		vobj.mpl.draw()

	d2=[]
	for d in dirs:
		d2.append([d,0])

	clusters = reconstruction.dbscan.dbscan(d2, a, b, debug=True)

	cn=0; mx=[]; my=[]
	nn=15

	counter=0
	for cluster, members in clusters.iteritems(): counter += 1

	colors=[]
	n=counter
	#color=iter(cm.rainbow(np.linspace(0,1,n)))
	#color=iter(cm.prism(np.linspace(0,1,n)))
	color=iter(cm.hsv(np.linspace(0,1,n)))
	#color=iter(cm.hsv(np.linspace(0,1,180)))

	for i in range(n):
		c=next(color)
		colors.append((c[0],c[1],c[2]))

	count=0

	for cluster, members in clusters.iteritems():
		print '--------Cluster {0}---member count--{1}----'.format(cluster,len(members))
		x=[]; y=[]; lc=[]
		members.sort()

		for c in members:
			x.append(c[0])
			y.append(c[1])
			lc.append(len(arc2lines[c[0]]))

		if len(members) <0 or cluster== -1:
				coo='y'
				n1=nn
		else:
				n1=nn+5
				cn +=1

				# center of the cluster
				xm=np.mean(np.array(x))
				ym=np.mean(np.array(y))
				mx.append(xm)
				my.append(ym+n1+13)

		y=np.array(y); x=np.array(x); lc=np.array(lc)

		lc2=[]
		for l in lc:
			if l>10: l=11
			lc2.append(l)
		lc2=np.array(lc2)

		mcolor=colors[count]
		#print("xm",xm)
		#mcolor=colors[int(round(xm))]

		if ploton: 
			if cluster== -1:
				pp=ax.plot(x,y+n1,'oy')
				pp=ax.plot(x,lc2+n1-1,'-y')
			else:
				pp=ax.plot(x,y+n1,'o', c=mcolor)
				pp=ax.plot(x,lc2+n1+1,'-', c=mcolor)
				count += 1

	if ploton: 
		mx=np.array(mx)
		ax.plot(mx,my,"sr")
		vobj.mpl.draw()

	count=0
	for cluster, members in clusters.iteritems():
		print '--------Cluster {0}---member count--{1}----'.format(cluster,len(members))
		c=colors[count]
		if cluster == -1:
			c=(1.0,1.0,1.0)
		for m in members:
			arc=m[0]
			for l in arc2lines[arc]:
				ll=mkline(l)
				ll.ViewObject.LineColor=c
		count += 1

	return clusters

def resize(img,y,x):
	''' resize a cv2 image '''

	yi,xi= img.shape[0],img.shape[1]

	if 1.0*x/xi > 1.0*y/yi:
		img2=cv2.resize(img,(xi*y/yi,y),interpolation = cv2.INTER_CUBIC)
	else:
		img2=cv2.resize(img,(x,yi*x/xi),interpolation = cv2.INTER_CUBIC)
	return img2



def run_HoughLinesPost(obj,vobj):
	t2=App.ActiveDocument.My_HoughLines
	lines=t2.Proxy.lines
	dirs=t2.Proxy.directions
	arc2lines=createLines(lines,dirs)
	clusters=create_clusters(arc2lines,0.1*obj.epsilon,0.1*obj.count,vobj)
