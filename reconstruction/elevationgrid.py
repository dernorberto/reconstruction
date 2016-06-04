#: utf-8 -*-
#-------------------------------------------------
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

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

hh=10


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


import Points

def text2coordList(datatext):
	x=[]; y=[]; z=[]
	if len(datatext) <> 0:
		lines=datatext.split('\n')
		for zn,l in enumerate(lines):
			words=l.split()
			try:
				[xv,yv,zv]=[float(words[0]),float(words[1]),float(words[2])]
				print xv+yv+zv
				x.append(xv)
				y.append(yv)
				z.append(10*zv)
			except:
				print "Fehler in Zeile ",zn
	x=np.array(x)
	y=np.array(y)
	z=np.array(z)
	x=x-x.min()
	y=y-y.min()

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


x,y,z= text2coordList(datatext)
p= coordLists2points(x,y,z)
# Points.show(p)




def interpolate(x,y,z, gridsize):

##	x=np.array(x)
##	y=np.array(y)
##	z=np.array(z)

	# Set up a regular grid of interpolation points
##	grids=50 # 100  0.93
##	grids=100 # 100  
##	
##	grids=20
	grids=gridsize
	
	xi, yi = np.linspace(0, np.max(x)-np.min(x), grids), np.linspace(0, np.max(y)-np.min(y), grids)

	xi, yi = np.meshgrid(xi, yi)

	# Interpolate rbf
#	rbf = scipy.interpolate.Rbf(x, y, z, function='linear')
#	rbf = scipy.interpolate.Rbf(x, y, z, function='cubic')
	rbf = scipy.interpolate.Rbf(x, y, z, function='thin_plate')
#	rbf = scipy.interpolate.Rbf(x, y, z, function='multiquadradic')
#	rbf = scipy.interpolate.Rbf(x, y, z, function='gaussian')


	# interpolate 2d
 	# rbf = scipy.interpolate.interp2d(x, y, z, kind='cubic')
 	# rbf = scipy.interpolate.interp2d(x, y, z)
	zi = rbf(xi, yi)
	# zi ist grids * grids
	return xi,yi,zi


gridsize=19
xi,yi,zi = interpolate(x,y,z, gridsize)


def showFace(xi,yi,zi,gridsize):

	import Draft
	grids=gridsize

	print zi
	print zi.shape
	print "haha"
	lx,ly=zi.shape
	ws=[]

	for ix in range(lx):
		points=[]
		for iy in range(ly):
			print ix,iy, "huhu"
			points.append(FreeCAD.Vector(0.5*ix,0.5*iy,1*zi[ix,iy]))

		w=Draft.makeWire(points,closed=False,face=False,support=None)
		ws.append(w)
#-		FreeCAD.activeDocument().recompute()
#-		FreeCADGui.updateGui()
#-		Gui.SendMsgToActiveView("ViewFit")

	ll=FreeCAD.activeDocument().addObject('Part::Loft','elevation')
	ll.Sections=ws
	ll.Ruled = True
	ll.ViewObject.ShapeColor = (0.00,0.67,0.00)
	ll.ViewObject.LineColor = (0.00,0.67,0.00)
	for w in ws:
		w.ViewObject.Visibility=False
	# ll.Placement.Base=FreeCAD.Vector(10.0*grids/100,10.0*grids/100,0)


	##lc=Draft.clone(ll)
##	ll.ViewObject.Visibility=False
	ll.Label="Interpolation Gitter " + str(grids)
##y	lc.Scale=(0.95,0.95,1.0)
#n	lc.Scale=(0.92,0.92,1.0)

	FreeCAD.activeDocument().recompute()
	FreeCADGui.updateGui()
	Gui.SendMsgToActiveView("ViewFit")


showFace(xi,yi,zi,gridsize)

Points.show(p)
pob=App.ActiveDocument.ActiveObject
pob.ViewObject.PointSize = 10.00



def showHeightMap(x,y,z,zi):
	''' show height map in maptplotlib '''
	plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
			   extent=[x.min(), x.max(), y.min(), y.max()])
	plt.scatter(x, y, c=z)
	plt.colorbar()
	plt.show()


showHeightMap(x,y,z,zi)
