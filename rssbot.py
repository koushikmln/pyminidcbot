#!/usr/bin/env python
# -*- coding: cp1251 -*-
import socket, feedparser, string
from func import readsock
from func import lock2key2

#main features - login to hub, and announce new rss entries
class rssbot:
    HOST='hub'
    PORT=411
    debug=1
    #share = 2Gb
    sharesize=1024*1024*1024*100
    botnick = 'RssBot'
    botpassword='password'
    botip='127.0.0.1'
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ownernick='dr-evil'
    rssurl="http://core.arbital.ru/rss.xml"
    def saytochat(self,message):
        self.serversocket.send('<'+self.botnick+'> '+message+'|')

    def login(self):
        self.serversocket.connect((self.HOST,self.PORT))
        print 'Connection established'
        while 1:
            t=readsock(self.serversocket)
            if self.debug==1: print t
            if t!='':
                if t[0]=='$':
                    #we got message starting with $ (for example $Lock)
                    hubmsg=t.split()
                    if hubmsg[0]=='$Lock':
                        #we have $Lock message
                        self.serversocket.send('$Key '+lock2key2(hubmsg[1])+'|'+'$ValidateNick '+self.botnick+'|')
                        #if self.debug==1: print 'Sending $Key '+lock2key2(hubmsg[1])+'|'+'$ValidateNick '+self.botnick+'|'
                    if self.debug==1: print 'Got '+hubmsg[0]
                    if hubmsg[0]=='$Hello':
                        #we got $Hello so we need to answer with $Version <version>|$MyINFO <info string>|$GetNickList|
                        self.serversocket.send('$Version 1,0091|$MyINFO $ALL '+self.botnick+' simple python bot$ $100$bot@bot.com$'+str(self.sharesize)+'|$GetNickList|')
                    if hubmsg[0]=='$GetPass':
                            self.serversocket.send('$MyPass '+self.botpassword+'|')
                    if hubmsg[0]=='$Search':
                        #it seems that we have succesfully loggen on to hub :)
                        print "Login complete."
                        
                        return
                
            
            
            
        return
    
        return


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
                    self.rss()
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
