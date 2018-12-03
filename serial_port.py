import serial
 
port = "COM1"
baud = 57600
 
ser = serial.Serial(port, baud)
ser.isopen()
print(ser.name + ' is open...')
 



    
 
