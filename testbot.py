#!/usr/bin/env python
# -*- coding: cp1251 -*-
#testing bot - for testing new features
from botclass import *
from func import *

class TestBot(PyBot):
    botnick='TestBot'
    HOST='10.4.20.2'
    debug=2
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
tbot.workloop()