#***************************************************************************
#*																		*
#*   Copyright (c) 2016													 *  
#*   <microelly2@freecadbuch.de>										 * 
#*																		 *
#*   This program is free software; you can redistribute it and/or modify*
#*   it under the terms of the GNU Lesser General Public License (LGPL)	*
#*   as published by the Free Software Foundation; either version 2 of	*
#*   the License, or (at your option) any later version.				*
#*   for detail see the LICENCE text file.								*
#*																		*
#*   This program is distributed in the hope that it will be useful,	*
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of		*
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		*
#*   GNU Library General Public License for more details.				*
#*																		*
#*   You should have received a copy of the GNU Library General Public	*
#*   License along with this program; if not, write to the Free Software*
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307*
#*   USA																*
#*																		*
#************************************************************************

__title__="FreeCAD Geodata Toolkit"
__author__ = "Thomas Gundermann"
__url__ = "http://www.freecadbuch.de"

import FreeCAD, FreeCADGui

windowCreated = 0


class nurbsEditor:

	def Activated(self):
		FreeCAD.Console.PrintMessage("run  ... ")
		import reconstruction.nurbs
		reload(reconstruction.nurbs)
		print "okay"
		reconstruction.nurbs.createnurbs()


	def GetResources(self):
		return {
			'Pixmap'  : 'Std_Tool1', 
			'MenuText': 'Nurbs Editor', 
			'ToolTip': ''
		}

FreeCADGui.addCommand('Nurbs Editor', nurbsEditor())



'''
class perspectiveTrafo:

	def Activated(self):
		FreeCAD.Console.PrintMessage("run  ... ")
		import reconstruction.perspective_trafo
		reload(reconstruction.perspective_trafo)
		print "okay"
		reconstruction.perspective_trafo.run()


	def GetResources(self):
		return {
			'Pixmap'  : 'Std_Tool1', 
			'MenuText': 'Perspective Image Trafo ', 
			'ToolTip': ''
		}

FreeCADGui.addCommand('Perspective Image Trafo',  perspectiveTrafo())
'''


class pointcloudComposer:

	def Activated(self):
		FreeCAD.Console.PrintMessage("run  ... ")
		import reconstruction.pointcloud_composer
		reload(reconstruction.pointcloud_composer)
		print "okay"
		reconstruction.pointcloud_composer.run()


	def GetResources(self):
		return {
			'Pixmap'  : 'Std_Tool1', 
			'MenuText': 'Point Cloud Composer', 
			'ToolTip': ''
		}

FreeCADGui.addCommand('Point Cloud Composer', pointcloudComposer())


class mydialog:

	def Activated(self):
		FreeCAD.Console.PrintMessage("run  ... ")
		import reconstruction.create_perspective_tool
		reload(reconstruction.create_perspective_tool)
		print "okay"
		reconstruction.create_perspective_tool.run()


	def GetResources(self):
		return {
			'Pixmap'  : 'Std_Tool1', 
			'MenuText': 'Part Creator', 
			'ToolTip': ''
		}

FreeCADGui.addCommand('Import Image', mydialog())

class houghlines:

	def Activated(self):
		print "run import ..."
		import reconstruction.houghlines
		reload(reconstruction.houghlines)
		print "okay"
		reconstruction.houghlines.run()

	def GetResources(self):
		return {
			'Pixmap'  : 'Std_Tool2', 
			'MenuText': 'houghlines', 
			'ToolTip': 'houghlines'
		}

FreeCADGui.addCommand('houghlines', houghlines())

        
class makeSphere:

	def Activated(self):
		print "run import ..."
		import reconstruction.makeSphere
		reload(reconstruction.makeSphere)
		print "okay"
		reconstruction.makeSphere.run()

	def GetResources(self):
		return {
			'Pixmap'  : 'Std_Tool2', 
			'MenuText': 'makeSphere', 
			'ToolTip': 'makeSphere'
		}

FreeCADGui.addCommand('makeSphere', makeSphere())

class makeCylinder:

	def Activated(self):
		print "run import ..."
		import reconstruction.makeCylinder
		reload(reconstruction.makeCylinder)
		print "okay"
		reconstruction.makeCylinder.run()

	def GetResources(self):
		return {
			'Pixmap'  : 'Std_Tool2', 
			'MenuText': 'makeCylinder', 
			'ToolTip': 'makeCylinder'
		}

FreeCADGui.addCommand('makeCylinder', makeCylinder())


class makePlane:

	def Activated(self):
		print "run import ..."
		import reconstruction.makePlane
		reload(reconstruction.makePlane)
		print "okay"
		reconstruction.makePlane.run()

	def GetResources(self):
		return {
			'Pixmap'  : 'Std_Tool2', 
			'MenuText': 'makePlane', 
			'ToolTip': 'makePlane'
		}

FreeCADGui.addCommand('makePlane', makePlane())


class makePrism:

	def Activated(self):
		print "run import ..."
		import reconstruction.makePrism
		reload(reconstruction.makePrism)
		print "okay"
		reconstruction.makePrism.run()

	def GetResources(self):
		return {
			'Pixmap'  : 'Std_Tool2', 
			'MenuText': 'makePrism', 
			'ToolTip': 'makePrism'
		}

FreeCADGui.addCommand('makePrism', makePrism())


class makeCVX:

	def Activated(self):
		print "run import ..."
		import reconstruction.CV
		reload(reconstruction.CV)
		print "okay"
		reconstruction.CV.createCV()

	def GetResources(self):
		return {
			'Pixmap'  : 'Std_Tool2', 
			'MenuText': 'create openCV Filter', 
			'ToolTip': 'makeCV'
		}

# FreeCADGui.addCommand('makeCV', makeCV())





def runme(s):
	exec("import "+s)
	exec("reload("+s+")")
	rc=eval( s+".run()")
	return rc

class makeCV_master:
	global runme
	def __init__(self,classname='CV',pixmap='Std_Tool1',menutext=None,tooltip=None):
		self.classname=classname
		self.pixmap=pixmap
		if menutext==None:
			self.menutext="create " + self.classname
		else:
			self.menutext=menutext
		if tooltip==None: 
			self.tooltip="create a new " + self.classname
		else:
			self.tooltip=tooltip


	def Activated(self):
		s="reconstruction." + self.classname
		print "run import ..." + s
		t=runme(s)
		print t.Label
		print  s + " done, okay"

	def GetResources(self):
		return {
			'Pixmap'  : self.pixmap, 
			'MenuText': self.menutext, 
			'ToolTip': self.tooltip
		}


def createcmd(cmd='CV',pixmap='Std_Tool1',menutext=None,tooltip=None):
	global makeCV_master
	FreeCADGui.addCommand(cmd, makeCV_master(cmd,pixmap,menutext,tooltip))
	cvCmds.append(cmd)

#----------------------------------------------------------------

def runme2(s):
	import reconstruction.CV2
	reload(reconstruction.CV2)
	t2=reconstruction.CV2.createCV(s)
	return t2


import reconstruction
import reconstruction.configuration


class makeCV_master2:

	global runme2
	global reconstruction

	def __init__(self,classname='CV'):
		self.classname=classname

	def xxx(): # ignore
		self.pixmap=pixmap
		if menutext==None:
			self.menutext="create " + self.classname
		else:
			self.menutext=menutext
		if tooltip==None: 
			self.tooltip="create a new " + self.classname
		else:
			self.tooltip=tooltip


	def Activated(self):
		s="reconstruction." + self.classname
		print "run import ..." + s
		t=runme2(self.classname)
		print t.Label
		print  s + " done, okay"

	def GetResources(self):
		try:
			reconstruction.configuration.configMode[self.classname]['MenuText']
			return reconstruction.configuration.configMode[self.classname]
		except:
			return {
			'Pixmap'  : 'Std_Tool2',  
			'MenuText': self.classname, 
			'ToolTip': "self.tooltip"
			}




def createcmd2(cmd='CV',pixmap='Std_Tool1',menutext=None,tooltip=None):
	global makeCV_master2
	try:
		FreeCADGui.addCommand(cmd, makeCV_master2(cmd))
		cvCmds.append(cmd)
	except:
		pass


#----------------------------------------

cvCmds=[]

if 0:
	#createcmd('CV','Std_Tool2','cv base','cv tipp2')
	#createcmd('CV_demo','Std_Tool3','demo ','demo tipp2')
	createcmd('CV_cornerharris','Std_Tool1','corner Harris','corner Harris')
	createcmd('CV_canny','Std_Tool2','edge Canny','edge Canny')
	createcmd('CV_opening','Std_Tool3','opening','opening')
	createcmd('CV_closing','Std_Tool3','closing','closing')
	createcmd('CV_combiner','Std_Tool1','combiner','combiner')

#-----------------------------------------

#
# neue version
#

for m in reconstruction.configuration.modes:
	createcmd2(m)

#------------------------------------------


# fast command adder template

import os, reconstruction
global __dir__
__dir__ = os.path.dirname(reconstruction.__file__)


global _Command
class _Command():

	def __init__(self,lib=None,name=None,icon='/../icons/eye.svg',command=None,modul='reconstruction'):

		if lib==None: lmod=modul
		else: lmod=modul+'.'+lib
		if command==None: command=lmod+".run()"
		else: command =lmod + "."+command

		self.lmod=lmod
		self.command=command
		self.modul=modul
		self.icon=  __dir__+ icon

		if name==None: name=command
		self.name=name


	def GetResources(self): 
		return {'Pixmap' : self.icon, 'MenuText': self.name, 'ToolTip': self.name } 

	def IsActive(self):
		if FreeCADGui.ActiveDocument: return True
		else: return False

	def Activated(self):
		#FreeCAD.ActiveDocument.openTransaction("create " + self.name)
		if self.command <> '':
			if self.modul <>'': modul=self.modul
			else: modul=self.name
			FreeCADGui.doCommand("import " + modul)
			FreeCADGui.doCommand("import "+self.lmod)
			FreeCADGui.doCommand("reload("+self.lmod+")")
			FreeCADGui.doCommand(self.command)
		#FreeCAD.ActiveDocument.commitTransaction()
		FreeCAD.ActiveDocument.recompute()


class _alwaysActive(_Command):

	def IsActive(self):
			return True




#-----------------------------------------------
def always():
	return True

def ondocument():
	return FreeCADGui.ActiveDocument <> None

def onselection():
	return len(FreeCADGui.Selection.getSelection())>0

def onselection1():
	return len(FreeCADGui.Selection.getSelection())==1

def onselection2():
	return len(FreeCADGui.Selection.getSelection())==2

def onselection3():
	return len(FreeCADGui.Selection.getSelection())==3

def onselex():
	return len(FreeCADGui.Selection.getSelectionEx())<>0

def onselex1():
	return len(FreeCADGui.Selection.getSelectionEx())==1


FreeCAD.tcmds6=[]

def c1(menu,name,*info):
	global _Command
	name1="Reconstruction_"+name
	t=_Command(name,*info)
	FreeCADGui.addCommand(name1,t)
	FreeCAD.tcmds6.append([menu,name1])

def c1a(menu,isactive,name,*info):
	global _Command
	name1="Reconstruction_"+name
	t=_Command(name,*info)
	t.IsActive=isactive
	FreeCADGui.addCommand(name1,t)
	FreeCAD.tcmds6.append([menu,name1])

def c2(menu,title,name,*info):
	print info
	global _Command
	title1="Reconstruction_"+title
	FreeCADGui.addCommand(title1,_Command(name,*info))
	FreeCAD.tcmds6.append([menu,title1])

def c2a(menu,isactive,title,name,*info):
	print info
	global _Command
	t=_Command(name,*info)
	title1="Reconstruction_"+title
	t.IsActive=isactive
	FreeCADGui.addCommand(title1,t)
	FreeCAD.tcmds6.append([menu,title1])

#-------------------------------

# special conditions fore actions
def onneedle():
	dokname=FreeCAD.ParamGet('User parameter:Plugins/reconstruction').GetString("Document","Needle")
	try: App.getDocument(dokname); return True
	except: return False

def onspread():
	try: App.ActiveDocument.Spreadsheet;return True
	except: return False





if FreeCAD.GuiUp:

	c1a(["Image"],always,"perspective_trafo","perspective trafo",'/../icons/perspective_trafo.svg')
	c1a(["Image"],always,"perspective_trafo_sketch","align bordersfr perspective trafo",'/../icons/align_borders_for_perspective_trafo.svg')


	for cmd in FreeCADGui.listCommands():
		if cmd.startswith("Reconstruction_"):
			print cmd




class Reconstruction ( Workbench ):
	'''Reconstruction'''
	
	MenuText = "Reconstruction"
	ToolTip = "Reconstruct from images"

	def GetClassName(self):
		return "Gui::PythonWorkbench"

	def Initialize(self):
		global cvCmds
		cmds= ['Nurbs Editor',"houghlines","Import Image","makeSphere","makeCylinder","makePlane","makePrism","makeCV",'Point Cloud Composer']
		cmds += cvCmds
#		cmds2 = ['Perspective Image Trafo']
#		self.appendToolbar("Image Tools", cmds2 )

	##	self.appendToolbar("Reconstruction", cmds )
		self.appendMenu("Reconstruction", cmds)
		Log ("Loading Reconstruction Workbench ... done\n")

		menues={}
		for (c,a) in FreeCAD.tcmds6:
			try:menues[tuple(c)].append(a)
			except: menues[tuple(c)]=[a]

		for m in menues:
			print m
			print menues[m]
			self.appendMenu(list(m),menues[m])
			self.appendToolbar(list(m)[0],menues[m])


	Icon = """
/* XPM */
static char * osm_xpm[] = {
"64 64 260 2",
"  	c #42426F",
". 	c #424270",
"+ 	c #434370",
"@ 	c #444470",
"# 	c #444471",
"$ 	c #464674",
"% 	c #454571",
"& 	c #42426B",
"* 	c #22222C",
"= 	c #24242F",
"- 	c #4B4B7D",
"; 	c #484877",
"> 	c #474775",
", 	c #3E3E62",
"' 	c #201614",
") 	c #291818",
"! 	c #2A1818",
"~ 	c #141715",
"{ 	c #161715",
"] 	c #282838",
"^ 	c #42426C",
"/ 	c #43436E",
"( 	c #454572",
"_ 	c #484878",
": 	c #12140F",
"< 	c #A11010",
"[ 	c #FF0909",
"} 	c #871212",
"| 	c #901111",
"1 	c #911111",
"2 	c #591413",
"3 	c #061715",
"4 	c #081715",
"5 	c #071715",
"6 	c #192129",
"7 	c #2D2D41",
"8 	c #494979",
"9 	c #151715",
"0 	c #991111",
"a 	c #FF0A0A",
"b 	c #FB0A0A",
"c 	c #F40B0B",
"d 	c #8F1111",
"e 	c #161919",
"f 	c #242430",
"g 	c #311717",
"h 	c #23232D",
"i 	c #4B4B7E",
"j 	c #131714",
"k 	c #201919",
"l 	c #25232E",
"m 	c #464672",
"n 	c #484875",
"o 	c #212129",
"p 	c #311818",
"q 	c #FE0A0A",
"r 	c #FF0808",
"s 	c #061817",
"t 	c #383857",
"u 	c #2F1818",
"v 	c #071918",
"w 	c #393958",
"x 	c #031918",
"y 	c #3A3A5A",
"z 	c #DB0C0D",
"A 	c #0A140E",
"B 	c #494977",
"C 	c #25242E",
"D 	c #CC0D0D",
"E 	c #0D1613",
"F 	c #383856",
"G 	c #D30D0D",
"H 	c #171613",
"I 	c #42426A",
"J 	c #464673",
"K 	c #474773",
"L 	c #3A3A59",
"M 	c #601515",
"N 	c #191919",
"O 	c #4A4A79",
"P 	c #5C1515",
"Q 	c #1B1B1D",
"R 	c #3C3B5C",
"S 	c #001918",
"T 	c #9D1010",
"U 	c #181B1C",
"V 	c #404066",
"W 	c #484876",
"X 	c #141C1E",
"Y 	c #AE0F0F",
"Z 	c #111919",
"` 	c #2F2F43",
" .	c #0C1613",
"..	c #CB0D0D",
"+.	c #0E1A19",
"@.	c #302F45",
"#.	c #474774",
"$.	c #2C2C3E",
"%.	c #3F1514",
"&.	c #F00B0B",
"*.	c #162026",
"=.	c #45456F",
"-.	c #484873",
";.	c #4B4B79",
">.	c #45456D",
",.	c #404064",
"'.	c #171A1C",
").	c #A41010",
"!.	c #F30B0B",
"~.	c #001715",
"{.	c #474771",
"].	c #2F2F44",
"^.	c #7F1212",
"/.	c #1C1D20",
"(.	c #484874",
"_.	c #282B3C",
":.	c #3C1717",
"<.	c #4C4C7C",
"[.	c #001713",
"}.	c #FD0A0A",
"|.	c #171818",
"1.	c #323249",
"2.	c #494976",
"3.	c #4C4C7B",
"4.	c #151613",
"5.	c #931111",
"6.	c #181919",
"7.	c #262632",
"8.	c #494974",
"9.	c #4F4F7F",
"0.	c #8A1212",
"a.	c #981111",
"b.	c #131410",
"c.	c #4F4F80",
"d.	c #4A4A77",
"e.	c #292937",
"f.	c #271818",
"g.	c #F50B0B",
"h.	c #151614",
"i.	c #414165",
"j.	c #494975",
"k.	c #4B4B77",
"l.	c #262631",
"m.	c #241818",
"n.	c #FA0A0A",
"o.	c #061613",
"p.	c #414164",
"q.	c #101C1F",
"r.	c #C80E0E",
"s.	c #531515",
"t.	c #242937",
"u.	c #484872",
"v.	c #3D3D5D",
"w.	c #061917",
"x.	c #121919",
"y.	c #313147",
"z.	c #4A4A76",
"A.	c #262A39",
"B.	c #621313",
"C.	c #501515",
"D.	c #1C1B1E",
"E.	c #4E4E7D",
"F.	c #4A4A75",
"G.	c #0B1612",
"H.	c #C30E0E",
"I.	c #5F1515",
"J.	c #4D4D7B",
"K.	c #591515",
"L.	c #071613",
"M.	c #4F4F7E",
"N.	c #1E1D20",
"O.	c #461616",
"P.	c #0A130D",
"Q.	c #4C4C78",
"R.	c #313146",
"S.	c #0F1918",
"T.	c #EE0B0B",
"U.	c #3E3D5D",
"V.	c #3F3F60",
"W.	c #34344B",
"X.	c #051510",
"Y.	c #081714",
"Z.	c #111614",
"`.	c #8F1112",
" +	c #831212",
".+	c #161F23",
"++	c #44446A",
"@+	c #474770",
"#+	c #484871",
"$+	c #141411",
"%+	c #161716",
"&+	c #251818",
"*+	c #3A1717",
"=+	c #24242D",
"-+	c #4B4B75",
";+	c #4F4F7C",
">+	c #50507E",
",+	c #25252E",
"'+	c #282834",
")+	c #242631",
"!+	c #041715",
"~+	c #021917",
"{+	c #C70E0E",
"]+	c #F90A0A",
"^+	c #EB0B0B",
"/+	c #281717",
"(+	c #303044",
"_+	c #4C4C77",
":+	c #3F3F5F",
"<+	c #414162",
"[+	c #09130D",
"}+	c #401615",
"|+	c #491616",
"1+	c #C10E0E",
"2+	c #961111",
"3+	c #141714",
"4+	c #272732",
"5+	c #1E1E22",
"6+	c #141B1D",
"7+	c #0B1919",
"8+	c #E70C0C",
"9+	c #8B1111",
"0+	c #191B1D",
"a+	c #4E4E7B",
"b+	c #4B4B76",
"c+	c #4D4D7A",
"d+	c #4E4E7C",
"e+	c #35354D",
"f+	c #05140F",
"g+	c #011714",
"h+	c #841212",
"i+	c #DA0C0C",
"j+	c #001612",
"k+	c #494871",
"l+	c #4A4A73",
"m+	c #4D4D79",
"n+	c #141511",
"o+	c #1C1818",
"p+	c #1F1919",
"q+	c #7B1313",
"r+	c #1A1919",
"s+	c #2E2E41",
"t+	c #373751",
"u+	c #1B222A",
"v+	c #001816",
"w+	c #C00E0E",
"x+	c #BF0E0E",
"y+	c #2E2E40",
"z+	c #4C4C76",
"A+	c #4D4D78",
"B+	c #494970",
"C+	c #454569",
"D+	c #0D130D",
"E+	c #131817",
"F+	c #1A1A1B",
"G+	c #494971",
"H+	c #2F2F41",
"I+	c #212127",
"J+	c #4E4E79",
"K+	c #4F4F7B",
"                                                                                                                                ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
"+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ",
"+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ",
"+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ",
"+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ",
"+ + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + + ",
"@ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ ",
"@ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ ",
"# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ",
"# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ",
"# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ",
"# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ",
"# # # # # # # # # # # # # # # # # # # # # # # $ $ $ $ $ $ $ # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ",
"% % % % % % % % % % % % % % % % % % % % % % & * = = = = = = - ; ; ; ; > % % % % % % % % % % % % % % % % % % % % % % % % % % % % ",
"% % % % % % % % % % % % % % % % % % % % % % , ' ) ) ) ) ) ! ~ { { { { ] ^ & & & / ( % % % % % % % % % % % % % % % % % % % % % % ",
"% % % % % % % % % % % % % % % % % % % % % _ : < [ [ [ [ [ [ } | | | 1 2 3 4 4 5 6 7 8 % % % % % % % % % % % % % % % % % % % % % ",
"( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( _ 9 0 a a a a a a a a a a a b c c c c d e f > ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ",
"( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( _ 9 0 a a a a a a a a a a a a a a a a [ g h > ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ",
"( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( i j 1 a a a a a a a a a a a a a a a a [ k l ; ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ( ",
"m m m m m m m m m m m m m m m m m m m m n o p [ a a a a a a a a a a a a a a a a q r s t m m m m m m m m m m m m m m m m m m m m ",
"m m m m m m m m m m m m m m m m m m m m n h u [ a a a a a a a a a a a a a a a a a [ v w m m m m m m m m m m m m m m m m m m m m ",
"m m m m m m m m m m m m m m m m m m m m n h u [ a a a a a a a a a a a a a a a a a [ x y m m m m m m m m m m m m m m m m m m m m ",
"m m m m m m m m m m m m m m m m m m m m n h u [ a a a a a a a a a a a a a a a a a q z A n m m m m m m m m m m m m m m m m m m m ",
"m m m m m m m m m m m m m m m m m m m m B C k [ a a a a a a a a a a a a a a a a a a D E > m m m m m m m m m m m m m m m m m m m ",
"m m m m m m m m m m m m m m m m m m m m F s r q a a a a a a a a a a a a a a a a a a G H I J m m m m m m m m m m m m m m m m m m ",
"K K K K K K K K K K K K K K K K K K K K L v [ a a a a a a a a a a a a a a a a a a a [ M N O K K K K K K K K K K K K K K K K K K ",
"K K K K K K K K K K K K K K K K K K K K L v [ a a a a a a a a a a a a a a a a a a a a P Q O K K K K K K K K K K K K K K K K K K ",
"K K K K K K K K K K K K K K K K K K K K R S [ a a a a a a a a a a a a a a a a a a a a T U V K K K K K K K K K K K K K K K K K K ",
"K K K K K K K K K K K K K K K K K K K W X Y a a a a a a a a a a a a a a a a a a a a a [ Z ` K K K K K K K K K K K K K K K K K K ",
"K K K K K K K K K K K K K K K K K K K B  ...a a a a a a a a a a a a a a a a a a a a a [ +.@.#.K K K K K K K K K K K K K K K K K ",
"K K K K K K K K K K K K K K K K K K B $.%.&.a a a a a a a a a a a a a a a a a a a a a a < *.=.K K K K K K K K K K K K K K K K K ",
"-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.;.Q P a a a a a a a a a a a a a a a a a a a a a a a c 5 >.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.",
"-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.,.'.).a a a a a a a a a a a a a a a a a a a a a a a !.~.{.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.",
"-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.].Z [ a a a a a a a a a a a a a a a a a a a a a a a q ^./.;.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.",
"(.(.(.(.(.(.(.(.(.(.(.(.(.(.(.(.(.-._.:.[ a a a a a a a a a a a a a a a a a a a a a a a a | { <.(.(.(.(.(.(.(.(.(.(.(.(.(.(.(.(.",
"(.(.(.(.(.(.(.(.(.(.(.(.(.(.(.(.(.(.[.}.q a a a a a a a a a a a a a a a a a a a a a a a a | |.1.2.(.(.(.(.(.(.(.(.(.(.(.(.(.(.(.",
"(.(.(.(.(.(.(.(.(.(.(.(.(.(.(.(.3.4.5.a a a a a a a a a a a a a a a a a a a a a a a a a a | 6.7.B (.(.(.(.(.(.(.(.(.(.(.(.(.(.(.",
"8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.9.9 0.a a a a a a a a a a a a a a a a a a a a a a a a a a a.b.c.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.",
"8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.d.e.f.a a a a a a a a a a a a a a a a a a a a a a a a a a g.h.i.j.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.",
"8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.k.l.m.[ a a a a a a a a a a a a a a a a a a a a a a a a a n.o.>.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.",
"8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.p.q.r.a a a a a a a a a a a a a a a a a a a a a a a a a [ s.t.u.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.",
"8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.v.w.[ a a a a a a a a a a a a a a a a a a a a a a a a a [ x.y.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.",
"8.8.8.8.8.8.8.8.8.8.8.8.8.8.z.A.B.a a a a a a a a a a a a a a a a a a a a a a a a a a C.D.E.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.8.",
"F.F.F.F.F.F.F.F.F.F.F.F.F.F.E.G.H.a a a a a a a a a a a a a a a a a a a a a a a a a [ I.N J.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.",
"F.F.F.F.F.F.F.F.F.F.F.F.F.J.N K.[ a a a a a a a a a a a a a a a a a a a a a a a a a r.L.9.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.",
"F.F.F.F.F.F.F.F.F.F.F.F.F.M.N.O.a a a a a a a a a a a a a a a a a a a a a a a a a q z P.Q.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.",
"F.F.F.F.F.F.F.F.F.F.F.F.F.R.S.a T.&.a a a a a a a a a a a a a a a a a a a a a a a [ S U.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.",
"F.F.F.F.F.F.F.F.F.F.F.F.F.V.W.X.Y.Z.`. +r [ [ q a a a a a a a a a a a a a a a a a 0 .+++F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.",
"F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.@+#+++$+%+&+m.*+[ [ q a a a a a a a a a a a a a a [ u =+Q.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.F.",
"-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+;+>+,+'+)+!+~+{+]+[ a a a a a a a a a a a a ^+/+(+_+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+",
"-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+Q._+-+:+<+[+}+|+1+[ q a a a a a a a a a 2+3+>+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+",
"-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+>+4+5+6+7+]+8+a a a a a a a a 9+0+a+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+",
"b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+c+d+V.e+f+g+h+i+[ [ a a q [ j+k+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+",
"b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+l+m+n+o+p+q+[ a [ r+s+k.b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+",
"b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+M.t+e.u+v+w+x+e y+k.b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+b+",
"z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+_+A+B+C+D+E+F+G+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+",
"z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+>+H+I+;+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+",
"z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+J+K+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+",
"z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+",
"z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+z+",
"_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+"};
"""

FreeCADGui.addWorkbench(Reconstruction)
