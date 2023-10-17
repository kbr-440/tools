from scapy.all import sniff, TCP


def print_ports(pkt):
    if pkt.haslayer(TCP):
        src_port = pkt[TCP].sport
        dst_port = pkt[TCP].dport
        print(f"Source Port: {src_port}, Destination Port: {dst_port}")


interface = 'eth0'  # The interface to capture packets from

https_filter = 'tcp and port 443'  # Filter for capturing four HTTPS packets (TCP packets with destination port 443)
print(f"Sniffing four HTTPS packets on interface {interface}...")
sniff(iface=interface, filter=https_filter, prn=print_ports, count=4)
