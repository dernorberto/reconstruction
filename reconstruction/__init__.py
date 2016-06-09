

def sayErr():
	print("--------------ERROR loading reconstruction workbench ---------------------")

#try: raise Exception("test exception from reconstruction")
#except: sayErr()

try: import reconstruction.makePlane
except: sayErr()

try: import reconstruction.makeSphere
except: sayErr()

try: import reconstruction.makeCylinder
except: sayErr()

try: import reconstruction.makePrism
except: sayErr()

try: import reconstruction.projectiontools
except: sayErr()

try: import reconstruction.houghlines
except: sayErr()
