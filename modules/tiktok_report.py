#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
TikTok Report Spam Module
Created by s3cret_proj3ct
"""

import os
import sys
import time
import random
import requests
import threading
import json
from colorama import Fore, Style

from utils.ascii_art import get_ascii
from utils.validators import validate_tiktok_username, validate_count
from utils.formatters import print_section, print_success, print_error, print_info, print_warning

# ============================================================
# GLOBAL VARIABLES
# ============================================================
SUCCESS_COUNT = 0
FAILED_COUNT = 0
LOCK = threading.Lock()
RUNNING = True

REPORT_REASONS = [
    "spam", "harassment", "nudity", "violence",
    "hate_speech", "terrorism", "child_safety",
    "intellectual_property", "impersonation"
]

def get_tiktok_user_info(username):
    """Get TikTok user info from username"""
    # Note: TikTok API requires proper headers and sometimes cookies
    # This is a simplified version
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        # Try to get user info via public endpoint
        url = f"https://www.tiktok.com/@{username}"
        response = requests.get(url, headers=headers, timeout=10)
        
        # Extract user ID from HTML (simplified)
        if response.status_code == 200:
            # This is a placeholder - real implementation would parse HTML
            return True, f"@{username}"
    except:
        pass
    
    return False, None

def send_report(target, reason):
    """Send a report to TikTok"""
    # Note: This is a simplified version - real TikTok API is more complex
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
    # Randomize data to avoid detection
    session = requests.Session()
    
    # Generate random IP-like header
    fake_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    headers['X-Forwarded-For'] = fake_ip
    
    # Random user agent
    user_agents = [
        'TikTok 26.2.0 rv:262018 (iPhone; iOS 14.4.2; en_US) Cronet',
        'TikTok 26.2.0 (Android; Build 14; en_US)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ]
    headers['User-Agent'] = random.choice(user_agents)
    
    # Report endpoint (placeholder)
    url = "https://www.tiktok.com/api/report/user/"
    
    data = {
        'object_id': target,
        'reason': reason,
        'report_type': 'user',
        'source': 'profile'
    }
    
    try:
        response = session.post(url, headers=headers, json=data, timeout=5)
        return response.status_code in [200, 201, 202]
    except:
        return False

def worker(target, count, worker_id):
    """Worker thread for sending reports"""
    global SUCCESS_COUNT, FAILED_COUNT, RUNNING
    
    local_success = 0
    local_failed = 0
    
    for i in range(count):
        if not RUNNING:
            break
        
        try:
            # Random report reason
            reason = random.choice(REPORT_REASONS)
            
            # Send report
            if send_report(target, reason):
                local_success += 1
                with LOCK:
                    print(f"{Fore.GREEN}[✓] Worker {worker_id}: Report {i+1}/{count}{Style.RESET_ALL}")
            else:
                local_failed += 1
                with LOCK:
                    print(f"{Fore.RED}[✗] Worker {worker_id}: Failed{Style.RESET_ALL}")
            
            # Random delay
            time.sleep(random.uniform(0.5, 2))
            
        except:
            local_failed += 1
    
    with LOCK:
        SUCCESS_COUNT += local_success
        FAILED_COUNT += local_failed
        print_info(f"Worker {worker_id} done: {local_success} success, {local_failed} failed")

def tiktok_report():
    """Main TikTok report spam function"""
    global SUCCESS_COUNT, FAILED_COUNT, RUNNING
    
    os.system('clear')
    print(get_ascii('tiktok'))
    print_section("TIKTOK REPORT SPAM")
    
    # Input target
    print(f"\n{Fore.CYAN}Enter target TikTok username:{Style.RESET_ALL}")
    print(f"Display: {Fore.WHITE}@example{Style.RESET_ALL}")
    print(f"Real: {Fore.WHITE}blabla123{Style.RESET_ALL}")
    
    while True:
        target = input(f"\n{Fore.YELLOW}Real username: {Style.RESET_ALL}").strip()
        if validate_tiktok_username(target):
            break
        print_error("Invalid username!")
    
    # Verify user exists
    print_info("Verifying user...")
    exists, user_info = get_tiktok_user_info(target)
    
    if not exists:
        print_warning("Could not verify user, continuing anyway...")
    
    # Input count
    while True:
        count_input = input(f"\n{Fore.YELLOW}Number of reports (1-1000): {Style.RESET_ALL}").strip()
        is_valid, count = validate_count(count_input, 1, 1000)
        if is_valid:
            break
        print_error("Must be between 1-1000!")
    
    print_info(f"Sending {count} reports to @{target}")
    print_warning("This may trigger rate limiting...")
    
    # Reset counters
    SUCCESS_COUNT = 0
    FAILED_COUNT = 0
    RUNNING = True
    
    # Determine workers
    workers = min(10, count // 10)
    if workers < 1:
        workers = 1
    
    per_worker = count // workers
    remainder = count % workers
    
    print_info(f"Launching {workers} workers...")
    
    # Start threads
    threads = []
    for i in range(workers):
        msg_count = per_worker + (1 if i < remainder else 0)
        t = threading.Thread(target=worker, args=(target, msg_count, i+1))
        t.start()
        threads.append(t)
        time.sleep(0.2)
    
    # Monitor progress
    try:
        start_time = time.time()
        last_total = 0
        
        while any(t.is_alive() for t in threads) and RUNNING:
            time.sleep(3)
            elapsed = time.time() - start_time
            total = SUCCESS_COUNT + FAILED_COUNT
            rps = (total - last_total) / 3
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
