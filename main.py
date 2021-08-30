import socket
import os
import struct
import time
import select
from ping_data import Ping_Data



def checksum(bytes_header):
    size = len(bytes_header) 
    sum_bytes = 0

    for i in range(0, size - (size % 2), 2):
        sum_bytes += (bytes_header[i]) + ((bytes_header[i+1]) << 8)
    
    if size % 2:
        sum_bytes += (bytes_header[-1])

    sum_bytes = (sum_bytes >> 16) + (sum_bytes & 0xffff)
    sum_bytes += (sum_bytes >> 16) 
    answer = ~sum_bytes & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer



def convert_header(header_type,header_code,header_checksum,header_identifier,header_sequence_number,header_payload):
    #converte o cabeçalho para binário
    bytes_header = struct.pack('>BBHHH32s',header_type,header_code,header_checksum,header_identifier,header_sequence_number,header_payload)
    #faz o checksum
    data_checksum = checksum(bytes_header) 
    packet = struct.pack('>BBHHH32s',header_type,header_code,data_checksum,header_identifier,header_sequence_number,header_payload)

    return packet

def reply(connect_time, my_socket, header_sequence):
    timeout = 2
    while True:
        reply_time = time.time()
        has_timeout = select.select([my_socket], [], [], timeout)

        waiting_time = (time.time() - reply_time)

        if has_timeout[0] == []:  #timeout
            return -1
         
        time_received = time.time()
        received_packet, addr = my_socket.recvfrom(1024)

        reply_type, reply_code, reply_checksum, reply_identifier, reply_sequence = struct.unpack(">BBHHH", received_packet[20:28])
        #reply_type == 0 porque 0 é o echo reply ICMP
        if reply_type == 0 and reply_sequence == header_sequence:
            return time_received - connect_time # o tempo de resposta do ping

        #timeout
        timeout = timeout - waiting_time
        if timeout <= 0:
            return -1    

def connect_socket(dest_ipv4, packet):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    connect_time = time.time()
    my_socket.sendto(packet,(dest_ipv4,80))
    # 
    return connect_time, my_socket
  

def ping(dest):
    ping_data = Ping_Data()
    count = 5  #cinco requisições de ping
    
    # Coverte o nome para endereço ipv4 (retorna uma string no formato ipv4)
    try:
        dest_ipv4 = socket.gethostbyname(dest)
        print("Ping ", dest, " [", dest_ipv4,"]")
    except Exception as e:
        print("Invalid Adrress ", dest)
        print(e)
        return

    #var do cabeçalho
    header_type = 8 #echo request ICMP 
    header_code = 0 #code
    header_checksum = 0
    header_identifier = 0 
    header_sequence_number = 1
    header_payload = b'trabalhoDeRedes2021'
    
    for i in range(count):
        header_sequence_number = i + header_sequence_number
        packet = convert_header(header_type, header_code, header_checksum, header_identifier, header_sequence_number, header_payload)
        #conectar com o socket
        connect_time, my_socket = connect_socket(dest_ipv4, packet)
        ping_time = reply(connect_time, my_socket, header_sequence_number)
        ping_data.print_ping(ping_time, dest_ipv4)
        time.sleep(0.5)
    
    ping_data.statistics_ping(dest_ipv4)

if __name__=="__main__":
    print("Digite o endereco")
    ping(input())
