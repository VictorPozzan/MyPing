import socket
import os
import struct
import time
import select



def checksum(bytes_header):
    size = len(bytes_header) #
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

def ping(dest):
    count = 5  #cinco requisições de ping
    
    # Coverte o nome para endereço ipv4 (retorna uma string no formato ipv4)
    dest_ipv4 = socket.gethostbyname(dest)
    print("Ping ", dest, " [", dest_ipv4,"]")

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
        send_request_ping_time,rawsocket,addr = raw_socket(dest_ipv4, packet)


        print("ping ", dest)


if __name__=="__main__":
    ping("www.google.com")
