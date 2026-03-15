#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
WhatsApp Spam Module (Fonnte API)
Created by s3cret_proj3ct
"""

import os
import sys
import time
import threading
import requests
import re
from colorama import Fore, Style

from utils.ascii_art import get_ascii
from utils.validators import validate_phone
from utils.formatters import print_section, print_success, print_error, print_info, print_warning

# ============================================================
# GLOBAL VARIABLES
# ============================================================
SUCCESS_COUNT = 0
FAILED_COUNT = 0
LOCK = threading.Lock()
RUNNING = True

# ============================================================
# FUNGSI CLEAR SCREEN
# ============================================================
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# ============================================================
# FUNGSI CEK SALDO
# ============================================================
def cek_saldo(api_key):
    """Cek saldo via endpoint /get-balance"""
    url = "https://api.fonnte.com/get-balance"
    headers = {'Authorization': api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status'):
                return True, data.get('data', {}).get('balance', 0)
        return False, 0
    except:
        return False, 0

# ============================================================
# FUNGSI KIRIM PESAN
# ============================================================
def send_via_fonnte(api_key, phone, message):
    """Kirim pesan via Fonnte API"""
    url = "https://api.fonnte.com/send"
    
    headers = {
        'Authorization': api_key
    }
    
    data = {
        'target': phone,
        'message': message,
        'delay': '5',
        'countryCode': '62'
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=15)
        
        try:
            result = response.json()
        except:
            result = {'status': False, 'reason': 'Invalid JSON response'}
        
        if response.status_code == 200 and result.get('status'):
            return True, result
        else:
            error_msg = result.get('reason', result.get('message', 'Unknown error'))
            return False, error_msg
            
    except Exception as e:
        return False, str(e)

# ============================================================
# FUNGSI WORKER
# ============================================================
def spam_worker(api_key, phone, message, count, worker_id):
    global SUCCESS_COUNT, FAILED_COUNT, RUNNING
    
    local_success = 0
    local_failed = 0
    
    for i in range(count):
        if not RUNNING:
            break
        
        try:
            success, result = send_via_fonnte(api_key, phone, message)
            
            if success:
                local_success += 1
                with LOCK:
                    print(f"{Fore.GREEN}[✓] Worker {worker_id}: {i+1}/{count}{Style.RESET_ALL}")
            else:
                local_failed += 1
                with LOCK:
                    print(f"{Fore.RED}[✗] Worker {worker_id}: Failed{Style.RESET_ALL}")
            
            time.sleep(1)
            
        except Exception as e:
            local_failed += 1
            with LOCK:
                print(f"{Fore.RED}[✗] Worker {worker_id}: Error{Style.RESET_ALL}")
            time.sleep(2)
    
    with LOCK:
        SUCCESS_COUNT += local_success
        FAILED_COUNT += local_failed

# ============================================================
# FUNGSI SPAM
# ============================================================
def spam_whatsapp():
    """Main WhatsApp spam function"""
    clear_screen()
    print(get_ascii('spam_wa'))
    print_section("WHATSAPP SPAM (FONTTE API)")
    
    # Input API Key
    api_key = input(f"\n{Fore.YELLOW}Enter Fonnte API Key: {Style.RESET_ALL}").strip()
    if not api_key:
        print_error("API Key required!")
        input("\nPress Enter to continue...")
        return
    
    # Cek saldo
    print_info("Checking balance...")
    valid, balance = cek_saldo(api_key)
    
    if valid:
        print_success(f"Balance: {balance}")
    else:
        print_warning("Cannot verify balance, continuing...")
    
    # Input nomor
    while True:
        phone_input = input(f"\n{Fore.YELLOW}Target number (81234567890): {Style.RESET_ALL}").strip()
        is_valid, formatted_phone = validate_phone(phone_input)
        
        if is_valid:
            print_success(f"Valid: {formatted_phone}")
            break
        else:
            print_error("Invalid number!")
    
    # Input pesan
    message = input(f"\n{Fore.YELLOW}Message: {Style.RESET_ALL}").strip()
    if not message:
        message = "Test message from MultiTool"
    
    # Pilih mode
    print(f"\n{Fore.CYAN}Select mode:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}>>> Spam [1]{Style.RESET_ALL}")
    print(f"{Fore.WHITE}>>> Ban [2]{Style.RESET_ALL}")
    print(f"{Fore.WHITE}>>> Back [0]{Style.RESET_ALL}")
    
    choice = input(f"\n{Fore.YELLOW}Choice: {Style.RESET_ALL}").strip()
    
    if choice == '0':
        return
    elif choice == '1':
        min_count, max_count = 20, 500
        mode = "Spam"
    elif choice == '2':
        min_count, max_count = 5000, 10000
        mode = "Ban"
    else:
        print_error("Invalid choice!")
        return
    
    # Input count
    while True:
        try:
            count = int(input(f"\n{Fore.YELLOW}Enter count ({min_count}-{max_count}): {Style.RESET_ALL}"))
            if min_count <= count <= max_count:
                break
            else:
                print_error(f"Must be between {min_count}-{max_count}!")
        except:
            print_error("Invalid number!")
    
    print(f"\n{Fore.YELLOW}Sending {count} messages...{Style.RESET_ALL}")
    
    # Reset counters
    global SUCCESS_COUNT, FAILED_COUNT, RUNNING
    SUCCESS_COUNT = 0
    FAILED_COUNT = 0
    RUNNING = True
    
    # Tentukan workers
    if mode == "Spam":
        workers = min(10, count // 10)
        if workers < 1:
            workers = 1
    else:
        workers = 20
    
    per_worker = count // workers
    remainder = count % workers
    
    print_info(f"Launching {workers} workers...")
    
    # Start threads
    threads = []
    for i in range(workers):
        msg_count = per_worker + (1 if i < remainder else 0)
        t = threading.Thread(target=spam_worker, 
                           args=(api_key, formatted_phone, message, msg_count, i+1))
        t.start()
        threads.append(t)
        time.sleep(0.1)
    
    # Monitor progress
    try:
        start_time = time.time()
        last_total = 0
        
        while any(t.is_alive() for t in threads) and RUNNING:
            time.sleep(2)
            elapsed = time.time() - start_time
            total = SUCCESS_COUNT + FAILED_COUNT
            rps = (total - last_total) / 2
            last_total = total
            
            percent = (total / count) * 100
            bar_length = 30
            filled = int(bar_length * total // count)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            sys.stdout.write(f'\r{Fore.CYAN}Progress: |{bar}| {percent:.1f}% '
                           f'[{total}/{count}] ✓:{SUCCESS_COUNT} ✗:{FAILED_COUNT} '
                           f'RPS:{rps:.1f}{Style.RESET_ALL}')
            sys.stdout.flush()
        
        print(f"\n\n{Fore.GREEN}Complete!{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        RUNNING = False
        print(f"\n\n{Fore.RED}Stopped by user{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
