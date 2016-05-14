#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import xbmc
import xbmcplugin
import xbmcgui
import urllib
import _utils as utils

videoQuality =10000000000000000

def getVideoUrl(url=False,videoID=False):
	xbmc.log(videoID)
	if not videoID:
		videoID = url.split('documentId=')[1]
		if '&' in videoID:
			videoID = videoID.split('&')[0]
	if url:
		content = utils.getUrl(url)
		match = re.compile('<div class="box fsk.*?class="teasertext">(.+?)</p>', re.DOTALL).findall(content)
	#if match:
	if False:
		xbmc.executebuiltin('XBMC.Notification(Info:,'+match[0].strip()+',15000)')
		return False
	else:
		return fetchTvaVideo(videoID)

def fetchTvaVideo(id):
	print 'http://www.ardmediathek.de/ard/servlet/export/tva/id='+id+'/index.xml'
	xml = utils.getUrl('http://www.ardmediathek.de/ard/servlet/export/tva/id='+id+'/index.xml')
	if "crid://ard.de/videolive" in xml:
		return False
	try:
		programURL = re.compile('<tva:ProgramURL>(.+?)</tva:ProgramURL>', re.DOTALL).findall(xml)[0]
		if programURL.endswith('.mp3'):
			return programURL
	except: pass
	
	match = re.compile('<tva:OnDemandProgram>(.+?)</tva:OnDemandProgram>', re.DOTALL).findall(xml)
	finalUrl = False
	qualityHLS = 0
	for item in match:
		videoUrl = re.compile('<tva:ProgramURL>(.+?)</tva:ProgramURL>', re.DOTALL).findall(item)[0]
		if not 'rtmp://' in videoUrl and not 'rtmpt://' in videoUrl and not 'manifest.f4m' in videoUrl:
			quality = re.compile('<tva:FileFormat href="urn:ard:tva:metadata:cs:ARDFormatCS:(.+?)"/>', re.DOTALL).findall(item)[0]
			if 'smil/master.m3u8' in videoUrl:
				if quality in qualityDictHLS:
					q = qualityDictHLS[quality]
				else:
					print '######################'+quality
					q = 1
				if q >= qualityHLS:
					finalUrl = videoUrl
					qualityHLS = q
			else:
				if quality in qualityDict2:
					if qualityDict2[quality] <= videoQuality:
						selectedVideoUrl = videoUrl
				else:
					print item
					print quality
	if not finalUrl:
		finalUrl = selectedVideoUrl
		print '###############using mp4'
	else:
		print '###############using HLS'

	return finalUrl

### video type to bitrate###
qualityDict = {'2012:1.58': 1620000,
			   '2012:1.83': 47000,
			   '2012:1.54': 608000,
			   '2012:1.28': 0,
			   '2014:1.2.3.14.1': 3814000,
			   '2014:1.2.3.12.2': 1725000,
			   '2014:1.2.3.11.1': 1149000,
			   '2014:1.2.3.9.1': 639000,
			   '2014:1.2.3.7.1': 380000,
			   '2014:1.2.3.6.1': 319000};
###video type to rating###
qualityDict2 = {'2012:1.58': 29,
			   '2012:1.83': 1,
			   '2012:1.54': 9,
			   '2012:1.28': 0,
			   '2014:1.2.3.14.1': 40,
			   '2014:1.2.3.12.2': 30,
			   '2014:1.2.3.11.1': 20,
			   '2014:1.2.3.9.1': 10,
			   '2014:1.2.3.7.1': 8,
			   '2014:1.2.3.6.1': 7};

qualityDictHLS = {'2014:5.2.13.14.1': 100,
				  '2014:5.2.13.12.1': 95,
				  '2012:5.28': 90,
				  '2012:5.10': 50,
				  '2012:1.65': 1,};