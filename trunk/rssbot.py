#!/usr/bin/env python
# -*- coding: cp1251 -*-
import socket, feedparser, string
from func import *
from botclass import *

#main features - login to hub, and announce new rss entries
class rssbot(PyBot):
    HOST='10.4.20.2'
    PORT=411
    debug=0
    #share = 2Gb
    sharesize=1024*1024*1024*100
    botnick = 'RssBot'
    botpassword='123321'
    botip='127.0.0.1'
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ownernick='dr-evil'
    rssurl="http://core.arbital.ru/rss.xml"
    def rss(self):
        self.saytochat('Новое на хабе:')
        tlist=" "
        d=feedparser.parse(self.rssurl)
        print "rss got"
        for entry in d.entries:
            t=entry.title+' - '+entry.link
            #print "Here is t="+t
            tlist+=t+'\n'
        #print "Writing to MainChat "+t.encode("CP1251")
        
        #print tlist
        self.saytochat(tlist.encode("CP1251"))
        
    def workloop(self):
        rssdone=0
        while rssdone==0:
            if rssdone !=1:
                    #self.rss()
                    print "rssdone"
                    rssdone=1
            
                  
        
        
##############################################
#       Doing things....
##############################################


bot=rssbot()
print 'Starting login process...'
print 'My OWNER nick='+bot.ownernick+' My nick='+bot.botnick+' My share='+str(bot.sharesize)+' MyIp='+bot.botip
print 'Connecting to dc hub '+bot.HOST+ ' using port '+str(bot.PORT)
bot.login()
bot.workloop()
#now let's check what about rss ;)
