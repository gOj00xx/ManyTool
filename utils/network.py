#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Network Utilities
Created by s3cret_proj3ct
"""

import os
import socket
import subprocess
import json
import requests

def check_termux_api():
    """Check if Termux API is available"""
    result = os.system('command -v termux-torch > /dev/null 2>&1')
    return result == 0

def check_location():
    """Check if location is enabled"""
    result = os.system('termux-location -p once -r network > /dev/null 2>&1 & sleep 1 && killall termux-location 2>/dev/null')
    return result == 0

def ensure_location():
    """Ensure location is enabled for WiFi scanning"""
    if not check_location():
        return False
    return True

def get_local_ip():
    """Get local IP address"""
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
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        if response.status_code == 200:
            return response.json().get('ip', 'Unknown')
    except:
        pass
    return "Unknown"

def scan_wifi_once():
    """Scan WiFi networks once"""
    result = subprocess.run(['termux-wifi-scaninfo'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0 and result.stdout:
        try:
            return json.loads(result.stdout)
        except:
            return None
    return None

def get_wifi_info():
    """Get current WiFi connection info"""
    result = subprocess.run(['termux-wifi-connectioninfo'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0 and result.stdout:
        try:
            return json.loads(result.stdout)
        except:
            return None
    return None

def scan_devices():
    """Scan for devices on local network"""
    devices = []
    local_ip = get_local_ip()
    if local_ip == "127.0.0.1":
        return devices
    
    network = '.'.join(local_ip.split('.')[:3]) + '.'
    
    for i in range(1, 255):
        ip = f"{network}{i}"
        if ip == local_ip:
            continue
        result = os.system(f'ping -c 1 -W 1 {ip} > /dev/null 2>&1')
        if result == 0:
            devices.append(ip)
    
    return devices
