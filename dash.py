from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from scapy.all import sniff, IP, TCP, UDP, ICMP
import threading
import time
from collections import Counter, deque

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# State
total_packets = 0
protocol_counts = Counter()
recent_packets = deque(maxlen=1000)  # store metadata

state_lock = threading.Lock()

def packet_handler(pkt):
    global total_packets, protocol_counts
    with state_lock:
        total_packets += 1

        # Determine protocol
        if IP in pkt:
            if TCP in pkt:
                proto = 'TCP'
            elif UDP in pkt:
                proto = 'UDP'
            elif ICMP in pkt:
                proto = 'ICMP'
            else:
                proto = f'IP_OTHER({pkt[IP].proto})'
        else:
            proto = 'NON_IP'

        protocol_counts[proto] += 1

        # Store minimal packet info
        info = {
            'timestamp': time.time(),
            'src': pkt[IP].src if IP in pkt else None,
            'dst': pkt[IP].dst if IP in pkt else None,
            'protocol': proto,
            'size': len(pkt)
        }
        recent_packets.append(info)

def start_sniff(interface):
    sniff(iface=interface, prn=packet_handler, store=False)

def stats_broadcaster():
    """
    In a loop, every interval send stats to connected clients via socketio
    """
    while True:
        time.sleep(1)  # broadcast interval (1 sec)
        with state_lock:
            tp = total_packets
            pc = dict(protocol_counts)
            # compute rate in last N seconds
            now = time.time()
            # how many packets in last 10 seconds:
            recent = [p for p in recent_packets if now - p['timestamp'] <= 10]
            rate = len(recent) / 10.0
            # top source IPs (last N packets)
            srcs = Counter(p['src'] for p in recent if p['src'] is not None)
            top_src = srcs.most_common(5)

        socketio.emit('stats', {
            'total_packets': tp,
            'protocol_counts': pc,
            'packets_per_sec': rate,
            'top_src_ips': top_src,
            'recent': list(recent_packets)[-10:]  # last 10
        })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Choose the interface you want to sniff on
    interface = 'eth0'  # change as needed

    sniff_thread = threading.Thread(target=start_sniff, args=(interface,), daemon=True)
    sniff_thread.start()

    broadcaster = threading.Thread(target=stats_broadcaster, daemon=True)
    broadcaster.start()

    socketio.run(app, host='0.0.0.0', port=5000)

