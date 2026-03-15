#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Network Utilities - FIXED LOCATION DETECTION
Created by s3cret_proj3ct
"""

import os
import socket
import subprocess
import json
import requests
import time

def check_termux_api():
    """Check if Termux API is available"""
    result = os.system('command -v termux-torch > /dev/null 2>&1')
    return result == 0

def check_location_real():
    """Cek location dengan metode yang lebih akurat"""
    
    # Metode 1: Coba dapatkan lokasi (paling akurat)
    result1 = os.system('termux-location -p once -r network > /dev/null 2>&1 & sleep 2 && killall termux-location 2>/dev/null')
    
    # Metode 2: Cek permission
    result2 = os.system('dumpsys package com.termux | grep -A 5 "android.permission.ACCESS_FINE_LOCATION" | grep -q "granted=true" 2>/dev/null')
    
    # Metode 3: Cek apakah bisa scan WiFi
    result3 = os.system('termux-wifi-scaninfo > /dev/null 2>&1')
    
    # Gabungkan hasil
    if result1 == 0:
        return True, "GPS aktif dan merespon"
    elif result2 == 0:
        return True, "Permission location diberikan"
    elif result3 == 0:
        return True, "WiFi scan berjalan (location mungkin aktif)"
    else:
        return False, "Location TIDAK aktif"

def ensure_location():
    """Pastikan location aktif dengan pesan detail"""
    print("\n📍 CEK LOKASI:")
    print("-" * 30)
    
    # Cek dengan metode real
    is_active, message = check_location_real()
    
    if is_active:
        print(f"✅ {message}")
        return True
    else:
        print(f"❌ {message}")
        print("\n📱 CARA AKTIFKAN LOKASI:")
        print("   1. Settings → Location → ON")
        print("   2. Settings → Apps → Termux → Permissions")
        print("   3. Izinkan 'Location' (Allow all the time)")
        print("   4. Set mode ke 'High Accuracy'")
        return False

def get_local_ip():
    """Get local IP address (cepat)"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_public_ip():
    """Get public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=3)
        if response.status_code == 200:
            return response.json().get('ip', 'Unknown')
    except:
        pass
    return "Unknown"

def scan_wifi_once():
    """Scan WiFi networks once - OPTIMIZED"""
    # Aktifkan location sebentar
    os.system('termux-location -p once -r network > /dev/null 2>&1 &')
    time.sleep(1)  # Tunggu sebentar
    
    result = subprocess.run(['termux-wifi-scaninfo'], capture_output=True, text=True, timeout=3)
    if result.returncode == 0 and result.stdout:
        try:
            return json.loads(result.stdout)
        except:
            return None
    return None

def get_wifi_info():
    """Get current WiFi connection info - CEPAT"""
    result = subprocess.run(['termux-wifi-connectioninfo'], capture_output=True, text=True, timeout=2)
    if result.returncode == 0 and result.stdout:
        try:
            return json.loads(result.stdout)
        except:
            return None
    return None

def scan_devices_fast():
    """Scan for devices on local network - CEPAT (hanya 20 IP pertama)"""
    devices = []
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        return devices
    
    network = '.'.join(local_ip.split('.')[:3]) + '.'
    
    print(f"📡 Scanning network {network}0/24 (fast mode)...")
    
    # Scan hanya 20 IP pertama biar cepat
    for i in range(1, 21):
        ip = f"{network}{i}"
        if ip == local_ip:
            continue
        result = os.system(f'ping -c 1 -W 1 {ip} > /dev/null 2>&1')
        if result == 0:
            devices.append(ip)
            print(f"   ✓ {ip}")
    
    return devices

def scan_devices_full():
    """Scan for devices on local network - LENGKAP (semua 254 IP)"""
    devices = []
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        return devices
    
    network = '.'.join(local_ip.split('.')[:3]) + '.'
    
    print(f"📡 Scanning network {network}0/24 (full mode)...")
    print("   Ini akan memakan waktu ~2 menit\n")
    
    for i in range(1, 255):
        ip = f"{network}{i}"
        if ip == local_ip:
            continue
        result = os.system(f'ping -c 1 -W 1 {ip} > /dev/null 2>&1')
        if result == 0:
            devices.append(ip)
            print(f"   ✓ {ip}")
    
    return devices
