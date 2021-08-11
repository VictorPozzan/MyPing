import socket
import os
import struct


def send_ping(my_socket, dest, my_id):
    dest_host = socket.gethostbyname(dest)
    print(dest_host)
    my_checksum = 0
    
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, my_id, 1)


def ping(dest):
    count = 5 #five ping requests
    timeout = 2
    
    for i in range(count):
        print("ping ", dest)
        try:
            icmp = socket.getprotobyname("icmp")
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, icmp)
            my_id = os.getpid() #& 0xFFFF
            #enviar o ping 
            send_ping(my_socket, dest, my_id)

        except socket.gaierror:
            print("error")
            break
            
    

if __name__=="__main__":
    ping("google.com")
