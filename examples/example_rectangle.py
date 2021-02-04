#
#  hand drawn rectangle
#

from say import *
import reconstruction.CV2
import importlib
importlib.reload( reconstruction.CV2)
createCV=reconstruction.CV2.createCV


if App.ActiveDocument==None:
	App.newDocument("Unnamed")
	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	Gui.ActiveDocument=Gui.getDocument("Unnamed")



import reconstruction
fn=reconstruction.__path__[0] + "/../testdata/bn_990.png"

t=createCV('ImageFile')
t.sourceFile=fn
#t.subX1=100
#t.subY0=200

t.invert=True

t2=createCV('Morphing')
t2.sourceObject=t
t2.filter='dilation'
t2.kernel=11
FreeCAD.ActiveDocument.recompute()

t3=createCV('Skeleton',"Skeleton")
t3.sourceObject=t2
t3.threshold=1
FreeCAD.ActiveDocument.recompute()

t5=createCV("PathAnalyzer")
t5.sourceObject=t3
t5.pathSelection=True
t5.N=5
t5.Threshold=143
t5.useCanny=False

App.activeDocument().recompute()
