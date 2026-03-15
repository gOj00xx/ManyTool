#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
About Tool Module - Informasi & Disclaimer
Created by s3cret_proj3ct
"""

import os
import sys
from colorama import Fore, Style, init

from utils.ascii_art import get_ascii
from utils.formatters import print_section

init(autoreset=True)

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def about_tool():
    """Menampilkan informasi tentang tool dengan disclaimer"""
    clear_screen()
    
    # ASCII Art (bisa diganti dengan yang lebih keren)
    print(f"{Fore.RED}")
    print("███╗   ███╗ █████╗ ███╗   ██╗██╗   ██╗████████╗ ██████╗  ██████╗ ██╗")
    print("████╗ ████║██╔══██╗████╗  ██║╚██╗ ██╔╝╚══██╔══╝██╔═══██╗██╔═══██╗██║")
    print("██╔████╔██║███████║██╔██╗ ██║ ╚████╔╝    ██║   ██║   ██║██║   ██║██║")
    print("██║╚██╔╝██║██╔══██║██║╚██╗██║  ╚██╔╝     ██║   ██║   ██║██║   ██║██║")
    print("██║ ╚═╝ ██║██║  ██║██║ ╚████║   ██║      ██║   ╚██████╔╝╚██████╔╝███████╗")
    print("╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝")
    print(f"{Style.RESET_ALL}")
    
    # Border
    print(f"{Fore.RED}{'=' * 60}{Style.RESET_ALL}")
    
    # Judul
    print(f"{Fore.YELLOW}This Tools \"ManyTool\" Made by s3cret_proj3ct{Style.RESET_ALL}")
    print()
    
    # Disclaimer (YANG PENTING)
    print(f"{Fore.RED}⚠️  DISCLAIMER ⚠️{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}we are not responsible if you are subject to sanctions{Style.RESET_ALL}")
    print()
    
    # Penjelasan
    print(f"{Fore.CYAN}This tool is created for EDUCATIONAL PURPOSES ONLY.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Using this tool against any system without permission is ILLEGAL.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}The developer assumes NO LIABILITY for any misuse.{Style.RESET_ALL}")
    print()
    
    # Informasi Tool
    print(f"{Fore.GREEN}📋 Tool Information:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • Version     : 7.0{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • Creator     : s3cret_proj3ct{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • Release     : 2025{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • Modules     : 20+{Style.RESET_ALL}")
    print()
    
    # Fitur
    print(f"{Fore.GREEN}⚡ Features:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • WhatsApp Spam (Fonnte API){Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • DDoS Attack (10 methods){Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • Roblox Follow Spam{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • TikTok Report Spam{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • WiFi Scanner (Once & Loop){Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • Device Scanner (Once & Loop){Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • IP Information{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • Battery Status{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  • GitHub Repo Info{Style.RESET_ALL}")
    print()
    
    # Credits
    print(f"{Fore.GREEN}👤 Credits:{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  Main Developer : s3cret_proj3ct{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  Special Thanks : All Member About Jailbreak Text{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  Thanks to      : Internet, WorkerGLT{Style.RESET_ALL}")
    print()
    
    # Warning besar
    print(f"{Fore.RED}{'!' * 60}{Style.RESET_ALL}")
    print(f"{Fore.RED}!!! USE AT YOUR OWN RISK !!!{Style.RESET_ALL}")
    print(f"{Fore.RED}{'!' * 60}{Style.RESET_ALL}")
    print()
    
    # Footer
    print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Copyright © 2025 s3cret_proj3ct{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
