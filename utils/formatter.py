#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Output Formatters
Created by s3cret_proj3ct
"""

from colorama import Fore, Style
import json

def print_section(title):
    """Print section title"""
    print(f"\n{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW} {title}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

def print_menu_item(number, description, color=Fore.WHITE):
    """Print menu item with >>> format"""
    print(f"{Fore.CYAN}>>>{Style.RESET_ALL} {color}[{number}]{Style.RESET_ALL} {description}")

def print_success(message):
    """Print success message"""
    print(f"{Fore.GREEN}[✓] {message}{Style.RESET_ALL}")

def print_error(message):
    """Print error message"""
    print(f"{Fore.RED}[✗] {message}{Style.RESET_ALL}")

def print_warning(message):
    """Print warning message"""
    print(f"{Fore.YELLOW}[⚠] {message}{Style.RESET_ALL}")

def print_info(message):
    """Print info message"""
    print(f"{Fore.CYAN}[i] {message}{Style.RESET_ALL}")

def format_json(data):
    """Format JSON data for display"""
    if isinstance(data, (dict, list)):
        return json.dumps(data, indent=2, ensure_ascii=False)
    return str(data)

def signal_strength_bar(rssi):
    """Convert RSSI to signal strength bar"""
    if rssi > -50:
        return f"{Fore.GREEN}██████{Style.RESET_ALL}"
    elif rssi > -65:
        return f"{Fore.GREEN}████▒▒{Style.RESET_ALL}"
    elif rssi > -75:
        return f"{Fore.YELLOW}███▒▒▒{Style.RESET_ALL}"
    elif rssi > -85:
        return f"{Fore.YELLOW}██▒▒▒▒{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}█▒▒▒▒▒{Style.RESET_ALL}"
