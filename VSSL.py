import socket
import sys
import time
import subprocess
import os
from datetime import datetime

def SendMsearchPackets():
    msg = \
        'M-SEARCH * HTTP/1.1\r\n' \
        'HOST:239.255.255.250:1800\r\n' \
        'ST:upnp:rootdevice\r\n' \
        'MX:2\r\n' \
        'MAN:"ssdp:discover"\r\n'

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.settimeout(5)
    s.sendto(bytes(msg.encode()),('239.255.255.250',1800))
    print ("Sending M-Search packets")
   

    speakerinfo={}
    d={}
    devices={}

        
    try: 
        
        while True:

            data, addr = s.recvfrom(6557)
            a = str(data)
            b = str(addr)
            print ("---Address-->: ", b)
            tempdata = a.split('\\r\\n')
            for i in range(1,(len(tempdata)-1)):
                dictsplit=tempdata[i].split(':')
                speakerinfo.update({dictsplit[0]:dictsplit[1]})
            d.update(speakerinfo)
            for k,v in d.items():
                if k == 'DeviceName':
                    print(k,'--->',v)
            tm = (b.split(",")[0])
            tm1 = tm[2:-1]
            print (tm1)
            fm = open('msearch'+'.txt','a')
            fm.write(str(datetime.now()))
            fm.write("\n\n----------------------\n\n")
            
            fm.write(tm1)
            fm.write("\n\n----------------------\n\n")
            fm.close()
            
            fo = open(tm1+'.txt','a')
            tim = str(datetime.now())
            print (tim)
            fo.write("\n\n----------------------\n\n")
            
            fo.write(tim)
            fo.write("\n\n----------------------\n\n")
            fo.close()
            cmdd = "ping "+str(tm1)+" -n 10 >> "+str(tm1)+".txt" 
            #proc = subprocess.call(cmdd)
            print (cmdd)
            os.system(cmdd)
            
            
    except Exception as e:
        s.close()


if __name__=="__main__":
    iteration = 0
    while True:
        iteration = iteration +1
        print (iteration)
        SendMsearchPackets()

