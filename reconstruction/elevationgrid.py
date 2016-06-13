#: utf-8 -*-
# ------------------------------------------
#-- reconstruction workbench
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

#
# interpolate point cloud to a quad mesh face
#



# http://forum.freecadweb.org/viewtopic.php?f=13&t=15988
#
#
#

import FreeCAD, Draft
import FreeCADGui
Gui=FreeCADGui
App=FreeCAD


import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
import Points


# test data
datatext='''1 1 1
1 2 1
1 3 1
1 4 1
1 5 1
1 6 1
1 7 1
1 8 1
1 9 1
1 10 1
2 1 1
2 2 1
2 3 1.2
2 4 1.2
2 5 1.2
2 6 1
2 7 1
2 8 1
2 9 1
2 10 1
3 1 1
3 2 1
3 3 1.2
3 4 1.3
3 5 1.2
3 6 1
3 7 1
3 8 1
3 9 1
3 10 1
4 1 1
4 2 1
4 3 1.2
4 4 1.2
4 5 1.2
4 6 1
4 7 1
4 8 1
4 9 1
4 10 1
5 1 1
5 2 1
5 3 1
5 4 1
5 5 1
5 6 1
5 7 1
5 8 1
5 9 1
5 10 1
6 1 1
6 2 0.9
6 3 0.9
6 4 0.9
6 5 1
6 6 1
6 7 1
6 8 1
6 9 1
6 10 1
7 1 1
7 2 0.9
7 3 0.8
7 4 0.9
7 5 1
7 6 1
7 7 1
7 8 1
7 9 1
7 10 1
8 1 1
8 2 0.9
8 3 0.9
8 4 0.9
8 5 1
8 6 1
8 7 1
8 8 1
8 9 1
8 10 1
9 1 1
9 2 1
9 3 1
9 4 1
9 5 1
9 6 1
9 7 1
9 8 1
9 9 1
9 10 1
10 1 1
10 2 1
10 3 1
10 4 1
10 5 1
10 6 1
10 7 1
10 8 1
10 9 1
10 10 1
'''



def text2coordList(datatext):
	x=[]; y=[]; z=[]
	if len(datatext) <> 0:
		lines=datatext.split('\n')
		for zn,l in enumerate(lines):
			words=l.split()
			try:
				[xv,yv,zv]=[float(words[0]),float(words[1]),float(words[2])]
#				print xv+yv+zv
				x.append(xv)
				y.append(yv)
				z.append(10*zv)
			except:
				print "Fehler in Zeile ",zn

	x=np.array(x)
	y=np.array(y)
	z=np.array(z)
	#x=x-x.min()
	#y=y-y.min()

	return (x,y,z)
# x,y,z= text2coordList(datatext)



def points2coordList(points):
	''' convert Pointsobject to numpy 1D-arrays of coordinates  '''
	x=np.array([ p[0] for p in points])
	y=np.array([ p[1] for p in points])
	z=np.array([ p[2] for p in points])
	return x,y,z
#  x,y,z= points2coordList(p.Points)



def coordLists2points(x,y,z):
	''' convert coordinate lists to Points  '''
	p=Points.Points()
	pts=[]
	try:
		# simple list
		n=len(x)
	except:
		# numpy
		n=x.shape(0)

	for i in range(n):
		pts.append(FreeCAD.Vector(y[i],x[i],z[i]))

	p.addPoints(pts)
	return p
#   p= coordLists2points(x,y,z)





def interpolate(x,y,z, gridsize,mode='thin_plate',rbfmode=True,shape=None):

	grids=gridsize

	dx=np.max(x)-np.min(x)
	dy=np.max(y)-np.min(y)

	if dx>dy:
		gridx=grids
		gridy=int(round(dy/dx*grids))
	else:
		gridy=grids
		gridx=int(round(dx/dy*grids))

	if shape<>None:
		(gridy,gridx)=shape

	xi, yi = np.linspace(np.min(x), np.max(x), gridx), np.linspace(np.min(y), np.max(y), gridy)
	xi, yi = np.meshgrid(xi, yi)

	if rbfmode:
		rbf = scipy.interpolate.Rbf(x, y, z, function=mode)
		rbf2 = scipy.interpolate.Rbf( y,x, z, function=mode)
	else:
		print "interp2d nicht implementiert"
		rbf = scipy.interpolate.interp2d(x, y, z, kind=mode)

	zi=rbf2(yi,xi)
	return [rbf,xi,yi,zi]




def showFace(rbf,rbf2,x,y,gridsize,shapeColor):

	import Draft
	grids=gridsize

	ws=[]


	xi, yi = np.linspace(np.min(x), np.max(x), grids), np.linspace(np.min(y), np.max(y), grids)

	for ix in xi:
		points=[]
		for iy in yi:
#			print (ix,iy, rbf(ix,iy))
			iz=float(rbf(ix,iy))
#			if rbf2<>None:
#				iz -= float(rbf2(ix,iy))

			points.append(FreeCAD.Vector(iy,ix,iz))
		w=Draft.makeWire(points,closed=False,face=False,support=None)
		ws.append(w)
#-		FreeCAD.activeDocument().recompute()
#-		FreeCADGui.updateGui()
#-		Gui.SendMsgToActiveView("ViewFit")

	ll=FreeCAD.activeDocument().addObject('Part::Loft','elevation')
	ll.Sections=ws
	ll.Ruled = True
	ll.ViewObject.ShapeColor = shapeColor
	ll.ViewObject.LineColor = (0.00,0.67,0.00)

	for w in ws:
		w.ViewObject.Visibility=False

	ll.Label="Interpolation Gitter " + str(grids)




def showHeightMap(x,y,z,zi):
	''' show height map in maptplotlib '''
	zi=zi.transpose()

	plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
			   extent=[ y.min(), y.max(),x.min(), x.max()])

	plt.colorbar()

	CS = plt.contour(zi,15,linewidths=0.5,colors='k',
			   extent=[ y.min(), y.max(),x.min(), x.max()])
	CS = plt.contourf(zi,15,cmap=plt.cm.rainbow, 
			   extent=[ y.min(), y.max(),x.min(), x.max()])

	z=z.transpose()
	plt.scatter(y, x, c=z)

	# achsen umkehren
	#plt.gca().invert_xaxis()
	#plt.gca().invert_yaxis()

	plt.show()
	return









def createElevationGrid(mode,rbfmode=True,source=None,gridCount=20):
	
	modeColor={
	'linear' : ( 1.0, 0.3, 0.0),
	'thin_plate' : (0.0, 1.0, 0.0),
	'cubic' : (0.0, 1.0, 1.0),
	'inverse' : (1.0, 1.0, 0.0),
	'multiquadric' : (1.0, .0, 1.0),
	'gaussian' : (1.0, 1.0, 1.0),
	'quintic' :(0.5,1.0, 0.0)
	}

	if source<>None:

		if hasattr(source,"Shape"):
			# part object
			pts=[v.Point for v in  source.Shape.Vertexes]

			p=Points.Points(pts)
			Points.show(p)
			pob=App.ActiveDocument.ActiveObject
			pob.ViewObject.PointSize = 10.00
			pob.ViewObject.ShapeColor=(1.0,0.0,0.0)

		elif hasattr(source,"Points"):
			# point cloud
			pts=source.Points.Points
		else:
			raise Exception("don't know to get points")

		x=[v[1] for v in pts]
		y=[v[0] for v in pts]
		z=[v[2] for v in pts]

	else:
		# testdata
		x,y,z= text2coordList(datatext)
		p= coordLists2points(x,y,z)

	x=np.array(x)
	y=np.array(y)
	z=np.array(z)

	gridsize=gridCount

	rbf,xi,yi,zi1 = interpolate(x,y,z, gridsize,mode,rbfmode)
	
	# hilfsebene
	xe=[100,-100,100,-100]
	ye=[100,100,-100,-100]
	ze=[20,10,20,5]

	rbf2,xi2,yi2,zi2 = interpolate(xe,ye,ze, gridsize,mode,rbfmode,zi1.shape)
	
	#print zi1.shape
	#print zi2.shape
	
	#zi=zi1-zi2
	zi=zi1

	try: color=modeColor[mode]
	except: color=(1.0,0.0,0.0)

	xmin=np.min(x)
	ymin=np.min(y)

	showFace(rbf,rbf2,x,y,gridsize,color)
	
	showHeightMap(x,y,z,zi)

	# interpolation for image
	gridsize=400
	rbf,xi,yi,zi = interpolate(x,y,z, gridsize,mode,rbfmode)
	rbf2,xi2,yi2,zi2 = interpolate(xe,ye,ze, gridsize,mode,rbfmode,zi.shape)
	return [rbf,rbf2,x,y,z,zi,zi2]


if __name__ == '__main__':

	createElevationGrid('thin_plate')
	createElevationGrid('linear')
	createElevationGrid('inverse')
	createElevationGrid('multiquadric')
	createElevationGrid('gaussian')
	App.activeDocument().recompute()

# radial basis function interpolator instance
# http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.Rbf.html




