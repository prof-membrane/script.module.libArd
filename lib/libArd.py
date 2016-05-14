# -*- coding: utf-8 -*-
import listing
import rssparser
import player
import subtitle
import libArdJsonParser

import libMediathek

pluginpath = 'plugin://script.module.libArd/'
#libMediathek.addEntry(d) = addEntry(d)

#u = "http://www.ardmediathek.de/appdata/servlet/tv/sendungAbisZ?json"
u2 = "http://www.ardmediathek.de/appdata/servlet/tv/sendungVerpasst?json&kanal=5868&tag=2"
#u3 = "http://www.ardmediathek.de/appdata/servlet/tv/Sendung?documentId=3822076&json"
u3 = "http://www.ardmediathek.de/appdata/servlet/tv/Sendung?documentId=32325376&json"
#libArdJsonParser.parseAZ(u)
#libArdJsonParser.parseDate(u2)
#libArdJsonParser.parseVideos(u3)

def getNew():
	return listing.listRSS('http://www.ardmediathek.de/tv/Neueste-Videos/mehr?documentId=23644268&m23644322=quelle.tv&rss=true')
def getMostViewed():
	return listing.listRSS('http://www.ardmediathek.de/tv/Meistabgerufene-Videos/mehr?documentId=21282514&m23644322=quelle.tv&rss=true')
def getAZ(letter):
	#return listing.getAZ(letter)
	return libArdJsonParser.parseAZ(letter)
def getDate(url):
	return listing.listDate(url)
def getSearch(search_string,page=0):
	return listing.listVideos('http://www.ardmediathek.de/suche?searchText='+search_string.replace(" ", "+"))

def getVideoUrl(videoID,sub=False):
	xbmc.log(videoID)
	if sub:
		#videoID = url.split('documentId=')[1]
		#if '&' in videoID:
		#	videoID = videoID.split('&')[0]
		return player.getVideoUrl(videoID=videoID),subtitle.getSub(videoID)
	else:
		return player.getVideoUrl(videoID=videoID),False
def getPage(url,page=1):
	return listing.listRSS(url,page)
	
#def getAZ(letter):
#	return listing.getAZ(letter)
def getVideosJson(url):
	return libArdJsonParser.parseVideos(url)

def getVideosXml(videoId):
	return listing.getVideosXml(videoId)
def parser(data):
	return rssparser.parser(data)
	
def libArdPvrPlay(dict):
	import libArdPvr
	libArdPvr.play(dict)
	
import time
import urllib,urllib2,re,random,xbmc,xbmcplugin,xbmcgui,xbmcaddon,cookielib,HTMLParser,datetime
import sys
from datetime import date, timedelta
try:
	xbmc.log(sys.argv[0])
	xbmc.log(sys.argv[1])
	xbmc.log(sys.argv[2])
	pluginhandle = int(sys.argv[1])
except: pass
hideAudioDisa = True
showSubtitles = False
helix = False
fanart = ''

addon = xbmcaddon.Addon()
transAddon = addon.getLocalizedString
transBuildin = xbmc.getLocalizedString
weekdayDict = { '0': transBuildin(17),#Sonntag
				'1': transBuildin(11),#Montag
				'2': transBuildin(12),#Dienstag
				'3': transBuildin(13),#Mittwoch
				'4': transBuildin(14),#Donnerstag
				'5': transBuildin(15),#Freitag
				'6': transBuildin(16),#Samstag
				}

cannelList = [['3sat',                  'ZDF',  '1209116'],
			  ['ARD-alpha',             'ARD',  '5868'   ],
			  ['Arte',                  'Arte', ''       ],
			  ['BR',                    'ARD',  '2224'   ],
			  ['Einsfestival',          'ARD',  '673348' ],
			  ['EinsPlus',              'ARD',  '4178842'],
			  ['Das Erste',             'ARD',  '208'    ],
			  ['HR',                    'ARD',  '5884'   ],
			  ['MDR Fernsehen',         'ARD',  '5882'   ],
			  ['MDR Thüringen',         'ARD',  '1386988'],
			  ['MDR Sachsen',           'ARD',  '1386804'],
			  ['MDR Sachsen-Anhalt',    'ARD',  '1386898'],
			  ['NDR Fernsehen',         'ARD',  '5906'   ],
			  ['Phoenix',               'ZDF',  '2256088'],
			  ['RB',                    'ARD',  '5898'   ],
			  ['RBB',                   'ARD',  '5874'   ],
			  ['SR',                    'ARD',  '5870'   ],
			  ['SWR Fernsehen',         'ARD',  '5310'   ],
			  ['SWR Rheinland-Pfalz',   'ARD',  '5872'   ],
			  ['SWR Baden-Württemberg', 'ARD',  '5904'   ],
			  ['tagesschau24',          'ARD',  '5878'   ],
			  ['WDR',                   'ARD',  '5902'   ],
			  ['ZDF',                   'ZDF',  '1209114'],
			  ['ZDFinfo',               'ZDF',  '1209120'],
			  ['ZDF.kultur',            'ZDF',  '1317640'],
			  ['ZDFneo',                'ZDF',  '1209122']]
			  
def libArdListMain():
	libMediathek.addEntry({'name':'Neu', 'mode':'libArdListVideosSinglePage', 'url':'http://www.ardmediathek.de/tv/Neueste-Videos/mehr?documentId=23644268&m23644322=quelle.tv&rss=true', 'pluginpath': pluginpath})
	libMediathek.addEntry({'name':'MV', 'mode':'libArdListVideosSinglePage', 'url':'http://www.ardmediathek.de/tv/Meistabgerufene-Videos/mehr?documentId=21282514&m23644322=quelle.tv&rss=true', 'pluginpath': pluginpath})
	libMediathek.addEntry({'name':'Sendungen A-Z', 'mode':'libArdListLetters', 'pluginpath': pluginpath})
	libMediathek.addEntry({'name':'Sendung nach Datum', 'mode':'libArdListDate'})
	libMediathek.addEntry({'name':'Suche', 'mode':'libArdSearch', 'pluginpath': pluginpath})
	
def libArdListVideos():
	page = params.get('page','1')
	xbmc.log(str(params))
	#items,nextPage = getPage(params['url'],page)
	items = getVideosJson(params['url'])#,page)
	for dict in items:
		if "showname" in params and dict['name'].startswith(params['showname']):
			i = len(params['showname'])
			i+=3 # ' - '
			dict['name'] = dict['name'][i:]
		libMediathek.addEntry(dict)
		
def libArdListVideosSinglePage():
	page = params.get('page','1')
	xbmc.log(str(params))
	items,nextPage = getPage(params['url'],page)
	#items = getVideosJson(params['url'])#,page)
	for dict in items:
		if "showname" in params and dict['name'].startswith(params['showname']):
			i = len(params['showname'])
			i+=3 # ' - '
			dict['name'] = dict['name'][i:]
		libMediathek.addEntry(dict)
	#if nextPage:
	#	addDir({'name':transBuildin(33078),'url':params['url'],'page':str(int(page)+1),'thumb':params.get('fanart',''), 'fanart':params.get('fanart',''), 'mode':'libArdListVideos'})
	
def libArdListLetters():
	dict = {}
	dict['name'] = "0-9"
	dict['letter'] = '0-9'
	dict['mode'] = 'libArdListShows'
	addDir(dict)
	letters = [chr(i) for i in xrange(ord('a'), ord('z')+1)]
	for letter in letters:
		letter = letter.upper()
		dict['name'] = letter
		dict['letter'] = letter
		if letter != "X" and letter != "Y":
			addDir(dict)
	
def libArdListShows():
	items = getAZ(params['letter'])
	for dict in items:
		dict['mode'] = 'libArdListVideos'
		addDir(dict)
	
def libArdListDate():
	dict = {}
	dict['mode'] = 'libArdListDateChannels'
	dict['name'] = 'Heute'#translation(31020)
	dict['datum']  = '0'
	addDir(dict)
	dict['name'] = 'Gestern'#translation(31021)
	dict['datum']  = '1'
	addDir(dict)
	i = 2
	while i <= 6:
		day = date.today() - timedelta(i)
		dict['name'] = weekdayDict[day.strftime("%w")]
		dict['datum']  = str(i)
		addDir(dict)
		i += 1
	
def libArdListDateChannels(datum=False):
	if not datum:#TODO: share global params gracefully
		datum = params['datum']
	dict = {}
	for channel,source,id in cannelList:
		if source == 'ARD':
			dict['mode'] = 'libArdListDateVideos'
			dict['name'] = channel
			dict['url']  = 'http://www.ardmediathek.de/tv/sendungVerpasst?tag='+datum+'&kanal='+id
			addDir(dict)
	
def libArdListDateVideos():
	items = getDate(params['url'])
	for dict in items:
		dict['mode'] = 'libArdPlay'
		addLink(dict)
	
def libArdSearch():
	keyboard = xbmc.Keyboard('', 'TODO')
	keyboard.doModal()
	if keyboard.isConfirmed() and keyboard.getText():
		libArdListSearch(keyboard.getText())
		

def libArdListSearch(searchString):
	list = getSearch(searchString)
	for dict in list:
		dict['mode'] = 'libArdPlay'
		addLink(dict)
	
def libArdPlay():
	xbmc.log(str(params))
	url,sub = getVideoUrl(params['documentId'],showSubtitles)
	listitem = xbmcgui.ListItem(path=url)
	if showSubtitles and helix and sub:
		listitem.setSubtitles(sub)
	if url:
		xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	else:
		xbmcplugin.setResolvedUrl(pluginhandle, False, listitem)
	
def addLink(dict):
	name = dict['name']#.encode('utf8')
	url  = dict['url']
	mode = dict['mode']
	iconimage = dict['thumb']
	if dict.has_key('plot'):
		plot = dict['plot']
	else:
		plot = ''
	if dict.has_key('duration'):
		duration = dict['duration']
	else:
		duration = ''
	if dict.has_key('fanart'):
		fanart = dict['fanart']
	else:
		fanart = ''
	if hideAudioDisa:
		if 'Hörfassung' in name or 'Audiodeskription' in name:
			return False
	name = name.replace('&amp;','&')
	#u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	u = buildUri(dict)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": plot , "Plotoutline": plot , "Duration": duration , "ShareOnTV" : "true"} )
	liz.setProperty('IsPlayable', 'true')
	if fanart:
		liz.setProperty('fanart_image',fanart)
	else:
		liz.setProperty('fanart_image',iconimage)
	xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok

def addDir(dict):
	u = buildUri(dict)
	ok=True
	liz=xbmcgui.ListItem(dict.get('name',''), iconImage="DefaultFolder.png", thumbnailImage=dict.get('thumb',''))
	liz.setInfo( type="Video", infoLabels={ "Title": dict.get('name','') , "Plot": dict.get('plot','') , "Plotoutline": dict.get('plot','') } )
	liz.setProperty('fanart_image',dict.get('thumb',''))
	xbmcplugin.setContent( handle=int( sys.argv[ 1 ] ), content="episodes" )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok
	
def buildUri(dict):
	#u = sys.argv[0]+'?'
	xbmc.log(sys.argv[0])
	u = 'plugin://script.module.libArd/'+'?'
	i = 0
	for key in dict.keys():
		if i > 0:
			u += '&'
		if isinstance(dict[key], basestring):
			dict[key] = dict[key]#.encode('utf8')
		else:
			dict[key] = str(dict[key])
		u += key + '=' + urllib.quote_plus(dict[key])
		i += 1
	return u
	
params = {}
def list(p=False):	
	global params
	if p:
		params = p
	else:
		params = get_params()
	
	for key,val in params.items():
		print key
		print val
		print urllib.unquote_plus(val)
		try:
			params[key] = urllib.unquote_plus(val)
		except: 
			print 'Cant unquote this: '+ str(val)

	if not params.has_key('mode'):
		libArdListMain()
	elif params['mode']=='libArdListVideos':
		libArdListVideos()
	elif params['mode']=='libArdListVideosSinglePage':
		libArdListVideosSinglePage()
	elif params['mode']=='libArdListLetters':
		libArdListLetters()
	elif params['mode']=='libArdListShows':
		libArdListShows()
	elif params['mode']=='libArdListDate':
		libArdListDate()
	elif params['mode']=='libArdListDateChannels':
		libArdListDateChannels()
	elif params['mode']=='libArdListDateVideos':
		libArdListDateVideos()
	elif params['mode']=='libArdSearch':
		libArdSearch()
	elif params['mode']=='libArdListSearch':
		libArdListSearch(params["searchString"])
	elif params['mode']=='libArdPlay':
		libArdPlay()
	else:
		libArdListMain()
	xbmcplugin.endOfDirectory(int(sys.argv[1]))	

def get_params():
	param={}
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
								
	return param
	
def translation(i):
	if i >=30000 and i <= 32999:
		addon.getLocalizedString(i)
	else:
		xbmc.getLocalizedString(i)