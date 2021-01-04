# -*- coding: utf-8 -*-

"""
Name: Kiran Mai Puli
UTA id: 1001661668
"""


"""                             Project 1                       """
""" Building a Simple Web Client and a Multithreaded Web Server """                            

"""
References:
1)	Programming Assignment 1_reference_Python.pdf – canvas UTA
2)	https://www.youtube.com/watch?v=PNt8zXl7EJ0
3)	https://www.youtube.com/watch?v=vyCboBjK4us
4)	https://www.youtube.com/watch?v=hFNZ6kdBgO0
5)	https://www.tutorialspoint.com/http/http_requests.htm
6)	https://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php
7)	https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
8)	https://www.tutorialspoint.com/socket-programming-with-multi-threading-in-python

"""

### all the import statements ####
from socket import *
import sys
import traceback
from threading import Thread
import os
import time

""" accessing command line arguments for getting serverPort from user """
if len(sys.argv) > 1:
    serverPort = int(sys.argv[1])
else:
    serverPort = 8080


""" creating socket for tcp connection """
def createServer():
    
    """ ServerSocket is the listening socket of the server """
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print("socket is created")
    try:
        """ localhost is used as the server ip address. 
        To change the ip address of the server, change localhost"""                
        serverSocket.bind(("localhost",serverPort))
    except:
        print("Bind failed. Error: ",str(sys.exc_info))
        sys.exit()
    serverSocket.listen(5)
    print("socket is listening")
    
############ infinite loop for every requests#############    
    
    while(1):
        
        """ welcomeSocket is the response socket """        
        (welcomeSocket, address) = serverSocket.accept()
        ip, port = str(address[0]), str(address[1])
        print("connected with",ip,":",port,welcomeSocket)
        try:
            
            """ for serving multiple clients at a time """            
            Thread(target=clientThread, args=(welcomeSocket, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()
    welcomeSocket.close()
    serverSocket.close()

        
""" Defining the response data to be sent to the client """
def definingResponse(filePath,fileName):
    t = time.localtime()
    t = time.strftime("%H:%M:%S", t)
    data = ""
    headerCreation = "Content-Type: text/html; charset = utf-8\r\n"
    headerCreation += 'Date: {now}\n'.format(now=t)
    headerCreation += 'Server: Simple-Python-Server\r\n'
    headerCreation += 'Connection: close\r\n' 
    headerCreation += "\r\n"
    
    """ if the client sends a request without a filename """
    if fileName == "" or fileName == "index.html":
        
        data = "HTTP/1.1 200 OK\r\n"
        data = data + headerCreation
        data += "<html><body><body><h1>Home page</h1><p>This is the home page of the server</p></body></body></html>"
        return data
    if filePath == "" or filePath == "/":
        
        """ if no path is mentioned by the user, 
        it is assumed that the requested file path is same as server's path """        
        filePath = os.path.dirname(__file__)
    try:
        
        """ path is set to the filePath """        
        os.chdir(filePath)
    except:
        data = "HTTP/1.1 400 Bad Request\r\n"
        data = data + headerCreation
        
    if data == "":
        if os.path.isfile(fileName):
            data = "HTTP/1.1 200 OK\r\n"
            data = data + headerCreation
            
            with open(fileName,'r') as f:
                l = f.read(5024)
            f.close()
            data = data + l 
            data += "\r\n\r\n"
        else:
            data = "HTTP/1.1 404 Not Found\r\n"
            data = data + headerCreation
    return data
            

""" for getting the path and filename of the client requested file"""
def getFileDetails(fileToBeSent):
    filePath = ""
    if fileToBeSent == "" or fileToBeSent == "/":
        fileName = ""
    else:
        getFilePathToBeSplit = fileToBeSent.split("/")
        if len(getFilePathToBeSplit) == 1:
            fileName = fileToBeSent
        else:
            fileName = getFilePathToBeSplit[-1]
            for i in range(0,len(getFilePathToBeSplit) - 1):
                filePath = filePath + getFilePathToBeSplit[i] + "/"
    return (fileName, filePath)
    
    
def clientThread(connection, ip, port, max_buffer_size = 5054):
    fileToBeSent = ""
    data = ""
    rd = connection.recv(max_buffer_size).decode() #request messages from client
    print(rd,"request received from the client")
    pieces = rd.split("\n")
    
    """ getting file Name and file Path for a web browser request """    
    if len(pieces) > 5:
        splittingURL = pieces[0].split(" ")
        if 'favicon.ico' not in pieces[0]:
            x = getFileDetails(splittingURL[1])
            fileName = x[0]
            filePath = x[1]
            if len(filePath) > 1:
                filePath = filePath[1:]
            data = definingResponse(filePath,fileName)

    
    """ getting file Name and file Path for a client 
    request through command prompt """    
    if len(pieces) == 1 and pieces[0] != "":  
        fileToBeSent = rd
        x = getFileDetails(fileToBeSent)
        fileName = x[0]
        filePath = x[1]
        data = definingResponse(filePath,fileName)
        
    """ sending server response with data to the client """
    connection.sendall(data.encode()) 
    rd = ''
    pieces = []
    connection.close()
    
        
createServer() # calling the server
        
            