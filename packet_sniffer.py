from scapy.all import sniff, IP

# Callback function to process each packet
def packet_callback(packet):
    if packet.haslayer(IP):
        ip_layer = packet[IP]
        print(f"[+] Packet: {ip_layer.src} → {ip_layer.dst} | Protocol: {ip_layer.proto}")

# Choose your filter: "tcp", "udp", or "port 80"
packet_filter = ["tcp","udp","port 80"]  # Change to "udp" or "port 80" as needed
for i in packet_filter:


      # Start sniffing (you may need sudo privileges)
      print(f"Starting packet capture with filter: {packet_filter}... Press Ctrl+C to stop.")
      sniff(filter= i, prn=packet_callback, store=False)

