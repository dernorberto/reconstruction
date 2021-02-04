#
#  path finder and analyzer tests
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
# fn=reconstruction.__path__[0] + "/../testdata/bn_930.png"
fn=reconstruction.__path__[0] + "/../testdata/bn_935.png"


t=createCV('ImageFile')
t.sourceFile=fn

t2=createCV("PathAnalyzer")
t2.sourceObject=t
t2.pathSelection=True
t2.N=6
t2.Threshold=100

App.activeDocument().recompute()

