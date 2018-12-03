import socket
import sys
import time


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
                
    except Exception as e:
        s.close()

SendMsearchPackets()

s = -1
host = ""
def create_luci_packet(CommandType,Command,Data,DataLength):
    RemoteID = 0
    CommandStatus = 0
    L_Crc = 0
    values = bytearray(10)
    values [0] = RemoteID & 0x00FF
    values [1] = ((RemoteID & 0xFF00) >> 8)
    values [2] = CommandType & 0x00FF 
    values [3] = Command & 0x00FF
    values [4] = ((Command & 0xFF00) >> 8)
    values [5] = CommandStatus
    values [6] = L_Crc & 0x00FF
    values [7] = (L_Crc & 0xFF00)>>8
    values [8] = DataLength & 0x00FF
    values [9] = ((DataLength & 0xFF00)>>8)
    values.extend(Data.encode())
    return values

def sendlucipacket(values):
    global s
    try:
        s.sendall(values)
        rec = s.recv(1024)
       # print ('Received packets\n', rec)
        print ('MB number------> ', rec[4])
        print ('Data-----------> ', rec[10:])
    except:
        s.close()


def Create_Connection(host):
    print ("Create connection",host)
    global s
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = 7777
    s.connect((host,port))

def RegAsync():
    global s
    CommandType = 2
    MB = 3
    RemoteID = 0
    CommandStatus = 0
    L_Crc = 0
    CommandType=2  
   # Create_Connection()
    print ("Connection created")
    Data=s.getsockname()[0]
    Data+=","
    Data+=str(s.getsockname()[1])
    print("\n IP addr of laptop is: " + Data + "Port: " + str(s.getsockname()[1]))
    data_len=len(Data)
    val=create_luci_packet(CommandType,MB,Data,data_len)
    print(val)
    sendlucipacket(val)
    
def trigger_wac():
    MB = 142
    CommandType = 2
    Data=""
    data_len=len(Data)
    val=create_luci_packet(CommandType,MB,Data,data_len)
    sendlucipacket(val)

def set_master():
    CommandType = 2
    MB = 100
    data = 'SETMASTER'
    data_len = len(data)
    val = create_luci_packet(CommandType,MB,data,data_len)
    sendlucipacket(val)

def set_free():
    CommandType = 2
    MB = 100
    data = 'SETFREE'
    data_len = len(data)
    val = create_luci_packet(CommandType,MB,data,data_len)
    sendlucipacket(val)

def playerstate():
    CommandType = 1
    MB = 103
    data = ''
    data_len = len(data)
    val = create_luci_packet(CommandType,MB,data,data_len)
    sendlucipacket(val)

def get_vol():
    CommandType = 1
    MB = 64
    data = ''
    data_len = len(data)
    val = create_luci_packet(CommandType,MB,data,data_len)
    sendlucipacket(val)

def device_name():
    CommandType = 1
    MB = 90
    data = ''
    data_len = len(data)
    val = create_luci_packet(CommandType,MB,data,data_len)
    sendlucipacket(val)

def browse_UI():
    CommandType = 2
    MB = 41
    data = 'GETUI'
    data_len = len(data)
    val = create_luci_packet(CommandType,MB,data,data_len)
    sendlucipacket(val)

def de_reg():
    MB = 4
    CommandType = 2
    Data=str(s.getsockname()[0])
    data_len = len(Data)
    val=create_luci_packet(CommandType,MB,Data,data_len)
    sendlucipacket(val)
    print ('De reg done')

def getenv():
    MB = 208
    CommandType = 1
    a = input('Plz enter the env name: ')
    Data = "READ_"+str(a)
    data_len = len(Data)
    val = create_luci_packet(CommandType,MB,Data,data_len)
    sendlucipacket(val)

def setenv():
    MB = 208
    CommandType = 2
    a = input('Plz enter the env name followed by a comma and env value: ')
    Data = "WRITE_"+a
    print ('setenv data',Data)
    data_len = len(Data)
    val = create_luci_packet(CommandType,MB,Data,data_len)
    sendlucipacket(val)

def switchdevice():
   # de_reg()
    s = input('Enter the IP address of the DUT you want to switch to:\n')
    Create_Connection(s)
    RegAsync()
    operation()

def main():
    m = input("Enter the IP address of the DUT\n")
    print(m)
    Create_Connection(m)
    RegAsync()
    operation()

def operation():
    while 1 :
        option=input('''Enter an option\n
                     1:device_name\n
                     2:set_master\n
                     3:set_free\n
                     4:ddms_state\n
                     5:get_vol\n
                     6:browse_UI\n
                     7:trigger_wac\n
                     8:exit\n
                     9:browse UI\n
                     10:getenv\n
                     11:setenv\n
                     12:choose another device\n''')
        print (option)
        if option == '1':
             device_name()
        elif option == '2':
             set_master()
        elif option == '3':
            set_free()
        elif option == '4':
            playerstate()
        elif option == '5':
             get_vol()
        elif option == '6':
            browse_UI()
        elif option == '7':
            trigger_wac()
        elif option == '8':
            s.close()
            sys.exit()
        elif option == '9':
            browse_UI()
        elif option == '10':
            getenv()
        elif option == '11':
            setenv()
        elif option == '12':
            switchdevice()
main()
    
