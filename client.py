#!/usr/bin/env python 

import select
import socket 
import sys

host= sys.argv[1]
port = int(sys.argv[2])
size = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((host,port)) 
print("You are connected: ")
data= s.recv(size)
print data
username=sys.stdin.readline()
s.send(username)
print s.recv(size)
pw=sys.stdin.readline()
s.send(pw)
data= s.recv(size)
print data
running=1
while running:
	input=[sys.stdin, s]
	read, write, error = select.select(input, [], [])
	for x in read:
		if x==s:
			data=s.recv(4096)
			if data=="":	
				print "Server has disconnected"
				s.close	
				sys.exit()
			sys.stdout.write(data)
			sys.stdout.write('\n')

		else:
			data=x.readline()
			s.send(data)
s.close()  


