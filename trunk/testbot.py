#!/usr/bin/env python2.6
# -*- coding: cp1251 -*-
#testing bot - for testing new features
from botclass import *
from func import *
import random, io




class TestBot(PyBot):
    botnick='TestBot'
    HOST='10.4.20.2'
    PORT=411
    botif='eth0'
    botip='192.168.1.4'
    debug=1
    #for temp
    useport=6881
    #for testing will use @ as command prefix
    commandprefix='@'
    
    def processownercmd(self,fullstr):
        cmd=''
        if self.debug==2: print 'Got full hub string '+str(fullstr)
        cmd=fullstr[1].strip(self.commandprefix)
        if self.debug==2: print 'Parsed command: '+ str(cmd)
        if cmd=='????':
            self.saytochat_me('???????? '+fullstr[2])
        if cmd=='welcome':
            self.saytochat('Python standalone bot welcomes all over hub!')
        
        
        return
    
    def DownloadFL_adc(self,Bnick):
        print 'Trying...'
        ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ds.bind((self.botip, self.useport))
        print 'Started to listen port '+str(self.useport)
        ds.listen(1)
        self.saycommand('$ConnectToMe '+Bnick+' '+self.botip+':'+str(self.useport)+'|')
        while 1:
            
            csock, caddr = ds.accept()
            print 'accepted connection from '+str(caddr)
            while 1:
                    t=readsock(csock)
                    print 'Got '+t
                    text=t.split()
                    if text[0]=='$MyNick': csock.send('$MyNick '+self.botnick+'|')
                    if text[0]=='$Lock':
                        csock.send('$Lock EXTENDEDPROTOCOLABCABCABCABCABCABC Pk=DCPLUSPLUS0.706ABCABC|')
                        #print 'Trying to generate a $Key from: '+str(text[1])
                        zz=lock2key2(text[1])
                        #csock.send('$Key '+zz+' |')
                        print '$key sent!'
                        #csock.send('$Direction Download '+str(random.randint(1,100000))+'|')
                    if text[0]=='$Key':
                        #csock.send('$ADCGET file files.xml.bz2 0 -1 ZL1|')
                        csock.send('$Supports MiniSlots XmlBZList ADCGet |')
                        csock.send('$Direction Download 77777|')
                        csock.send('$Key '+zz+' |')
                        csock.send('$ADCGET file files.xml.bz2 0 -1|')
                        #csock.send('$Get MyList.DcLst$1|')
                    if text[0]=='$ADCSND':
                        filename='files.xml.bz2'
                        print 'Reading '+text[4]+' bytes of data'
                        #tf=readsock_counted_debug(csock,int(text[4])+7)
                        tf=readsock_counted_debug(csock,int(text[4]))
                        print 'Got '+str(len(tf))
                        FILE = io.open(filename,"wb")
                        FILE.write(tf)
                        FILE.close
                        print "files.xml.bz2 saved to current directory"
                        break
                    #if text[0]=='':
                    #random.randint(1,10000)
        return
    
    def DownloadFL_nmdc(self,Bnick):
        print 'Trying...'
        ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ds.bind((self.botip, self.useport))
        print 'Started to listen port '+str(self.useport)
        ds.listen(1)
        self.saycommand('$ConnectToMe '+Bnick+' '+self.botip+':'+str(self.useport)+'|')
        while 1:
            csock, caddr = ds.accept()
            print 'accepted connection from '+str(caddr)
            while 1:
                    t=readsock(csock)
                    print 'Got '+t
                    text=t.split()
                    if text[0]=='$MyNick': csock.send('$MyNick '+self.botnick+'|')
                    if text[0]=='$Lock':
                        csock.send('$Lock EXTENDEDPROTOCOLABCABCABCABCABCABC Pk=DCPLUSPLUS0.706ABCABC|')
                        zz=lock2key2(text[1])
                    if text[0]=='$Key':
                        csock.send('$Supports MiniSlots XmlBZList |')
                        print "Sent $Supports"
                        csock.send('$Direction Download 77777|')
                        print "Sent $Direction"
                        csock.send('$Key '+zz+' |')
                        print '$key sent!'
                        #csock.send('$ADCGET file files.xml.bz2 0 -1|')
                        #csock.send('$GET files.xml.bz2$1 |')
                        csock.send('$Get files.xml.bz2$1|')
                    if text[0]=='$FileLength':
                        filename='files.xml.bz2'
                        print 'Reading '+text[1]+' bytes of data'
                        fsize=int(text[1])
                        csock.send('$Send|')
                        
                        ###tmp buff = 40960 bytes
                        ###wanna read a lot of chunks
                        ### read from socket, write to file, etc...
                        FILE = io.open(filename,"wb")
                        gottedsize=0
                        while gottedsize<fsize:
                            if (fsize-gottedsize)/40960==0:
                                #we have do additional download a (fsize-gottedsize)%40960 bytes
                                tf=readsock_counted_debug(csock,(fsize-gottedsize)%40960)
                            else:
                                tf=readsock_counted_debug(csock,40960)
                            ### progress showing
                            
                            
                            #print 'Got '+str(len(tf))
                            gottedsize+=len(tf)
                            FILE.write(tf)
                        
                        
                        #FILE.write(tf)
                        FILE.close
                        print "files.xml.bz2 saved to current directory"
                        ds.close
                        break
                    #if text[0]=='':
                    #random.randint(1,10000)
            break
        return
    
    def UploadFL_nmdc(self,Bnick):
        print 'Trying...'
        ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ds.bind((self.botip, self.useport))
        print 'Started to listen port '+str(self.useport)
        ds.listen(1)
        self.saycommand('$ConnectToMe '+Bnick+' '+self.botip+':'+str(self.useport)+'|')
        while 1:
            
            csock, caddr = ds.accept()
            print 'accepted connection from '+str(caddr)
            while 1:
                    t=readsock(csock)
                    print 'Got '+t
                    text=t.split()
                    if text[0]=='$MyNick': csock.send('$MyNick '+self.botnick+'|')
                    if text[0]=='$Lock':
                        csock.send('$Lock EXTENDEDPROTOCOLABCABCABCABCABCABC Pk=DCPLUSPLUS0.706ABCABC|')
                        zz=lock2key2(text[1])
                    if text[0]=='$Key':
                        csock.send('$Supports MiniSlots XmlBZList |')
                        print "Sent $Supports"
                        csock.send('$Direction Download 77777|')
                        print "Sent $Direction"
                        csock.send('$Key '+zz+' |')
                        print '$key sent!'
                        #csock.send('$ADCGET file files.xml.bz2 0 -1|')
                        #csock.send('$GET files.xml.bz2$1 |')
                        csock.send('$Get MyList.DcLst$1|')
                    if text[0]=='$ADCSND':
                        filename='files.xml.bz2'
                        print 'Reading '+text[4]+' bytes of data'
                        #tf=readsock_counted_debug(csock,int(text[4])+7)
                        tf=readsock_counted_debug(csock,int(text[4]))
                        print 'Got '+str(len(tf))
                        FILE = io.open(filename,"wb")
                        FILE.write(tf)
                        FILE.close
                        print "files.xml.bz2 saved to current directory"
                        break
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

#tbot.DownloadFL('[Elenet]Werb')
tbot.DownloadFL_nmdc('dr-evil')
tbot.workloop()