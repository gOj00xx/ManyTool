#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Device Scanner Module - OPTIMIZED (CEPAT)
Created by s3cret_proj3ct
"""

import os
import sys
import time
import threading
from colorama import Fore, Style

from utils.ascii_art import get_ascii
from utils.network import get_local_ip, scan_devices_fast, scan_devices_full
from utils.formatters import print_section, print_success, print_error, print_info

# ============================================================
# GLOBAL VARIABLES
# ============================================================
SCAN_ACTIVE = False
SCAN_THREAD = None

def scan_once():
    """Scan for devices on network - MODE CEPAT (20 IP)"""
    os.system('clear')
    print(get_ascii('wifi'))
    print_section("DEVICE SCAN - FAST MODE")
    
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        print_error("❌ Tidak terhubung ke jaringan!")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return
    
    network = '.'.join(local_ip.split('.')[:3]) + '.'
    print_info(f"📱 IP Lokal : {local_ip}")
    print_info(f"🌐 Network  : {network}0/24")
    print_info(f"⚡ Mode      : Fast (20 IP pertama)")
    print()
    
    start_time = time.time()
    devices = scan_devices_fast()
    elapsed = time.time() - start_time
    
    if devices:
        print(f"\n{Fore.GREEN}✅ Ditemukan {len(devices)} perangkat dalam {elapsed:.1f} detik:{Style.RESET_ALL}\n")
        for i, ip in enumerate(devices, 1):
            print(f"   {i:2d}. 📱 {ip}")
    else:
        print_error(f"❌ Tidak ada perangkat lain ditemukan (dalam {elapsed:.1f} detik)")
        print_info("Mungkin hanya device ini yang online")
    
    print(f"\n{Fore.CYAN}⏱️  Waktu scan: {elapsed:.1f} detik{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def scan_full():
    """Scan for devices on network - MODE LENGKAP (254 IP)"""
    os.system('clear')
    print(get_ascii('wifi'))
    print_section("DEVICE SCAN - FULL MODE")
    
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        print_error("❌ Tidak terhubung ke jaringan!")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return
    
    network = '.'.join(local_ip.split('.')[:3]) + '.'
    print_info(f"📱 IP Lokal : {local_ip}")
    print_info(f"🌐 Network  : {network}0/24")
    print_info(f"⚡ Mode      : Full (254 IP - butuh waktu ~2 menit)")
    print()
    
    confirm = input(f"{Fore.YELLOW}Lanjutkan? (y/n): {Style.RESET_ALL}").lower()
    if confirm != 'y':
        return
    
    start_time = time.time()
    devices = scan_devices_full()
    elapsed = time.time() - start_time
    
    if devices:
        print(f"\n{Fore.GREEN}✅ Ditemukan {len(devices)} perangkat dalam {elapsed:.1f} detik:{Style.RESET_ALL}\n")
        for i, ip in enumerate(devices, 1):
            print(f"   {i:2d}. 📱 {ip}")
    else:
        print_error(f"❌ Tidak ada perangkat lain ditemukan (dalam {elapsed:.1f} detik)")
    
    print(f"\n{Fore.CYAN}⏱️  Total waktu: {elapsed:.1f} detik{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def scan_loop_function():
    """Thread for continuous scanning (fast mode)"""
    global SCAN_ACTIVE
    
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        return
    
    network = '.'.join(local_ip.split('.')[:3]) + '.'
    scan_count = 0
    
    while SCAN_ACTIVE:
        scan_count += 1
        os.system('clear')
        print(get_ascii('wifi'))
        print_section(f"DEVICE SCAN - LOOP #{scan_count}")
        print_info("Tekan [9] lagi untuk STOP\n")
        print_info(f"Network: {network}0/24 (fast mode - 20 IP)")
        
        devices = []
        start_time = time.time()
        
        # Fast scan (20 IP)
        for i in range(1, 21):
            if not SCAN_ACTIVE:
                break
            ip = f"{network}{i}"
            if ip == local_ip:
                continue
            result = os.system(f'ping -c 1 -W 1 {ip} > /dev/null 2>&1')
            if result == 0:
                devices.append(ip)
        
        elapsed = time.time() - start_time
        
        if devices:
            print(f"\n{Fore.GREEN}✅ Online ({len(devices)}):{Style.RESET_ALL}")
            for ip in devices[:5]:  # Tampilkan 5 pertama
                print(f"   📱 {ip}")
            if len(devices) > 5:
                print(f"   ... dan {len(devices)-5} lainnya")
        else:
            print(f"\n{Fore.YELLOW}❌ Tidak ada perangkat lain{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}⏱️  Scan time: {elapsed:.1f}s | Next in 10s{Style.RESET_ALL}")
        
        # Countdown 10 detik
        for i in range(10, 0, -1):
            if not SCAN_ACTIVE:
                break
            sys.stdout.write(f"\r   🔄 Refresh in {i:2d} seconds...   ")
            sys.stdout.flush()
            time.sleep(1)

def scan_loop():
    """Start/stop continuous scanning"""
    global SCAN_ACTIVE, SCAN_THREAD
    
    if SCAN_ACTIVE:
        SCAN_ACTIVE = False
        if SCAN_THREAD:
            SCAN_THREAD.join(timeout=2)
        print_info("\n📱 Device scan loop STOPPED")
        time.sleep(1)
    else:
        # Cek koneksi dulu
        local_ip = get_local_ip()
        if local_ip == "127.0.0.1":
            print_error("❌ Tidak terhubung ke jaringan!")
            time.sleep(2)
            return
        
        SCAN_ACTIVE = True
        SCAN_THREAD = threading.Thread(target=scan_loop_function)
        SCAN_THREAD.daemon = True
        SCAN_THREAD.start()
        print_info("📱 Device scan loop STARTED (refresh setiap 10 detik)")
        time.sleep(1)
