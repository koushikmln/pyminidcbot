#!/usr/bin/env python
# -*- coding: cp1251 -*-
import socket, array, time, string,sys,random,threading,pickle

class ClientThread(threading.Thread):

    # Override Thread's __init__ method to accept the parameters needed:
    def __init__(self, channel, details):
        self.channel = channel
        self.details = details
        threading.Thread.__init__(self)
    def downloader(self):
        while 1:


            return 0
    def run(self):

        print 'Received connection:', self.details[0]
        self.channel.settimeout(10)
        self.channel.send('$Direction Download 75|') #this sent to channel
        outfile=open(self.details[0]+'.tmp','wb')
        print 'file opened to write'
        buff=""
        while True:
            try:
                while True:
                    t = self.channel.recv(1)
                    buff += t
            except socket.timeout: pass
            except socket.error, msg: break
        print 'got from connect '+t
        outfile.write(t)
        self.channel.close()
        print 'Closed connection:', self.details[0]


class pyminidcbot2:
    HOST = 'dc.elenet.info'
    PORT = 411
    nick = '0PyMiniDCBot'
    sharesize='1501200000'
    debugflag=1
    commanddebug=1
    ownernick='dr-evil'
    loggedon=0
    havenicklist=0
    myip='10.0.0.197'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tmpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def readsock(self,sock):
        buff = ""
        sock.settimeout(0.13)
        while True:
            try:
                while True:
                    t = sock.recv(1)
                    if t != '|': buff += t
                    else: return buff
            except socket.timeout:
                pass    # Проверяем, не нужно ли завершить цикл?
            except socket.error, msg:
                return    # Обрабатываем ошибку сокета
        # Здесь в buff будет целый пакет, делаем с ним много всякого полезного...
        return buff

    def readconn(self,conn):
        buff = ""
        conn.settimeout(0.13)
        while True:
            try:
                while True:
                    t = conn.recv(1)
                    if t != '|': buff += t
                    else: return buff
            except socket.timeout:
                pass    # Проверяем, не нужно ли завершить цикл?
            except socket.error, msg:
                return    # Обрабатываем ошибку сокета
        # Здесь в buff будет целый пакет, делаем с ним много всякого полезного...
        return buff

        return
    def parsecommand(self,gotstring):
    #смотрим на полученную строку и выполняем действия
        if (gotstring != ''):
            str = gotstring.split()
            if (self.debugflag): print 'DEBUG: '+gotstring
            if str[0] == '$Lock':
                #print 'Here the lock'+str[0]+' and param '+str[1]
                self.s.send('$Key '+self.lock2key2(str[1])+'|')
                self.s.send('$ValidateNick '+self.nick+'|')
            elif str[0] == '$UserIP': # $Hello
                    if (self.debugflag): print '\nGot $UserIP'

            elif str[0] == '$Hello':
                    self.s.send('$Version 1,0091|')
                    if (self.debugflag): print 'DEBUG: Sending $Version'
                    self.s.send('$MyINFO $ALL '+self.nick+' simple python bot$ $100$bot@bot.com$'+self.sharesize+'$|')
                    if (self.debugflag): print 'DEBUG: Sending $MyINFO'
            elif str[0] == '$HubTopic':
                        if (self.debugflag): print 'DEBUG: Got $HubTopic - login complete'
                        return 'Logged'
            if str[0]: return str[0]
        return
    def lock2key2(self,lock):
        "Generates response to $Lock challenge from Direct Connect Servers"
        lock = array.array('B', lock)
        ll = len(lock)
        key = list('0'*ll)
        for n in xrange(1,ll):
            key[n] = lock[n]^lock[n-1]
        key[0] = lock[0] ^ lock[-1] ^ lock[-2] ^ 5
        for n in xrange(ll):
            key[n] = ((key[n] << 4) | (key[n] >> 4)) & 255
        result = ""
        for c in key:
            if c in (0, 5, 36, 96, 124, 126):
                result += "/%%DCN%.3i%%/" % c
            else:
                result += chr(c)
        return result
    def loginloop(self):
        #print "in mainloop\n"
        while 1:
             data=self.readsock(self.s)
             t=self.parsecommand(data)
             if t =='Logged': break
        return
    def dispatch(self,command):
        #if command: print '\nHere the command'+command

        return
    def logintohub(self):
        print 'connecting....'
        self.s.connect((self.HOST, self.PORT))
        self.s.send('Hello, world|')
        self.loginloop()
        return
    def saytest(self):
        self.s.send('<'+self.nick+'> Hi! I\'m an ugly bot written in Python by dr-evil (c)|')

    def saytochat(self,message):
        self.s.send('<'+self.nick+'> '+message+'|')
        return
    def rawprint(self,message):
        self.s.send(message)

    def commands(self,mycommand):
        cstr = mycommand.split()
        lsize=len(cstr)
        ti=0
        if (self.commanddebug):
            while ti != lsize:
                print '%d=%s' %(ti,cstr[ti])
                ti=ti+1
        if (cstr[1]=='\QUIT'):
                self.saytochat('Leaving this hub.... bye all')
                sys.exit()
        if (cstr[1]=='\GET'):
                self.saytochat('Getting filelist....')
                self.downloadfilelist('[elenet]dr-evil')

        return
    def upload(self):
        return 0

    def mainloop(self):
        while 1:
            data=self.readsock(self.s)

            if (data != ''):
                str = data.split()
                #print '------------DEBUG: '+str[0]
                if (str[0] !='$Search') and (str[0] !='$MyINFO') and (str[0] !='$Hello') and (str[0] !='$Quit'):   print 'DEBUGdataML: '+data
                if (str[0]=='<'+self.ownernick+'>'):
                        print 'DEBUG: GOT OWNER MESSAGE!!!!!!!'+data
                        self.commands(data)
                elif ((str[0]=='$Hello') and (str[1]==self.nick)):
                        print '-----DEBUGdata: We finished logging on. Yahoo!'
                        self.loggedon=1

                elif (str[0])=='$NickList':
                        print 'got nicklist'
                        self.getnicklist(str[1])
                elif (str[0])=='$ConnectToMe':
                        print '-----DEBUGdata: Got connect request to '+str[2]
                        self.upload()

            if ((self.loggedon==1) and (self.havenicklist==0)):
                self.rawprint('$GetNickList|')
                print "-----DEBUGdata: requesting nicklist"
#            time.sleep(3)
#            print 'requesting download'

        return
    def getnicklist(self,nicks):
        nicklist=nicks.split("$$")
        print 'processing nicklist'
        print len(nicklist)
        self.havenicklist=1
        #self.downloadfilelist('[elenet]dr-evil')
        return

    def downloadfilelist(self,nick):
        timeout=15
        starttime=time.time()
        #create an INET, STREAMing socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', 32000))
        server.settimeout(timeout)
        #become a server socket
        self.rawprint('$ConnectToMe [elenet]dr-evil 217.195.88.66:32000 |') #establish a connect with client
        print 'listening socket....111'
        server.listen(5)
        while time.time() <= starttime+timeout:
            try:
                print 'going....'
                channel, details = server.accept()
                ClientThread(channel, details).run()
            except socket.timeout:
                print 'timeout :('
                break

        return
t=pyminidcbot2()
t.logintohub()
#t.saytochat('My message test')
t.mainloop()
