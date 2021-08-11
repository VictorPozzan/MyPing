import socket




def ping(dest):
    count = 4 #five ping requests
    timeout = 2
    
    for i in range(count):
        print("ping ", dest)
        try:
            icmp = socket.getprotobyname("icmp")
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, icmp)
            print(icmp)
            print(my_socket)
        except socket.gaierror:
            print("error")
            break
            
    

if __name__=="__main__":
    ping("google.com")
