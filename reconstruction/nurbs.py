# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- nurbs editor -
#--
#-- microelly 2016 v 0.0
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


# idea from  FreeCAD TemplatePyMod module by (c) 2013 Werner Mayer LGPL

# http://de.wikipedia.org/wiki/Non-Uniform_Rational_B-Spline
# http://www.opencascade.com/doc/occt-6.9.0/refman/html/class_geom___b_spline_surface.htm


import numpy as np
from say import *


class PartFeature:
	def __init__(self, obj):
		obj.Proxy = self
		self.obj2=obj


class Nurbs(PartFeature):
	def __init__(self, obj):
		PartFeature.__init__(self, obj)

		obj.addProperty("App::PropertyInteger","polnumber","Nurbs","Length of the Nurbs").polnumber=0

		obj.addProperty("App::PropertyInteger","degree_u","Nurbs","").degree_u=2
		obj.addProperty("App::PropertyInteger","degree_v","Nurbs","").degree_v=2
		obj.addProperty("App::PropertyInteger","nNodes_u","Nurbs","").nNodes_u=5
		obj.addProperty("App::PropertyInteger","nNodes_v","Nurbs","").nNodes_v=5
		obj.addProperty("App::PropertyFloatList","knot_u","Nurbs","").knot_u=[0,0,0,0.33,0.67,1,1,1]
		obj.addProperty("App::PropertyFloatList","knot_v","Nurbs","").knot_v=[0,0,0,0.33,0.67,1,1,1]


		obj.addProperty("App::PropertyFloat","Height","Nurbs", "Height of the Nurbs").Height=1.0
		obj.addProperty("App::PropertyStringList","poles","Nurbs","")
		# obj.setEditorMode("poles", 2)

		#the poles and surface helper object link
		obj.addProperty("App::PropertyLink","polobj","Nurbs","")

	def onChanged(self, fp, prop):

		if  prop== "Height":
			if hasattr(fp,"polobj"):
				if fp.polobj<>None: App.ActiveDocument.removeObject(fp.polobj.Name) 
				fp.polobj=self.run(fp,fp.poles)
				fp.polobj.ViewObject.PointSize=4
				fp.polobj.ViewObject.PointColor=(1.0,0.0,0.0)


	def execute(self, fp):
		pass

	def run(self,obj,poles=None):

		degree_u=obj.degree_u
		degree_v=obj.degree_v
		nNodes_u=obj.nNodes_u
		nNodes_v=obj.nNodes_v


		knot_u=[0,0,0,0.2,0.3,1,1,1]
		knot_v=[0,0,0,0.2,0.7,1,1,1]

		knot_u=[0,0,0,0.33,0.67,1,1,1]
		knot_v=[0,0,0,0.33,0.67,1,1,1]

		uc=nNodes_u
		vc=nNodes_v

		l=[1.0/(uc-2)*i for i in range(uc-1)]
		obj.knot_u=[0,0]+ l + [1,1]

		l=[1.0/(vc-2)*i for i in range(vc-1)]
		obj.knot_v=[0,0]+ l + [1,1]



		knot_u=obj.knot_u
		knot_v=obj.knot_v




		coor=[[0,0,1],[1,0,1],[2,0,1],[3,0,1],[4,0,1],\
			   [0,1,1],[1,1,0],[2,1,0],[3,1,0],[4,1,1],\
			   [0,2,1],[1,2,0],[2,2,3],[3,2,0],[4,2,1],\
			   [0,3,1],[1,3,0],[2,3,1],[3,3,-3],[4,3,1],\
			   [0,4,1],[1,4,1],[2,4,1],[3,4,1],[4,4,1]]

		if poles<>None:
			cc=""
			for l in poles: cc += str(l)
			coor=eval(cc)

		val=coor[obj.polnumber]
		coor[obj.polnumber]=[val[0],val[1],obj.Height]
		obj.poles=str(coor)

		bs=Part.BSplineSurface()
		bs.increaseDegree(degree_u,degree_v)
		 
		id=1
		for i in range(0,len(knot_u)-1):
				 if knot_u[i+1] > knot_u[i]:
						 bs.insertUKnot(knot_u[i],id,0.0000001)

		id=1
		for i in range(0,len(knot_v)-1):
				 if knot_v[i+1] > knot_v[i]:
						 bs.insertVKnot(knot_v[i],id,0.0000001)

		i=0
		for jj in range(0,nNodes_v):
			for ii in range(0,nNodes_u):
				bs.setPole(ii+1,jj+1,FreeCAD.Vector((coor[i][0],coor[i][1],coor[i][2])),1);
				i=i+1;

		s=bs.toShape()
		obj.Shape=s

		#create the poles and surface helper for visualization
		#the pole point cloud
		pts=[FreeCAD.Vector(tuple(c)) for c in coor]
		vts=[Part.Vertex(pp) for pp in pts]

		#and the surface
		vts.append(s)
		comp=Part.makeCompound(vts)
		Part.show(comp)
		App.ActiveDocument.ActiveObject.Label="Poles and Surface"

		return App.ActiveDocument.ActiveObject


	def getPoints(self):
		ps=[]
		vc=self.obj2.nNodes_v
		uc=self.obj2.nNodes_u
		
		for v in range(vc):
			for u in range(uc):
				ps.append(FreeCAD.Vector(u*20,v*10,0))
		return ps



	def togrid(self,ps):
		vc=self.obj2.nNodes_v
		uc=self.obj2.nNodes_u
		grid=np.array(ps)
		grid=grid.reshape(vc,uc,3)
		self.g=grid
		self.grid=None
		return grid

	def showGriduv(self):
		
		gg=self.g
		if 0: # wenns schnell gehen muss, spart 75%
			return

		# global grid
		ls=[]
#		vc,uc,tt=gg.shape
		uc=self.obj2.nNodes_v
		vc=self.obj2.nNodes_u
		
		print "shwoGriduv"
		print gg.shape
		print ("uc vc ",uc,vc)
		
		for u in range(uc):
			for v in range(vc):
	#			print(u,v)
				if u<uc-1:
					l=Part.makeLine(tuple(gg[u][v]),tuple(gg[u+1][v]))
					#print (tuple(gg[u][v]),tuple(gg[u+1][v]))
					#vx=Part.Vertex(tuple(gg[u][v]))
					#Part.show(vx)
					ls.append(l)
				if v<vc-1:
					pass
					l=Part.makeLine(tuple(gg[u][v]),tuple(gg[u][v+1]))
					ls.append(l)

	#	print ls
		comp=Part.makeCompound(ls)
		if self.grid <> None:
			self.grid.Shape=comp
		else:
			Part.show(comp)
			self.grid=App.ActiveDocument.ActiveObject
			self.grid.Label="Pole Grid"
		App.activeDocument().recompute()
		return comp


	def setpointZ(self,u,v,h):
		self.g[v][u][2]=h
		self.updatePoles()
		self.showGriduv()

	def movePoint(self,u,v,dx,dy,dz):
		self.g[v][u][0] += dx
		self.g[v][u][1] += dy
		self.g[v][u][2] += dz
		self.updatePoles()
		self.showGriduv()

	def addUline(self,vp):

		g=self.g
		vc,uc,tt=self.g.shape

		vline=[]
		for i in range(uc):
			vline.append([(g[vp-1][i][0]+g[vp][i][0])/2,(g[vp-1][i][1]+g[vp][i][1])/2,20] )# (g[vp-1][i][2]+g[vp][i][2])/2

		vline=np.array(vline)

		gg=np.concatenate((g[:vp],[vline],g[vp:]))

		self.g=gg
		
		#self.obj2.nNodes_u=uc
		self.obj2.nNodes_v += 1

		self.updatePoles()
		c=self.showGriduv()
		return gg


	def addVline(self,vp):

		g=self.g
		vc,uc,tt=self.g.shape
		print "add V line"
		print self.g.shape
		g=g.swapaxes(0,1)

		vline=[]
		for i in range(vc):
			vline.append([(g[vp-1][i][0]+g[vp][i][0])/2,(g[vp-1][i][1]+g[vp][i][1])/2,20] )# (g[vp-1][i][2]+g[vp][i][2])/2

		vline=np.array(vline)

		print(g[:vp].shape)
		print vline.shape
		
		gg=np.concatenate((g[:vp],[vline],g[vp:]))
		gg=gg.swapaxes(0,1)

		self.g=gg

		#self.obj2.nNodes_u=uc
		self.obj2.nNodes_u += 1

		self.updatePoles()
		c=self.showGriduv()
		
		return gg


	def updatePoles(self):
		ll="["
		print "rshale 1"
		vc,uc,tt=self.g.shape
		gf=self.g.reshape(uc*vc,3)
		print "resh 2"
		for i in gf: 
			ll += str( list(i)) +","
		ll +="]"
		self.obj2.poles=ll
		self.onChanged(self.obj2,"Height")


class ViewProviderNurbs:
	def __init__(self, obj):
		''' Set this object to the proxy object of the actual view provider '''
		obj.Proxy = self
		self.Object=obj

	def attach(self, obj):
		''' Setup the scene sub-graph of the view provider, this method is mandatory '''
		return

	def updateData(self, fp, prop):
		''' If a property of the handled feature has changed we have the chance to handle this here '''
		return

	def getDisplayModes(self,obj):
		''' Return a list of display modes. '''
		modes=[]
		return modes

	def getDefaultDisplayMode(self):
		''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
		return "Shaded"

	def setDisplayMode(self,mode):
		''' Map the display mode defined in attach with those defined in getDisplayModes.
		Since they have the same names nothing needs to be done. This method is optinal.
		'''
		return mode

	def onChanged(self, vp, prop):
		''' Print the name of the property that has changed '''
		FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

	def getIcon(self):
		''' Return the icon in XMP format which will appear in the tree view. This method is optional
		and if not defined a default icon is shown.
		'''
		return """
			/* XPM */
			static const char * ViewProviderNurbs_xpm[] = {
			"16 16 6 1",
			" 	c None",
			".	c #141010",
			"+	c #615BD2",
			"@	c #C39D55",
			"#	c #000000",
			"$	c #57C355",
			"        ........",
			"   ......++..+..",
			"   .@@@@.++..++.",
			"   .@@@@.++..++.",
			"   .@@  .++++++.",
			"  ..@@  .++..++.",
			"###@@@@ .++..++.",
			"##$.@@$#.++++++.",
			"#$#$.$$$........",
			"#$$#######      ",
			"#$$#$$$$$#      ",
			"#$$#$$$$$#      ",
			"#$$#$$$$$#      ",
			" #$#$$$$$#      ",
			"  ##$$$$$#      ",
			"   #######      "};
			"""

	def __getstate__(self):
		return None

	def __setstate__(self,state):
		return None


	def edit(self):
		print "edit"
		import nurbs_dialog
		reload (nurbs_dialog)
		self.miki=nurbs_dialog.mydialog(self.Object)
#		self.dialog=EditWidget(self,self.emenu + anims,False)
#		self.dialog.show()

	def setEdit(self,vobj,mode=0):
		self.edit()
		return True

	def unsetEdit(self,vobj,mode=0):
		return False


	def doubleClicked(self,vobj):
		say("double click")
		vobj.Visibility=True
		#self.setEdit(vobj,1)



def makeNurbs():
	a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Nurbs")
	Nurbs(a)
	ViewProviderNurbs(a.ViewObject)
	return a


if 1:

	coorstring='''[[0,0,1],[1,0,1],[2,0,1],[3,0,1],[4,0,1],
[0,1,1],[1,1,0],[2,1,2],[3,1,1],[4,1,1],
[0,2,1],[1,2,0],[2,2,3],[3,2,0],[4,2,1],
[0,3,1],[1,3,2],[2,3,3],[3,3,2],[4,3,1],
[0,4,1],[1,4,1],[2,4,1],[3,4,1],[4,4,1]]'''


	if 0:
		a=makeNurbs()
		a.poles=coorstring
		a.Height=1

		# punkte holen
		ps=a.Proxy.getPoints()
		print ps


		# daten in gitter
		g=a.Proxy.togrid(ps)
		g.shape
		print a.Proxy.g
		
		a.Proxy.showGriduv()
	


	uc=6
	vc=10

	a=makeNurbs()
	a.nNodes_u=uc
	a.nNodes_v=vc



	# punkte holen
	ps=a.Proxy.getPoints()

	# daten in gitter
	g=a.Proxy.togrid(ps)
	g.shape


	# horizontale Linien einfgen

	if 0:
		g=addUline(g,4)
		g=addUline(g,7)
		g=addUline(g,1)

		g=addVline(g,6)
		g=addVline(g,9)
		g=addVline(g,10)

		movePoint(g,2,7,0,0,30)
		movePoint(g,3,8,5,-3,15)
		movePoint(g,1,1,5,-3,15)
		movePoint(g,3,4,0,0,-30)

		movePoint(g,6,12,0,0,-30)
		movePoint(g,4,15,5,5,30)

		movePoint(g,9,15,5,5,30)




	'''
	a.knot_u=[0,0,0,0.25,0.5,0.75,1,1,1]
	a.knot_v=[0,0,0,0.25,0.5,0.75,1,1,1]
	'''




	ll="["
	gf=a.Proxy.g.reshape(uc*vc,3)
	for i in gf: 
		ll += str( list(i)) +","

	ll +="]"
	a.poles=ll

	a.Height=0

	# punkte holen
	ps=a.Proxy.getPoints()

	# daten in gitter
	g=a.Proxy.togrid(ps)


	#a.Proxy.showGriduv()

	a.Proxy.movePoint(1,1,0,0,15)
	a.Proxy.movePoint(3,4,0,0,-30)

	print "add Uline"
	a.Proxy.addUline(1)

	a.Proxy.addVline(3)
	a.Proxy.addVline(4)

	App.ActiveDocument.Nurbs.ViewObject.ShapeColor=(0.00,1.00,1.00)
	App.ActiveDocument.Nurbs.ViewObject.Transparency = 70
