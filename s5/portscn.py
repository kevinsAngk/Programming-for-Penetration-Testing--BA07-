import socket
import errno #buat baca error code
import threading

START_PORT = 0
END_PORT = 5000
opened_list =[]
thread_list =[]

def check_port(port):
    global opened_list
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(3)
    result= s.connect_ex(("127.0.0.1", port))
    #kalau result 0 berarti portnya open
    if result == 0:
        print(f"port {port} is opened")
    # else:
    #     print (f"{port} is closed: {errno.errorcode[result]}")
        
for port in range(START_PORT, END_PORT+1):
    t = threading.Thread(target=check_port, args=(port,))
    t.start()
    
for t in thread_list:
    t.join()
    
print(f"opened promt: {opened_list}")