import sqlite3
from scapy.all import sniff, IP

# Step 1: Set up SQLite database
conn = sqlite3.connect("packets.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS packets (
        timestamp TEXT,
        src_ip TEXT,
        dst_ip TEXT,
        protocol INTEGER
    )
""")
conn.commit()

# Step 2: Callback to log packets
def packet_callback(packet):
    if packet.haslayer(IP):
        ip_layer = packet[IP]
        cursor.execute("INSERT INTO packets VALUES (?, ?, ?, ?)", (
            packet.time,
            ip_layer.src,
            ip_layer.dst,
            ip_layer.proto
        ))
        conn.commit()
        print(f"[+] Logged: {ip_layer.src} → {ip_layer.dst} | Protocol: {ip_layer.proto}")

# Step 3: Start sniffing
print("Capturing and logging packets... Press Ctrl+C to stop.")
sniff(filter="tcp", prn=packet_callback, store=False)

