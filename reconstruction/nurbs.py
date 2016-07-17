# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- nurbs editor -
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------


# idea from  FreeCAD TemplatePyMod module by (c) 2013 Werner Mayer LGPL

# http://de.wikipedia.org/wiki/Non-Uniform_Rational_B-Spline
# http://www.opencascade.com/doc/occt-6.9.0/refman/html/class_geom___b_spline_surface.htm

import numpy as np
from say import *

from pivy import coin

if 0:

	view = Gui.ActiveDocument.ActiveView
	viewer=view.getViewer()
	render=viewer.getSoRenderManager()

	glAction=coin.SoGLRenderAction(render.getViewportRegion())
	render.setGLRenderAction(glAction)
	render.setRenderMode(render.WIREFRAME_OVERLAY)




def setNice(flag=True): 
	p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Part")
	w=p.GetFloat("MeshDeviation")
	if flag:
		p.SetFloat("MeshDeviation",0.05)
	else:
		p.SetFloat("MeshDeviation",0.5)

setNice()




class PartFeature:
	def __init__(self, obj):
		obj.Proxy = self
		self.obj2=obj


class Nurbs(PartFeature):
	def __init__(self, obj,uc=5,vc=5):
		PartFeature.__init__(self, obj)

		obj.addProperty("App::PropertyInteger","polnumber","Nurbs","Length of the Nurbs").polnumber=0

		obj.addProperty("App::PropertyInteger","degree_u","Nurbs","").degree_u=2
		obj.addProperty("App::PropertyInteger","degree_v","Nurbs","").degree_v=2
		obj.addProperty("App::PropertyInteger","nNodes_u","Nurbs","").nNodes_u=uc
		obj.addProperty("App::PropertyInteger","nNodes_v","Nurbs","").nNodes_v=vc
		obj.addProperty("App::PropertyFloatList","knot_u","Nurbs","").knot_u=[0,0,0,0.33,0.67,1,1,1]
		obj.addProperty("App::PropertyFloatList","knot_v","Nurbs","").knot_v=[0,0,0,0.33,0.67,1,1,1]
		obj.addProperty("App::PropertyFloatList","weights","Nurbs","").weights=[1]*(uc*vc)


		obj.addProperty("App::PropertyFloat","Height","Nurbs", "Height of the Nurbs").Height=1.0
		obj.addProperty("App::PropertyStringList","poles","Nurbs","")
		obj.setEditorMode("poles", 2)

		#the poles and surface helper object link
		obj.addProperty("App::PropertyLink","polobj","Nurbs","")

	def onChanged(self, fp, prop):

		if  prop== "Height":
			if hasattr(fp,"polobj"):
				if fp.polobj<>None: App.ActiveDocument.removeObject(fp.polobj.Name) 
				fp.polobj=self.createSurface(fp,fp.poles)
				fp.polobj.ViewObject.PointSize=4
				fp.polobj.ViewObject.PointColor=(1.0,0.0,0.0)


	def execute(self, fp):
		pass


	def createSurface(self,obj,poles=None):

		starttime=time.time()
		degree_u=obj.degree_u
		degree_v=obj.degree_v
		nNodes_u=obj.nNodes_u
		nNodes_v=obj.nNodes_v

		'''
		knot_u=[0,0,0,0.2,0.3,1,1,1]
		knot_v=[0,0,0,0.2,0.7,1,1,1]

		knot_u=[0,0,0,0.33,0.67,1,1,1]
		knot_v=[0,0,0,0.33,0.67,1,1,1]
		'''

#		print "POLES"
#		print poles

		uc=nNodes_u
		vc=nNodes_v

		l=[1.0/(uc-2)*i for i in range(uc-1)]
		obj.knot_u=[0,0]+ l + [1,1]
		
		
		if obj.degree_u==1:
#			l=[1.0/(uc-2)*i for i in range(uc-1)]
			l=[1.0/(uc-1)*i for i in range(uc)]
			obj.knot_u=[0]+ l + [1]

		l=[1.0/(vc-2)*i for i in range(vc-1)]
		obj.knot_v=[0,0]+ l + [1,1]
		#obj.knot_v=[0]+ l + [1]

		if obj.degree_v==1:
#			l=[1.0/(vc-2)*i for i in range(vc-1)]
			l=[1.0/(vc-1)*i for i in range(vc)]
			obj.knot_v= l 
			obj.knot_v=[0]+ l + [1]

		try:
			weights=np.array(obj.weights)
			weights=weights.reshape(vc,uc)
		except:
			weights=np.ones(vc*uc)
			weights=weights.reshape(vc,uc)

		obj.weights=list(np.ravel(weights))

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

		#val=coor[obj.polnumber]
		#coor[obj.polnumber]=[val[0],val[1],obj.Height]

		obj.poles=str(coor)

		bs=Part.BSplineSurface()
		bs.increaseDegree(degree_u,degree_v)

		for i in range(0,len(knot_u)):
				# if knot_u[i+1] > knot_u[i]:
						 bs.insertUKnot(knot_u[i],1,0.0000001)

		for i in range(0,len(knot_v)):
				# if knot_v[i+1] > knot_v[i]:
						 bs.insertVKnot(knot_v[i],1,0.0000001)

		i=0
		for jj in range(0,nNodes_v):
			for ii in range(0,nNodes_u):
				try:
					bs.setPole(ii+1,jj+1,FreeCAD.Vector((coor[i][0],coor[i][1],coor[i][2])),weights[jj,ii])
				except:
						print([ii+1,jj+1,FreeCAD.Vector((coor[i][0],coor[i][1],coor[i][2])),weights[jj,ii]])
						sayexc("setPols ii,jj:"+str([ii,jj]))
				i=i+1;

		obj.Shape=bs.toShape()
		# FreeCAD.bs=bs
		
		# create the box
		mx=np.array(coor).reshape(nNodes_v,nNodes_u,3)
		print "create box"
		print (mx.shape)
		a0=tuple(mx[0,0])
		b0=tuple(mx[0,-1])
		c0=tuple(mx[-1,-1])
		d0=tuple(mx[-1,0])

		a=tuple(mx[0,0]+[0,0,-20])
		b=tuple(mx[0,-1]+[0,0,-20])
		c=tuple(mx[-1,-1]+[0,0,-20])
		d=tuple(mx[-1,0]+[0,0,-20])
		print (a,b,c,d)
		
		lls=[Part.makeLine(a0,b0),Part.makeLine(b0,b),Part.makeLine(b,a),Part.makeLine(a,a0)]
		fab=Part.makeFilledFace(lls)
		lls=[Part.makeLine(b0,c0),Part.makeLine(c0,c),Part.makeLine(c,b),Part.makeLine(b,b0)]
		fbc=Part.makeFilledFace(lls)
		lls=[Part.makeLine(c0,d0),Part.makeLine(d0,d),Part.makeLine(d,c),Part.makeLine(c,c0)]
		fcd=Part.makeFilledFace(lls)
		lls=[Part.makeLine(d0,a0),Part.makeLine(a0,a),Part.makeLine(a,d),Part.makeLine(d,d0)]
		fda=Part.makeFilledFace(lls)
		lls=[Part.makeLine(a,b),Part.makeLine(b,c),Part.makeLine(c,d),Part.makeLine(d,a)]
		ff=Part.makeFilledFace(lls)
		
		fs=[fab,fbc,fcd,fda,ff,obj.Shape]

#		for f in fs: Part.show(f)

		comp=Part.makeCompound(fs)
		s=Part.makeShell(fs)
		# Part.show(s)
		sol=Part.makeSolid(s)
		
		
		# Part.show(sol)
		obj.Shape=sol
		
		
		print "done"
		
		nurbstime=time.time()
		#create the poles and surface helper for visualization
		#the pole point cloud
		pts=[FreeCAD.Vector(tuple(c)) for c in coor]
		vts=[Part.Vertex(pp) for pp in pts]

		#and the surface

		vts.append(obj.Shape)
		comp=Part.makeCompound(vts)
		comptime=time.time()
		try:
			yy=FreeCAD.ActiveDocument.Poles
		except:
			yy=FreeCAD.ActiveDocument.addObject("Part::Feature","Poles")

		yy.Shape=comp
		
#		Part.show(comp)
#		App.ActiveDocument.ActiveObject.Label="Poles and Surface"
#		
#		yy.Shape=App.ActiveDocument.ActiveObject.Shape

		endtime=time.time()
		print ("create Nirbs time",nurbstime-starttime)
		print ("create helper time",endtime-nurbstime)
		print ("create comp time",comptime-nurbstime)
		print ("create Surface time",endtime-comptime)
		
		return App.ActiveDocument.ActiveObject


	def getPoints(self):
		''' generic point set for grid'''
		ps=[]
		vc=self.obj2.nNodes_v
		uc=self.obj2.nNodes_u
		for v in range(vc):
			for u in range(uc):
				ps.append(FreeCAD.Vector(u*40,v*30,0))
		return ps



	def togrid(self,ps):
		''' points to 2D grid'''
		self.grid=None
		self.g=np.array(ps).reshape(self.obj2.nNodes_v,self.obj2.nNodes_u,3)
		return self.g

	def showGriduv(self):
		'''recompute and show the Pole grid '''

		starttime=time.time()
		gg=self.g

		try:
			if 	not self.calculatePoleGrid: return
		except:
			return

		ls=[]
		uc=self.obj2.nNodes_v
		vc=self.obj2.nNodes_u

		for u in range(uc):
			for v in range(vc):
				if u<uc-1:
					ls.append(Part.makeLine(tuple(gg[u][v]),tuple(gg[u+1][v])))
				if v<vc-1:
					ls.append(Part.makeLine(tuple(gg[u][v]),tuple(gg[u][v+1])))

		comp=Part.makeCompound(ls)
		if self.grid <> None:
			self.grid.Shape=comp
		else:
			Part.show(comp)
			App.ActiveDocument.ActiveObject.ViewObject.hide()
			self.grid=App.ActiveDocument.ActiveObject
			self.grid.Label="Pole Grid"

		App.activeDocument().recompute()
		Gui.updateGui()
		endtime=time.time()
		print ("create PoleGrid time",endtime-starttime)


	def setpointZ(self,u,v,h=0,w=20):
		''' set height and weight of a pole point '''

		FreeCAD.ActiveDocument.openTransaction("move Point")

		self.g[v][u][2]=h
		uc=self.obj2.nNodes_u
		vc=self.obj2.nNodes_v
		try:
			wl=self.obj2.weights
			wl[v*uc+u]=w
			self.obj2.weights=wl
		except:
			sayexc()

		self.updatePoles()
		self.showGriduv()
		FreeCAD.ActiveDocument.commitTransaction()

	def setpointRelativeZ(self,u,v,h=0,w=0,update=False):

		''' set relative height and weight of a pole point '''

		FreeCAD.ActiveDocument.openTransaction("move Point")

		print self.g[v][u]
		print "realtive ",h
		self.g[v][u][2] = self.gBase[v][u][2] + h
		
		print self.g[v][u]
		
		if update:
			self.gBase=self.g.copy()

		uc=self.obj2.nNodes_u
		vc=self.obj2.nNodes_v
		try:
			wl=self.obj2.weights
			wl[v*uc+u]=w
			self.obj2.weights=wl
		except:
			sayexc()

		self.updatePoles()
		self.showGriduv()
		FreeCAD.ActiveDocument.commitTransaction()



	def movePoint(self,u,v,dx,dy,dz):
		''' relative move ofa pole point '''

		FreeCAD.ActiveDocument.openTransaction("move Point")

		self.g[v][u][0] += dx
		self.g[v][u][1] += dy
		self.g[v][u][2] += dz

		self.updatePoles()
		self.showGriduv()
		FreeCAD.ActiveDocument.commitTransaction()

	def elevateUline(self,vp,height=40):
		''' change the height of all poles with teh same u value'''

		FreeCAD.ActiveDocument.openTransaction("move Point")

		uc=self.obj2.nNodes_u
		vc=self.obj2.nNodes_v

		for i in range(1,uc-1):
			self.g[vp][i][2]=height

		self.updatePoles()
		self.showGriduv()
		FreeCAD.ActiveDocument.commitTransaction()


	def elevateVline(self,vp,height=40):

		FreeCAD.ActiveDocument.openTransaction("move Point")

		uc=self.obj2.nNodes_u
		vc=self.obj2.nNodes_v

		for i in range(1,vc-1):
			self.g[i][vp][2]=height

		self.updatePoles()
		self.showGriduv()
		FreeCAD.ActiveDocument.commitTransaction()

	def elevateRectangle(self,v,u,dv,du,height=50):
		''' change the height of all poles inside a rectangle of the pole grid'''

		FreeCAD.ActiveDocument.openTransaction("move Point")

		uc=self.obj2.nNodes_u
		vc=self.obj2.nNodes_v

		for iv in range(v,v+dv+1):
			for iu in range(u,u+du+1):
				self.g[iu][iv][2]=height

		self.updatePoles()
		self.showGriduv()
		FreeCAD.ActiveDocument.commitTransaction()


	def elevateCircle(self,u=20,v=30,radius=10,height=60):
		''' change the height for poles around a cenral pole '''

		FreeCAD.ActiveDocument.openTransaction("move Point")

		uc=self.obj2.nNodes_u
		vc=self.obj2.nNodes_v

		g=self.g
		for iv in range(vc):
			for iu in range(uc):
				if (g[iu][iv][0]-g[u][v][0])**2 + (g[iu][iv][1]-g[u][v][1])**2 <= radius**2: 
					g[iu][iv][2]=height
		self.g=g

		self.updatePoles()
		self.showGriduv()
		FreeCAD.ActiveDocument.commitTransaction()


	def createWaves(self,height=10,depth=-5):
		'''wave pattern over all'''

		FreeCAD.ActiveDocument.openTransaction("move Point")

		uc=self.obj2.nNodes_u
		vc=self.obj2.nNodes_v

		for iv in range(1,vc-1):
			for iu in range(1,uc-1):
				
				if (iv+iu)%2 == 0:
					self.g[iu][iv][2]=height
				else:
					self.g[iu][iv][2]=depth

		self.updatePoles()
		self.showGriduv()
		FreeCAD.ActiveDocument.commitTransaction()


	def addUline(self,vp,pos=0.5):
		''' insert a line of poles after vp, pos is relative to the next Uline'''

		FreeCAD.ActiveDocument.openTransaction("move Point")

		uc=self.obj2.nNodes_u
		vc=self.obj2.nNodes_v

		if pos<=0: pos=0.00001
		if pos>=1: pos=1-0.00001
		pos=1-pos

		g=self.g

		vline=[]
		for i in range(uc):
			vline.append([(g[vp-1][i][0]+g[vp][i][0])/2,(g[vp-1][i][1]+g[vp][i][1])/2,20] )# (g[vp-1][i][2]+g[vp][i][2])/2

		vline=[]
		for i in range(uc):
			vline.append([(pos*g[vp-1][i][0]+(1-pos)*g[vp][i][0]),(pos*g[vp-1][i][1]+(1-pos)*g[vp][i][1]),20] )# (g[vp-1][i][2]+g[vp][i][2])/2

		vline=np.array(vline)

		gg=np.concatenate((g[:vp],[vline],g[vp:]))
		self.g=gg
		
		self.obj2.nNodes_v += 1

		self.updatePoles()
		self.showGriduv()
		FreeCAD.ActiveDocument.commitTransaction()



	def addVline(self,vp,pos=0.5):

		FreeCAD.ActiveDocument.openTransaction("move Point")

		uc=self.obj2.nNodes_u
		vc=self.obj2.nNodes_v

		if pos<=0: pos=0.00001
		if pos>=1: pos=1-0.00001
		pos=1-pos
		
		g=self.g
		g=g.swapaxes(0,1)

		vline=[]
		for i in range(vc):
			vline.append([(pos*g[vp-1][i][0]+(1-pos)*g[vp][i][0]),(pos*g[vp-1][i][1]+(1-pos)*g[vp][i][1]),20] )# (g[vp-1][i][2]+g[vp][i][2])/2

		vline=np.array(vline)

		gg=np.concatenate((g[:vp],[vline],g[vp:]))
		gg=gg.swapaxes(0,1)
		self.g=gg

		self.obj2.nNodes_u += 1

		self.updatePoles()
		self.showGriduv()
		FreeCAD.ActiveDocument.commitTransaction()


	def addS(self,vp):
		''' harte kante links, weicher uebergang, harte kante rechts ''' 

		FreeCAD.ActiveDocument.openTransaction("move Point")

		uc=self.obj2.nNodes_u
		vc=self.obj2.nNodes_v

		g=self.g
		g=g.swapaxes(0,1)

		vline=[]
		for i in range(vc):
			pos=0.5
			if i<0.3*vc: pos= 0.0001
			if i>0.6*vc: pos= 0.9999

			vline.append([(pos*g[vp-1][i][0]+(1-pos)*g[vp][i][0]),(pos*g[vp-1][i][1]+(1-pos)*g[vp][i][1]),(pos*g[vp-1][i][2]+(1-pos)*g[vp][i][2])] )

		vline=np.array(vline)

		gg=np.concatenate((g[:vp],[vline],g[vp:]))

		self.g=gg.swapaxes(0,1)
		self.obj2.nNodes_u += 1

		self.updatePoles()
		self.showGriduv()
		FreeCAD.ActiveDocument.commitTransaction()


	def updatePoles(self):
		'''recompute polestring and recompute surface'''

		uc=self.obj2.nNodes_u
		vc=self.obj2.nNodes_v

		ll=""
		gf=self.g.reshape(uc*vc,3)
		for i in gf: 
			ll += str( list(i)) +","
		ll ="[" + ll + "]"

		self.obj2.poles=ll
		self.onChanged(self.obj2,"Height")


class ViewProviderNurbs:
	def __init__(self, obj):
		obj.Proxy = self
		self.Object=obj

	def attach(self, obj):
		''' Setup the scene sub-graph of the view provider, this method is mandatory '''
		return

	def updateData(self, fp, prop):
		''' If a property of the handled feature has changed we have the chance to handle this here '''
		return

	def getDisplayModes(self,obj):
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
		pass

	def getIcon(self):

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
		import nurbs_dialog
		reload (nurbs_dialog)
		self.miki=nurbs_dialog.mydialog(self.Object)

	def setEdit(self,vobj,mode=0):
		self.edit()
		return True

	def unsetEdit(self,vobj,mode=0):
		return False


	def doubleClicked(self,vobj):
		say("double click")
		vobj.Visibility=True
		# self.setEdit(vobj,0)
		return False



def makeNurbs(uc=5,vc=7):

	a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Nurbs")
	Nurbs(a,uc,vc)
	ViewProviderNurbs(a.ViewObject)
	a.ViewObject.ShapeColor=(0.00,1.00,1.00)
	a.ViewObject.Transparency = 70

	return a


def test0():
	''' erster test '''

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



def test1():

	uc=20
	vc=20

	a=makeNurbs()

	App.ActiveDocument.Nurbs.ViewObject.ShapeColor=(0.00,1.00,1.00)
	App.ActiveDocument.Nurbs.ViewObject.Transparency = 70

	a.nNodes_u=uc
	a.nNodes_v=vc

	# punkte holen
	ps=a.Proxy.getPoints()

	# daten in gitter
	g=a.Proxy.togrid(ps)
	g.shape


	# horizontale Linien einfgen

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

	if 0:
		a.Proxy.movePoint(1,1,0,0,40)
		a.Proxy.movePoint(4,6,0,0,60)
		a.Proxy.movePoint(2,5,0,0,60)

		print "add Uline"
		a.Proxy.addUline(8)
		a.Proxy.addUline(8)
		a.Proxy.addUline(8)

		a.Proxy.addUline(4)

		a.Proxy.addUline(3,0.4)
		a.Proxy.addUline(3,0.7)

		a.Proxy.addUline(2,0.1)
		a.Proxy.addUline(2,0.1)


		a.Proxy.addVline(4,0)
		a.Proxy.addVline(4,0)

		a.Proxy.addVline(3,1)
		a.Proxy.addVline(3,1)
		

		a.Proxy.addVline(2,0.33)
		a.Proxy.addVline(1,0.67)


		a.Proxy.elevateUline(4)
		a.Proxy.elevateUline(6,-30)

		a.Proxy.elevateVline(3)
		a.Proxy.elevateUline(2,-30)

	# raender hochziehen



def runtest():

	uc=5
	vc=8

	a=makeNurbs(uc,vc)


	# punkte holen
	ps=a.Proxy.getPoints()

	# daten in gitter
	a.Proxy.togrid(ps)


	if 0:
		for i in range(uc-1):
			a.Proxy.addVline(uc-1-i)

	a.Proxy.addVline(3)
	a.Proxy.elevateVline(3,1)

	Gui.activeDocument().activeView().viewAxonometric()
	Gui.SendMsgToActiveView("ViewFit")


	if 1:
		a.Proxy.addVline(3,0.7)
		a.Proxy.addVline(3,0.2)

		a.Proxy.addS(4)
		a.Proxy.addVline(2,1)
		a.Proxy.elevateVline(2,0)

		a.Proxy.addVline(8,0)
		a.Proxy.elevateVline(8,0)

	if 1:
		a.Proxy.movePoint(1,1,0,0,40)
		a.Proxy.movePoint(2,4,0,0,60)
		a.Proxy.movePoint(2,5,0,0,60)


	Gui.activeDocument().activeView().viewAxonometric()
	Gui.SendMsgToActiveView("ViewFit")

	print "testscript nurbs done"






def runtest2():

	uc=10
	vc=10

	a=makeNurbs(uc,vc)
	a.degree_u=1

	a.degree_u=2

	a.degree_v=a.degree_u

	# punkte holen
	ps=a.Proxy.getPoints()

	# daten in gitter
	a.Proxy.togrid(ps)


	if 0:
		for i in range(uc-1):
			a.Proxy.addVline(uc-1-i)

#	a.Proxy.addVline(2)
#	a.Proxy.elevateVline(2,10)

	#a.Proxy.addUline(3)
	#a.Proxy.elevateUline(3,20)
	
	a.Proxy.addVline(3,0.9)
	a.Proxy.addVline(3,0.1)

	a.Proxy.addS(4)
	a.Proxy.elevateVline(4,30)




	a.Proxy.addVline(10,0.9)
	a.Proxy.addVline(10,0.1)

	a.Proxy.addS(11)
	a.Proxy.elevateVline(11,30)
	
	a.Proxy.addVline(10,0)
	a.Proxy.elevateVline(10,0)
	a.Proxy.addVline(15,0)
	a.Proxy.elevateVline(14,0)
	a.Proxy.elevateVline(15,0)




def runtest():
	# kreistest

	uc=6
	vc=5

	a=makeNurbs(uc,vc)
	a.degree_u=1

	a.degree_u=2

	a.degree_v=a.degree_u

	# punkte holen
	ps=a.Proxy.getPoints()

	ps=[]
	for v in range(vc):
			for u in range(uc):
				h=0
				if 1<=u and u<=3 and 1<=v and v<=3:
					h=100 
				if u==2 and v==2:
					h=105
				ps.append(FreeCAD.Vector(u*100,v*100,h))
	k=3.7
	
	
	a.weights=[
		1,1,1,1,1,1,
		1,1,k,1,1,1,
		1,k,1,k,1,1,
		1,1,k,1,1,1,
		1,1,1,1,1,1,
	]



	# daten in gitter
	a.Proxy.togrid(ps)


	a.Proxy.updatePoles()
	a.Proxy.showGriduv()





def createnurbs():


	a=makeNurbs(6,10)
	ps=a.Proxy.getPoints()
	a.Proxy.togrid(ps)
	a.Proxy.updatePoles()
	a.Proxy.showGriduv()

	App.activeDocument().recompute()
	Gui.updateGui()

	Gui.activeDocument().activeView().viewAxonometric()
	Gui.SendMsgToActiveView("ViewFit")
