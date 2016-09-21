# -*- coding: utf-8 -*-
import listing
import rssparser
import player
import subtitle
import libArdJsonParser

import libMediathek
import _utils
import xbmc,xbmcaddon
saveditemsfile = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')+'list.json').decode('utf-8')
lastPageFile = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')+'lastpage').decode('utf-8')
pluginpath = 'plugin://script.module.libArd/'
showSubtitles = xbmcaddon.Addon().getSetting('subtitle') == 'true'
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
def getVideosJson(url,page = '1'):
	return libArdJsonParser.parseVideos(url,page)

def getVideosXml(videoId):
	return listing.getVideosXml(videoId)
def parser(data):
	return rssparser.parser(data)

def libArdPvrDate(datum,channel):
	import libArdPvr
	return getDate('http://www.ardmediathek.de/tv/sendungVerpasst?tag='+datum+'&kanal='+libArdPvr.channelList[channel])
	
def libArdPvrPlay(dict):
	#showSubtitles = False
	url,sub = getVideoUrl(dict['documentId'],showSubtitles)
	#listitem = xbmcgui.ListItem(label=video["name"],thumbnailImage=video["thumb"],path=url)
	listitem = xbmcgui.ListItem(label=dict["name"],path=url)
	xbmc.Player().play(url, listitem)	
	
import time
import urllib,urllib2,re,random,xbmc,xbmcplugin,xbmcgui,xbmcaddon,cookielib,HTMLParser,datetime
import sys
from datetime import date, timedelta
translation = xbmcaddon.Addon(id='script.module.libMediathek').getLocalizedString
try:
	xbmc.log(sys.argv[0])
	xbmc.log(sys.argv[1])
	xbmc.log(sys.argv[2])
	pluginhandle = int(sys.argv[1])
except: pass
hideAudioDisa = True
#showSubtitles = False
helix = False
fanart = ''

addon = xbmcaddon.Addon()
transAddon = addon.getLocalizedString
transBuildin = xbmc.getLocalizedString

weekdayDict = { '0': translation(31013),#Sonntag
				'1': translation(31014),#Montag
				'2': translation(31015),#Dienstag
				'3': translation(31016),#Mittwoch
				'4': translation(31017),#Donnerstag
				'5': translation(31018),#Freitag
				'6': translation(31019),#Samstag
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
	libMediathek.addEntry({'name':translation(31030), 'mode':'libArdListVideosSinglePage', 'url':'http://www.ardmediathek.de/tv/Neueste-Videos/mehr?documentId=23644268&m23644322=quelle.tv&rss=true', 'pluginpath': pluginpath})
	libMediathek.addEntry({'name':translation(31031), 'mode':'libArdListVideosSinglePage', 'url':'http://www.ardmediathek.de/tv/Meistabgerufene-Videos/mehr?documentId=21282514&m23644322=quelle.tv&rss=true', 'pluginpath': pluginpath})
	libMediathek.addEntry({'name':translation(31032), 'mode':'libArdListLetters', 'pluginpath': pluginpath})
	libMediathek.addEntry({'name':translation(31033), 'mode':'libArdListDate'})
	libMediathek.addEntry({'name':translation(31034), 'mode':'libArdListVideos', 'url':'http://www.ardmediathek.de/appdata/servlet/tv/Rubriken/mehr?documentId=21282550&json'})
	libMediathek.addEntry({'name':translation(31035), 'mode':'libArdListVideos', 'url':'http://www.ardmediathek.de/appdata/servlet/tv/Themen/mehr?documentId=21301810&json'})
	#libMediathek.addEntry({'name':'Fußball EM 2016',  'mode':'libArdListVideos', 'url':'http://www.ardmediathek.de/appdata/servlet/tv/EM-Highlights-Spiele-Tore/Thema?documentId=35531744&json'})
	#libMediathek.addEntry({'name':'Olympia 2016',  'mode':'libArdListVideos', 'url':'http://www.ardmediathek.de/tv/Die-Olympischen-Spiele-2016/mehr?documentId=36636948'})
	libMediathek.addEntry({'name':translation(31039), 'mode':'libArdSearch', 'pluginpath': pluginpath})
	
def libArdListVideos():
	page = params.get('page','1')
	items = getVideosJson(params['url'],params.get('page','1'))#,page)
	libMediathek.addEntries(items,int(params.get('page','1')))
		
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
	libMediathek.populateDirAZ('libArdListShows')
	
def libArdListShows():
	libMediathek.addEntries(getAZ(params['name'].replace('#','0-9')))
	
def libArdListDate():
	libMediathek.populateDirDate('libArdListDateChannels')
	
def libArdListDateChannels(datum=False):
	if not datum:#TODO: share global params gracefully
		datum = params['datum']
	dict = {}
	for channel,source,id in cannelList:
		if source == 'ARD':
			dict['mode'] = 'libArdListDateVideos'
			dict['name'] = channel
			dict['url']  = 'http://www.ardmediathek.de/tv/sendungVerpasst?tag='+datum+'&kanal='+id
			libMediathek.addEntry(dict)
	
def libArdListDateVideos():
	libMediathek.addEntries(getDate(params['url']))
	
def libArdSearch():
	keyboard = xbmc.Keyboard('', 'TODO')
	keyboard.doModal()
	if keyboard.isConfirmed() and keyboard.getText():
		libArdListSearch(keyboard.getText())
		

def libArdListSearch(searchString):
	list = getSearch(searchString)
	for dict in list:
		dict['mode'] = 'libArdPlay'
		dict['type'] = 'video'
		libMediathek.addEntry(dict)
	
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
	
	
	
params = {}
def list(p=False):	
	import _utils
	global params
	if p:
		params = p
	else:
		params = libMediathek.get_params()
	
	for key,val in params.items():
		print key
		print val
		print urllib.unquote_plus(val)
		try:
			params[key] = urllib.unquote_plus(val)
		except: 
			print 'Cant unquote this: '+ str(val)

	#isCached = libMediathek.checkIfCachedVersionIsAvailable()
	if False:#isCached:
		libMediathek.retrieveCached()
	elif not params.has_key('mode'):
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