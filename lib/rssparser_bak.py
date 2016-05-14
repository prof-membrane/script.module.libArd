#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import utils
print '11111111111111111111'
def parser(data):
	print '####################'
	list = []
	match = re.compile('<item>(.+?)</item>', re.DOTALL).findall(data)
	for item in match:
		thumb = ''
		plot = ''
		title = re.compile('<title>(.+?)</title>', re.DOTALL).findall(item)[0]
		pubDate = re.compile('<pubDate>(.+?)</pubDate>', re.DOTALL).findall(item)[0]
		description = re.compile('<description>(.+?)</description>', re.DOTALL).findall(item)[0]
		if '<category>' in item:
			category = cleanTitle(re.compile('<category>(.+?)</category>', re.DOTALL).findall(item)[-1])
		else:
			category = ''
		if 'img src="' in description:
			thumb = re.compile('img src="(.+?)"', re.DOTALL).findall(description)[0]
		infos = re.compile('&lt;p&gt;(.*?)&lt;/p&gt;', re.DOTALL).findall(description)
		print len(infos)
		if len(infos) == 4:
			if infos[1] == '' or infos[1].endswith('...') and len(infos[1]) < len(title):
				plot = title +'\n\n'+ infos[2]
			else:
				plot = infos[1].replace('\n','')+'\n\n'+infos[2]
			link = re.compile('<link>(.+?)</link>', re.DOTALL).findall(item)[0]
			documentId = link.split('documentId=')[1]
			if '&' in documentId:
				documentId = documentId.split('&')[0]
			split = infos[2].split('|')
			runtime = 0
			for part in split:
				if 'Min' in part or 'min' in part:
					runtime = runtimeToInt(part)
			list.append([title,pubDate,thumb,plot,link,documentId,category,runtime])
	return list
	
def cleanTitle(title):
	title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#034;", "\"").replace("&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
	title = title.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&ouml;", "ö").replace("&eacute;", "é").replace("&egrave;", "è")
	title = title.replace("&#x00c4;","Ä").replace("&#x00e4;","ä").replace("&#x00d6;","Ö").replace("&#x00f6;","ö").replace("&#x00dc;","Ü").replace("&#x00fc;","ü").replace("&#x00df;","ß")
	title = title.replace("&apos;","'").strip()
	return title

def runtimeToInt(runtime):
	t = runtime.replace('Min','').replace('min','').replace('.','').replace(' ','')
	HHMM = t.split(':')
	return int(HHMM[0])*60 + int(HHMM[1])