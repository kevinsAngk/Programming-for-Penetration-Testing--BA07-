import sys
from getopt import getopt
import threading
import socket



# print(sys.argv())

ip =""
port= 0
is_server = False

def handle_client(connection, client_address):
    while True:
        # 1024 adalah maksimum byte yang diterima dalam 1 kali kirim pesan
        message = connection.recv(1024)
        if not message:
            connection.close()
            break
        else:
             print(f"{client_address}:{message.decode()}")






def create_server():
    print("create server socker")
    #bikin socket
    #parameternya : tipe address(Ipv4) , protokol(Tcp)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #di alamat adan port mana
    server.bind((ip,port))

    #listen
    server.listen()
    print("server is listening")

    while True:
    #accept
        connection, client_address =server.accept()
        print(f"connected with client at{client_address}")
        # handle_client(connection, client_address)
        t= threading.Thread(target=handle_client, args=(connection, client_address))
        t.start()



def create_client():
    print ("creating client socket")
    #bikin socket client
    client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #connect ke server
    client.connect((ip,port))
    print("connected to server")
    # send data
    while True:
        message = input("input message['exit' to close connection]: ")
        #kalau exit -> dead
        if message == "exit":
            client.close()
            break
        else:
            client.sendall(bytes(message, "utf-8"))

def main():
    global ip,port, is_server
    opts, _ =getopt(sys.argv[1:], "i:p:s", {"ip=","port=", "server"})
    for opt, value in opts:
        # print(f"{opt}:{value}")
        if opt == "-i" or opt == "--ip":
            ip=value
        elif opt == "-p" or opt =="--port":
            port = int(value)
        elif opt == "-s" or opt =="--server":
            is_server = True

    if ip == "" or port ==0:
        print("ip and port is requires")
        exit()

    if is_server == True:
        create_server()
    else  : create_client()



main()




















































































































































