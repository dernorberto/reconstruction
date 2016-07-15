import reconstruction.nurbs

if  App.ActiveDocument==None:
	App.newDocument("Unnamed")
	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	Gui.ActiveDocument=Gui.getDocument("Unnamed")

def createPool():

	a=reconstruction.nurbs.makeNurbs()

	Gui.activeDocument().activeView().viewAxonometric()
	Gui.SendMsgToActiveView("ViewFit")

	App.ActiveDocument.Nurbs.ViewObject.ShapeColor=(0.00,1.00,1.00)

	a.nNodes_u=8
	a.nNodes_v=5

	# create the base grid
	ps=a.Proxy.getPoints()
	g=a.Proxy.togrid(ps)


	#---------- apply Nurbs Tool s   elevateRectangle, elevateCircle, elevateUVLine

	# create the ground
	a.Proxy.elevateRectangle(0,0,29,29,40)
	Gui.activeDocument().activeView().viewAxonometric()
	Gui.SendMsgToActiveView("ViewFit")

	# sunshine hill
	a.Proxy.elevateRectangle(3,5,2,13,50)

	# pool
	a.Proxy.elevateRectangle(10,8,15,15,-30)

	#volcano
	a.Proxy.elevateCircle(15,15,30,100)
	a.Proxy.elevateCircle(15,15,10,30)

	# inner border
	a.Proxy.elevateVline(7,30)

	# outer border of the garden
	a.Proxy.elevateVline(-1,30)
	a.Proxy.elevateUline(-1,30)
	a.Proxy.elevateVline(0,30)
	a.Proxy.elevateUline(0,30)
	a.Label="Pool"

createPool()
