import socket 
import serial
import time 
print("opening dev/ttyS10")
ser = serial.Serial('/dev/ttyS10')
print("creating socket")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost',50000))
print("created socket")
s.listen(5)
conn, addr = s.accept() 
print("conn: ", conn, "addr: ", addr, "accepted" )
while 1: 
    data = ser.read()
    if(data == b'R' or data == b'C' or data == b'L' or data == b'U' or data == b'D' or data == b'O'):
        print("data from bluetooth-> sending:", data)
        conn.sendall(data)
conn.close()