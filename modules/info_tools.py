#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Information Tools Module
Created by s3cret_proj3ct
"""

import os
import sys
import time
import socket
import json
import subprocess
import requests
from datetime import datetime
from colorama import Fore, Style

from utils.ascii_art import get_ascii
from utils.network import get_local_ip, get_public_ip, get_wifi_info
from utils.formatters import print_section, print_success, print_error, print_info

# ============================================================
=== WIFI INFO
--============================================================
def wifi_info():
    """Get current WiFi connection info"""
    os.system('clear')
    print(get_ascii('info'))
    print_section("WIFI CONNECTION INFO")
    
    info = get_wifi_info()
    
    if info:
        ssid = info.get('ssid')
        if ssid:
            print_success(f"SSID: {ssid}\n")
            print(f"   BSSID      : {info.get('bssid', 'N/A')}")
            print(f"   IP Address : {info.get('ip', 'N/A')}")
            print(f"   Speed      : {info.get('link_speed', 'N/A')} Mbps")
            print(f"   Frequency  : {info.get('frequency', 'N/A')} MHz")
            print(f"   RSSI       : {info.get('rssi', 'N/A')} dBm")
        else:
            print_error("Not connected to WiFi")
    else:
        print_error("Could not get connection info")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

# ============================================================
=== IP INFO
--============================================================
def ip_info():
    """Get IP information"""
    os.system('clear')
    print(get_ascii('info'))
    print_section("IP INFORMATION")
    
    local_ip = get_local_ip()
    public_ip = get_public_ip()
    
    print_info("Local Network:")
    print(f"   Local IP : {local_ip}")
    
    try:
        hostname = socket.gethostname()
        print(f"   Hostname : {hostname}")
    except:
        pass
    
    print(f"\n{Fore.CYAN}Internet:{Style.RESET_ALL}")
    print(f"   Public IP: {public_ip}")
    
    # Get geolocation for public IP
    if public_ip != "Unknown":
        try:
            response = requests.get(f'http://ip-api.com/json/{public_ip}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    print(f"\n{Fore.CYAN}Geolocation:{Style.RESET_ALL}")
                    print(f"   Country : {data.get('country', 'N/A')}")
                    print(f"   Region  : {data.get('regionName', 'N/A')}")
                    print(f"   City    : {data.get('city', 'N/A')}")
                    print(f"   ISP     : {data.get('isp', 'N/A')}")
        except:
            pass
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

# ============================================================
=== BATTERY INFO
--============================================================
def battery_info():
    """Get battery information"""
    os.system('clear')
    print(get_ascii('info'))
    print_section("BATTERY INFORMATION")
    
    try:
        result = subprocess.run(['termux-battery-status'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            
            percentage = data.get('percentage', 0)
            status = data.get('status', 'UNKNOWN')
            health = data.get('health', 'UNKNOWN')
            temp = data.get('temperature', 0) / 10
            
            print_success(f"Battery: {percentage}%\n")
            
            # Status
            if status == 'CHARGING':
                print(f"   Power     : 🔌 CHARGING")
            elif status == 'DISCHARGING':
                print(f"   Power     : 🔋 DISCHARGING")
            elif status == 'FULL':
                print(f"   Power     : ✅ FULL")
            else:
                print(f"   Power     : {status}")
            
            print(f"   Health    : {health}")
            print(f"   Temp      : {temp:.1f}°C")
            
            # Battery bar
            bar_len = 30
            filled = int(bar_len * percentage / 100)
            bar = '█' * filled + '░' * (bar_len - filled)
            print(f"\n   [{bar}] {percentage}%")
            
        else:
            print_error("Could not get battery info")
    except:
        print_error("Battery info not available")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
