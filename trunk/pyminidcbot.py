#!/usr/bin/env python
# -*- coding: utf8 -*-
import socket, array, time, string
class pyminidcbot:
    HOST='10.4.20.7'
    PORT=411
    nick='BotTest'
    debugflag=1
    loggedon=(0)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def getsocketdata(self,somesocket):
        
        #print "in readsock\n"
        buff = ""
        counter=0
        somesocket.settimeout(0.13)
        while True:
            try:
                while True:
                    counter+=1
                    t = somesocket.recv(1)
                    if t != '|': buff += t
                    else: return buff
                    if counter>=4096: return buff
            except socket.timeout:
                pass    # Проверяем, не нужно ли завершить цикл?
            except socket.error, msg:
                return    # Обрабатываем ошибку сокета
        # Здесь в buff будет целый пакет, делаем с ним много всякого полезного...
        return buff
    def lock2key2(self,lock):
    #"Generates response to $Lock challenge from Direct Connect Servers"
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
    def connect(self,socket):
        self.s.connect((self.HOST, self.PORT))
        return
    def dispatch(self,message):
        if not message: return
        datalist = message.split();
        if (message) and self.debugflag==1: print "DEBUG: "+message
        if datalist[0] == '$Lock' :
            self.s.send('$Key '+self.lock2key2(datalist[1])+'|')
            self.s.send('$ValidateNick '+self.nick+'|')
            print 'Key & ValidateNick sent'
        if  ((datalist[0] == '$Hello') and (datalist[1]==self.nick)):
                self.loggedon = 1
                print 'Login complete ;) sending MyINFO'
                self.s.send('$MyINFO $ALL '+self.nick+' [[2M/192K]]<++ V:0.698,M:A,H:0/0/1,S:3>$DSL?$no@spam.thx$152177393537$|')    
                return
    
    def run(self):
        self.connect(self.s)
        while 1:
             self.dispatch(self.getsocketdata(self.s))
             if self.loggedon==1 : self.s.send('<'+self.nick+'> test|')
        return
       
      
t=pyminidcbot()
t.run()    