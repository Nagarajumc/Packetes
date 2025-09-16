# Save as dashboard_packets.py

import threading
import time
from collections import Counter, deque

from scapy.all import sniff, IP, TCP, UDP, ICMP
import streamlit as st
import pandas as pd
import plotly.express as px

# Shared state
packet_buffer = deque(maxlen=2000)  # store recent packet infos
protocol_counts = Counter()
total_packets = 0
lock = threading.Lock()
capturing = False

def packet_handler(pkt):
    global total_packets
    with lock:
        total_packets += 1

        # Detect protocol
        if IP in pkt:
            if TCP in pkt:
                proto = "TCP"
            elif UDP in pkt:
                proto = "UDP"
            elif ICMP in pkt:
                proto = "ICMP"
            else:
                proto = f"IP‑Other (proto={pkt[IP].proto})"
        else:
            proto = "Non‑IP"

        protocol_counts[proto] += 1

        # record minimal info
        info = {
            "time": time.time(),
            "src": pkt[IP].src if IP in pkt else None,
            "dst": pkt[IP].dst if IP in pkt else None,
            "protocol": proto,
            "size": len(pkt)
        }
        packet_buffer.append(info)

def start_sniff(iface):
    # Scapy sniff will block, so run in thread
    sniff(iface=iface, prn=packet_handler, store=False)

def run_dashboard():
    st.title("Network Packets & Protocol Dashboard")

    iface = st.sidebar.text_input("Interface to sniff on", value="eth0")
    start_button = st.sidebar.button("Start Capture")
    stop_button = st.sidebar.button("Stop Capture")

    global capturing
    sniffer_thread = None

    if start_button and not capturing:
        capturing = True
        sniffer_thread = threading.Thread(target=start_sniff, args=(iface,), daemon=True)
        sniffer_thread.start()

    if stop_button and capturing:
        capturing = False
        # Once stop, we can’t easily stop sniff from Scapy unless we have stop_filter etc.
        # This example is simple; for full stop you can use a custom approach.

    # Dashboard content
    while True:
        time.sleep(1)  # refresh interval

        with lock:
            tp = total_packets
            pc = protocol_counts.copy()
            buf = list(packet_buffer)

        st.metric("Total Packets", tp)

        # Protocol Distribution
        protos = list(pc.keys())
        counts = [pc[p] for p in protos]
        df_proto = pd.DataFrame({"protocol": protos, "count": counts})
        fig1 = px.pie(df_proto, names="protocol", values="count", title="Protocol Breakdown")
        st.plotly_chart(fig1, use_container_width=True)

        # Packets per second in recent window (last 10 secs)
        if buf:
            now = time.time()
            recent = [p for p in buf if now - p["time"] <= 10]
            rate = len(recent) / 10.0
            st.metric("Packets per second (last 10s)", f"{rate:.2f}")

        # Recent packets table
        if buf:
            df_buf = pd.DataFrame(buf[-10:])  # last 10 packets
            # Format time
            df_buf["ts"] = df_buf["time"].apply(lambda t: time.strftime("%H:%M:%S", time.localtime(t)))
            st.table(df_buf[["ts", "src", "dst", "protocol", "size"]])

        # Break loop if capturing stopped
        if not capturing:
            break

        # Force rerun / refresh
        st.experimental_rerun()


if __name__ == "__main__":
    run_dashboard()

