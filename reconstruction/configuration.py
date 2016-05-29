#
# implemented modes
#

modes=[
	'BlobDetector',
	'ImageFile',
	'Color','ColorSpace','CannyEdge',
	'FatColor',
	'GoodFeaturesToTrack',
	'HSV','HoughLines','HoughLinesPost',
	'Invert',
	'Mixer','Morphing',
	'Pathes',
	'PathAnalyzer',
	'Skeleton',
	'Threshold']


configMode= {}

configMode['test']= { 'props' : [],}

configMode['BlobDetector'] = {
	'props' : [
		['Convexity2','App::PropertyInteger','CannyEdge',100],
		['Area','App::PropertyInteger','CannyEdge',200],
		['showBlobs','App::PropertyBool','CannyEdge',True],
		['Convexity','App::PropertyInteger','CannyEdge',0],
	],


	'widgets' : [ 
		{
			'id':'Area', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'showBlobs', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'Convexity', 
			'params' : ['slider'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

#		{
#			'id':'Convexity', 
#			'params' : ['dialer'],
#			'p2w' : lambda x:x,
#			'w2p' : lambda x:x
#		},
	],
}


configMode['CannyEdge'] = {
	'a' : {2:5},
	'props' : [
		['minVal','App::PropertyInteger','CannyEdge',100],
		['maxVal','App::PropertyInteger','CannyEdge',200],
		
	],


	'widgets' : [ 
		{
			'id':'minVal', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{ 
			'id' :'maxVal',
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x		
		},
	]
	
}

configMode['GoodFeaturesToTrack'] = {
	'props' : [
		['maxCorners','App::PropertyInteger','CannyEdge',25],
		['qualityLevel','App::PropertyFloat','CannyEdge',0.01],
		['minDistance','App::PropertyInteger','CannyEdge',100],
		['useHarrisDetector','App::PropertyBool','CannyEdge',False],
		['k','App::PropertyFloat','CannyEdge',0.04],
	],

	'widgets' : [ 
		{
			'id':'maxCorners', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'minDistance', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

	
	]
}


configMode['HoughLines'] = {

	'props': [
		['canny1','App::PropertyInteger','HoughLines',100],
		['canny2','App::PropertyInteger','HoughLines',200],
		['rho','App::PropertyInteger','HoughLines',1],
		['theta','App::PropertyInteger','HoughLines',1],
		['threshold','App::PropertyInteger','HoughLines',10],
		['minLineLength','App::PropertyInteger','HoughLines',25],
		['maxLineGap','App::PropertyInteger','HoughLines',10],
		
		
		
	],
	'widgets' : [ 
		{
			'id':'threshold', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'minLineLength', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'maxLineGap', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'canny1', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'canny2', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
	]
}



configMode['HoughLinesPost'] = {

	'props': [
		['epsilon','App::PropertyInteger','HoughLines',100],
		['count','App::PropertyInteger','HoughLines',200],
		
		
		
	],
	'widgets' : [ 
		{
			'id':'epsilon', 
			'params' : ['dialernr'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'count', 
			'params' : ['dialernr'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
	]
}

configMode['HSV'] = {

	'props': [
		['onColor','App::PropertyBool','HoughLines',True],
		['invertColor','App::PropertyBool','HoughLines',False],
		['valueColor','App::PropertyInteger','HoughLines',130],
		['deltaColor','App::PropertyInteger','HoughLines',110],
		
		
		
		
	],
	'widgets' : [ 
		{
			'id':'valueColor', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'deltaColor', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
	]
}


configMode['ImageFile'] = {


	'props' : [
		['minVal','App::PropertyInteger','CannyEdge',100],
		['maxVal','App::PropertyInteger','CannyEdge',200],
		['testSlider','App::PropertyInteger','CannyEdge',10],
		['testDialer','App::PropertyInteger','CannyEdge',50],
		['testLineEdit','App::PropertyString','CannyEdge',"test"],
		['testcheckBox','App::PropertyBool','CannyEdge',True],
	],


	'widgets' : [ 
#		{ 
#			'id' :'maxVal',
#			'params' : ['dialer'],
#			'p2w' : lambda x:x+10,
#			'w2p' : lambda x:x-10		
#		},
		{
			'id':'testDialer', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'testSlider', 
			'params' : ['slider'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'testLineEdit', 
			'params' : ['lineEdit'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'testcheckBox', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},



	]

}


configMode['Skeleton'] = {

	'props' : [
		['threshold','App::PropertyInteger','CannyEdge',128],
		['otsu','App::PropertyBool','CannyEdge',True],
	],


	'widgets' : [ 
#		{ 
#			'id' :'maxVal',
#			'params' : ['dialer'],
#			'p2w' : lambda x:x+10,
#			'w2p' : lambda x:x-10		
#		},
		{
			'id':'threshold', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'otsu', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},



	]

}




configMode['Color'] = {

	'props' : [
		['red','App::PropertyBool','CannyEdge',False],
		['green','App::PropertyBool','CannyEdge',False],
		['blue','App::PropertyBool','CannyEdge',False],
	],

	'widgets' : [ 
		{
			'id':'red', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'blue', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'green', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},



	]

}


configMode['Mixer'] = {

	'props' : [
		['source2Object','App::PropertyLink','CannyEdge',None],
		['sourceOffsetX','App::PropertyInteger','CannyEdge',0],
		['sourceOffsetY','App::PropertyInteger','CannyEdge',0],
		['modeMixer','App::PropertyEnumeration','CannyEdge',['addWeighted','add',"or"]],
		['weight','App::PropertyInteger','CannyEdge',70],
		['flipOrder','App::PropertyBool','CannyEdge',False],
		['inverse','App::PropertyBool','CannyEdge',False],
		['inverse2','App::PropertyBool','CannyEdge',False],
		
		['zoom','App::PropertyBool','CannyEdge',True],
		['zoomMode','App::PropertyEnumeration','CannyEdge',['leftup','rightup',"middle"]],
		['zoomX','App::PropertyInteger','CannyEdge',0],
		['zoomX2','App::PropertyInteger','CannyEdge',100],
		['zoomY','App::PropertyInteger','CannyEdge',50],
		['zoomY2','App::PropertyInteger','CannyEdge',100],

		

#		['pathname','App::PropertyString','CannyEdge','Path'],
	],

	'widgets' : [ 
		{
			'id':'flipOrder', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'inverse', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'inverse2', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'sourceOffsetX', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'sourceOffsetY', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'weight', 
			'params' : ['dialer2'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'zoom', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'zoomX', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'zoomX2', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'zoomY', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'zoomY2', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},



	]

}



configMode['Morphing'] = {

	'props' : [
		['filter','App::PropertyEnumeration','CannyEdge',['erosion','dilation','opening','closing']],
		['kernel','App::PropertyInteger','CannyEdge',5],
	],
		'widgets' : [ 
			{
				'id':'kernel', 
				'params' : ['dialer'],
				'p2w' : lambda x:x,
				'w2p' : lambda x:x
			},

	]
}



configMode['Pathes'] = {

	'props' : [
		['modelColor','App::PropertyEnumeration','CannyEdge',['rainbow','hsv',"prism"]],
		['pathname','App::PropertyString','CannyEdge','Path'],
	],

	'widgets' : [ 



	]

}



configMode['PathAnalyzer'] = {

	'props' : [
		['pathId','App::PropertyInteger','PathAnalyzer',1],
		['pathObject','App::PropertyLink','PathAnalyzer',None],
		['pathSelection','App::PropertyBool','PathAnalyzer',False],
		['N','App::PropertyInteger','PathAnalyzer',10],
		['minPathPoints','App::PropertyInteger','PathAnalyzer',20],
		['Threshold','App::PropertyInteger','PathAnalyzer',20],
#		['ThresholdFactor','App::PropertyInteger','PathAnalyzer',10],
		['createWire','App::PropertyBool','PathAnalyzer',False],
		['hideApproximation','App::PropertyBool','PathAnalyzer',False],
		['hideLegend','App::PropertyBool','PathAnalyzer',True],
		['showPics','App::PropertyBool','PathAnalyzer',False],
		['maxRadius','App::PropertyFloat','PathAnalyzer',200],
		['useCanny','App::PropertyBool','PathAnalyzer',True],
	],

	'widgets' : [ 
		{
			'id':'N', 
			'params' : ['dialer',3,30],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'Threshold', 
			'params' : ['dialer',1,200],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},
		{
			'id':'createWire', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},


	]

}


configMode['Threshold'] = {


	'props' : [
		['globalThresholding','App::PropertyBool','CannyEdge',False],
		['adaptiveMeanTresholding','App::PropertyBool','CannyEdge',False],
		['adaptiveGaussianThresholding','App::PropertyBool','CannyEdge',False],
		['param1','App::PropertyInteger','CannyEdge',100],
		['param2','App::PropertyInteger','CannyEdge',150],

	],


	'widgets' : [ 

		{
			'id':'globalThresholding', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'adaptiveMeanTresholding', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'adaptiveGaussianThresholding', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'param1', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},


		{
			'id':'param2', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},




	]

}


configMode['ColorSpace'] = {


	'props' : [
		['globalThresholding','App::PropertyBool','CannyEdge',False],
		['adaptiveMeanTresholding','App::PropertyBool','CannyEdge',False],
		['adaptiveGaussianThresholding','App::PropertyBool','CannyEdge',False],
		['h1','App::PropertyInteger','CannyEdge',100],
		['h2','App::PropertyInteger','CannyEdge',150],
		['s1','App::PropertyInteger','CannyEdge',100],
		['s2','App::PropertyInteger','CannyEdge',150],
		['v1','App::PropertyInteger','CannyEdge',100],
		['v2','App::PropertyInteger','CannyEdge',255],


	],


	'widgets' : [ 

		{
			'id':'globalThresholding', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'adaptiveMeanTresholding', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'adaptiveGaussianThresholding', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'h1', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},


		{
			'id':'h2', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},


		{
			'id':'s1', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},


		{
			'id':'s2', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},



		{
			'id':'v1', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},


		{
			'id':'v2', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},




	]

}


configMode['FatColor'] = {


	'props' : [
		['globalThresholding','App::PropertyBool','CannyEdge',False],
		['adaptiveMeanTresholding','App::PropertyBool','CannyEdge',False],
		['adaptiveGaussianThresholding','App::PropertyBool','CannyEdge',False],
		['h1','App::PropertyInteger','CannyEdge',100],
		['h2','App::PropertyInteger','CannyEdge',150],
		['s1','App::PropertyInteger','CannyEdge',100],
		['s2','App::PropertyInteger','CannyEdge',150],
		['v1','App::PropertyInteger','CannyEdge',100],
		['v2','App::PropertyInteger','CannyEdge',255],


	],


	'widgets' : [ 

		{
			'id':'globalThresholding', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'adaptiveMeanTresholding', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'adaptiveGaussianThresholding', 
			'params' : ['checkBox'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},

		{
			'id':'h1', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},


		{
			'id':'h2', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},


		{
			'id':'s1', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},


		{
			'id':'s2', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},



		{
			'id':'v1', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},


		{
			'id':'v2', 
			'params' : ['dialer'],
			'p2w' : lambda x:x,
			'w2p' : lambda x:x
		},




	]

}










