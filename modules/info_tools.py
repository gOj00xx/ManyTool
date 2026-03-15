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

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# ============================================================
=== FUNGSI WIFI_INFO (UNTUK MENU 10)
--============================================================
def wifi_info():
    """Get current WiFi connection info"""
    clear_screen()
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
=== FUNGSI IP_INFO (UNTUK MENU 11)
--============================================================
def ip_info():
    """Get IP information"""
    clear_screen()
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
=== FUNGSI BATTERY_INFO (UNTUK MENU 12)
--============================================================
def battery_info():
    """Get battery information"""
    clear_screen()
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

# ============================================================
=== FUNGSI TAMBAHAN (UNTUK KREDIT - BISA DIPANGGIL)
--============================================================
def show_credits():
    """Show credits information"""
    clear_screen()
    print(get_ascii('info'))
    print_section("CREDITS")
    
    print(f"{Fore.GREEN}")
    print("╔════════════════════════════════════════════════════╗")
    print("║                                                    ║")
    print("║              CREATED BY s3cret_proj3ct            ║")
    print("║                                                    ║")
    print("╠════════════════════════════════════════════════════╣")
    print("║                                                    ║")
    print("║  🔹 WhatsApp Spam Tool                             ║")
    print("║  🔹 DDoS Attack Suite                              ║")
    print("║  🔹 Roblox Follow Spam                             ║")
    print("║  🔹 TikTok Report Spam                             ║")
    print("║  🔹 WiFi & Device Scanner                          ║")
    print("║  🔹 Information Tools                              ║")
    print("║                                                    ║")
    print("╠════════════════════════════════════════════════════╣
    print(f"{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}⚠️  DISCLAIMER:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}This tool is for educational purposes only.{Style.RESET_ALL}")
    print(f"{Fore.WHITE}We are not responsible for any misuse.{Style.RESET_ALL}")
    print(f"{Fore.RED}Use at your own risk!{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
