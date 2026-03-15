#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Device Scanner Module
Created by s3cret_proj3ct
"""

import os
import sys
import time
import socket
import threading
import subprocess
from colorama import Fore, Style

from utils.ascii_art import get_ascii
from utils.network import get_local_ip, scan_devices
from utils.formatters import print_section, print_success, print_error, print_info

# ============================================================
# GLOBAL VARIABLES
# ============================================================
SCAN_ACTIVE = False
SCAN_THREAD = None

def scan_once():
    """Scan for devices on network once"""
    os.system('clear')
    print(get_ascii('wifi'))
    print_section("DEVICE SCAN - ONCE")
    
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        print_error("Not connected to network!")
        input("\nPress Enter to continue...")
        return
    
    network = '.'.join(local_ip.split('.')[:3]) + '.'
    print_info(f"Local IP: {local_ip}")
    print_info(f"Network: {network}0/24")
    print_info("Scanning...\n")
    
    devices = scan_devices()
    
    if devices:
        print_success(f"Found {len(devices)} devices:\n")
        for i, ip in enumerate(devices, 1):
            print(f"   {i:2d}. 📱 {ip}")
    else:
        print_error("No devices found")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def scan_loop_function():
    """Thread for continuous scanning"""
    global SCAN_ACTIVE
    
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        return
    
    network = '.'.join(local_ip.split('.')[:3]) + '.'
    
    while SCAN_ACTIVE:
        os.system('clear')
        print(get_ascii('wifi'))
        print_section("DEVICE SCAN - LOOP")
        print_info("Press [9] again to stop\n")
        print_info(f"Network: {network}0/24\n")
        
        devices = []
        for i in range(1, 255):
            if not SCAN_ACTIVE:
                break
            ip = f"{network}{i}"
            if ip == local_ip:
                continue
            
            result = os.system(f'ping -c 1 -W 1 {ip} > /dev/null 2>&1')
            if result == 0:
                devices.append(ip)
                print(f"   📱 {ip}")
        
        if not devices:
            print_error("No devices found")
        
        print(f"\n{Fore.CYAN}Next scan in 10 seconds...{Style.RESET_ALL}")
        
        for i in range(10):
            if not SCAN_ACTIVE:
                break
            time.sleep(1)

def scan_loop():
    """Start/stop continuous scanning"""
    global SCAN_ACTIVE, SCAN_THREAD
    
    if SCAN_ACTIVE:
        SCAN_ACTIVE = False
        if SCAN_THREAD:
            SCAN_THREAD.join(timeout=2)
        print_info("Scan loop stopped")
        time.sleep(1)
    else:
        SCAN_ACTIVE = True
        SCAN_THREAD = threading.Thread(target=scan_loop_function)
        SCAN_THREAD.daemon = True
        SCAN_THREAD.start()
        print_info("Scan loop started (refreshes every 10s)")
