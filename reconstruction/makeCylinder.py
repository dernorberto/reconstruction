# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- reconstruction workbench
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import sympy
from sympy import Point3D,Plane


import FreeCAD,FreeCADGui
App=FreeCAD

Gui=FreeCADGui
import Part

def makeCylinder(p1,p2,p3,p4):
	s=Part.makePolygon([p1,p2,p3,p1])
	f=Part.makeFilledFace(s.Edges)
	n=f.Faces[0].normalAt(0,0)
	# Drehung 
	n2=FreeCAD.Vector(0,0,1)
	r=FreeCAD.Rotation(n,n2)


	k1=r.multVec(p1)
	sp1=sympy.point.Point2D(k1.x,k1.y)
	z=k1.z
	sp1
	k2=r.multVec(p2)
	sp2=sympy.point.Point2D(k2.x,k2.y)
	sp2
	k3=r.multVec(p3)
	sp3=sympy.point.Point2D(k3.x,k3.y)
	sp3

	k4=r.multVec(p4)
	sp4=sympy.point.Point2D(k4.x,k4.y)
	sp4

	t=sympy.Triangle(sp1,sp2,sp3)
	rad=t.circumradius.evalf()
	center=t.circumcenter
	print(rad)
	print(center)
	x=center.x.evalf()
	y=center.y.evalf()

	circ=Part.makeCircle(rad,FreeCAD.Vector(x,y,z))
	Part.show(circ)
	cb=App.ActiveDocument.ActiveObject


	h=k4.z-k3.z

	# und wieder zurueck
	r2=FreeCAD.Rotation(n2,n)

	ex=App.ActiveDocument.addObject("Part::Extrusion","Extrude")
	ex.Base = cb
	ex.Dir = (0,0,h)
	ex.Solid = (True)
	ex.Placement.Rotation=r2
	ex.ViewObject.Transparency=80

	cb.ViewObject.hide()


	s2=Part.makePolygon([p1,p2,p3,p4])
	Part.show(s2)
	for p in [p1,p2,p3,p4]:
		k1=App.ActiveDocument.addObject("Part::Sphere","Sphere")
		k1.Placement.Base=p
		k1.Radius=0.5
		k1.ViewObject.ShapeColor=(1.0,0.0,0.0)
		App.activeDocument().recompute()


def run():
	s=Gui.Selection.getSelectionEx()[0]
	sels=[]
	for s in Gui.Selection.getSelectionEx():
		subs=s.SubObjects
		print(subs)
		sels += subs
	subs=sels
	for ss in subs:
		print(ss)
	if len(subs)!=4:
		raise Exception("keine vier kanten")
	l=[]
	for e in s.SubObjects: 
		if e.__class__.__name__ !='Vertex':
			raise Exception ("Non edge in selection" + str(e))
		print(e.Point)
		l.append(e.Point)
	[p1,p2,p3,p4]=l
	print(s.SubObjects)
	makeCylinder(p1,p2,p3,p4)

# run()
