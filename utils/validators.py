#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Input Validators
Created by s3cret_proj3ct
"""

import re
import ipaddress

def validate_phone(phone):
    """Validate Indonesian phone number"""
    phone = re.sub(r'\D', '', phone)
    
    if phone.startswith('0'):
        phone = phone[1:]
    
    if phone.startswith('62'):
        phone = phone[2:]
    
    if len(phone) < 10 or len(phone) > 13:
        return False, None
    
    return True, phone

def validate_url(url):
    """Validate URL"""
    url = url.strip()
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        if parsed.netloc:
            return True, url
        return False, None
    except:
        return False, None

def validate_ip(ip):
    """Validate IP address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False

def validate_port(port):
    """Validate port number"""
    try:
        port = int(port)
        if 1 <= port <= 65535:
            return True, port
        return False, None
    except:
        return False, None

def validate_count(count, min_val=1, max_val=1000):
    """Validate count number"""
    try:
        count = int(count)
        if min_val <= count <= max_val:
            return True, count
        return False, None
    except:
        return False, None

def validate_roblox_username(username):
    """Validate Roblox username"""
    if not username or len(username) < 3 or len(username) > 20:
        return False
    # Roblox usernames only allow letters, numbers, and underscores
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    return True

def validate_tiktok_username(username):
    """Validate TikTok username"""
    if not username or len(username) < 2 or len(username) > 24:
        return False
    # TikTok usernames only allow letters, numbers, dots, underscores
    if not re.match(r'^[a-zA-Z0-9._]+$', username):
        return False
    return True
