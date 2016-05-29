# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- reconstruction workbench
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

from say import *


def computeDirection(p,N,x,y):
	''' mean direction of  N points at position p in  datalistes x,y'''

	dirl=[]
	for i in range(N):
		dx=x[p-N+i]-x[p+i]
		dy=y[p-N+i]-y[p+i]
		dir=np.arctan2(dy,dx)
		dirl.append(dir)

	# approximation by a line
	[krumm,richtung] = np.polyfit(range(N), dirl, 1)
	pp = np.poly1d([krumm,richtung])

	# quality of the approx
	err=np.sum(np.abs(pp(np.arange(N))-np.array(dirl)))/N

	# direction in intervall [0, 2*pi]
	if richtung<0: richtung += 2*np.pi

	# restrict piks for diagram display
	if abs(krumm) >0.1: krumm=0.1

	return(err,richtung,krumm)


def splitpath(mplw,N,x,y,tresh=0.004,plotit=False):
	''' split a path into intervals on strong changes of the direction and generate a plot of the data'''

	iv0=range(len(x))
	iv=range(N,len(x)-N)
	s=[0]*N; s2=[0]*N

	intervals=[0]
	krummon=False
	dirs=[]; errs=[]; krumms=[]

	for i in iv: # len(x)
		z=computeDirection(i,N,x,y)
		dirs.append(z[1])
		errs.append(z[0])
		krumm=z[2]
		krumms.append(krumm)
		# print ("krumm ",krumm, "thresh", tresh)
		if krumm <= tresh and krummon:
			krummon=False
			intervals.append((i))
			#print ("intervalpunkt ",i,x[i],y[i])
		if krumm >= tresh and not krummon:
			krummon=True
			intervals.append((i))
			#print ("intervalpunkt ",i,x[i],y[i])
	intervals.append(len(x)-N)

	krumms=np.array(s+krumms+s2)
	h=np.mean(np.abs(krumms))
	# print ("mean of abs curvature:",h)

	if plotit:
		krumms=krumms*100

		mplw.plot(iv0,s+dirs+s2,'b',label="direction")
		mplw.plot(iv0,s+errs+s2,'g',label="dir change")

		err=np.array(s+errs+s2)
		err2=err >tresh

		mplw.plot(iv0,err2,'r',label="critical")
		mplw.plot(iv0,krumms,'m',label="curvature")

	return intervals,dirs


def showIntervals(mplw,N,intervals,dirs,x,y,createFC,obj=None):
	''' draw the intervals in the plot widget'''

	if obj <> None:
		hideApprox=obj.hideApproximation
		hideLegend=obj.hideLegend
		maxRadius=obj.maxRadius
	else:
		hideApprox=False
		hideLegend=True
		maxRadius=200


#	print ("intervals ",len(intervals),intervals)
	for l in range(len(intervals)-1):

		# intervals must be long enough
		if intervals[l] +N < intervals[1+l]:
			dd=dirs[intervals[l]:intervals[1+l]]
			ra=range(intervals[l],intervals[l]+len(dd))

			# plot the raw data
			if not hideApprox:
				mplw.plot(ra,dd,'o',label= str(l) + '. dirset')
			else:
				mplw.plot(ra,dd,'x')

			if ra[N:-N-N] <>[]:
				z = np.polyfit(ra[N:-N-N],dd[N:-N-N], 1)
				z = np.polyfit(ra[N+3:-N-N+3],dd[N+3:-N-N+3], 1)
				arc1=np.pi+z[1]
				arc=round(270.0-z[1]/np.pi*180,1)
				len1=intervals[1+l]-intervals[l]
				if l==0: len1 -= N
				if l == len(intervals) - 2: len1 +=N
				if l==0:
					mx=np.average(x[0:intervals[1+l]])
					my=np.average(y[0:intervals[1+l]])
				else:
					mx=np.average(x[intervals[l]-N:intervals[1+l]])
					my=np.average(y[intervals[l]-N:intervals[1+l]])
				
				# print ("center of the intevall ",mx,my)
				
				bending=round(1000*z[0],1)

				# curvature threshold for switch between straight line and cirle
				if abs(bending) >0.2:
					radius=round(1000.0/bending)
				else:
					radius=0

				print
				print ("loop",l,"startpoint",intervals[l],"endpoint",intervals[1+l],"point count:",len1)
				print ("curvature ",bending,"direction:",arc,"radius ", radius)

				x1=x[intervals[l]-N]; x2=x[intervals[1+l]]
				y1=y[intervals[l]-N]; y2=y[intervals[1+l]]
				if l==0: 
					x1=x[0]; y1=y[0]

				# length of the line
				d=np.sqrt((x1-x2)**2+(y1-y2)**2)


				# interpret large circles as lines
				if abs(radius)>maxRadius or radius==0:

					#direction of the line
					if l<>0 and abs(arc)>2:
						zd = np.polyfit(x[intervals[l]-N//2:intervals[1+l]+N//2],y[intervals[l]-N//2:intervals[1+l]+N//2], 1)
						zd = np.polyfit(x[intervals[l]:intervals[1+l]],y[intervals[l]:intervals[1+l]], 1)
						m=zd[0]
						am=np.arctan2(m,1)
					elif abs(arc)<2:
						m=0
						am=np.pi/2
					else:
						zd = np.polyfit(x[0:intervals[1+l]-N],y[0:intervals[1+l]-N], 1)
						# zd = np.polyfit(x[0:intervals[1+l]+N],y[N:intervals[1+l]+N], 1)
						m=zd[0]
						am=np.arctan2(m,1)

					# print ("m ",m, "am",am)

					# create the FreeCAD line objects
					if createFC:
						points=[FreeCAD.Vector(mx-0.5*d*np.cos(am),my-0.5*d*np.sin(am),0),FreeCAD.Vector(mx+0.5*d*np.cos(am),my+0.5*d*np.sin(am),0)]
						print "create Line"
						print points
						Draft.makeWire(points,closed=False,face=True,support=None)
						App.ActiveDocument.ActiveObject.ViewObject.LineWidth=7.0
						App.ActiveDocument.ActiveObject.ViewObject.LineColor=(.0,0.0,1.0)

				else:
					# circles
					if l==0:
						kx=x[0:intervals[1+l]+N//2]
						ky=y[0:intervals[1+l]+N//2]
					else:
						kx=x[intervals[l]-N//2:intervals[1+l]+N//2]
						ky=y[intervals[l]-N//2:intervals[1+l]+N//2]

					# create FreeCAD arcs #+# still dummy hack -> todo
					if createFC:
						pl=[FreeCAD.Vector(kx[i],ky[i],1) for i in range(len(kx))]
						pol=Part.makePolygon(pl)
						Part.show(pol)
						App.ActiveDocument.ActiveObject.ViewObject.LineWidth=7.0
						App.ActiveDocument.ActiveObject.ViewObject.LineColor=(.0,1.0,1.0)


				if 0: # for debugging the scanned data as line

					dy=y2-y1
					dx=x2-x1
					dir2=np.arctan2(dy,dx)
					dir2=90.0- dir2*180/np.pi
					
					print("l",l,"coord", x1,y1,x2,y2,"dist points ",d, " dir2:",round(dir2,1))
					
					x1=x[intervals[l]-N//2]
					x2=x[intervals[1+l]+N//2]
					y1=y[intervals[l]-N//2]
					y2=y[intervals[1+l]+N//2]
					if l==0:
						x1=x[0+N//2]
						y1=y[0+N//2]

					points=[FreeCAD.Vector(x1,y1,0),FreeCAD.Vector(x2,y2,0)]
					Draft.makeWire(points,closed=False,face=True,support=None)
					App.ActiveDocument.ActiveObject.ViewObject.LineWidth=5.0
					App.ActiveDocument.ActiveObject.ViewObject.LineColor=(1.0,0.0,0.0)


				# plot mean value direction
				pp = np.poly1d(z)
				ya=pp(ra)
				if not hideApprox:
					lab = str(l) + '. '
					if radius == 0: lab +="line"
					else: lab +="arc r=" + str(round(radius,1))

					mplw.plot(ra,ya,"s",label=lab)

	if not hideLegend: mplw.axes.legend()

	mplw.draw()
	mplw.show()


def run(pl2,nr,N,threshold,mplw=None,createFC=False,obj=None):
	''' run on a number '''

	# create the dialog widget
	if mplw==None:
		mplw=reconstruction.mpl.MatplotlibWidget()

	# clear the diagnose window
	mplw.clf()
	mplw.subplot()

	# prepare data rows for x,y
	path=pl2[nr]
	x=[p[0] for p in path]
	y=[p[1] for p in path]

	#  calculate the segments of the path
	intervals,dirs=splitpath(mplw,N,x,y,0.001*threshold,True)

	# display the segments im the widget
	showIntervals(mplw,N,intervals,dirs,x,y,createFC,obj)

	return mplw



def runobj(obj,N=4,tresh=0.1,mplw=None,createFC=False,obj2=None):
	''' run on an obect obj '''

	if mplw==None:
		mplw=reconstruction.mpl.MatplotlibWidget()
	
	mplw.clf()
	mplw.subplot()

	p=obj
	x=[v.Point.x for v in p.Shape.Vertexes]
	y=[v.Point.y for v in p.Shape.Vertexes]

	intervals,dirs=splitpath(mplw,N,x,y,0.001*tresh,True)
	showIntervals(mplw,N,intervals,dirs,x,y,createFC,obj2)

	return mplw


def runsel(N=4,tresh=0.1,mplw=None,createFC=False,obj=None):
	''' run a selected 3D path/wire '''

	sels=Gui.Selection.getSelection()
	if sels == []:
		sayexc("You have to select at least one path/wire/thread")
		return

	if mplw==None:
		mplw=reconstruction.mpl.MatplotlibWidget()

	mplw.clf()
	mplw.subplot()


	for p in sels:
		# calculate the segments of the path
		x=[v.Point.x for v in p.Shape.Vertexes]
		y=[v.Point.y for v in p.Shape.Vertexes]

		intervals,dirs=splitpath(mplw,N,x,y,0.001*tresh,True)
		showIntervals(mplw,N,intervals,dirs,x,y,createFC,obj)

	# restore the starting selection
	Gui.Selection.clearSelection()
	for p in sels:
		Gui.Selection.addSelection(p)

	return mplw
