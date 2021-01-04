# -*- coding: utf-8 -*-
"""
Name: Kiran Mai Puli
UTA id: 1001661668
"""

from socket import *
import sys

if len(sys.argv) > 1:
    serverName = sys.argv[1]
else:
    serverName = "localhost"

if len(sys.argv) > 2:
    serverPort = int(sys.argv[2])
else:
    serverPort = 8080

if len(sys.argv) > 3:
    filename = sys.argv[3]
else:
    filename = "index.html"

""" Source code referenced from Programming Assignment 1_reference_Python.pdf"""
clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
#sentence = input("enter a filename")
print("this is the client")
clientSocket.send(bytes(filename,"utf-8"))
fromServer = clientSocket.recv(1024)
print("from server: ",fromServer.decode("utf-8"))
clientSocket.close()
