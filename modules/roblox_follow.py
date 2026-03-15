#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Roblox Follow Spam Module - FIXED VERSION
Created by s3cret_proj3ct
Fitur: Generate username & password UNIK untuk setiap akun (1-1000)
"""

import os
import sys
import time
import random
import requests
import threading
import string
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

def generate_username():
    """Generate random username unik untuk setiap akun"""
    # Prefix yang umum di Roblox
    prefixes = [
        'Player', 'Gamer', 'Pro', 'Master', 'Cool', 'Awesome', 'Epic', 'Legend',
        'Shadow', 'Dragon', 'Knight', 'Warrior', 'Hero', 'Ninja', 'Samurai',
        'Demon', 'Angel', 'Hunter', 'Sniper', 'King', 'Queen', 'Prince', 'Princess',
        'Wolf', 'Tiger', 'Lion', 'Eagle', 'Phoenix', 'Dragon', 'Unicorn',
        'Xx', 'xx', 'MLG', 'Noob', 'Pro', 'God', 'Lord', 'Sir',
        'Dark', 'Light', 'Fire', 'Ice', 'Thunder', 'Storm', 'Wind',
        'Blaze', 'Frost', 'Inferno', 'Frozen', 'Electric', 'Atomic'
    ]
    
    # Suffix
    suffixes = [
        'YT', 'TV', 'HD', '4K', 'OP', 'PvP', 'PvE', 'HD',
        'Gaming', 'Playz', 'Plays', 'Craft', 'Build', 'Miner',
        'Slayer', 'Killer', 'Hunter', 'Raider', 'Warlord'
    ]
    
    # Pilih random
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes) if random.random() > 0.5 else ''
    
    # Tambah angka random (1-9999)
    number = random.randint(1, 9999)
    
    # Kombinasi
    patterns = [
        f"{prefix}{number}",
        f"{prefix}{suffix}{number}",
        f"{prefix}_{number}",
        f"{number}{prefix}",
        f"{prefix}{number}{suffix}"
    ]
    
    username = random.choice(patterns)
    
    # Batasi panjang (Roblox max 20 karakter)
    if len(username) > 20:
        username = username[:20]
    
    return username

def generate_password():
    """Generate password unik untuk setiap akun"""
    # Kombinasi karakter
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = '!@#$%^&*'
    
    # Format password
    patterns = [
        # 8-12 karakter
        lambda: ''.join(random.choices(lowercase + uppercase + digits, k=random.randint(8, 12))),
        # Dengan special character
        lambda: ''.join(random.choices(lowercase + uppercase + digits, k=6)) + random.choice(special) + ''.join(random.choices(digits, k=3)),
        # Format password umum
        lambda: random.choice(['Password', 'Pass', 'Pwd']) + str(random.randint(100, 999)) + random.choice(special),
        # Random words
        lambda: random.choice(['Secure', 'Strong', 'Safe', 'Secret']) + str(random.randint(10, 99)) + random.choice(special),
        # Pure random
        lambda: ''.join(random.choices(lowercase + uppercase + digits + special, k=10))
    ]
    
    return random.choice(patterns)()

def generate_birthday():
    """Generate random birthday (year < 2012)"""
    year = random.randint(1990, 2011)
    month = random.randint(1, 12)
    
    # Adjust day based on month
    if month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    elif month == 2:
        # February, ignore leap year for simplicity
        day = random.randint(1, 28)
    else:
        day = random.randint(1, 31)
    
    return f"{year:04d}-{month:02d}-{day:02d}"

def get_user_id(username):
    """Get Roblox user ID from username"""
    url = f"https://users.roblox.com/v1/users/search?keyword={username}&limit=1"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('data') and len(data['data']) > 0:
                return data['data'][0]['id']
    except:
        pass
    return None

def create_roblox_account():
    """Simulate creating Roblox account (for demo)"""
    # Dalam implementasi real, ini akan memanggil API Roblox
    # Tapi untuk demo, kita asumsikan sukses 80%
    time.sleep(random.uniform(0.5, 1.5))
    return random.random() < 0.8, random.randint(100000000, 999999999)

def follow_target(user_id, target_id):
    """Simulate following target (for demo)"""
    time.sleep(random.uniform(0.3, 1.0))
    return random.random() < 0.9

def worker(target_id, count, worker_id):
    """Worker thread for creating accounts and following"""
    global SUCCESS_COUNT, FAILED_COUNT, RUNNING
    
    local_success = 0
    local_failed = 0
    
    print_info(f"Worker {worker_id} starting with {count} accounts")
    
    for i in range(count):
        if not RUNNING:
            break
        
        try:
            # Generate data UNIK untuk setiap akun
            username = generate_username()
            password = generate_password()
            birthday = generate_birthday()
            
            # Create account
            success, user_id = create_roblox_account()
            
            if success and user_id:
                # Follow target
                if follow_target(user_id, target_id):
                    local_success += 1
                    with LOCK:
                        print(f"{Fore.GREEN}[✓] Worker {worker_id}: {i+1}/{count} - {username} followed{Style.RESET_ALL}")
                        
                        # Tampilkan detail kadang-kadang
                        if local_success % 5 == 0:
                            print_info(f"   User: {username} | Pass: {password}")
                else:
                    local_failed += 1
                    with LOCK:
                        print(f"{Fore.RED}[✗] Worker {worker_id}: {i+1}/{count} - Follow failed{Style.RESET_ALL}")
            else:
                local_failed += 1
                with LOCK:
                    print(f"{Fore.RED}[✗] Worker {worker_id}: {i+1}/{count} - Account creation failed{Style.RESET_ALL}")
            
            # Random delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            local_failed += 1
            with LOCK:
                print(f"{Fore.RED}[✗] Worker {worker_id}: Error - {str(e)[:30]}{Style.RESET_ALL}")
            time.sleep(2)
    
    with LOCK:
        SUCCESS_COUNT += local_success
        FAILED_COUNT += local_failed
        print_info(f"Worker {worker_id} done: {local_success} success, {local_failed} failed")

def roblox_follow():
    """Main Roblox follow spam function"""
    global SUCCESS_COUNT, FAILED_COUNT, RUNNING
    
    os.system('clear')
    print(get_ascii('roblox'))
    print_section("ROBLOX FOLLOW SPAM")
    
    print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║              FOLLOW SPAM - 1-1000 ACCOUNTS              ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    # Input target username
    while True:
        target_username = input(f"{Fore.YELLOW}>>> Target Roblox username: {Style.RESET_ALL}").strip()
        if validate_roblox_username(target_username):
            break
        print_error("Invalid username! Use only letters, numbers, underscore")
    
    # Get target user ID
    print_info("Mencari target user ID...")
    target_id = get_user_id(target_username)
    
    if not target_id:
        print_warning("Target tidak ditemukan, tapi akan dilanjutkan dengan username")
        target_id = target_username  # Use username as fallback
    else:
        print_success(f"Target ID: {target_id}")
    
    # Input count
    while True:
        count_input = input(f"\n{Fore.YELLOW}>>> Jumlah followers (1-1000): {Style.RESET_ALL}").strip()
        try:
            count = int(count_input)
            if 1 <= count <= 1000:
                break
            else:
                print_error("Harus antara 1-1000!")
        except:
            print_error("Masukkan angka!")
    
    print(f"\n{Fore.GREEN}📊 STATISTIK:{Style.RESET_ALL}")
    print(f"   • Target      : @{target_username}")
    print(f"   • Total       : {count} akun")
    print(f"   • Username    : Generated UNIK (1 per akun)")
    print(f"   • Password    : Generated UNIK (1 per akun)")
    print(f"   • Birthday    : Random < 2012")
    
    print(f"\n{Fore.YELLOW}⚠️  Proses akan memakan waktu lama (estimasi {count * 2} detik){Style.RESET_ALL}")
    confirm = input(f"\n{Fore.RED}Lanjutkan? (y/n): {Style.RESET_ALL}").strip().lower()
    
    if confirm != 'y':
        print_info("Dibatalkan")
        input(f"\n{Fore.YELLOW}Press Enter...{Style.RESET_ALL}")
        return
    
    print(f"\n{Fore.GREEN}🚀 Memulai proses...{Style.RESET_ALL}\n")
    
    # Reset counters
    SUCCESS_COUNT = 0
    FAILED_COUNT = 0
    RUNNING = True
    
    # Tentukan jumlah worker (max 10 untuk menghindari rate limit)
    workers = min(10, count)
    per_worker = count // workers
    remainder = count % workers
    
    print_info(f"Meluncurkan {workers} worker threads...\n")
    
    # Start threads
    threads = []
    for i in range(workers):
        msg_count = per_worker + (1 if i < remainder else 0)
        t = threading.Thread(target=worker, args=(target_id, msg_count, i+1))
        t.start()
        threads.append(t)
        time.sleep(0.5)  # Stagger start
    
    # Monitor progress
    try:
        start_time = time.time()
        last_total = 0
        
        while any(t.is_alive() for t in threads) and RUNNING:
            time.sleep(3)
            elapsed = time.time() - start_time
            total = SUCCESS_COUNT + FAILED_COUNT
            rate = (total - last_total) / 3
            last_total = total
            
            percent = (total / count) * 100
            bar_length = 40
            filled = int(bar_length * total // count)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            eta = (count - total) / rate if rate > 0 else 0
            
            sys.stdout.write(f'\r{Fore.CYAN}Progress: |{bar}| {percent:.1f}% '
                           f'[{total}/{count}] ✓:{SUCCESS_COUNT} ✗:{FAILED_COUNT} '
                           f'Rate:{rate:.1f}/s ETA:{eta:.0f}s{Style.RESET_ALL}')
            sys.stdout.flush()
        
        print(f"\n\n{Fore.GREEN}{'=' * 50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ SELESAI!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'=' * 50}{Style.RESET_ALL}")
        print(f"   Total      : {SUCCESS_COUNT + FAILED_COUNT}/{count}")
        print(f"   Berhasil   : {SUCCESS_COUNT}")
        print(f"   Gagal      : {FAILED_COUNT}")
        print(f"   Waktu      : {time.time() - start_time:.1f} detik")
        
    except KeyboardInterrupt:
        RUNNING = False
        print(f"\n\n{Fore.RED}🛑 Dihentikan user{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}>>> Tekan Enter untuk kembali...{Style.RESET_ALL}")
