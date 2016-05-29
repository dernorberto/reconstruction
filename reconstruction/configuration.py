# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- reconstruction workbench
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

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

	'Pathes', 'PathAnalyzer',
	'Skeleton',
	'Threshold']


configMode= {}

configMode['test']= { 'props' : [],}

configMode['BlobDetector'] = {

	'props' : [
		['Convexity2','App::PropertyInteger','BlobDetector',100],
		['Area','App::PropertyInteger','BlobDetector',200],
		['showBlobs','App::PropertyBool','BlobDetector',True],
		['Convexity','App::PropertyInteger','BlobDetector',0],
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

	],
}


configMode['CannyEdge'] = {

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
		['maxCorners','App::PropertyInteger','GoodFeaturesToTrack',25],
		['qualityLevel','App::PropertyFloat','GoodFeaturesToTrack',0.01],
		['minDistance','App::PropertyInteger','GoodFeaturesToTrack',100],
		['useHarrisDetector','App::PropertyBool','GoodFeaturesToTrack',False],
		['k','App::PropertyFloat','GoodFeaturesToTrack',0.04],
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
		['epsilon','App::PropertyInteger','HoughLinesPost',100],
		['count','App::PropertyInteger','HoughLinesPost',200],
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
		['onColor','App::PropertyBool','HSV',True],
		['invertColor','App::PropertyBool','HSV',False],
		['valueColor','App::PropertyInteger','HSV',130],
		['deltaColor','App::PropertyInteger','HSV',110],
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
		['minVal','App::PropertyInteger','ImageFile',100],
		['maxVal','App::PropertyInteger','ImageFile',200],
		['testSlider','App::PropertyInteger','ImageFile',10],
		['testDialer','App::PropertyInteger','ImageFile',50],
		['testLineEdit','App::PropertyString','ImageFile',"test"],
		['testcheckBox','App::PropertyBool','ImageFile',True],
	],


	'widgets' : [ 

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
		['threshold','App::PropertyInteger','Skeleton',128],
		['otsu','App::PropertyBool','Skeleton',True],
	],

	'widgets' : [ 

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
		['red','App::PropertyBool','Color',False],
		['green','App::PropertyBool','Color',False],
		['blue','App::PropertyBool','Color',False],
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
		['source2Object','App::PropertyLink','Mixer',None],
		['sourceOffsetX','App::PropertyInteger','Mixer',0],
		['sourceOffsetY','App::PropertyInteger','Mixer',0],
		['modeMixer','App::PropertyEnumeration','Mixer',['addWeighted','add',"or"]],
		['weight','App::PropertyInteger','Mixer',70],
		['flipOrder','App::PropertyBool','Mixer',False],
		['inverse','App::PropertyBool','Mixer',False],
		['inverse2','App::PropertyBool','Mixer',False],

		['zoom','App::PropertyBool','Mixer',True],
		['zoomMode','App::PropertyEnumeration','Mixer',['leftup','rightup',"middle"]],
		['zoomX','App::PropertyInteger','Mixer',0],
		['zoomX2','App::PropertyInteger','Mixer',100],
		['zoomY','App::PropertyInteger','Mixer',50],
		['zoomY2','App::PropertyInteger','Mixer',100],
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
		['filter','App::PropertyEnumeration','Morphing',['erosion','dilation','opening','closing']],
		['kernel','App::PropertyInteger','Morphing',5],
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
		['modelColor','App::PropertyEnumeration','Pathes',['rainbow','hsv',"prism"]],
		['pathname','App::PropertyString','Pathes','Path'],
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
		['globalThresholding','App::PropertyBool','Threshold',False],
		['adaptiveMeanTresholding','App::PropertyBool','Threshold',False],
		['adaptiveGaussianThresholding','App::PropertyBool','Threshold',False],
		['param1','App::PropertyInteger','Threshold',100],
		['param2','App::PropertyInteger','Threshold',150],
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
		['globalThresholding','App::PropertyBool','ColorSpace',False],
		['adaptiveMeanTresholding','App::PropertyBool','ColorSpace',False],
		['adaptiveGaussianThresholding','App::PropertyBool','ColorSpace',False],
		['h1','App::PropertyInteger','ColorSpace',100],
		['h2','App::PropertyInteger','ColorSpace',150],
		['s1','App::PropertyInteger','ColorSpace',100],
		['s2','App::PropertyInteger','ColorSpace',150],
		['v1','App::PropertyInteger','ColorSpace',100],
		['v2','App::PropertyInteger','ColorSpace',255],
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
		['globalThresholding','App::PropertyBool','FatColor',False],
		['adaptiveMeanTresholding','App::PropertyBool','FatColor',False],
		['adaptiveGaussianThresholding','App::PropertyBool','FatColor',False],
		['h1','App::PropertyInteger','FatColor',100],
		['h2','App::PropertyInteger','FatColor',150],
		['s1','App::PropertyInteger','FatColor',100],
		['s2','App::PropertyInteger','FatColor',150],
		['v1','App::PropertyInteger','FatColor',100],
		['v2','App::PropertyInteger','FatColor',255],
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
