#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
WiFi Scanner Module - FIXED ATTRIBUTE ERROR
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

def scan_once():
    """Scan WiFi networks once - DENGAN LOCATION CHECK REAL"""
    os.system('clear')
    print(get_ascii('wifi'))
    print_section("WiFi SCAN - ONCE")
    
    # Cek location beneran
    if not ensure_location():
        print_error("\n⚠️  Location harus ON untuk scan WiFi!")
        print_info("Coba aktifkan location dulu ya")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return
    
    print_info("Scanning WiFi... (mohon tunggu 3 detik)")
    
    # Scan dengan timeout
    networks = scan_wifi_once()
    
    # CEK TIPE DATA - FIX UTAMA!
    if networks is None:
        print_error("❌ Tidak ada jaringan ditemukan (scan gagal)")
    elif isinstance(networks, dict):
        # Kalo networks berupa dict (error), tampilkan pesan
        print_error("❌ Error scanning WiFi:")
        for key, value in networks.items():
            print(f"   {key}: {value}")
    elif isinstance(networks, list) and len(networks) > 0:
        print_success(f"✅ Ditemukan {len(networks)} jaringan!\n")
        
        # Sort by signal strength (hanya kalo list)
        networks.sort(key=lambda x: x.get('level', 0), reverse=True)
        
        for i, net in enumerate(networks[:15], 1):
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
        print_error("❌ Tidak ada jaringan ditemukan!")
        print_info("Pastikan:")
        print_info("• WiFi dalam keadaan ON")
        print_info("• Location sudah aktif")
        print_info("• Ada jaringan di sekitar")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def scan_loop_function():
    """Thread for continuous scanning"""
    global SCAN_ACTIVE
    
    # Cek location sekali di awal
    if not ensure_location():
        print_error("Location tidak aktif, scan loop tidak bisa jalan")
        SCAN_ACTIVE = False
        return
    
    scan_count = 0
    
    while SCAN_ACTIVE:
        scan_count += 1
        os.system('clear')
        print(get_ascii('wifi'))
        print_section(f"WiFi SCAN - LOOP (Scan #{scan_count})")
        print_info("Tekan [8] lagi untuk STOP\n")
        
        # Scan dengan timeout cepat
        networks = scan_wifi_once()
        
        if networks is None:
            print_error("❌ Scan gagal")
        elif isinstance(networks, dict):
            print_error("❌ Error scanning WiFi")
        elif isinstance(networks, list) and len(networks) > 0:
            networks.sort(key=lambda x: x.get('level', 0), reverse=True)
            print_success(f"✅ Ditemukan {len(networks)} jaringan:\n")
            
            for i, net in enumerate(networks[:8], 1):
                ssid = net.get('ssid', 'Hidden')
                level = net.get('level', 0)
                signal = signal_strength_bar(level)
                print(f"   {signal} {level:4d} dBm | {ssid[:30]}")
        else:
            print_error("❌ Tidak ada jaringan ditemukan")
        
        print(f"\n{Fore.CYAN}⏱️  {time.strftime('%H:%M:%S')} - Next scan in 5 seconds...{Style.RESET_ALL}")
        
        # Countdown 5 detik (bisa diinterupsi)
        for i in range(5, 0, -1):
            if not SCAN_ACTIVE:
                break
            sys.stdout.write(f"\r   🔄 Refresh in {i} seconds...   ")
            sys.stdout.flush()
            time.sleep(1)

def scan_loop():
    """Start/stop continuous scanning"""
    global SCAN_ACTIVE, SCAN_THREAD
    
    if SCAN_ACTIVE:
        SCAN_ACTIVE = False
        if SCAN_THREAD:
            SCAN_THREAD.join(timeout=2)
        print_info("\n📡 WiFi scan loop STOPPED")
        time.sleep(1)
    else:
        # Cek location dulu
        if not ensure_location():
            print_error("⚠️  Location tidak aktif!")
            time.sleep(2)
            return
        
        SCAN_ACTIVE = True
        SCAN_THREAD = threading.Thread(target=scan_loop_function)
        SCAN_THREAD.daemon = True
        SCAN_THREAD.start()
        print_info("📡 WiFi scan loop STARTED (refresh setiap 5 detik)")
        time.sleep(1)

def connection_info():
    """Get current WiFi connection info"""
    os.system('clear')
    print(get_ascii('wifi'))
    print_section("WiFi CONNECTION INFO")
    
    info = get_wifi_info()
    
    if info and isinstance(info, dict):
        ssid = info.get('ssid')
        if ssid:
            print_success(f"✅ Terkoneksi ke: {ssid}\n")
            
            print(f"   📶 SSID      : {ssid}")
            print(f"   🔵 BSSID     : {info.get('bssid', 'N/A')}")
            print(f"   🌐 IP        : {info.get('ip', 'N/A')}")
            print(f"   ⚡ Speed     : {info.get('link_speed', 'N/A')} Mbps")
            print(f"   📻 Frequency : {info.get('frequency', 'N/A')} MHz")
            
            rssi = info.get('rssi', 0)
            if rssi:
                signal = signal_strength_bar(rssi)
                print(f"   📶 Signal    : {signal} {rssi} dBm")
        else:
            print_error("❌ Tidak terhubung ke WiFi")
    else:
        print_error("❌ Gagal mendapatkan info koneksi")
        print_info("Pastikan WiFi menyala dan terhubung")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
