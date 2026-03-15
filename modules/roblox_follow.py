#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Roblox Follow Spam Module - OPTIMIZED (LEBIH CEPAT)
Created by s3cret_proj3ct
"""

import os
import sys
import time
import random
import requests
import threading
import json
from datetime import datetime
from colorama import Fore, Style

from utils.ascii_art import get_ascii
from utils.validators import validate_roblox_username, validate_count
from utils.formatters import print_section, print_success, print_error, print_info, print_warning

# ============================================================
# GLOBAL VARIABLES
# ============================================================
SUCCESS_COUNT = 0
FAILED_COUNT = 0
LOCK = threading.Lock()
RUNNING = True

def get_user_id(username):
    """Get Roblox user ID from username - CEPAT"""
    url = f"https://users.roblox.com/v1/users/search?keyword={username}&limit=1"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                return data['data'][0]['id']
    except:
        pass
    return None

def worker(target_id, count, worker_id):
    """Worker thread untuk spam follow"""
    global SUCCESS_COUNT, FAILED_COUNT, RUNNING
    
    local_success = 0
    local_failed = 0
    
    # Daftar user agent random
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Roblox/WinINet/1.0',
        'Roblox/iPhone/2.5.4'
    ]
    
    for i in range(count):
        if not RUNNING:
            break
        
        try:
            # Simulasi follow request (di real implementation perlu cookie/token)
            time.sleep(random.uniform(0.5, 1.5))
            
            # 80% success rate untuk simulasi
            if random.random() < 0.8:
                local_success += 1
                with LOCK:
                    print(f"{Fore.GREEN}[✓] Worker {worker_id}: Follow {i+1}/{count} sukses{Style.RESET_ALL}")
            else:
                local_failed += 1
                with LOCK:
                    print(f"{Fore.RED}[✗] Worker {worker_id}: Follow {i+1}/{count} gagal{Style.RESET_ALL}")
            
        except Exception as e:
            local_failed += 1
    
    with LOCK:
        SUCCESS_COUNT += local_success
        FAILED_COUNT += local_failed
        print_info(f"Worker {worker_id} selesai: {local_success} sukses, {local_failed} gagal")

def roblox_follow():
    """Main Roblox follow spam function"""
    global SUCCESS_COUNT, FAILED_COUNT, RUNNING
    
    os.system('clear')
    print(get_ascii('roblox'))
    print_section("ROBLOX FOLLOW SPAM")
    
    # Input target username
    print_info("Masukkan username Roblox target")
    while True:
        target_username = input(f"\n{Fore.YELLOW}Target username: {Style.RESET_ALL}").strip()
        if validate_roblox_username(target_username):
            break
        print_error("Username tidak valid! (hanya huruf, angka, underscore)")
    
    # Get user ID
    print_info("Mencari user ID...")
    target_id = get_user_id(target_username)
    
    if not target_id:
        print_error("User tidak ditemukan!")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return
    
    print_success(f"User ID: {target_id}")
    
    # Input jumlah
    while True:
        count_input = input(f"\n{Fore.YELLOW}Jumlah followers (1-1000): {Style.RESET_ALL}").strip()
        is_valid, count = validate_count(count_input, 1, 1000)
        if is_valid:
            break
        print_error("Harus antara 1-1000!")
    
    print_info(f"Memproses {count} followers...")
    print_warning("Ini hanya simulasi - untuk real implementation perlu cookie/token")
    
    # Konfirmasi
    confirm = input(f"\n{Fore.YELLOW}Lanjutkan simulasi? (y/n): {Style.RESET_ALL}").lower()
    if confirm != 'y':
        return
    
    # Reset counters
    SUCCESS_COUNT = 0
    FAILED_COUNT = 0
    RUNNING = True
    
    # Tentukan jumlah worker
    workers = min(5, count // 10)
    if workers < 1:
        workers = 1
    
    per_worker = count // workers
    remainder = count % workers
    
    print_info(f"Menjalankan {workers} worker...")
    
    # Start threads
    threads = []
    start_time = time.time()
    
    for i in range(workers):
        msg_count = per_worker + (1 if i < remainder else 0)
        t = threading.Thread(target=worker, args=(target_id, msg_count, i+1))
        t.start()
        threads.append(t)
        time.sleep(0.2)
    
    # Monitor progress
    try:
        last_total = 0
        
        while any(t.is_alive() for t in threads) and RUNNING:
            time.sleep(1)
            elapsed = time.time() - start_time
            total = SUCCESS_COUNT + FAILED_COUNT
            rps = (total - last_total) / 1
            last_total = total
            
            percent = (total / count) * 100
            bar_length = 20
            filled = int(bar_length * total // count)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            sys.stdout.write(f'\r{Fore.CYAN}Progress: |{bar}| {percent:.1f}% '
                           f'[{total}/{count}] ✓:{SUCCESS_COUNT} ✗:{FAILED_COUNT} '
                           f'⏱️:{elapsed:.0f}s 📊:{rps:.1f}/s{Style.RESET_ALL}')
            sys.stdout.flush()
        
        print(f"\n\n{Fore.GREEN}✅ Selesai!{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        RUNNING = False
        print(f"\n\n{Fore.RED}🛑 Dihentikan user{Style.RESET_ALL}")
    
    # Final stats
    elapsed = time.time() - start_time
    total = SUCCESS_COUNT + FAILED_COUNT
    print(f"\n{Fore.CYAN}📊 Statistik Final:{Style.RESET_ALL}")
    print(f"   Total     : {total}/{count}")
    print(f"   Sukses    : {SUCCESS_COUNT}")
    print(f"   Gagal     : {FAILED_COUNT}")
    print(f"   Waktu     : {elapsed:.1f} detik")
    print(f"   Kecepatan : {total/elapsed:.1f} req/s")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
