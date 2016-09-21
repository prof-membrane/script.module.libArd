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
			j2 = entry["inhalte"][0]
			dict["name"] += j2["ueberschrift"]
			#dict["channel"] = j2["unterzeile"]
			dict["thumb"] = j2["bilder"][0]["schemaUrl"].replace("##width##","0")
			dict["url"] = j2["link"]["url"]
			dict["duration"] = runtimeToInt(j2["unterzeile"])
			#dict["pluginpath"] = pluginpath
			dict["type"] = 'video'
			dict['mode'] = 'libArdPlay'
			list.append(dict)
	return list
		
def parseAZ(letter):
	if letter == "0-9":
		letter = '#'
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
		dict["entries"] = int(entry["dachzeile"].encode("utf-8").split(' ')[0])
		#dict["thumb"] = entry["bilder"][0]["schemaUrl"].replace("##width##","0").encode("utf-8")
		dict["thumb"] = entry["bilder"][0]["schemaUrl"].replace("##width##","1920").encode("utf-8")
		dict["url"] = entry["link"]["url"].encode("utf-8")
		dict['mode'] = 'libArdListVideos'
		#dict["documentId"] = entry["link"]["url"].split("documentId=")[1].split("&")[0]
		#dict["pluginpath"] = pluginpath
		dict["type"] = 'shows'
		xbmc.log(str(dict))
		list.append(dict)
		
		
	return list
	
def parseVideos(url,page='1'):
	list = []
	response = _utils.getUrl(url)
	xbmc.log(response)
	j = json.loads(response)
	
	#j1 = j["sections"][-1]["modCons"][-1]["mods"][-1]
	
	
	#j1 = j["sections"][-1]["modCons"][-1]["mods"][-1]
	j1 = j["sections"][-1]["modCons"][-1]["mods"][-1]
	
	for j2 in j1["inhalte"]:
		xbmc.log(str(j2))
		dict = {}
		if "ueberschrift" in j2:
			dict["name"] = j2["ueberschrift"].encode("utf-8")
			if 'Hörfassung' in dict["name"] or 'Audiodeskription' in dict["name"]:
				dict["name"] = dict["name"].replace(' - Hörfassung','').replace(' - Audiodeskription','')
				dict["name"] = dict["name"].replace(' (mit Hörfassung)','').replace(' (mit Audiodeskription)','')
				dict["name"] = dict["name"].replace(' mit Hörfassung','').replace(' mit Audiodeskription','')
				dict["name"] = dict["name"].replace(' (Hörfassung)','').replace(' (Audiodeskription)','')
				dict["name"] = dict["name"].replace(' Hörfassung','').replace(' Audiodeskription','')
				dict["name"] = dict["name"].replace('Hörfassung','').replace('Audiodeskription','')
				dict["name"] = dict["name"].strip()
				if dict["name"].endswith(' -'):
					dict["name"] = dict["name"][:-2]
				dict["name"] = dict["name"] + ' - Hörfassung'
				dict["audioDesc"] = True
				
		if "unterzeile" in j2:
			dict["duration"] = runtimeToInt(j2["unterzeile"])
		if "bilder" in j2:
			dict["thumb"] = j2["bilder"][0]["schemaUrl"].replace("##width##","384").encode("utf-8")
		if "teaserTyp" in j2:
			if j2["teaserTyp"] == "PermanentLivestreamClip" or j2["teaserTyp"] == "PodcastClip":
				continue
			elif j2["teaserTyp"] == "OnDemandClip":
				dict["type"] = 'video'
				dict['mode'] = 'libArdPlay'
			elif j2["teaserTyp"] == "Sammlung":
				dict["type"] = 'dir'
				dict['mode'] = 'libArdListVideos'
			else:
				xbmc.log('json parser: unknown item type: ' + j2["teaserTyp"])
				dict["type"] = 'dir'
				dict['mode'] = 'libArdListVideos'
				
		if "link" in j2:
			dict["url"] = j2["link"]["url"].encode("utf-8")
			dict["documentId"] = j2["link"]["url"].split("/player/")[-1].split("?")[0].encode("utf-8")
		if "dachzeile" in j2:
			dict["releasedate"] = j2["dachzeile"].encode("utf-8")
		if 'ut' in j2['kennzeichen']:
			dict["subtitle"] = True
		if 'geo' in j2['kennzeichen']:
			dict['geo'] = 'DACH'
		if 'fsk6' in j2['kennzeichen']:
			dict['mpaa'] = 'FSK6'
		if 'fsk12' in j2['kennzeichen']:
			dict['mpaa'] = 'FSK12'
		if 'fsk16' in j2['kennzeichen']:
			dict['mpaa'] = 'FSK16'
		if 'fsk18' in j2['kennzeichen']:
			dict['mpaa'] = 'FSK18'
		#dict["pluginpath"] = pluginpath
		
		
		list.append(dict)
	
	
	n = _fetchNextPage(j1["buttons"],page)
	if n:
		list.append(n)
		
	
	return list
	
def _fetchNextPage(j,page):
	dict = False
	p = str(int(page) + 1)
	for group in j:
		if group["label"]["text"] == "Seiten":
			for button in group["buttons"]:
				url = button["buttonLink"]["url"]
				if url.endswith('page.' + p):
					dict = {}
					dict["url"] = url
					dict["page"] = p
					dict["type"] = 'nextPage'
					dict['mode'] = 'libArdListVideos'
	return dict
	
def runtimeToInt(runtime):
	xbmc.log(str(runtime))
	try:
		if '|' in runtime:
			for s in runtime.split('|'):
				if 'Min' in s:
					runtime = s
		if '<br>' in runtime:
			runtime = runtime.split('<br>')[0]
		t = runtime.replace('Min','').replace('min','').replace('.','').replace(' ','').replace('|','').replace('UT','')
		xbmc.log(t)
		HHMM = t.split(':')
		if len(HHMM) == 1:
			return int(HHMM[0])*60
		else:
			return int(HHMM[0])*60 + int(HHMM[1])
	except: 
		return ''