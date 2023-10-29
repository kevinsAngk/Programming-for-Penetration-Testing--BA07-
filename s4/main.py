import sys 
from getopt import getopt
import socket

ip =""
port = 0
is_server= False

def handle_client(connection, client_address):

    pass

def run_server():
    print("server is trying to listening")
    #bikin socket
    #parameternya : tipe address(Ipv4) , protokol(Tcp)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip,port))
    #listen
    server.listen()
    print("server is listening")
    connection, client_address =server.accept()
    print(f"connected with client at{client_address}")
    while True:
    #accept
        message = input("input message['exit' to close connection]: ")
        #kalau exit -> dead
        if message == "exit":
            server.close()
            break
        connection.send(message.encode())
        #terima response/result dari targetnya
        result = connection.recv(1024).decode()
        print(result)



def run_target():
    print("target is trying to listening")
    target = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    target.connect((ip,port))
    while True:
        message = target.recv(1024).decode()
        message = input("input message['exit' to close connection]: ")
        if message == "exit":
            target.close()
            break
        result= "executing command" + message
        target.send(result.encode())

    


def main():
    global ip , port, is_server
    
    opts, _ = getopt(sys.argv[1:], "i:p:s",["ip=","port=", "server"] )
    print(opts)
    
    for opt, value in opts:
        print(f"{opt}:{value}")
        if opt == "-i" or opt == "--ip":
            ip=value
        elif opt == "-p" or opt =="--port":
            port = int(value)
        elif opt == "-s" or opt =="--server":
            is_server = True

    if ip == "":
        print("Ip must be filled !")
        exit()
    if port >2500 :
        print("Port must be between 2000 and 2500!")
        exit()
    if port <2000 :
        print("Port must be between 2000 and 2500!")
        exit()
    
    if is_server :
        run_server()
    else:
        run_target()






main()