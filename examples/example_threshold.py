#
#  threshold tests
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


t2=createCV('Threshold',"My global Thresholding")
t2.sourceObject=t
t2.globalThresholding=True
t2.param1=127
t2.param2=255


t3=createCV('CannyEdge')
t3.sourceObject=t2


App.activeDocument().recompute()

for j in [t,t2,t3]:
	try:
		App.activeDocument().recompute()
		j.ViewObject.Proxy.setEdit(j.ViewObject)
	except:
		App.activeDocument().recompute()
