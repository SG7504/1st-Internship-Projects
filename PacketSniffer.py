import socket
import struct
import binascii

def decode_ethernet(data):
    dest_mac, src_mac, protocol = struct.unpack("!6s6sH", data[:14])
    return (binascii.hexlify(dest_mac), binascii.hexlify(src_mac), socket.htons(protocol))

def decode_ip(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 0xF) * 4
    ttl, proto, src, dst = struct.unpack("!8xBB2x4s4s", data[:20])
    return (version, header_length, ttl, proto, socket.inet_ntoa(src), socket.inet_ntoa(dst))

def decode_tcp(data):
    (src_port, dst_port, sequence, acknowledgement, offset_reserved_flags) = struct.unpack("!HHLLH", data[:14])
    offset = (offset_reserved_flags >> 12) * 4
    flag_urg = (offset_reserved_flags & 32) >> 5
    flag_ack = (offset_reserved_flags & 16) >> 4
    flag_psh = (offset_reserved_flags & 8) >> 3
    flag_rst = (offset_reserved_flags & 4) >> 2
    flag_syn = (offset_reserved_flags & 2) >> 1
    flag_fin = offset_reserved_flags & 1
    return (src_port, dst_port, sequence, acknowledgement, offset, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin)

def decode_udp(data):
    src_port, dst_port, size = struct.unpack("!HH2x", data[:6])
    return (src_port, dst_port, size)

def main():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    while True:
        
        packet = s.recvfrom(65565)
        packet = packet[0]

        
        eth_length = 14
        eth_header = packet[:eth_length]
        eth_protocol, eth_src, eth_dst = decode_ethernet(eth_header)

        
        ip_length = 20
        ip_header = packet[eth_length:eth_length+ip_length]
        version, header_length, ttl, proto, src_ip, dst_ip = decode_ip(ip_header)

        
        transport_header = packet[eth_length+header_length:]
        if proto == 6:  
            src_port, dst_port, sequence, acknowledgement, offset, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin = decode_tcp(transport_header)
            print(f"Source IP: {src_ip}, Destination IP: {dst_ip}, Protocol: TCP, Source Port: {src_port}, Destination Port: {dst_port}")
        elif proto == 17:  
            src_port, dst_port, size = decode_udp(transport_header)
            print(f"Source IP: {src_ip}, Destination IP: {dst_ip}, Protocol: UDP, Source Port: {src_port}, Destination Port: {dst_port}")
        else:
            print(f"Source IP: {src_ip}, Destination IP: {dst_ip}, Protocol: {proto}")

        
        payload = packet[eth_length+header_length+len(transport_header):]
        if payload:
            print(f"Payload: {payload.decode('utf-8', errors='replace')}")

        print("---")

if __name__ == "__main__":
    main()