#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
GitHub Tools Module
Created by s3cret_proj3ct
"""

import os
import sys
import time
import requests
from colorama import Fore, Style

from utils.ascii_art import get_ascii
from utils.formatters import print_section, print_success, print_error, print_info

# ============================================================
=== GET REPO INFO
--============================================================
def get_repo_info(repo):
    """Get GitHub repository information"""
    url = f"https://api.github.com/repos/{repo}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            return {'error': f'HTTP {response.status_code}'}
    except Exception as e:
        return {'error': str(e)}

def github_info():
    """Get GitHub repository info"""
    os.system('clear')
    print(get_ascii('info'))
    print_section("GITHUB REPOSITORY INFO")
    
    repo = input(f"\n{Fore.YELLOW}Enter repo (user/repo): {Style.RESET_ALL}").strip()
    
    if '/' not in repo:
        print_error("Format must be 'username/repository'")
        input("\nPress Enter to continue...")
        return
    
    print_info(f"Fetching info for {repo}...")
    
    data = get_repo_info(repo)
    
    if data:
        if 'error' in data:
            print_error(f"Error: {data['error']}")
        elif 'message' in data:
            print_error(f"Error: {data['message']}")
        else:
            print_success(f"\nRepository: {data.get('full_name', repo)}\n")
            
            print(f"   Description : {data.get('description', 'No description')}")
            print(f"   Stars       : {data.get('stargazers_count', 0)} ⭐")
            print(f"   Forks       : {data.get('forks_count', 0)} 🍴")
            print(f"   Watchers    : {data.get('watchers_count', 0)} 👁️")
            print(f"   Language    : {data.get('language', 'Unknown')}")
            print(f"   Created     : {data.get('created_at', 'Unknown')[:10]}")
            print(f"   Updated     : {data.get('updated_at', 'Unknown')[:10]}")
            print(f"   License     : {data.get('license', {}).get('name', 'None')}")
            print(f"\n   URL         : {data.get('html_url', 'N/A')}")
    else:
        print_error("Repository not found!")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
