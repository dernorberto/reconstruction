#
#  threshold tests
#

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
#fn=reconstruction.__path__[0] + "/../testdata/bn_511.png"
#fn="/home/thomas/Bilder/bn_917_schwelle.png"

t=createCV('ImageFile')
t.sourceFile=fn
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





t4=createCV('Mixer')
t4.sourceObject=t2
t4.source2Object=t3
t4.inverse2=True
t4.inverse=True
t4.flipOrder=True
t4.zoom=False
FreeCAD.ActiveDocument.recompute()








for j in [t,t2,t3,t4]:
	try:
		App.activeDocument().recompute()
		j.ViewObject.Proxy.setEdit(j.ViewObject)
	except:
		App.activeDocument().recompute()
