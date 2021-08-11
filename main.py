import socket
import os
import struct
import time


def checksum(analyse_string):
    sum = 0
    countTo = (len(analyse_string)/2)*2
    count = 0
    while count < countTo:
        thisVal = ord(analyse_string[count + 1])*256 + ord(analyse_string[count])
        sum = sum + thisVal
        sum = sum & 0xffffffff
        count = count + 2

    if countTo < len(analyse_string):
        sum = sum + ord(analyse_string[len(analyse_string) - 1])
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff

    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer

def source_string(my_id):
    # 8 is the icmp echo request, checksum = 0
    bytes_header = struct.pack("bbHHh", 8, 0, 0, my_id, 1)
    string_header = bytes_header.decode("latin-1")

    bytesInDouble = struct.calcsize("d")
    
    #calc to know where data init
    data = (192 - bytesInDouble) * "U"
    byte_struct = struct.pack("d", time.time())
    string_struct = byte_struct.decode("latin-1")
    
    data =  string_struct + data 
    
    return string_header + data, data
    


def send_ping(my_socket, dest, my_id):
    dest_host = socket.gethostbyname(dest)
    print(dest_host)

    analyse_string, data = source_string(my_id)

    my_checksum = checksum(analyse_string)
    myChecksum = socket.htons(my_checksum)
    bytes_header = struct.pack("bbHHh", 8, 0, myChecksum, my_id, 1)
    string_header = bytes_header.decode("latin-1")
    packet = string_header + data


    my_socket.sendto(str.encode(packet), (dest, 1))

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
