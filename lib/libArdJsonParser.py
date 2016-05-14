# -*- coding: utf-8 -*-
import xbmc
import json
import _utils

pluginpath = 'plugin://script.module.libArd/'

def parse(url):
	list = []
	response = _utils.getUrl(url)
	j = json.loads(response)
	
def parseDate(url):
	list = []
	response = _utils.getUrl(url)
	j = json.loads(response)
	j1 = j["sections"][-1]["modCons"][0]["mods"][0]["inhalte"]
	for entry in j1:
		j2 = entry["inhalte"]
		for entry in j2:
			dict = {}
			dict["name"] = entry["dachzeile"] + ' - '
			dict["name"] += entry["ueberschrift"] + ' - '
			j3 = entry["inhalte"][0]
			dict["name"] += j3["ueberschrift"]
			#dict["channel"] = j3["unterzeile"]
			dict["thumb"] = j3["bilder"][0]["schemaUrl"].replace("##width##","0")
			dict["url"] = j3["link"]["url"]
			dict["duration"] = runtimeToInt(j3["unterzeile"])
			dict["pluginpath"] = pluginpath
			dict["type"] = 'video'
			dict['mode'] = 'libArdPlay'
			list.append(dict)
	return list
		
def parseAZ(letter):
	list = []
	response = _utils.getUrl("http://www.ardmediathek.de/appdata/servlet/tv/sendungAbisZ?json")
	j = json.loads(response)
	j1 = j["sections"][0]["modCons"][0]["mods"][0]["inhalte"]
	for entry in j1:
		if entry["ueberschrift"] == letter.upper():
			j2 = entry["inhalte"]
	for entry in j2:
		dict = {}
		dict["name"] = entry["ueberschrift"].encode("utf-8")
		dict["channel"] = entry["unterzeile"].encode("utf-8")
		dict["thumb"] = entry["bilder"][0]["schemaUrl"].replace("##width##","0").encode("utf-8")
		dict["url"] = entry["link"]["url"].encode("utf-8")
		#dict["documentId"] = entry["link"]["url"].split("documentId=")[1].split("&")[0]
		dict["pluginpath"] = pluginpath
		dict["type"] = 'dir'
		list.append(dict)
		
		
	return list
	
def parseVideos(url):
	list = []
	response = _utils.getUrl(url)
	xbmc.log(response)
	j = json.loads(response)
	#for e in j:
	#	xbmc.log(str(e))
	j1 = j["sections"][-1]["modCons"][-1]["mods"][0]["inhalte"]
	for j2 in j1:
		dict = {}
		if "ueberschrift" in j2:
			dict["name"] = j2["ueberschrift"].encode("utf-8")
		if "unterzeile" in j2:
			dict["duration"] = runtimeToInt(j2["unterzeile"])
			if "UT" in j2["unterzeile"]:
				dict["subtitle"] = True
			else:
				dict["subtitle"] = False
		if "bilder" in j2:
			dict["thumb"] = j2["bilder"][0]["schemaUrl"].replace("##width##","0").encode("utf-8")
		if "link" in j2:
			dict["url"] = j2["link"]["url"].encode("utf-8")
			dict["documentId"] = j2["link"]["url"].split("/player/")[-1].split("?")[0].encode("utf-8")
		if "dachzeile" in j2:
			dict["releasedate"] = j2["dachzeile"].encode("utf-8")
		dict["pluginpath"] = pluginpath
		dict["type"] = 'video'
		dict['mode'] = 'libArdPlay'
		
		list.append(dict)
	return list#,False
			
def runtimeToInt(runtime):
	try:
		t = runtime.replace('Min','').replace('min','').replace('.','').replace(' ','').replace('|','').replace('UT','')
		xbmc.log(t)
		HHMM = t.split(':')
		if len(HHMM) == 1:
			return int(HHMM[0])*60
		else:
			return int(HHMM[0])*60 + int(HHMM[1])
	except: 
		return ''