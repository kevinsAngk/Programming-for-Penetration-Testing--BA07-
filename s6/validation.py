


port = input("imput port: ")
port =int(port)
#validation port
if port<1000 or port >2000 :
    exit()



#validation ip
ip = input("input ip: ")
# validasi ip
# 0-255
# 4 bagian dipisah pakai tanda titik
if ip.count(".")!=3:
    print("invalid ip")
    exit()

for part in ip.split("."):
    print(f"{part}")
    part = int(part)
    if part<0 or part>255:
        print("invalid ip")
        exit()

