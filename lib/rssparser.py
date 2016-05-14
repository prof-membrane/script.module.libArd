#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import xbmcplugin
import xbmcgui
import urllib
import xbmc
import xbmcaddon
import xbmcvfs
import time
from email.utils import parsedate
#import _utils
import bcast2thumb
baseUrl = "http://www.ardmediathek.de"
defaultThumb = baseUrl+"/ard/static/pics/default/16_9/default_webM_16_9.jpg"
temp = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')+'temp').decode('utf-8')
#utils.bcastIdXml2Dict()
def parser(data):
	items = []
	list = []
	match = re.compile('<item>(.+?)</item>', re.DOTALL).findall(data)
	for item in match:
		thumb = ''
		plot = ''
		title = re.compile('<title>(.+?)</title>', re.DOTALL).findall(item)[0]
		pubDate = re.compile('<pubDate>(.+?)</pubDate>', re.DOTALL).findall(item)[0]
		xbmc.log(pubDate)
		description = re.compile('<description>(.+?)</description>', re.DOTALL).findall(item)[0]
		if '<category>' in item:
			category = cleanTitle(re.compile('<category>(.+?)</category>', re.DOTALL).findall(item)[-1])
		else:
			category = ''
		if 'img src="' in description:
			thumb = re.compile('img src="(.+?)"', re.DOTALL).findall(description)[0]
		infos = re.compile('&lt;p&gt;(.*?)&lt;/p&gt;', re.DOTALL).findall(description)
		if len(infos) >= 4:
			dict = {}
			
			if infos[1] == '' or infos[1].endswith('...') and len(infos[1]) < len(title):
				plot = title +'\n\n'+ infos[2]
			else:
				plot = infos[1].replace('\n','')+'\n\n'+infos[2]
			link = re.compile('<link>(.+?)</link>', re.DOTALL).findall(item)[0]
			try:
				tmp = link.split('/')[4]
				tmp = tmp.lower()
				if 'Video-Podcast' in link or tmp.endswith('audio') or tmp.endswith('radio'):
					continue
			except: pass
			documentId = link.split('documentId=')[1]
			if '&' in documentId:
				documentId = documentId.split('&')[0]
			split = infos[2].split('|')
			runtime = 0
			for part in split:
				if 'Min' in part or 'min' in part:
					runtime = runtimeToInt(part)
					if runtime:
						dict['duration'] = runtime
				channel = part[1:]#ugly
			if runtime > 0:
				
				bcastId = link.split('bcastId=')[1]
				if '&' in bcastId:
					bcastId = bcastId.split('&')[0]
				fanart = bcast2thumb.getThumb(bcastId)
				if fanart:
					dict['fanart'] = fanart
				else:
					print 'bcastid not in archive '+bcastId
					print title
				dict['name'] = title
				dict['url'] = link.replace('&amp;','&')
				#dict["epoch"] = int(time.mktime(time.strptime(pubDate, '%D, %d %M %Y %H:%i:%s %O')))#
				dict["epoch"] = int(time.mktime(parsedate(pubDate)))#
				dict["documentId"] = dict['url'].split("documentId=")[-1].split("&")[0]
				dict['thumb'] = thumb
				dict['plot'] = plot
				dict['channel'] = channel
				dict['type'] = 'video'
				dict['mode'] = 'libArdPlay'
				xbmc.log(str(dict))
				list.append(dict)
	#writeTemp(t)
			
	return list

	
def cleanTitle(title):
	title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#034;", "\"").replace("&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
	title = title.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&ouml;", "ö").replace("&eacute;", "é").replace("&egrave;", "è")
	title = title.replace("&#x00c4;","Ä").replace("&#x00e4;","ä").replace("&#x00d6;","Ö").replace("&#x00f6;","ö").replace("&#x00dc;","Ü").replace("&#x00fc;","ü").replace("&#x00df;","ß")
	title = title.replace("&apos;","'").strip()
	return title

def runtimeToInt(runtime):
	try:
		t = runtime.replace('Min','').replace('min','').replace('.','').replace(' ','')
		HHMM = t.split(':')
		if len(HHMM) == 1:
			return int(HHMM[0])*60
		else:
			return int(HHMM[0])*60 + int(HHMM[1])
	except: 
		return False
		
	
	
def readTemp():
	f = xbmcvfs.File(temp)
	result = f.read()
	f.close()
	return result
def writeTemp(content):
	
	if xbmcvfs.exists(temp):
		xbmcvfs.delete(temp)
	f = xbmcvfs.File(temp, 'w')
	f.write(content)
	f.close()