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

def seq(v):
	return (v.x,v.y,v.z)


def makeSphere(p1,p2,p3,p4):

	sp1=Point3D(seq(p1))
	sp2=Point3D(seq(p2))
	sp3=Point3D(seq(p3))
	sp4=Point3D(seq(p4))

	# helper planes 
	e12=Plane((sp1+sp2)/2,sp2-sp1)
	e23=Plane((sp2+sp3)/2,sp3-sp2)
	e14=Plane((sp1+sp4)/2,sp4-sp1)

	# intersect to find the circumcenter
	its=e12.intersection(e23)
	l=its[0]
	r=sympy.Ray3D(l)

	ins=sympy.intersection(e14,r)

	m=ins[0]

	# check the radius
	r1=m.distance(sp1)
	r1
	m.distance(sp2)
	m.distance(sp3)

	r1.evalf()


	# visualize

	k1=App.ActiveDocument.addObject("Part::Sphere","Sphere")
	k1.Placement.Base=p1
	k1.Radius=0.2
	k1.ViewObject.ShapeColor=(1.0,0.0,0.0)
	k2=App.ActiveDocument.addObject("Part::Sphere","Sphere")
	k2.Placement.Base=p2
	k2.Radius=0.2
	k2.ViewObject.ShapeColor=(1.0,0.0,0.0)
	k3=App.ActiveDocument.addObject("Part::Sphere","Sphere")
	k3.Placement.Base=p3
	k3.Radius=0.2
	k3.ViewObject.ShapeColor=(1.0,0.0,0.0)
	k4=App.ActiveDocument.addObject("Part::Sphere","Sphere")
	k4.Placement.Base=p4
	k4.Radius=0.2
	k4.ViewObject.ShapeColor=(1.0,0.0,0.0)
	
	k=App.ActiveDocument.addObject("Part::Sphere","Sphere")
	k.Radius.Value=r1.evalf()
	k.Placement.Base=FreeCAD.Vector(m.x.evalf(),m.y.evalf(),m.z.evalf())
	k.ViewObject.Transparency=80
	App.activeDocument().recompute()


def run():
	s=Gui.Selection.getSelectionEx()[0]
	sels=[]
	for s in Gui.Selection.getSelectionEx():
		subs=s.SubObjects
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

	makeSphere(p1,p2,p3,p4)


#run()

