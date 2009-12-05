#!/usr/bin/env python
# -*- coding: cp1251 -*-
#testing bot - for testing new features
from botclass import *
from func import *
import random

class TestBot(PyBot):
    botnick='TestBot'
    HOST='10.4.20.2'
    botip='10.4.255.156'
    debug=0
    #for testing will use @ as command prefix
    commandprefix='@'
    
    def processownercmd(self,fullstr):
        cmd=''
        if self.debug==2: print 'Got full hub string '+str(fullstr)
        cmd=fullstr[1].strip(self.commandprefix)
        if self.debug==2: print 'Parsed command: '+ str(cmd)
        if cmd=='шлеп':
            self.saytochat_me('отшлепал '+fullstr[2])
        if cmd=='welcome':
            self.saytochat('Python standalone bot welcomes all over hub!')
        
        return
    
    def DownloadFL(self,Bnick):
        
        ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ds.bind((self.botip, 55445))
        print 'Started to listen port 55445'
        self.saycommand('$ConnectToMe '+Bnick+' '+self.botip+':55445')
        while 1:
            ds.listen(1)
            csock, caddr = ds.accept()
            print 'accepted connection from '+str(caddr)
            while 1:
                
                csock.send('$MyNick '+self.botnick+'|')
                ct=readsock(csock)
                print 'Sent my nick'
                print 'Got '+str(ct)
                while 1:
                    t=readsock(csock)
                    print 'Got '+t
                    text=t.split()
                    if text[0]=='$MyNick': csock.send('$Lock EXTENDEDPROTOCOLABCABCABCABCABCABC Pk=DCPLUSPLUS0.706ABCABC|')
                    if text[0]=='$Lock':
                        csock.send('$Lock '+lock2key2(text[1])+'|')
                        csock.send('$Direction Download '+str(random.randint(1,100000))+'|')
                    if text[0]=='$Key':
                        csock.send('$ADCGET file files.xml.bz2 0 -1 ZL1|')
                    #if text[0]=='':
                    #random.randint(1,10000)
        return
    
    
    
    def workloop(self):
        while 1:
            hubstr=readsock(self.serversocket)
            #print hubstr
            t=hubstr.split()
            if t[1][0]==self.commandprefix:
                    cmd=t[0].strip("<>")
                    if  cmd == self.ownernick:
                        self.processownercmd(t)
            
            
            
tbot=TestBot()
tbot.login()
print 'Login Complete'
tbot.DownloadFL('dr-evil')
#tbot.workloop()