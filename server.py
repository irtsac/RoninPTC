import socket
import threading
import os
import base64
from cryptography.fernet import Fernet
import sys
import random
import string
import time
from datetime import datetime
currentDateAndTime = datetime.now()
global key

def printc(message):
    logs = False
    print(str(message))
    if logs == True:
        f = open("logs.txt", "a")
        message = str(currentDateAndTime) + "  :" + str(message) + "\n "
        f.write(message)
        f.close()
    
    

def encrypt(key, source):

    fernet = Fernet(key)
    encMessage = fernet.encrypt(source.encode('utf-8'))
    return encMessage

def decrypt(key, source):

    fernet = Fernet(key)
    decMessage = fernet.decrypt(source).decode('utf-8')
    return decMessage

host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
printc(f"[++]Server listening at {host, port}")
printc(f"[++]Generating key")

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
all_clients = []
chatrooms = []
codes = []
def broadcast(message, chatroom):
    message = encrypt(key, message)
    for client in chatroom:
        client.send(message)
def sendtochat(client, conn, chatroom, nickname):
    while True:
        try:
            message = client.recv(1024)
            message = decrypt(key, message)
            #printc
            broadcast(message, chatroom)
        except Exception as e:
            remove(client, conn, chatroom, nickname)
            break

def handle(client, conn):
    while True:
        try:
            # Broadcasting Messages
            hwid = client.recv(1024)
            hwid = decrypt(key, hwid)
            hwids = gethwids()
            printc(f"[+]{hwid} TRYING TO CONNECT")
            if hwid not in hwids:
                error = encrypt(key, 'ERROR')
                client.send(error)
                remove(client, conn, chatroom, nickname)
            else:
                logged = encrypt(key, 'LOGGED')
                client.send(logged)
                printc("[+] Connected with {}".format(str(conn)))
                # Request And Store Nickname
                nick = encrypt(key, 'NICK')
                client.send(nick)
                nickname = client.recv(1024)
                nickname = decrypt(key, nickname)
                if nickname not in nicknames:
                    OK = encrypt(key, "OK")
                    client.send(OK)
                    nicknames.append(nickname)
                    code = client.recv(1024)
                    code = decrypt(key, code)
                    printc(f"[+]Chatroom: {code}")
                    if code in codes:
                        pass
                    else:
                        codes.append(code)
                        chatroom = []
                        chatrooms.append(chatroom)
                        printc(f"[+] Chatroom created: {code}")
                    printc(f"[!] Current chatroom {str(codes)}")
                    chatroomnum = codes.index(code)
                    chatroom = chatrooms[chatroomnum]
                    chatroom.append(client)
                    printc("[+] Nickname is {}".format(nickname))
                    broadcast("{} joined the chatroom!".format(nickname), chatroom)
                    connected = encrypt(key, "Connected to the server!")
                    client.send(connected)
                    chatlethread = threading.Thread(target=sendtochat, args=(client,conn,chatroom,nickname))
                    chatlethread.start()
                    break
                else:
                    error = encrypt(key, "ERROR")
                    client.send(error)
                    remove(client, conn, chatroom, nickname)
                    break
        except Exception as e:
                printc("[!!!]Error handling the client")
                remove(client, conn,)
                break
            

def remove(client, conn, chatroom=None, nickname=None):
    try:
        if chatroom:
            if client in chatroom:
                chatroom.remove(client)
                if len(chatroom) == 0:
                    i = chatrooms.index(chatroom)
                    codes.remove(codes[i])
                    printc(f"[!] Available chatrooms: {str(codes)}")
                    chatrooms.remove(chatroom)
                    
        if nickname in nicknames:
            nicknames.remove(nickname)
        if client in clients:
            clients.remove(client)
            printc(f"[-] Removed {conn} from clients")
        if client in all_clients:
            all_clients.remove(client)
        printc("[-]" + str(conn) + " left!")
        client.close()
    except Exception as e:
            printc("[!!!]Error removing the client" + str(e))
def gethwids():
    hwids = []
    file = open("auths.txt", "r")
    lines = file.readlines()
    for line in lines:

        hwids.append(line[:-1])
    return hwids
def receive():
    while True:
        try:

            # Accept Connection
            client, address = server.accept()
            all_clients.append(client)
            printc(f"[?] {address} Trying to get key")
            ran =''.join(random.choice(string.ascii_letters) for _ in range(21))
            ran2 =''.join(random.choice(string.ascii_letters) for _ in range(15))
            keyy = ran + key.decode()[:-1] + "1y72ns0" + ran2
            client.send(keyy.encode())
            handlethread = threading.Thread(target=handle, args=(client, address,))
            handlethread.start()

        except Exception as e:
            printc("[!!!]Error receinving the client" + str(e))
            remove(client, address,)
            continue

def sendkey():

        while True:
            time.sleep(5)
            global key
            key = Fernet.generate_key()
            printc("[+]Generated new key!")
            ran =''.join(random.choice(string.ascii_letters) for _ in range(21))
            ran2 = ''.join(random.choice(string.ascii_letters) for _ in range(15))
            keyy = ran + key.decode()[:-1] + "1y72ns0" + ran2
            try:

                for client in all_clients:
                    client.send(keyy.encode())
                    
    
            except Exception as e:
                printc("[!!!]Error generating and sending key")
                continue


sendkey = threading.Thread(target=sendkey)
sendkey.start()

receive()
