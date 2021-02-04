# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- reconstruction workbench
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
'''
select n points for the bottom face in right order
select point n+1 for the extrusion height
'''


import sympy
from sympy import Point3D,Plane


import FreeCAD,FreeCADGui
App=FreeCAD

Gui=FreeCADGui
import Part

def makePrism(l):
	print(l)
	hp=l[-1]
	p1=l[0]
	bl=l[:-1]
	bl.append(p1)
	print(bl)
	
	s=Part.makePolygon(bl)
	f=Part.makeFilledFace(s.Edges)
	Part.show(f)
	cb=App.ActiveDocument.ActiveObject
	cb.Label="Prism Bottom Face"
	cb.ViewObject.hide()

	n=f.Faces[0].normalAt(0,0)
	n2=FreeCAD.Vector(0,0,1)
	r=FreeCAD.Rotation(n,n2)


	k1=r.multVec(p1)
	sp1=sympy.point.Point2D(k1.x,k1.y)
	z=k1.z
	sp1


	k4=r.multVec(hp)
	sp4=sympy.point.Point2D(k4.x,k4.y)
	sp4

	bl2=[]
	for p in bl:
		k=r.multVec(p)
		bl2.append(k)

	s=Part.makePolygon(bl2)
	f=Part.makeFilledFace(s.Edges)
	Part.show(f)
	cb=App.ActiveDocument.ActiveObject
	cb.Label="Prism Bottom Face Helper"
	cb.ViewObject.hide()

	h=k4.z-k1.z

	# und wieder zurueck
	r2=FreeCAD.Rotation(n2,n)

	ex=App.ActiveDocument.addObject("Part::Extrusion","Extrude")
	ex.Base = cb
	ex.Dir = (0,0,h)
	ex.Solid = (True)
	ex.Placement.Rotation=r2
	ex.ViewObject.Transparency=80
	ex.Label="Prism"
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
	if len(subs)<4:
		raise Exception("less than 4 points")
	l=[]
	for e in s.SubObjects: 
		if e.__class__.__name__ !='Vertex':
			raise Exception ("Non edge in selection" + str(e))
		print(e.Point)
		l.append(e.Point)
	print(s.SubObjects)
	makePrism(l)

# run()
