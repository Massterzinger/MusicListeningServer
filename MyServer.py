import socket
import os
import time
from urllib.parse import *
from threading import * 


ENC = 'UTF-8'
MainWebPage = "./Content/MainPage.html"
MusPath = r"/media/florian/01D1F32F6143C9A0/Music" #/media/florian/Elements/music"
WinMusPath = r"D:\Music\Sweet Dreams"
AudioMask = "<li>{0}<br/><audio controls preload='none'><source src='{1}' type='audio/mpeg'></audio></li>"
FolderRefMask = '<li><a href="{0}">{1}</a></li>'
PM = "HTTP/1.1 200 OK\r\n\r\n"
AudioFormats = ['.mp3', '.m4a', '.wav']
iconF = './Content/favicon.ico'
noImg = "./Content/NoImg.jpg"

def getfile(filepath):
    with open(filepath, 'r') as fil:
        text = fil.read()
        fil.close()
    return text
    
def getBin(Bpath):
    with open(Bpath,'rb') as bFil:
        bData = bFil.read()
        bFil.close()
    return bData
    
class MyThread (Thread):
    MainPageMask = ""
    def __init__(self,name, connection, address):
        Thread.__init__(self)
        self.name = name
        self.c = connection 
        self.addr = address
        self.data = ''
    def run (self):
        print ( 'run thread', self.name)
        self.data = dec (self.c.recv(1024))
        #print(self.data)
        if ('GET' in self.data): 
            try:
                self.ServeBrowser()
            except Exception as ex:
                print("Exception: ",ex)
        self.c.close ()
        print('Closed {}, name = {}'.format( self.addr, self.name))
        
    def ServeBrowser(self):
        pathX = unquote(self.data.split(' ')[1])
        #print(getText(self.data))
        resData = None
        print ('Browser on {} request, name = {}'.format(self.addr, self.name), pathX)
        if 'Content' in self.data:
            self.c.send(enc(PM)+getBin('.'+pathX))
            return    
        else:
            FullPath = os.path.join(MusPath,pathX[1:])
            print(FullPath, pathX)
            if ('.mp3' in pathX) or ('.m4a' in pathX): #need to Check if requested file is a music file
                resData = getBin(FullPath)
            elif ('.jpg' in pathX):
                try:
                    resData = getBin(FullPath)
                except:
                    resData = getBin(noImg)
            elif 'favicon' in pathX:
                resData = getBin(iconF)
            else:
                print('============================',pathX,'is not a file ==========')
                liMus = list(filter(lambda x: (".mp3" in x) or ('.m4a' in x), os.listdir(FullPath)))
                p = '\n'.join(list(map(lambda x : AudioMask.format(x,quote(pathX+x)), liMus)))
                liDirs = list(filter(lambda x: not((".mp3" in x) or ('.m4a' in x)), os.listdir(FullPath)))
                print(FullPath, liMus)
                print(FullPath, liDirs)
                if pathX[-1] != '/': pathX+='/'
                wpage = MyThread.MainPageMask.format(pathX+'folder.jpg',pathX,p)
                resData= enc(wpage)

        if len(resData) > (1024*512):
            self.c.sendall(enc(PM)+resData)           
        else:
            self.c.send (enc(PM)+resData)
            
             
        
def dec(bytMsg):
    return bytMsg.decode (ENC) 
def enc (strMsg):
    return strMsg.encode(ENC)
            
        
def Main():
    host = ''
    port = 80
    MyThread.MainPageMask = getfile(MainWebPage)
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    global work
    while True:
        c, addr = s.accept()
        thr = MyThread (addr, c, addr)
        thr.start()

Main()
