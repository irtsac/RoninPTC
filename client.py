import socket
import threading
import time
import os
import subprocess
import base64
from cryptography.fernet import Fernet
import sys


def encrypt(key, source):

    fernet = Fernet(key)
    encMessage = fernet.encrypt(source.encode())
    return encMessage

def decrypt(key, source):

    fernet = Fernet(key)
    decMessage = fernet.decrypt(source).decode()
    return decMessage



hwid = current_machine_id = str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
nickname = input("Username: ")
chatroom = input("chatroom: ")
# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))






key = client.recv(1024).decode()
print(key)
key = key[21:][:-22] + "="
key = key.encode()
print(key)
hwid = encrypt(key, hwid)
client.send(hwid)
message = client.recv(1024)
print(message)
message = decrypt(key, message)
if message == "LOGGED":
    pass
else:
    input(f"PC not authenticated. Contact me on discord for authenticate: @li3less . \nHWID: {hwid}")
    os._exit(0)



def receive(nickname):
    while True:
        #try:
            global key
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode()
            print(message)
            if "1y72ns0" in message:
                print("there is")
                key = message[21:][:-22] + "="
                print(key)
                key = key.encode()
                print(key)
                #return key
            else:
                message = message.encode()
                message = decrypt(key, message)
                if message == 'NICK':
                    print(nickname)
                    nickname = encrypt(key, nickname)
                    print(nickname)
                    client.send(nickname)
                    message = client.recv(1024)
                    message = decrypt(key, message)
                    if message == 'OK':
                        
                        message = encrypt(key, chatroom)
                        message = client.send(message)
                        continue
                    else:
                        input("Username alredy chosen. Or connection error! ")
                        os._exit(0)
                else:
                    print(message)
        #except Exception as e:

            # Close Connection When Error
            #print(e)
            #client.close()
            #break

def write(nickname):
    while True:
        time.sleep(0.2)
        firstmessage = input("")
        CURSOR_UP_ONE = '\x1b[1A'
        ERASE_LINE = '\x1b[2K'
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)
        if firstmessage == ("/quit"):
            os._exit(0)
        else:
            message = (nickname + ": " + firstmessage)
            cryptmessage = encrypt(key, message)
            client.send(cryptmessage)
            print (nickname + ": " + firstmessage, end="\r")


def getkey():
    global key
    while True:
        message = client.recv(1024).decode()
        print(message)


#keythread = threading.Thread(target=getkey)
#keythread.start()

write_thread = threading.Thread(target=receive, args=(nickname,))
write_thread.start()




write_thread = threading.Thread(target=write, args=(nickname,))
write_thread.start()
