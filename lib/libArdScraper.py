#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib2
baseUrl = "http://www.ardmediathek.de"
letr = 'J'
def scrapeDescriptions(letter):
	list = getAZ(letter)
	for dict in list:
		dict['url'] = dict['url'].replace('&m23644322=quelle.tv&rss=true','')
		url = dict['url']
		bcastId = url.split('bcastId=')[-1]
		if '&' in bcastId:
			bcastId = bcastId.split('&')[0]
		response = getUrl(dict['url'])
		text = re.compile('<p class="teasertext">(.+?)</p>', re.DOTALL).findall(response)[-1]
		print "'"+bcastId+"':'"+text.decode('utf-8')+"',"
		
def getAZ(letter):
	
	if letter == '#':
		letter = '0-9'
	list = []
	content = getUrl(baseUrl+"/tv/sendungen-a-z?buchstabe="+letter)
	spl = content.split('<div class="teaser" data-ctrl')
	for i in range(1, len(spl), 1):
		dict = {}
		entry = spl[i]
		url = re.compile('href="(.+?)"', re.DOTALL).findall(entry)[0]
		dict['url'] = baseUrl+url.replace("&amp;","&")+'&m23644322=quelle.tv&rss=true'
		dict['name'] = re.compile('class="headline">(.+?)<', re.DOTALL).findall(entry)[0]
		dict['channel'] = re.compile('class="subtitle">(.+?)<', re.DOTALL).findall(entry)[0]
		thumbId = re.compile('/image/(.+?)/16x9/', re.DOTALL).findall(entry)[0]
		dict['thumb'] = baseUrl+"/image/"+thumbId+"/16x9/0"
		dict['fanart'] = dict['thumb']
		list.append(dict)
	return list

def getUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:25.0) Gecko/20100101 Firefox/25.0')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link

def AZ():
	list = []
	response = getUrl("http://www.ardmediathek.de/appdata/servlet/tv/sendungAbisZ?json")
	j = json.loads(response)
	j1 = j["sections"][0]["modCons"][0]["mods"][0]["inhalte"]
	for e in j1:
		j2 = e["inhalte"]
		for entry in j2:
			dict = {}
			dict["name"] = entry["ueberschrift"].encode("utf-8")
			#dict["channel"] = entry["unterzeile"].encode("utf-8")
			#dict["entries"] = int(entry["dachzeile"].encode("utf-8").split(' ')[0])
			#dict["thumb"] = entry["bilder"][0]["schemaUrl"].replace("##width##","0").encode("utf-8")
			dict["url"] = entry["link"]["url"].encode("utf-8")
			#dict['mode'] = 'libArdListVideos'
			#dict["documentId"] = entry["link"]["url"].split("documentId=")[1].split("&")[0]
			#dict["pluginpath"] = pluginpath
			#dict["type"] = 'dir'
			list.append(dict)
		
		
	return list
import json
print str(AZ())


