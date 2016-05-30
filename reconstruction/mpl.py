# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- reconstruction workbench
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import PySide
from PySide import QtCore, QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MatplotlibWidget(FigureCanvas):

	def __init__(self, parent=None, width=5, height=4, dpi=100):

		super(MatplotlibWidget, self).__init__(Figure())
		self.setParent(parent)
		self.figure = Figure(figsize=(width, height), dpi=dpi) 
		self.canvas = FigureCanvas(self.figure)

		FigureCanvas.setSizePolicy(self,
				QtGui.QSizePolicy.Expanding,
				QtGui.QSizePolicy.Expanding)

		FigureCanvas.updateGeometry(self)
		self.axes = self.figure.add_subplot(111)
		self.setMinimumSize(self.size()*0.3)

		print("---------------------- done")




	def subplot(self,label='111'):
		self.axes=self.figure.add_subplot(label)

	def plot(self,*args,**args2):
		self.axes.plot(*args,**args2)
		self.draw()

	def clf(self):
		self.figure.clf()

