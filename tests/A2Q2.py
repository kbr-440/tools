from scapy.all import sniff, TCP

# Define a function to print source and destination port numbers
def print_ports(pkt):
    if pkt.haslayer(TCP):
        src_port = pkt[TCP].sport
        dst_port = pkt[TCP].dport
        print(f"Source Port: {src_port}, Destination Port: {dst_port}")

# Specify the interface to capture packets from (replace 'eth0' with your interface)
interface = 'eth0'

# Specify the filter for capturing four HTTPS packets (TCP packets with destination port 443)
https_filter = 'tcp and port 443'

# Start sniffing packets and print the source and destination port numbers
print(f"Sniffing four HTTPS packets on interface {interface}...")
sniff(iface=interface, filter=https_filter, prn=print_ports, count=4)
