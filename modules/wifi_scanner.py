#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
WiFi Scanner Module
Created by s3cret_proj3ct
"""

import os
import sys
import time
import json
import threading
from colorama import Fore, Style

from utils.ascii_art import get_ascii
from utils.network import scan_wifi_once, get_wifi_info, ensure_location
from utils.formatters import print_section, print_success, print_error, print_info, signal_strength_bar

# ============================================================
# GLOBAL VARIABLES
# ============================================================
SCAN_ACTIVE = False
SCAN_THREAD = None

# ============================================================
=== SCAN ONCE
--============================================================
def scan_once():
    """Scan WiFi networks once"""
    os.system('clear')
    print(get_ascii('wifi'))
    print_section("WiFi SCAN - ONCE")
    
    if not ensure_location():
        print_error("Location must be enabled!")
        input("\nPress Enter to continue...")
        return
    
    print_info("Scanning...")
    networks = scan_wifi_once()
    
    if networks:
        print_success(f"Found {len(networks)} networks:\n")
        
        # Sort by signal strength
        networks.sort(key=lambda x: x.get('level', 0), reverse=True)
        
        for i, net in enumerate(networks[:20], 1):
            ssid = net.get('ssid', 'Hidden Network')
            bssid = net.get('bssid', 'N/A')
            level = net.get('level', 0)
            freq = net.get('frequency', 0)
            
            # Channel
            if 2412 <= freq <= 2484:
                channel = f"2.4G Ch{(freq-2412)//5+1}"
            elif 5170 <= freq <= 5825:
                channel = f"5G Ch{(freq-5170)//5+34}"
            else:
                channel = "Unknown"
            
            signal = signal_strength_bar(level)
            print(f"{i:2d}. {signal} {level:4d} dBm | {channel:12} | {ssid}")
            
            if i <= 5:
                print(f"     BSSID: {bssid}")
    else:
        print_error("No networks found!")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

# ============================================================
=== SCAN LOOP
--============================================================
def scan_loop_function():
    """Thread for continuous scanning"""
    global SCAN_ACTIVE
    
    while SCAN_ACTIVE:
        os.system('clear')
        print(get_ascii('wifi'))
        print_section("WiFi SCAN - LOOP")
        print_info("Press [8] again to stop\n")
        
        networks = scan_wifi_once()
        
        if networks:
            networks.sort(key=lambda x: x.get('level', 0), reverse=True)
            print_success(f"Found {len(networks)} networks:\n")
            
            for net in networks[:10]:
                ssid = net.get('ssid', 'Hidden')
                level = net.get('level', 0)
                signal = signal_strength_bar(level)
                print(f"   {signal} {level:4d} dBm | {ssid[:30]}")
        else:
            print_error("No networks found")
        
        print(f"\n{Fore.CYAN}Next scan in 5 seconds...{Style.RESET_ALL}")
        
        for i in range(5):
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
        if not ensure_location():
            print_error("Location must be enabled!")
            time.sleep(2)
            return
        SCAN_ACTIVE = True
        SCAN_THREAD = threading.Thread(target=scan_loop_function)
        SCAN_THREAD.daemon = True
        SCAN_THREAD.start()
        print_info("Scan loop started (refreshes every 5s)")

# ============================================================
=== GET CONNECTION INFO
--============================================================
def connection_info():
    """Get current WiFi connection info"""
    os.system('clear')
    print(get_ascii('wifi'))
    print_section("WiFi CONNECTION INFO")
    
    info = get_wifi_info()
    
    if info:
        ssid = info.get('ssid')
        if not ssid:
            print_error("Not connected to WiFi")
        else:
            print_success(f"Connected to: {ssid}\n")
            
            print(f"   BSSID      : {info.get('bssid', 'N/A')}")
            print(f"   IP Address : {info.get('ip', 'N/A')}")
            print(f"   Speed      : {info.get('link_speed', 'N/A')} Mbps")
            
            rssi = info.get('rssi', 0)
            if rssi:
                signal = signal_strength_bar(rssi)
                print(f"   Signal     : {signal} {rssi} dBm")
    else:
        print_error("Could not get connection info")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
