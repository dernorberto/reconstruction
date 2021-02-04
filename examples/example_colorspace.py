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
fn=reconstruction.__path__[0] + "/../testdata/bn_511.png"
#fn="/home/thomas/Bilder/bn_904.png"
#fn="/home/thomas/Bilder/bn_883.png"
fn=reconstruction.__path__[0] + "/../testdata/bn_917.png"

t=createCV('ImageFile')
t.sourceFile=fn
# t.invert=True


t3=createCV('ColorSpace','Optimize Colorspace' )
t3.sourceObject=t
# t3.threshold=1
FreeCAD.ActiveDocument.recompute()
t3.h1=90
t3.h2=229
t3.s1=200
t3.s2=216
t3.v1=204
t3.v2=82
t3.invert=True





t5=createCV('FatColor','Use only the fat (hand drawn) lines')
t5.sourceObject=t3
# t3.threshold=1
FreeCAD.ActiveDocument.recompute()
t3.h1=90
t3.h2=229
t3.s1=200
t3.s2=216
t3.v1=204
t3.v2=82
t3.invert=True





t8=createCV('BlobDetector','First Refinement')
t8.sourceObject=t5
#t8.filter='dilation'
t8.Area=5
FreeCAD.ActiveDocument.recompute()



t6=createCV('Skeleton',"Skeleton")
t6.sourceObject=t8
t6.threshold=1
FreeCAD.ActiveDocument.recompute()


t7=createCV('HoughLines')
t7.sourceObject=t6
FreeCAD.ActiveDocument.recompute()
t7.threshold=10
t7.minLineLenght=15
t7.maxLineGap=10



t9=createCV('CannyEdge')
t9.sourceObject=t7
t9.invert=True
FreeCAD.ActiveDocument.recompute()


t8a=createCV('BlobDetector','Further Refinement')
t8a.sourceObject=t9
#t8.filter='dilation'
t8a.Area=9
t8a.showBlobs=False
FreeCAD.ActiveDocument.recompute()


ta=createCV('Morphing','Background Image')
ta.sourceObject=t8a
ta.filter='dilation'
ta.kernel=3
FreeCAD.ActiveDocument.recompute()




t4=createCV('Mixer','Morphing and Hough Lines')
t4.sourceObject=ta
t4.source2Object=t7
# t4.inverse2=True
t4.inverse=True
t4.flipOrder=True
t4.zoom=False
t4.invert=True
FreeCAD.ActiveDocument.recompute()


t4a=createCV('Mixer','Hough Lines and Skeleton')
t4a.sourceObject=t7
t4a.source2Object=t6
t4a.inverse2=True
t4a.inverse=True
t4a.flipOrder=True
t4a.zoom=False
t4a.invert=True
FreeCAD.ActiveDocument.recompute()

	
	
