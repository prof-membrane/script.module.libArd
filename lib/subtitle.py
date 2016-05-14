# -*- coding: utf-8 -*-
import _utils
import xbmc
import xbmcaddon
import xbmcvfs
import json
import subtitleJson2srt
baseUrl = "http://www.ardmediathek.de"
subFile = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')+'sub.srt').decode('utf-8')

#todo offset
def getSub(videoId):
	try: return _getSub(videoId)
	except: return False
def _getSub(videoId):
	sub = False
	print baseUrl+"/play/media/"+videoId+"?devicetype=pc&features=flash"
	response = utils.getUrl(baseUrl+"/play/media/"+videoId+"?devicetype=pc&features=flash")
	if '"_subtitleUrl"' in response:
		decoded = json.loads(response)
		subtitleUrl = decoded['_subtitleUrl']
		subtitleOffset = decoded['_subtitleOffset']
		print subtitleUrl
		print subtitleOffset
		if '/subtitle/' in subtitleUrl:
			subId = subtitleUrl.split('/')[-1]
			print 'http://hbbtv.ardmediathek.de/hbbtv-ard/mediathek/subtitle/'+subId+'?context=hbbtv'
			response = utils.getUrl('http://hbbtv.ardmediathek.de/hbbtv-ard/mediathek/subtitle/'+subId+'?context=hbbtv')
			#print response
			srt = subtitleJson2srt.makeSrt(response,subtitleOffset)
			#print srt
			writeSub(srt)
			sub = True
		else:
			print '#####unsupported subtitle type "'+subtitleUrl+'", report this please'

	if sub: return subFile
	else:   return False
	
def writeSub(content):
	
	if xbmcvfs.exists(subFile):
		xbmcvfs.delete(subFile)
	f = xbmcvfs.File(subFile, 'w')
	f.write(content)
	f.close()