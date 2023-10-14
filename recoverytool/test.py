# #!/usr/bin/env python
# from scapy.all import sniff, DNS, DNSQR, DNSRR
#
# def dns_sniffer(pkt):
#     if pkt.haslayer(DNS):
#         dns_layer = pkt.getlayer(DNS)
#
#         if dns_layer.qr == 0:  # DNS query
#             print("DNS Query:")
#             for q in dns_layer.qd:
#                 print(f"    Query: {q.qname.decode('utf-8')}")
#
#         elif dns_layer.qr == 1:  # DNS response
#             print("DNS Response:")
#             for r in dns_layer.an:
#                 if isinstance(r, DNSRR):
#                     print(f"    Answer: {r.rrname.decode('utf-8')} -> {r.rdata.decode('utf-8')}")
#
# # Specify the interface to capture packets from (replace 'eth0' with your interface)
# interface = 'eth0'
#
# # Specify the filter for capturing DNS packets
# dns_filter = 'udp and port 53'
#
# # Start sniffing packets
# print(f"Sniffing DNS traffic on interface {interface}...")
# sniff(iface=interface, filter=dns_filter, prn=dns_sniffer)
