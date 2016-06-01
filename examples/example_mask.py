#
#  hand drawn rectangle
#

from say import *
import reconstruction.CV2
reload( reconstruction.CV2)
createCV=reconstruction.CV2.createCV


if App.ActiveDocument==None:
	App.newDocument("Unnamed")
	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	Gui.ActiveDocument=Gui.getDocument("Unnamed")



import reconstruction
fn=reconstruction.__path__[0] + "/../testdata/bn_990.png"
fn=reconstruction.__path__[0] + "/../testdata/ba_500.png"

t=createCV('ImageFile')
t.sourceFile=fn
t.invert=True

t.subX0=200
t.subY0=100

#t.subX1=550
#t.subY1=500


# t.invert=True

t2=createCV('Mask')
t2.sourceObject=t
#t2.filter='dilation'
#t2.kernel=11
FreeCAD.ActiveDocument.recompute()



t3=createCV("Skeleton")
t3.sourceObject=t2
t3.threshold=3



t4=createCV("PathAnalyzer")
t4.sourceObject=t3
t4.pathSelection=True
t4.N=9
t4.Threshold=80
t4.useCanny=False
t4.radius=100




if 0:
	for tt in [t,t2,t3,t4]:
		tt.ViewObject.Proxy.hidden=True
		tt.ViewObject.Proxy.createDialog()
		tt.ViewObject.Proxy.edit()
		tt.Proxy.execute(tt)
		App.activeDocument().recompute()
		tt.Proxy.app.plot2()

