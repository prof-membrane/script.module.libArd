#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import xbmcplugin
import xbmcgui
import urllib
import rssparser
import _utils as utils
import xbmc
import xbmcaddon
import xbmcvfs
import bcast2thumb
import libArdBcastId2Desc
import HTMLParser
#import requests
h = HTMLParser.HTMLParser()
temp = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')+'temp').decode('utf-8')
useThumbAsFanart = True
baseUrl = "http://www.ardmediathek.de"
defaultThumb = baseUrl+"/ard/static/pics/default/16_9/default_webM_16_9.jpg"
defaultBackground = "http://www.ard.de/pool/img/ard/background/base_xl.jpg"
icon = ''#todo
showDateInTitle = False
#reload(sys) 
#sys.setdefaultencoding('utf-8')

def listRSS(url,page=0):
	if page > 1:
		url += '&mcontents=page.'+str(page)
	print url
	#r = requests.get(url)
	#response = rssparser.parser(r.text.decode('utf-8'))
	response = utils.getUrl(url)
	data = rssparser.parser(response)
	if page == 0:
		return data
	else:
		if len(data) == 50:
			return data,True
		else:
			return data,False
def getAzList(letter):
	print 'ARD getaz'
	items = []
	l = getAZ(letter)
	for name, url, thumb in l:
		#u = sys.argv[0]+"?url="+urllib.quote_plus(baseUrl+url+'&m23644322=quelle.tv&rss=true')+"&name="+urllib.quote_plus(name)+"&mode=listVideosRss"+"&nextpage=True"+"&hideshowname=True"+"&showName="+urllib.quote_plus(name)
		u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&name="+urllib.quote_plus(name)+"&mode=2"+"&nextpage=True"+"&hideshowname=True"+"&showName="+urllib.quote_plus(name)
		liz = xbmcgui.ListItem(name, iconImage=defaultThumb, thumbnailImage=thumb)
		liz.setInfo(type="Video", infoLabels={"Title": name})
		if useThumbAsFanart:
			if not thumb or thumb==icon or thumb==defaultThumb:
				thumb = defaultBackground
			liz.setProperty("fanart_image", thumb)
		else:
			liz.setProperty("fanart_image", defaultBackground)
		items.append([u, liz, True])
	return items
		

def getAZ(letter):
	#ids = []
	if letter == '#':
		letter = '0-9'
	list = []
	if letter == 'X' or letter == 'Y':
		return list
	content = utils.getUrl(baseUrl+"/tv/sendungen-a-z?buchstabe="+letter)
	
	#r = requests.get(baseUrl+"/tv/sendungen-a-z?buchstabe="+letter)
	#content = r.text.decode('utf-8')
	
	spl = content.split('<div class="teaser" data-ctrl')
	for i in range(1, len(spl), 1):
		dict = {}
		entry = spl[i]
		url = re.compile('href="(.+?)"', re.DOTALL).findall(entry)[0]
		url = url.replace("&amp;","&")
		dict['url'] = baseUrl+url+'&m23644322=quelle.tv&rss=true'
		dict['name'] = re.compile('class="headline">(.+?)<', re.DOTALL).findall(entry)[0]
		dict['channel'] = re.compile('class="subtitle">(.+?)<', re.DOTALL).findall(entry)[0]
		thumbId = re.compile('/image/(.+?)/16x9/', re.DOTALL).findall(entry)[0]
		dict['thumb'] = baseUrl+"/image/"+thumbId+"/16x9/0"
		dict['fanart'] = dict['thumb']
		bcastId = url.split('bcastId=')[-1]
		if '&' in bcastId:
			bcastId = bcastId.split('&')[0]
		dict['plot'] = libArdBcastId2Desc.toDesc(bcastId)
		dict["mode"] = "libArdListVideos"
		list.append(dict)
		#th = thumbId.split('/')
		#a = url.split('=')[-1]
		#b = th[0]+th[1]+th[2]+th[3]+th[4]
		
		#ids.append([a,b])
	#bcast2thumb.addBcastIDs(ids)
	return list
	
def getVideosXml(videoId):
	print 'getxml'
	list = []
	content = utils.getUrl(baseUrl+'/ard/servlet/export/collection/collectionId='+videoId+'/index.xml')
	match = re.compile('<content>(.+?)</content>', re.DOTALL).findall(content)
	for item in match:
		clip = re.compile('<clip(.+?)>', re.DOTALL).findall(item)[0]
		if 'isAudio="false"' in clip:
			name = re.compile('<name>(.+?)</name>', re.DOTALL).findall(item)[0]
			length = re.compile('<length>(.+?)</length>', re.DOTALL).findall(item)[0]
			if not '<mediadata:images/>' in item:
				thumb = re.compile('<image.+?url="(.+?)"', re.DOTALL).findall(item)[-1]
			else:
				thumb = ''
			id = re.compile(' id="(.+?)"', re.DOTALL).findall(clip)[0]
			list.append([name, id, thumb, length])
	return list
	

	
	
def listDate(url):
	list =[]
	response = utils.getUrl(url)
	videos = response.split('<span class="date">')
	videos = videos[1:]
	for video in videos:
		time = video[:5]
		titel = re.compile('<span class="titel">(.+?)</span>', re.DOTALL).findall(video)[0]
		match = re.compile('<div class="media mediaA">.+?<a href="(.+?)" class="mediaLink">.+?urlScheme&#039;:&#039;(.+?)##width##.+?<h4 class="headline">(.+?)</h4>.+?<p class="subtitle">(.+?)</p>', re.DOTALL).findall(video)
		#http://www.ardmediathek.de/ard/servlet/image/00/32/75/15/44/1547339463/16x9/320
		for url,thumb,name,plot in match:
			dict = {}
			dict['time'] = time
			length = plot.split(' ')[0]
			if ':' in length:
				length = length.split(':')
				dict['duration'] = str(int(length[0])*60+int(length[1]))
			else:
				dict['duration'] = str(int(length)*60)
			if name in titel:
				dict['name'] = dict['time'] + ' - ' + titel
			elif titel in name:
				dict['name'] = dict['time'] + ' - ' + name
			else:
				dict['name'] = dict['time'] + ' - ' + titel+' - '+name
			dict['thumb'] = 'http://www.ardmediathek.de/ard/servlet'+thumb+'0'
			dict['plot'] = plot
			dict['url'] = baseUrl+url.replace('&amp;','&')
			dict['name'] = dict['name'].decode('utf-8')
			dict['name'] = h.unescape(dict['name'])
			dict['name'] = dict['name'].encode('utf-8')
			dict['documentId'] = dict['url'].encode('utf-8').split("documentId=")[-1]
			list.append(dict)
	#print entry
	
	return list	
	
def listVideos(url,page=1):
	list =[]
	content = utils.getUrl(url)
	spl = content.split('<div class="teaser" data-ctrl')
	for i in range(1, len(spl), 1):
		dict ={}
		entry = spl[i]
		dict["url"] = baseUrl + re.compile('<a href="(.+?)" class="mediaLink">', re.DOTALL).findall(entry)[0].replace("&amp;","&")
		dict["name"] = cleanTitle(re.compile('class="headline">(.+?)<', re.DOTALL).findall(entry)[0])
		
		match = re.compile('class="dachzeile">(.+?)<', re.DOTALL).findall(entry)
		if match:
			dict["showname"] = match[0]
		
		match = re.compile('<p class="subtitle">(.+?)</p>', re.DOTALL).findall(entry)
		if match:
			subtitle = match[0].split(" | ")
			dict["date"] = subtitle[0]
			dict["duration"] = int(subtitle[1].replace(" Min.",""))*60
			dict["channel"] = subtitle[2]
			if len(subtitle) > 3:
				if subtitle[3] == "UT":
					dict["subtitle"] = True
			
		
		match = re.compile('/image/(.+?)/16x9/', re.DOTALL).findall(entry)
		if match:
			dict['thumb'] = baseUrl+"/image/"+match[0]+"/16x9/448"
		dict["type"] = 'video'
		dict['mode'] = 'libArdPlay'
		dict["documentId"] = dict["url"].split("documentId=")[-1]
		list.append(dict)
		
	return list
	

def cleanTitle(title):
	title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#034;", "\"").replace("&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
	title = title.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&ouml;", "ö").replace("&eacute;", "é").replace("&egrave;", "è")
	title = title.replace("&#x00c4;","Ä").replace("&#x00e4;","ä").replace("&#x00d6;","Ö").replace("&#x00f6;","ö").replace("&#x00dc;","Ü").replace("&#x00fc;","ü").replace("&#x00df;","ß")
	title = title.replace("&apos;","'").strip()
	return title
	
	
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