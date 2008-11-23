#!/usr/bin/env python
# -*- coding: cp1251 -*-
import socket, array, time, string,sys
class pyminidcbot2:
    HOST = '10.4.20.7'
    PORT = 411
    nick = 'MegaBotNick'
    sharesize='1501200'
    debugflag=0
    commanddebug=1
    ownernick='dr-evil'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

    def parsecommand(self,gotstring):
    #смотрим на полученную строку и выполняем действия
        if (gotstring != ''):
            str = gotstring.split()
            if (self.debugflag): print 'DEBUG: '+gotstring
            if str[0] == '$Lock':
                #print 'Here the lock'+str[0]+' and param '+str[1]
                self.s.send('$Key '+self.lock2key2(str[1])+'|')
                self.s.send('$ValidateNick '+self.nick+'|')
            elif str[0] == '$HubName':
                    print 'HubName= '
                    print str[1:-1]
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
        
        return
    def mainloop(self):
        while 1:
            data=self.readsock(self.s)
            if (self.debugflag): print 'DEBUG: '+data
            if (data != ''):
                str = data.split()
                if (str[0]=='<'+self.ownernick+'>'):
                        print 'DEBUG: GOT OWNER MESSAGE!!!!!!!'+data
                        self.commands(data)
            
        return

t=pyminidcbot2()
t.logintohub()
#t.saytochat('My message test')
t.mainloop()