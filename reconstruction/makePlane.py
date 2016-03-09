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
import Draft

def seq(v):
	return (v.x,v.y,v.z)

# 4 points in FreeCAD and SymPy

def makePlane(p1,p2,p3,p4):

	sp1=Point3D(seq(p1))
	sp2=Point3D(seq(p2))
	sp3=Point3D(seq(p3))
	sp4=Point3D(seq(p4))


	mp=(sp1+sp2+sp3+sp4)/4

	e4=Plane(sp1,sp2,sp3)
	e3=Plane(sp1,sp2,sp4)
	e2=Plane(sp1,sp4,sp3)
	e1=Plane(sp4,sp2,sp3)

	n=Point3D(e1.normal_vector)+Point3D(e2.normal_vector)+Point3D(e3.normal_vector)+Point3D(e3.normal_vector)
	e=Plane(mp,n)
	m=e.p1

	fm=FreeCAD.Vector(m.x.evalf(),m.y.evalf(),m.z.evalf())
	fn=FreeCAD.Vector(n[0],n[1],n[2])

	x=fm.cross(fn).normalize()
	y=x.cross(fn).normalize()

	Draft.makeWire([fm.add(x.multiply(10)),fm.add(y.multiply(10)),fm.sub(x),fm.sub(y)],closed=True,face=True)

	w=Draft.makeWire([p1,p2,p3],closed=True,face=True)
	w.ViewObject.Transparency=80
	w.ViewObject.ShapeColor=(0.,1.,0.)
	w=Draft.makeWire([p4,p2,p3],closed=True,face=True)
	w.ViewObject.Transparency=80
	w.ViewObject.ShapeColor=(0.,1.,0.)
	w=Draft.makeWire([p1,p4,p3],closed=True,face=True)
	w.ViewObject.Transparency=80
	w.ViewObject.ShapeColor=(0.,1.,0.)
	w=Draft.makeWire([p1,p2,p4],closed=True,face=True)
	w.ViewObject.Transparency=80
	w.ViewObject.ShapeColor=(0.,1.,0.)
	
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
		sels += subs
	subs=sels
	if len(subs)<>4:
		raise Exception("keine vier kanten")
	l=[]
	for e in s.SubObjects: 
		if e.__class__.__name__ <>'Vertex':
			raise Exception ("Non edge in selection" + str(e))
		print e.Point
		l.append(e.Point)
	[p1,p2,p3,p4]=l
	print s.SubObjects

	makePlane(p1,p2,p3,p4)


# run()






