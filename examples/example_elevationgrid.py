#
#  create an elevation grid
#


import FreeCAD,FreeCADGui
Gui=FreeCADGui
FreeCAD.open("/home/thomas/Dokumente/freecad_buch/b204_pcl/wires3.fcstd")
App.setActiveDocument("wires3")
App.ActiveDocument=App.getDocument("wires3")
Gui.ActiveDocument=Gui.getDocument("wires3")



import reconstruction.CV2

t2=reconstruction.CV2.createCV('ElevationGrid')

#
#  Fusion is a collection of 3 wires
#  example:  3 walks with the gps tracker  in my garden
#

t2.sourceObject=App.ActiveDocument.Fusion

FreeCAD.ActiveDocument.recompute()

reconstruction.CV2.run_elevationgrid(t2,None)






