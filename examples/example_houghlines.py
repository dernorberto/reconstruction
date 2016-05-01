#
#  houghlines tests
#

import reconstruction.CV2
reload( reconstruction.CV2)
createCV=reconstruction.CV2.createCV


if App.ActiveDocument==None:
	App.newDocument("Unnamed")
	App.setActiveDocument("Unnamed")
	App.ActiveDocument=App.getDocument("Unnamed")
	Gui.ActiveDocument=Gui.getDocument("Unnamed")


import reconstruction
fn=reconstruction.__path__[0] + "/../testdata/bn_949.png"

t=createCV('ImageFile')
t.sourceFile=fn


t3=createCV('HoughLines')
t3.sourceObject=t
FreeCAD.ActiveDocument.recompute()


t4=createCV('HoughLinesPost')
t4.sourceObject=t3
t4.epsilon=40
t4.count=5
FreeCAD.ActiveDocument.recompute()


App.activeDocument().recompute()
for j in [t3,t4]:
	try:
		App.activeDocument().recompute()
		j.ViewObject.Proxy.setEdit(j.ViewObject)
	except:
		App.activeDocument().recompute()
