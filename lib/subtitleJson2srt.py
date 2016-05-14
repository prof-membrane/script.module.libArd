import re, json
import _utils
import time
import math
import HTMLParser
h = HTMLParser.HTMLParser()

"""def makeSrt():
        srt = ''
        resp = utils.getUrl('http://hbbtv.ardmediathek.de/hbbtv-ard/mediathek/subtitle/42786?context=ardlib.py')"""
def makeSrt(resp,offset=0):
        srt = ''
        data = json.loads(resp)
        i = 1
        for subtitle in data["subtitles"]:
                srt += str(i)+'\n'
                srt += ms2time(subtitle['begin']) + ' --> ' + ms2time(subtitle['end']) + '\n'
                for entry in subtitle['tt']:
                        if entry == None:
                                srt += '\n'
                        elif entry['style']:
                                color = data['styles'][entry['style']]['fgcol']
                                if srt[-1] != '\n' and srt[-1] != ' ':
                                        srt += ' '
                                srt += '<font color="'+color+'>'+entry['text']+'</font>'
                srt += '\n\n'
                i = i+1  
        srt = h.unescape(srt)
        return srt.encode('utf-8')   
 

def ms2time(tMS):
        ts = tMS /1000
        if   tMS < 10:  MS = '00'+str(tMS)
        elif tMS < 100: MS = '0' +str(tMS)
        else:           MS =  str(tMS)[-3:]
        return time.strftime('%H:%M:%S', time.gmtime(ts))+','+MS
        
#makeSrt()
