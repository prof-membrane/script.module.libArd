# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import libArd
import listing
import urllib
import libMediathek

channelList = {'daserste':'208',
			   'br':'2224',
			   'wdr':'5902',
			   'einsfestival':'673348',
			   'mdr':'5882',
			   'mdrsachsen':'1386804',
			   'mdrthüringen':'1386988',
			   'mdrsachsenanhalt':'1386898',
			   'rbb':'5874',
			   'sr':'5870',
			   'hr':'5884',
			   'ndr':'5906',
			   'tagesschau24':'5878',
			   'ardalpha':'5868',
			   'einsplus':'4178842',
			   'swr':'5310',
			   'swrrheinlandpfalz':'5872',
			   'swrbadenwürttemberg':'5904',
			  }
			  
blacklist =			[
						#"LexiTV - Wissen für alle",
						"Giraffe, Erdmännchen & Co",
						"MDR um 11"
					]
whitelistGeneral = 	[
						"ardmittagsmagazin",
					]

#whitelist for re-runs

whitelistShow =		{
						"Tagesschau":"http://www.ardmediathek.de/tv/Tagesschau/Sendung?documentId=4326&bcastId=4326&m23644322=quelle.tv&rss=true",
						"Unser Sandmännchen":"http://www.ardmediathek.de/tv/Unser-Sandm%C3%A4nnchen/Sendung?documentId=11094342&bcastId=11094342&m23644322=quelle.tv&rss=true",
						"ARD-Mittagsmagazin":"http://www.ardmediathek.de/tv/Mittagsmagazin/Sendung?documentId=314636&bcastId=314636&m23644322=quelle.tv&rss=true",
						"Wer weiß denn sowas?":"http://www.ardmediathek.de/tv/Wer-wei%C3%9F-denn-sowas/Sendung?documentId=29322328&bcastId=29322328&m23644322=quelle.tv&rss=true",
						"artour":"http://www.ardmediathek.de/tv/artour/Sendung?documentId=7545220&bcastId=7545220&m23644322=quelle.tv&rss=true",
						"Maischberger":"http://www.ardmediathek.de/tv/Maischberger/Sendung?documentId=311210&bcastId=311210&m23644322=quelle.tv&rss=true",
						"Hauptsache gesund":"http://www.ardmediathek.de/tv/Hauptsache-gesund/Sendung?documentId=7545180&bcastId=7545180&m23644322=quelle.tv&rss=true",
						"Lebensretter":"http://www.ardmediathek.de/tv/Lebensretter/Sendung?documentId=18941746&bcastId=18941746&m23644322=quelle.tv&rss=true",
						
						#RBB
						"zibb":"http://www.ardmediathek.de/tv/zibb/Sendung?documentId=3822084&bcastId=3822084&m23644322=quelle.tv&rss=true",
						
						#EInsfestival
						"Druckfrisch":"http://www.ardmediathek.de/tv/Druckfrisch/Sendung?documentId=339944&m23644322=quelle.tv&rss=true",
						"kinokino":"http://www.ardmediathek.de/tv/kinokino/Sendung?documentId=14913678&bcastId=14913678&m23644322=quelle.tv&rss=true",
						#Folgen, evntl. ändern
						"Sturm der Liebe":"http://www.ardmediathek.de/tv/Sturm-der-Liebe/Sendung?documentId=5290&bcastId=5290&m23644322=quelle.tv&rss=true",
						"Rote Rosen":"http://www.ardmediathek.de/tv/Rote-Rosen/Sendung?documentId=317766&bcastId=317766&m23644322=quelle.tv&rss=true",
					}
showsAlias =		[
						"Sturm der Liebe",
						"Rote Rosen",
					]

def play(dict):
	if dict["name"] in blacklist:
		return False
	video = False
	video = _searchDateList(dict)
	
	for alias in showsAlias:
		if dict["name"].startswith(alias):
			dict["name"] = alias
	#TODO:
	#check if in future
	#check if in re-run window
	if not video and dict["name"] in whitelistShow: 
		video = _searchEpisode(dict,whitelistShow[dict["name"]])
	#if not video and dict["name"] in whitelistShow:#TODO
	#	video = _searchShow(dict)
		
	if not video:#last ditch efford
		video = _searchGeneral(dict)
		
	if not video:
		xbmc.executebuiltin("Notification(Kein Video gefunden,Nicht in Mediathek, 7000)")
		xbmc.log("no video found")
		return
		
	xbmc.log('############################')
	xbmc.log(str(video))
	xbmc.log(video["name"])
	xbmc.log(dict["name"])
	showSubtitles = False
	url,sub = libArd.getVideoUrl(video["documentId"],showSubtitles)
	if url:
		listitem = xbmcgui.ListItem(label=dict["name"],thumbnailImage=video["thumb"],path=url)

		xbmc.Player().play(url, listitem)
	
def _searchEpisode(dict,url):
	video = False
	savedEpoch = 0
	savedDuration = 0
	items,nextPage = libArd.getPage(whitelistShow[dict["name"]])
	#dict["epoch"] -= 8000
	xbmc.log("sendung epoch")
	xbmc.log(str(dict["epoch"]))
	for item in items:
		xbmc.log(str(item["epoch"]))
		xbmc.log(str(type(item["epoch"])))
		xbmc.log(str(type(dict["epoch"])))
		if libMediathek.pvrCheckDurationIsComparable(item["duration"],dict["duration"]):
			if item["epoch"] <= dict["epoch"]:
				xbmc.log("stage 1")
				if item["epoch"] != savedEpoch:
					savedDuration = 0
				if item["epoch"] > savedEpoch:
					savedDuration = item["duration"]
					savedEpoch = item["epoch"]
					video = item
					
				elif item["epoch"] == savedEpoch and item["duration"] > savedDuration:
					savedDuration = item["duration"]
					savedEpoch = item["epoch"]
					video = item
	return video
def _searchDateList(dict):
	items = listing.listDate('http://www.ardmediathek.de/tv/sendungVerpasst?tag='+str(dict["day"])+'&kanal='+channelList[dict["channel"]])
	return _pickEpisode(dict,items)
	
def _searchShow(dict):
	items,nextPage = libArd.getPage(whitelistShow[dict["name"]])
	return _pickEpisode(dict,items)
	
def _searchGeneral(dict):
	#searchString = urllib.quote_plus(dict["episode"])
	searchString = urllib.quote_plus(dict["name"])
	xbmc.log(searchString)
	items = libArd.getSearch(searchString)
	for item in items:
		xbmc.log(str(item))
		xbmc.log(str(dict["duration"]))
		if libMediathek.pvrCheckDurationIsComparable(item["duration"],dict["duration"]):
			xbmc.log("duration check passed")
			if libMediathek.pvrCheckNameIsComparable(item["name"],_generateCompareName(dict)):
				xbmc.log("compare check passed")
				return item
	else: 
		return False
	#return _pickEpisode(dict,items)
		
def _generateCompareName(dict):
	if dict["episode"].startswith("Fernsehfilm Deutschland"):
		return dict["name"]
	else:
		return dict["name"] + ' ' + dict["episode"]
		
def _passValidSearchWords(dict):
	string = _generateCompareName(dict)
	finalString = ""
	string = string.replace("&","").replace(".","")
	string = string.lower()
	s = string.split(" ")
	for word in s:
		if len(word) > 3:
			finalString += word + ' '
	return finalString
	
	
def _pickEpisode(dict,items):
	duration = 0
	foundAccurateTime = False
	video = False
	for item in items:
		xbmc.log(str(item))
		HH,MM = item["time"].split(":")
		t = int(HH) * 60 + int(MM)
		if dict["time"] == t:
			if int(item["duration"]) > duration:#picks the longest video, shows may be split up into chuncks
				#TODO: handle videos for audio disabled
				video = item
				duration = int(item["duration"])
				foundAccurateTime = True
		elif not foundAccurateTime and libMediathek.pvrCheckStartTimeIsComparable(dict["time"],t) and libMediathek.pvrCheckNameIsComparable(dict["name"],item["name"]):
			if int(item["duration"]) > duration:#picks the longest video, shows may be split up into chuncks
				#TODO: handle videos for audio disabled
				video = item
				duration = int(item["duration"])
		xbmc.log(str(libMediathek.pvrCheckStartTimeIsComparable(dict["time"],t)))
		xbmc.log(str(libMediathek.pvrCheckNameIsComparable(dict["name"],item["name"])))
			
	xbmc.log(str(video))
	return video
	