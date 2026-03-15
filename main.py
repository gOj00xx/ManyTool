#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Multi-Tool Framework - Main Entry Point
Created by s3cret_proj3ct
"""

import os
import sys
import json
import time
from colorama import Fore, Style, init

# Import modules
from utils.ascii_art import get_ascii
from utils.formatters import print_section, print_menu_item, print_info, print_error
from utils.network import check_termux_api

# Import tool modules
from modules.spam_wa import spam_whatsapp
from modules.ddos import run_ddos
from modules.roblox_follow import roblox_follow
from modules.tiktok_report import tiktok_report
from modules.wifi_scanner import scan_once as wifi_scan_once
from modules.wifi_scanner import scan_loop as wifi_scan_loop
from modules.wifi_scanner import connection_info as wifi_connection_info
from modules.device_scanner import scan_once as device_scan_once
from modules.device_scanner import scan_loop as device_scan_loop
from modules.info_tools import wifi_info, ip_info, battery_info
from modules.github_tools import github_info

init(autoreset=True)

# ============================================================
# KONFIGURASI
# ============================================================
CONFIG_FILE = 'config.json'

def load_config():
    """Load configuration from file"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    except:
        pass

# ============================================================
# CLEAR SCREEN
# ============================================================
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# ============================================================
# ABOUT TOOL
# ============================================================
def about_tool():
    """Show information about this tool"""
    clear_screen()
    print(get_ascii('main'))
    print_section("ABOUT THIS TOOL")
    
    print(f"""
{Fore.CYAN}Multi-Tool Framework v7.0
{Fore.YELLOW}Created by s3cret_proj3ct

{Fore.GREEN}Features:{Style.RESET_ALL}
• WhatsApp Spam (Fonnte API)
• DDoS Attack (10 methods)
• Roblox Follow Spam
• TikTok Report Spam
• WiFi Scanner (once & loop)
• Device Scanner (once & loop)
• Connection Info
• IP Information
• Battery Status
• GitHub Repository Info

{Fore.YELLOW}All tools are for educational purposes only!
Use at your own risk.
    """)
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

# ============================================================
# MAIN MENU
# ===========================================================
def main_menu():
    """Display main menu"""
    clear_screen()
    print(get_ascii('main'))
    
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}        ATTACK TOOL{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print_menu_item("1", "Spam Wa")
    print_menu_item("2", "DDos")
    print_menu_item("3", "Pull up Github")
    print_menu_item("4", "End Wifi 0 MBPS")
    
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}        REQUEST TOOL{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print_menu_item("5", "Spam follow account ROBLOX")
    print_menu_item("6", "Spam Report TikTok Account")
    
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}        SCAN TOOL{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print_menu_item("7", "Scan Nearest Wifi")
    print_menu_item("8", "Scan Nearest Wifi Loop")
    print_menu_item("9", "Scan Nearest Device")
    
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}        INFO TOOL{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print_menu_item("10", "Get Connect Wifi Info")
    print_menu_item("11", "Get IP Info")
    print_menu_item("12", "Get Battery Info")
    print_menu_item("13", "Get Github Repo Info")
    print_menu_item("A", "Info About This Tools")
    print_menu_item("B", "EXIT")
    
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

# ============================================================
# DDOS SUBMENU (UNTUK OPSI 2)
# ============================================================
def ddos_menu():
    """Display DDoS submenu"""
    clear_screen()
    print(get_ascii('ddos'))
    print_section("DDoS ATTACK METHODS")
    
    print_menu_item("1", "ICMP Flood")
    print_menu_item("2", "DNS Amplification")
    print_menu_item("3", "SYN Flood")
    print_menu_item("4", "Ping of Death")
    print_menu_item("5", "Fragmented Packet Attack")
    print_menu_item("6", "HTTP Flood")
    print_menu_item("7", "Slowloris")
    print_menu_item("8", "DNS Query Flood")
    print_menu_item("9", "SSL/TLS Exhaustion")
    print_menu_item("10", "Multi-Vector Attack")
    print_menu_item("0", "Back")
    
    return run_ddos()  # Run the DDoS module

# ============================================================
# MAIN
# ============================================================
def main():
    """Main function"""
    # Check Termux API
    if not check_termux_api():
        print_error("Termux API not found!")
        print_info("Install: pkg install termux-api")
        sys.exit(1)
    
    # Load config
    config = load_config()
    
    while True:
        main_menu()
        
        choice = input(f"\n{Fore.YELLOW}Select option: {Style.RESET_ALL}").strip().upper()
        
        if choice == '1':
            spam_whatsapp()
        elif choice == '2':
            ddos_menu()
        elif choice == '3':
            github_info()  # Pull up Github
        elif choice == '4':
            # End Wifi 0 MBPS - stress test
            print_info("Coming soon...")
            time.sleep(1)
        elif choice == '5':
            roblox_follow()
        elif choice == '6':
            tiktok_report()
        elif choice == '7':
            wifi_scan_once()
        elif choice == '8':
            wifi_scan_loop()
        elif choice == '9':
            device_scan_once()
        elif choice == '10':
            wifi_connection_info()
        elif choice == '11':
            ip_info()
        elif choice == '12':
            battery_info()
        elif choice == '13':
            github_info()
        elif choice == 'A':
            about_tool()
        elif choice == 'B':
            clear_screen()
            print(get_ascii('main'))
            print(f"\n{Fore.GREEN}Thank you for using Multi-Tool!")
            print(f"{Fore.MAGENTA}Created by s3cret_proj3ct{Style.RESET_ALL}\n")
            sys.exit(0)
        else:
            print_error("Invalid choice!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}Exiting...{Style.RESET_ALL}")
        sys.exit(0)
