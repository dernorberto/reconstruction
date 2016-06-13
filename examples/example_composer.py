
from reconstruction.say import *


import reconstruction.pointcloud_composer
reload(reconstruction.pointcloud_composer)

import numpy as np
# area of interest

def run():

	a=-5
	b=-5
	d=20
	c=50
	extend=(a,c,b,d)

	try:
		# example data garden
		ele=App.ActiveDocument.My_ElevationGrid

		x,y,z=ele.Proxy.x,ele.Proxy.y,ele.Proxy.z
		x = np.array(x) +a-b
		y = np.array(y) -a+b
		gridGarden=reconstruction.pointcloud_composer.getGriddata(x,y,z,extend)
		say("griddata shape")
		say(gridGarden.shape)

		# example plane
		xa=np.array([-10,20,20,-10])+a-b
		ya=np.array([-10,-10,0,5])-a+b
		za=np.array([0,0,4,4])
		gridPlane=reconstruction.pointcloud_composer.getGriddata(xa,ya,za,extend)

		say("griddata Plan shape")
		say(gridPlane.shape)

		garden,tt=reconstruction.pointcloud_composer.transformPointCloud2(gridGarden,"Grid of my Garden",extend)
		plane,tt=reconstruction.pointcloud_composer.transformPointCloud2(gridPlane,"Grid of a Plane",extend)


		# create composer
		reconstruction.pointcloud_composer._createComposer()
		composer=App.ActiveDocument.ActiveObject
		composer.Label
		composer.pointcloudA=garden
		composer.pointcloudB=plane
		composer.minBoundBox=FreeCAD.Vector(a,b,100)
		composer.maxBoundBox=FreeCAD.Vector(c,d,100)

		# apply the formula
		composer.expressionFormula="A+B"
		App.activeDocument().recompute()
		composer.Proxy.run()


	except:
		sayexc()
		errorDialog("To run this example first initiate data with example_elevationgrid.py")


#import cProfile
#cProfile.run('run()')

run()
