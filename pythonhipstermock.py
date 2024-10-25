from base64 import b64decode
import json
import time
import socket
import paho.mqtt.client as paho

def load_dict_from_file():
    f = open('requestanswer.txt','r')
    data=f.read()
    f.close()
    return eval(data)


reqAnswers = load_dict_from_file()

# creating a socket object
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

# get local Host machine name
host = '' # or just use (host == '')
port = 60250

# bind to pot
s.bind((host, port))

# Que up to 5 requests
s.listen(5)
# outer loop waiting for socket connections
while True:
    print("Waiting for socket connections on localhost:" + str(port))
    clientSocket, addr = s.accept()
    # establish connection
    print("got a connection from %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    #clientSocket.send(currentTime.encode('ascii'))

    # inner loop waiting for socket-calls
    while True:
        reqAnswers = load_dict_from_file() # uncomment in not debugging/developing
        data = clientSocket.recv(1024)
        if not data:
            break

        print('receive ' + str(data))
        if (data in reqAnswers):
            print('answer ' + str(reqAnswers[data]))
            clientSocket.send(reqAnswers[data]) # what to return?
        else:
            print('Comand not defined... please add to requestanswer.txt...')
        
    clientSocket.close()