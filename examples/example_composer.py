


import reconstruction.pointcloud_composer
reload(reconstruction.pointcloud_composer)

import numpy as np
# area of interest
extend=(-20,20,-20,20)

# example data garden
ele=App.ActiveDocument.My_ElevationGrid
x,y,z=ele.Proxy.x,ele.Proxy.y,ele.Proxy.z
gridGarden=reconstruction.pointcloud_composer.getGriddata(x,y,z,extend)

# example plane
xa=np.array([-10,10,10,-10])
ya=np.array([-10,-10,10,10])
za=np.array([0,0,4,4])
gridPlane=reconstruction.pointcloud_composer.getGriddata(xa,ya,za,extend)


garden,tt=reconstruction.pointcloud_composer.transformPointCloud2(gridGarden,"Grid of my Garden",extend)
plane,tt=reconstruction.pointcloud_composer.transformPointCloud2(gridPlane,"Grid of a Plane",extend)




import reconstruction.pointcloud_composer
reload(reconstruction.pointcloud_composer)

# create composer
reconstruction.pointcloud_composer._createComposer()
composer=App.ActiveDocument.ActiveObject
composer.Label
composer.pointcloudA=garden
composer.pointcloudB=plane

# apply the formula
composer.expressionFormula="A-0.5*B"
App.activeDocument().recompute()

