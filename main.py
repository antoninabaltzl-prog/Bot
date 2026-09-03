#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☠️ 𝑺𝑼𝑵𝑹𝑨𝑲𝑼 — 𝑼𝑳𝑻𝑰𝑴𝑨𝑻𝑬 𝑭𝑰𝑳𝑬 𝑹𝑼𝑵𝑵𝑬𝑹 𝑩𝑶𝑻 ☠️
✅ Upload .py files
✅ Auto input detection
✅ View Logs
✅ Credit System
✅ Referral System
✅ Daily Bonus (2 credits/24h)
✅ 1 Credit = 7 Hours Run
✅ Broadcast System
✅ Admin Panel
✅ Mixed Serif Font (𝐀ɴɪsʜ style)
👑 Owner: @SunrakuV2
📢 Channel: @Anishpy | @VOUCH_R
"""

import os
import sys
import time
import random
import json
import re
import select
import threading
import subprocess
import sqlite3
from datetime import datetime, timedelta
from telebot import TeleBot
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

# ============================================================
# MIXED SERIF FONT CONVERTER (𝐀ɴɪsʜ style)
# ============================================================
def mixed_serif(text):
    """
    Convert text to mixed serif style:
    - First letter of each word: Bold Serif (𝐀)
    - Rest letters: Light Serif (𝑎)
    """
    # Bold Serif (Uppercase/Lowercase)
    bold_serif = {
        'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆',
        'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍',
        'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔',
        'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
        'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠',
        'h': '𝐡', 'i': '𝐢', 'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧',
        'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫', 's': '𝐬', 't': '𝐭', 'u': '𝐮',
        'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳'
    }
    
    # Light Serif (Uppercase/Lowercase)
    light_serif = {
        'A': '𝐴', 'B': '𝐵', 'C': '𝐶', 'D': '𝐷', 'E': '𝐸', 'F': '𝐹', 'G': '𝐺',
        'H': '𝐻', 'I': '𝐼', 'J': '𝐽', 'K': '𝐾', 'L': '𝐿', 'M': '𝑀', 'N': '𝑁',
        'O': '𝑂', 'P': '𝑃', 'Q': '𝑄', 'R': '𝑅', 'S': '𝑆', 'T': '𝑇', 'U': '𝑈',
        'V': '𝑉', 'W': '𝑊', 'X': '𝑋', 'Y': '𝑌', 'Z': '𝑍',
        'a': '𝑎', 'b': '𝑏', 'c': '𝑐', 'd': '𝑑', 'e': '𝑒', 'f': '𝑓', 'g': '𝑔',
        'h': 'ℎ', 'i': '𝑖', 'j': '𝑗', 'k': '𝑘', 'l': '𝑙', 'm': '𝑚', 'n': '𝑛',
        'o': '𝑜', 'p': '𝑝', 'q': '𝑞', 'r': '𝑟', 's': '𝑠', 't': '𝑡', 'u': '𝑢',
        'v': '𝑣', 'w': '𝑤', 'x': '𝑥', 'y': '𝑦', 'z': '𝑧'
    }
    
    # Italic Serif (for special effect)
    italic_serif = {
        'A': '𝐴', 'B': '𝐵', 'C': '𝐶', 'D': '𝐷', 'E': '𝐸', 'F': '𝐹', 'G': '𝐺',
        'H': '𝐻', 'I': '𝐼', 'J': '𝐽', 'K': '𝐾', 'L': '𝐿', 'M': '𝑀', 'N': '𝑁',
        'O': '𝑂', 'P': '𝑃', 'Q': '𝑄', 'R': '𝑅', 'S': '𝑆', 'T': '𝑇', 'U': '𝑈',
        'V': '𝑉', 'W': '𝑊', 'X': '𝑋', 'Y': '𝑌', 'Z': '𝑍',
        'a': '𝑎', 'b': '𝑏', 'c': '𝑐', 'd': '𝑑', 'e': '𝑒', 'f': '𝑓', 'g': '𝑔',
        'h': 'ℎ', 'i': '𝑖', 'j': '𝑗', 'k': '𝑘', 'l': '𝑙', 'm': '𝑚', 'n': '𝑛',
        'o': '𝑜', 'p': '𝑝', 'q': '𝑞', 'r': '𝑟', 's': '𝑠', 't': '𝑡', 'u': '𝑢',
        'v': '𝑣', 'w': '𝑤', 'x': '𝑥', 'y': '𝑦', 'z': '𝑧'
    }
    
    # Numbers and symbols (keep as is or convert)
    symbols = {
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
        ' ': ' ', '.': '.', ',': ',', '!': '!', '?': '?',
        '(': '(', ')': ')', '[': '[', ']': ']', '{': '{', '}': '}',
        '-': '-', '_': '_', '=': '=', '+': '+', '*': '*',
        '/': '/', '\\': '\\', '|': '|', '@': '@', '#': '#',
        '$': '$', '%': '%', '^': '^', '&': '&', '~': '~',
        '`': '`', "'": "'", '"': '"', ':': ':', ';': ';',
        '<': '<', '>': '>', '₹': '₹', '€': '€', '£': '£',
        '¥': '¥', '¢': '¢', '©': '©', '®': '®', '™': '™',
        '✓': '✓', '✗': '✗', '★': '★', '☆': '☆',
        '♡': '♡', '♥': '♥', '♦': '♦', '♣': '♣', '♠': '♠',
        '☠': '☠', '🔥': '🔥', '💀': '💀', '👑': '👑', '💰': '💰',
        '📤': '📤', '▶': '▶', '⏹': '⏹', '📜': '📜', '📊': '📊',
        '👤': '👤', '🎁': '🎁', '🤝': '🤝', '📞': '📞', '👑': '👑',
        '✅': '✅', '❌': '❌', '⚠️': '⚠️', '⏳': '⏳', '🚀': '🚀',
        '🔄': '🔄', '📩': '📩', '📁': '📁', '📂': '📂', '📝': '📝',
        '🎫': '🎫', '🏆': '🏆', '🥇': '🥇', '🥈': '🥈', '🥉': '🥉',
    }
    
    # First, split by words
    words = str(text).split(' ')
    result_words = []
    
    for word in words:
        if not word:
            result_words.append('')
            continue
            
        # Check if word contains only special characters/emojis
        if all(c in symbols for c in word):
            result_words.append(''.join(symbols.get(c, c) for c in word))
            continue
            
        # Apply mixed serif: first letter bold serif, rest light serif
        converted = []
        for i, char in enumerate(word):
            if i == 0:
                # First letter: Bold Serif
                converted.append(bold_serif.get(char, char))
            else:
                # Rest: Light Serif
                converted.append(light_serif.get(char, char))
        result_words.append(''.join(converted))
    
    return ' '.join(result_words)

def ms(text):
    """Shortcut for mixed_serif"""
    return mixed_serif(text)

# ============================================================
# CONFIG
# ============================================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ BOT_TOKEN not set!")
    sys.exit()

bot = TeleBot(BOT_TOKEN, parse_mode='HTML')
OWNER_ID = 8641613327  # @SunrakuV2

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
DATA_DIR = os.path.join(BASE_DIR, 'data')
DATABASE_PATH = os.path.join(DATA_DIR, 'bot.db')

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================================
# DATABASE
# ============================================================
def init_db():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, credits INTEGER DEFAULT 10, 
                  username TEXT, referral_code TEXT, referred_by INTEGER,
                  daily_bonus_date TEXT, is_banned INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS referrals
                 (referrer_id INTEGER, referred_id INTEGER, 
                  credited INTEGER DEFAULT 0, referred_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_files
                 (user_id INTEGER, file_name TEXT, file_type TEXT, 
                  approved INTEGER DEFAULT 0, uploaded_at TEXT,
                  PRIMARY KEY (user_id, file_name))''')
    c.execute('''CREATE TABLE IF NOT EXISTS admins
                 (user_id INTEGER PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS running_sessions
                 (user_id INTEGER, file_name TEXT, start_time TEXT,
                  credits_used INTEGER DEFAULT 1, PRIMARY KEY (user_id, file_name))''')
    c.execute('''CREATE TABLE IF NOT EXISTS pending
                 (pending_id TEXT PRIMARY KEY, user_id INTEGER, 
                  file_name TEXT, file_path TEXT, submitted_at TEXT)''')
    
    c.execute('INSERT OR IGNORE INTO admins (user_id) VALUES (?)', (OWNER_ID,))
    conn.commit()
    conn.close()

init_db()

# ============================================================
# DATA STORES
# ============================================================
user_sessions = {}
bot_scripts = {}
admin_ids = {OWNER_ID}
pending_files = {}
running_sessions = {}
lock = threading.Lock()

# ============================================================
# LOAD ADMINS
# ============================================================
def load_admins():
    global admin_ids
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT user_id FROM admins')
    admin_ids = {row[0] for row in c.fetchall()}
    conn.close()

load_admins()

# ============================================================
# CREDIT SYSTEM
# ============================================================
def get_credits(user_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT credits FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return 10

def set_credits(user_id, amount):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, credits) VALUES (?, 10)', (user_id,))
    c.execute('UPDATE users SET credits = ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

def add_credits(user_id, amount):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, credits) VALUES (?, 10)', (user_id,))
    c.execute('UPDATE users SET credits = credits + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

def deduct_credit(user_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, credits) VALUES (?, 10)', (user_id,))
    c.execute('UPDATE users SET credits = credits - 1 WHERE user_id = ? AND credits > 0', (user_id,))
    conn.commit()
    conn.close()
    return get_credits(user_id)

def add_user(user_id, username=None):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, credits, username) VALUES (?, 10, ?)', (user_id, username))
    conn.commit()
    conn.close()

def is_admin(user_id):
    return user_id in admin_ids

def is_banned(user_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT is_banned FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == 1

def ban_user(user_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def unban_user(user_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('UPDATE users SET is_banned = 0 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

# ============================================================
# DAILY BONUS SYSTEM
# ============================================================
def can_claim_daily_bonus(user_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT daily_bonus_date FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    
    if not row or not row[0]:
        return True
    
    last_claim = datetime.fromisoformat(row[0])
    return datetime.now() - last_claim >= timedelta(hours=24)

def claim_daily_bonus(user_id):
    if not can_claim_daily_bonus(user_id):
        return False, 0
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, credits) VALUES (?, 10)', (user_id,))
    c.execute('UPDATE users SET credits = credits + 2, daily_bonus_date = ? WHERE user_id = ?', 
              (datetime.now().isoformat(), user_id))
    conn.commit()
    
    c.execute('SELECT credits FROM users WHERE user_id = ?', (user_id,))
    new_credits = c.fetchone()[0]
    conn.close()
    
    return True, new_credits

def get_next_bonus_time(user_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT daily_bonus_date FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    
    if not row or not row[0]:
        return ms("Claim now!")
    
    last_claim = datetime.fromisoformat(row[0])
    next_claim = last_claim + timedelta(hours=24)
    remaining = next_claim - datetime.now()
    
    if remaining.total_seconds() <= 0:
        return ms("Claim now!")
    
    hours = int(remaining.total_seconds() // 3600)
    minutes = int((remaining.total_seconds() % 3600) // 60)
    return ms(f"{hours}h {minutes}m")

# ============================================================
# REFERRAL SYSTEM
# ============================================================
def generate_referral_code(user_id):
    return f"SUNRAKU{user_id}{random.randint(100,999)}"

def get_referral_code(user_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT referral_code FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    
    if row and row[0]:
        return row[0]
    
    code = generate_referral_code(user_id)
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('UPDATE users SET referral_code = ? WHERE user_id = ?', (code, user_id))
    conn.commit()
    conn.close()
    return code

def get_referral_count(user_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM referrals WHERE referrer_id = ? AND credited = 1', (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count

def get_pending_referrals(user_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM referrals WHERE referrer_id = ? AND credited = 0', (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count

def add_referral(referrer_id, referred_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT * FROM referrals WHERE referrer_id = ? AND referred_id = ?', (referrer_id, referred_id))
    if c.fetchone():
        conn.close()
        return False
    
    c.execute('INSERT INTO referrals (referrer_id, referred_id, credited, referred_at) VALUES (?, ?, 0, ?)',
              (referrer_id, referred_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return True

def credit_referral(referrer_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM referrals WHERE referrer_id = ? AND credited = 0', (referrer_id,))
    pending = c.fetchone()[0]
    
    if pending > 0:
        c.execute('UPDATE referrals SET credited = 1 WHERE referrer_id = ? AND credited = 0 LIMIT 1', (referrer_id,))
        c.execute('UPDATE users SET credits = credits + 2 WHERE user_id = ?', (referrer_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def get_all_users():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT user_id FROM users')
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

# ============================================================
# 7-HOUR RUN SESSION
# ============================================================
def start_run_session(user_id, file_name):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO running_sessions (user_id, file_name, start_time, credits_used) VALUES (?, ?, ?, 1)',
              (user_id, file_name, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def end_run_session(user_id, file_name):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('DELETE FROM running_sessions WHERE user_id = ? AND file_name = ?', (user_id, file_name))
    conn.commit()
    conn.close()

def can_run_free(user_id, file_name):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT start_time FROM running_sessions WHERE user_id = ? AND file_name = ?', (user_id, file_name))
    row = c.fetchone()
    conn.close()
    
    if not row:
        return False
    
    start_time = datetime.fromisoformat(row[0])
    elapsed = datetime.now() - start_time
    return elapsed < timedelta(hours=7)

# ============================================================
# BROADCAST SYSTEM
# ============================================================
def broadcast_message(message_text, photo=None, document=None):
    users = get_all_users()
    sent = 0
    failed = 0
    
    for user_id in users:
        try:
            if photo:
                bot.send_photo(user_id, photo, caption=message_text, parse_mode='HTML')
            elif document:
                bot.send_document(user_id, document, caption=message_text, parse_mode='HTML')
            else:
                bot.send_message(user_id, message_text, parse_mode='HTML')
            sent += 1
        except:
            failed += 1
        time.sleep(0.05)
    
    return sent, failed

# ============================================================
# USER SESSION
# ============================================================
class UserSession:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.file_path = None
        self.process = None
        self.is_running = False
        self.is_approved = False
        self.logs = []
        self.start_time = None
        self.total_checks = 0
        self.awaiting_input = False
        self.current_file = None
        
    def add_log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {msg}")
        if len(self.logs) > 200:
            self.logs.pop(0)
            
    def get_logs(self, lines=20):
        return "\n".join(self.logs[-lines:]) if self.logs else ms("📭 No logs yet.")

# ============================================================
# LOADING ANIMATION
# ============================================================
LOADING_FRAMES = [
    ms("🔄 Loading ■□□□□□□□□□ 0%"),
    ms("🔄 Loading ■■□□□□□□□□ 20%"),
    ms("🔄 Loading ■■■□□□□□□□ 40%"),
    ms("🔄 Loading ■■■■□□□□□□ 50%"),
    ms("🔄 Loading ■■■■■□□□□□ 60%"),
    ms("🔄 Loading ■■■■■■□□□□ 70%"),
    ms("🔄 Loading ■■■■■■■□□□ 80%"),
    ms("🔄 Loading ■■■■■■■■□□ 90%"),
    ms("✅ Done! ■■■■■■■■■■ 100%")
]

START_FRAMES = [
    ms("🚀 Starting ■□□□□□□□□□ 0%"),
    ms("🚀 Starting ■■□□□□□□□□ 20%"),
    ms("🚀 Starting ■■■□□□□□□□ 40%"),
    ms("🚀 Starting ■■■■□□□□□□ 50%"),
    ms("🚀 Starting ■■■■■□□□□□ 60%"),
    ms("🚀 Starting ■■■■■■□□□□ 70%"),
    ms("🚀 Starting ■■■■■■■□□□ 80%"),
    ms("🚀 Starting ■■■■■■■■□□ 90%"),
    ms("✅ Ready! ■■■■■■■■■■ 100%")
]

def send_loading_animation(message, frames=LOADING_FRAMES, delay=0.3):
    msg = bot.reply_to(message, frames[0])
    for frame in frames[1:]:
        time.sleep(delay)
        try:
            bot.edit_message_text(frame, message.chat.id, msg.message_id)
        except:
            pass
    return msg

# ============================================================
# INPUT DETECTION
# ============================================================
ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
INPUT_PROMPT_RE = re.compile(
    r"(enter|input|choose|select|option|username|password|token|"
    r"chat\s*id|user\s*name|email|phone|number|confirm|yes/no|:\s*$|➜)",
    re.IGNORECASE
)

def clean_prompt(text):
    text = ANSI_ESCAPE_RE.sub("", text)
    return text.strip()[-600:] if len(text) > 600 else text.strip()

def looks_like_input(text):
    if not text:
        return False
    if text.strip().endswith((':', '?', '>', '➜')):
        return True
    return bool(INPUT_PROMPT_RE.search(text))

# ============================================================
# ASK USER FOR INPUT
# ============================================================
def ask_user_for_input(session, prompt):
    if session.awaiting_input:
        return
        
    session.awaiting_input = True
    session.add_log(ms("⏳ Waiting for input..."))
    
    try:
        logs = session.get_logs(15)
        if logs and logs != ms("📭 No logs yet."):
            bot.send_message(
                session.chat_id,
                f"{ms('📜 Recent Logs:')}\n```\n{logs}\n```",
                parse_mode='HTML'
            )
        
        prompt_msg = bot.send_message(
            session.chat_id,
            f"{ms('📥 Input Required!')}\n\n"
            f"{ms('Your file needs input:')}\n"
            f"```\n{prompt}\n```\n\n"
            f"{ms('💬 Reply with the value.')}\n"
            f"{ms('Type /cancel to cancel.')}",
            parse_mode='HTML'
        )
        
        bot.register_next_step_handler(prompt_msg, process_input, session.chat_id)
        
    except Exception as e:
        session.awaiting_input = False
        session.add_log(f"{ms('❌ Input error:')} {e}")

def process_input(message, chat_id):
    with lock:
        if chat_id not in user_sessions:
            return
        session = user_sessions[chat_id]
    
    if not session.awaiting_input:
        bot.reply_to(message, ms("⚠️ No input needed."))
        return
        
    if not session.process or not session.is_running:
        session.awaiting_input = False
        bot.reply_to(message, ms("⚠️ File stopped."))
        return
    
    value = message.text or ""
    
    if value.strip().lower() == "/cancel":
        session.awaiting_input = False
        bot.reply_to(message, ms("❎ Cancelled."))
        return
    
    try:
        if session.process.stdin:
            session.process.stdin.write(value + "\n")
            session.process.stdin.flush()
            session.awaiting_input = False
            session.add_log(f"{ms('✅ Input sent:')} {value[:40]}")
            bot.reply_to(message, f"{ms('✅ Input sent!')}\n`{value[:100]}`")
            
            time.sleep(0.3)
            logs = session.get_logs(10)
            if logs and logs != ms("📭 No logs yet."):
                bot.send_message(
                    chat_id,
                    f"{ms('📜 Updated Logs:')}\n```\n{logs}\n```",
                    parse_mode='HTML'
                )
    except Exception as e:
        session.awaiting_input = False
        session.add_log(f"{ms('❌ Input error:')} {e}")
        bot.reply_to(message, f"{ms('❌ Error:')} {e}")

# ============================================================
# MAIN MENU (With Mixed Serif Font)
# ============================================================
def main_menu(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if is_admin(user_id):
        buttons = [
            ms("📤 Upload File"),
            ms("▶️ Run File"),
            ms("⏹ Stop File"),
            ms("📜 View Logs"),
            ms("📊 My Files"),
            ms("💰 Credits"),
            ms("🎁 Daily Bonus"),
            ms("🤝 Refer & Earn"),
            ms("👤 Profile"),
            ms("👑 Admin Panel"),
            ms("📞 Contact")
        ]
        # Add buttons in rows of 2
        for i in range(0, len(buttons), 2):
            row = buttons[i:i+2]
            markup.add(*[KeyboardButton(btn) for btn in row])
    else:
        buttons = [
            ms("📤 Upload File"),
            ms("▶️ Run File"),
            ms("⏹ Stop File"),
            ms("📜 View Logs"),
            ms("📊 My Files"),
            ms("💰 Credits"),
            ms("🎁 Daily Bonus"),
            ms("🤝 Refer & Earn"),
            ms("👤 Profile"),
            ms("📞 Contact")
        ]
        for i in range(0, len(buttons), 2):
            row = buttons[i:i+2]
            markup.add(*[KeyboardButton(btn) for btn in row])
    
    return markup

# ============================================================
# START COMMAND
# ============================================================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.chat.id
    
    if is_banned(user_id):
        bot.reply_to(message, ms("🚫 You are banned from using this bot!"), parse_mode='HTML')
        return
    
    add_user(user_id, message.from_user.username)
    
    with lock:
        if user_id not in user_sessions:
            user_sessions[user_id] = UserSession(user_id)
    
    # Check referral
    if len(message.text.split()) > 1:
        ref_code = message.text.split()[1]
        if ref_code.startswith('SUNRAKU'):
            try:
                referrer_id = int(ref_code.replace('SUNRAKU', '')[:-3])
                if referrer_id != user_id and add_referral(referrer_id, user_id):
                    if credit_referral(referrer_id):
                        bot.send_message(referrer_id, ms("🎉 You got +2 credits! Someone used your referral link!"), parse_mode='HTML')
                    bot.reply_to(message, ms("🎉 You were referred! Referrer got +2 credits!"), parse_mode='HTML')
            except:
                pass
    
    # Send animation
    msg = bot.reply_to(message, START_FRAMES[0])
    for frame in START_FRAMES[1:]:
        time.sleep(0.2)
        try:
            bot.edit_message_text(frame, message.chat.id, msg.message_id)
        except:
            pass
    
    credits = get_credits(user_id)
    admin_status = ms("👑 Admin") if is_admin(user_id) else ms("👤 User")
    
    welcome = f"""
{ms('☠️ 𝑺𝑼𝑵𝑹𝑨𝑲𝑼 — 𝑼𝑳𝑻𝑰𝑴𝑨𝑻𝑬 𝑭𝑰𝑳𝑬 𝑹𝑼𝑵𝑵𝑬𝑹 𝑩𝑶𝑻 ☠️')}
━━━━━━━━━━━━━━━━━━━━━
{ms('👤 User:')} {message.from_user.first_name}
{ms('🎫 Role:')} {admin_status}
{ms('💰 Credits:')} {credits}
━━━━━━━━━━━━━━━━━━━━━
{ms('📤 Upload .py file (1 credit per 7h)')}
{ms('▶️ Run approved file')}
{ms('🎁 Daily Bonus: 2 credits (24h)')}
{ms('🤝 Refer & Earn: +2 credits per referral')}
━━━━━━━━━━━━━━━━━━━━━
{ms('👑 @SunrakuV2 | 📢 @Anishpy')}
"""
    
    time.sleep(0.3)
    bot.edit_message_text(welcome, message.chat.id, msg.message_id, parse_mode='HTML', reply_markup=main_menu(user_id))

# ============================================================
# UPLOAD FILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == ms("📤 Upload File"))
def upload_file_cmd(message):
    user_id = message.chat.id
    
    if is_banned(user_id):
        bot.reply_to(message, ms("🚫 You are banned!"), parse_mode='HTML')
        return
    
    msg = send_loading_animation(message, LOADING_FRAMES[:5], 0.2)
    bot.edit_message_text(ms("📤 Send your .py file"), message.chat.id, msg.message_id, parse_mode='HTML')
    bot.register_next_step_handler(message, handle_upload)

@bot.message_handler(content_types=['document'])
def handle_upload(message):
    user_id = message.chat.id
    
    if is_banned(user_id):
        bot.reply_to(message, ms("🚫 You are banned!"), parse_mode='HTML')
        return
    
    msg = bot.reply_to(message, ms("⏳ Processing..."), parse_mode='HTML')
    
    if not message.document or not message.document.file_name.endswith('.py'):
        bot.edit_message_text(ms("❌ Only .py files allowed!"), message.chat.id, msg.message_id, parse_mode='HTML')
        return
    
    if message.document.file_size > 5 * 1024 * 1024:
        bot.edit_message_text(ms("❌ Max 5MB!"), message.chat.id, msg.message_id, parse_mode='HTML')
        return
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT file_name FROM user_files WHERE user_id = ? AND file_name = ?', 
              (user_id, message.document.file_name))
    if c.fetchone():
        conn.close()
        bot.edit_message_text(ms(f"⚠️ {message.document.file_name} already exists!"), message.chat.id, msg.message_id, parse_mode='HTML')
        return
    conn.close()
    
    for frame in LOADING_FRAMES:
        time.sleep(0.15)
        try:
            bot.edit_message_text(f"{ms('📤')} {frame}", message.chat.id, msg.message_id)
        except:
            pass
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        
        file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{message.document.file_name}")
        with open(file_path, 'wb') as f:
            f.write(downloaded)
        
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        c.execute('INSERT INTO user_files (user_id, file_name, file_type, approved, uploaded_at) VALUES (?, ?, ?, ?, ?)',
                  (user_id, message.document.file_name, 'py', 0, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        approve_markup = InlineKeyboardMarkup(row_width=2)
        approve_markup.add(
            InlineKeyboardButton(ms("✅ Approve"), callback_data=f"approve_{user_id}_{message.document.file_name}"),
            InlineKeyboardButton(ms("❌ Reject"), callback_data=f"reject_{user_id}_{message.document.file_name}")
        )
        
        for admin_id in admin_ids:
            try:
                bot.send_message(
                    admin_id,
                    f"{ms('📩 New File Upload')}\n"
                    f"{ms('👤 User:')} <code>{user_id}</code>\n"
                    f"{ms('📁 File:')} <code>{message.document.file_name}</code>\n"
                    f"{ms('💰 Credits:')} {get_credits(user_id)}",
                    reply_markup=approve_markup,
                    parse_mode='HTML'
                )
            except:
                pass
        
        bot.edit_message_text(
            f"{ms('✅ Uploaded:')} <code>{message.document.file_name}</code>\n"
            f"{ms('⏳ Waiting for admin approval...')}",
            message.chat.id,
            msg.message_id,
            parse_mode='HTML'
        )
        
    except Exception as e:
        bot.edit_message_text(f"{ms('❌ Error:')} {e}", message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# APPROVE/REJECT CALLBACKS
# ============================================================
@bot.callback_query_handler(func=lambda c: c.data.startswith('approve_'))
def approve_file(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, ms("⚠️ Admin only!"), show_alert=True)
        return
    
    parts = call.data.split('_')
    user_id = int(parts[1])
    file_name = '_'.join(parts[2:])
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('UPDATE user_files SET approved = 1 WHERE user_id = ? AND file_name = ?', (user_id, file_name))
    conn.commit()
    conn.close()
    
    bot.answer_callback_query(call.id, ms("✅ Approved!"))
    bot.edit_message_text(
        f"{ms('✅ Approved:')} <code>{file_name}</code>",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='HTML'
    )
    
    bot.send_message(
        user_id,
        f"{ms('✅ Your file')} <code>{file_name}</code> {ms('has been approved!')}\n"
        f"{ms('▶️ Use Run File button to start.')}",
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith('reject_'))
def reject_file(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, ms("⚠️ Admin only!"), show_alert=True)
        return
    
    parts = call.data.split('_')
    user_id = int(parts[1])
    file_name = '_'.join(parts[2:])
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('DELETE FROM user_files WHERE user_id = ? AND file_name = ?', (user_id, file_name))
    conn.commit()
    conn.close()
    
    file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{file_name}")
    if os.path.exists(file_path):
        os.remove(file_path)
    
    bot.answer_callback_query(call.id, ms("❌ Rejected!"))
    bot.edit_message_text(
        f"{ms('❌ Rejected:')} <code>{file_name}</code>",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='HTML'
    )
    
    bot.send_message(
        user_id,
        f"{ms('❌ Your file')} <code>{file_name}</code> {ms('was rejected.')}\n"
        f"{ms('📞 Contact @SunrakuV2 for details.')}",
        parse_mode='HTML'
    )

# ============================================================
# MY FILES
# ============================================================
@bot.message_handler(func=lambda m: m.text == ms("📊 My Files"))
def my_files_cmd(message):
    user_id = message.chat.id
    
    if is_banned(user_id):
        bot.reply_to(message, ms("🚫 You are banned!"), parse_mode='HTML')
        return
    
    msg = send_loading_animation(message, LOADING_FRAMES[:4], 0.2)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT file_name, approved FROM user_files WHERE user_id = ?', (user_id,))
    files = c.fetchall()
    conn.close()
    
    if not files:
        bot.edit_message_text(ms("📭 No files uploaded.\n\nUse Upload File button."), message.chat.id, msg.message_id, parse_mode='HTML')
        return
    
    text = f"{ms('📂 Your Files:')}\n━━━━━━━━━━━━━━━━━━━━━\n"
    for file_name, approved in files:
        status = ms("✅ Approved") if approved else ms("⏳ Pending")
        text += f"📄 {file_name} — {status}\n"
    
    time.sleep(0.3)
    bot.edit_message_text(text, message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# RUN FILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == ms("▶️ Run File"))
def run_file_cmd(message):
    user_id = message.chat.id
    
    if is_banned(user_id):
        bot.reply_to(message, ms("🚫 You are banned!"), parse_mode='HTML')
        return
    
    msg = send_loading_animation(message, LOADING_FRAMES[:4], 0.2)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT file_name FROM user_files WHERE user_id = ? AND approved = 1', (user_id,))
    files = c.fetchall()
    conn.close()
    
    if not files:
        bot.edit_message_text(ms("❌ No approved files!\n📤 Upload and wait for approval."), message.chat.id, msg.message_id, parse_mode='HTML')
        return
    
    if len(files) == 1:
        file_name = files[0][0]
        if can_run_free(user_id, file_name):
            bot.edit_message_text(f"{ms('🔄 Free run!')}\n<code>{file_name}</code>\n{ms('⏳ 7-hour session active')}", message.chat.id, msg.message_id, parse_mode='HTML')
            run_file(message, file_name, free=True)
            return
        
        credits = get_credits(user_id)
        if credits <= 0:
            bot.edit_message_text(ms("❌ Insufficient credits!\n💰 Use Daily Bonus or Refer & Earn"), message.chat.id, msg.message_id, parse_mode='HTML')
            return
        
        bot.edit_message_text(f"{ms('🚀 Starting:')} <code>{file_name}</code> {ms('(1 credit)')}", message.chat.id, msg.message_id, parse_mode='HTML')
        run_file(message, file_name, free=False)
        return
    
    markup = InlineKeyboardMarkup(row_width=1)
    for file_name in files:
        markup.add(InlineKeyboardButton(f"▶️ {file_name[0]}", callback_data=f"run_{user_id}_{file_name[0]}"))
    bot.edit_message_text(ms("📂 Select file to run:"), message.chat.id, msg.message_id, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith('run_'))
def run_selected_file(call):
    parts = call.data.split('_')
    user_id = int(parts[1])
    file_name = '_'.join(parts[2:])
    
    if call.from_user.id != user_id:
        bot.answer_callback_query(call.id, ms("⚠️ Not your file!"), show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    
    if can_run_free(user_id, file_name):
        bot.send_message(call.message.chat.id, f"{ms('🔄 Free run!')}\n<code>{file_name}</code>\n{ms('⏳ 7-hour session active')}", parse_mode='HTML')
        run_file(call.message, file_name, free=True)
        return
    
    credits = get_credits(user_id)
    if credits <= 0:
        bot.send_message(call.message.chat.id, ms("❌ Insufficient credits!\n💰 Use Daily Bonus or Refer & Earn"), parse_mode='HTML')
        return
    
    bot.send_message(call.message.chat.id, f"{ms('🚀 Starting:')} <code>{file_name}</code> {ms('(1 credit)')}", parse_mode='HTML')
    run_file(call.message, file_name, free=False)

def run_file(message, file_name, free=False):
    user_id = message.chat.id
    
    with lock:
        if user_id not in user_sessions:
            user_sessions[user_id] = UserSession(user_id)
        session = user_sessions[user_id]
    
    if session.is_running:
        bot.reply_to(message, ms("⚠️ File already running!\nUse Stop File first."), parse_mode='HTML')
        return
    
    file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{file_name}")
    if not os.path.exists(file_path):
        bot.reply_to(message, f"{ms('❌ File not found:')} <code>{file_name}</code>", parse_mode='HTML')
        return
    
    if not free:
        new_credits = deduct_credit(user_id)
    else:
        new_credits = get_credits(user_id)
    
    # Show run animation
    msg = bot.reply_to(message, f"{ms('🚀 Starting:')} {ms(file_name)}", parse_mode='HTML')
    for frame in LOADING_FRAMES[:7]:
        time.sleep(0.15)
        try:
            bot.edit_message_text(f"🚀 {frame}", message.chat.id, msg.message_id)
        except:
            pass
    
    try:
        session.process = subprocess.Popen(
            [sys.executable, "-u", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        session.is_running = True
        session.start_time = datetime.now()
        session.file_path = file_path
        session.total_checks = 0
        session.is_approved = True
        session.current_file = file_name
        session.add_log(f"{ms('✅ Started:')} {file_name}")
        
        if not free:
            start_run_session(user_id, file_name)
        
        def read_logs():
            stdout = session.process.stdout
            partial = ""
            prompt_sent = False
            
            while True:
                try:
                    if stdout is None:
                        break
                    ready, _, _ = select.select([stdout], [], [], 0.25)
                    if ready:
                        chunk = os.read(stdout.fileno(), 4096)
                        if not chunk:
                            break
                        text = chunk.decode("utf-8", errors="replace")
                        partial += text
                        prompt_sent = False
                        
                        while "\n" in partial:
                            line, partial = partial.split("\n", 1)
                            line = line.rstrip("\r")
                            if line.strip():
                                session.add_log(line.strip())
                                session.total_checks += 1
                    else:
                        prompt = clean_prompt(partial)
                        if prompt and not prompt_sent and session.process.poll() is None and looks_like_input(prompt):
                            ask_user_for_input(session, prompt)
                            partial = ""
                            prompt_sent = True
                    
                    if session.process.poll() is not None:
                        break
                except Exception as e:
                    session.add_log(f"{ms('⚠️ Reader error:')} {e}")
                    break
            
            remaining = clean_prompt(partial)
            if remaining and not session.awaiting_input:
                session.add_log(remaining)
            
            session.is_running = False
            session.awaiting_input = False
            
            if session.process.poll() == 0:
                session.add_log(ms("✅ File finished"))
            else:
                session.add_log(f"{ms('⚠️ Exited with code')} {session.process.poll()}")
            
            end_run_session(user_id, file_name)
        
        threading.Thread(target=read_logs, daemon=True).start()
        
        time.sleep(0.3)
        bot.edit_message_text(
            f"{ms('✅ Running:')} <code>{file_name}</code>\n"
            f"{ms('💰 Credits left:')} {new_credits}\n"
            f"{ms('📜 Use View Logs to see output')}",
            message.chat.id,
            msg.message_id,
            parse_mode='HTML'
        )
        
    except Exception as e:
        session.is_running = False
        session.add_log(f"{ms('❌ Run error:')} {e}")
        bot.edit_message_text(f"{ms('❌ Error:')} {e}", message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# STOP FILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == ms("⏹ Stop File"))
def stop_file_cmd(message):
    user_id = message.chat.id
    
    msg = send_loading_animation(message, LOADING_FRAMES[:4], 0.2)
    
    with lock:
        if user_id not in user_sessions:
            bot.edit_message_text(ms("❌ No session!"), message.chat.id, msg.message_id, parse_mode='HTML')
            return
        session = user_sessions[user_id]
    
    if not session.is_running:
        bot.edit_message_text(ms("⚠️ No file running!"), message.chat.id, msg.message_id, parse_mode='HTML')
        return
    
    for frame in LOADING_FRAMES[4:7]:
        time.sleep(0.15)
        try:
            bot.edit_message_text(f"⏹ {frame}", message.chat.id, msg.message_id)
        except:
            pass
    
    try:
        session.is_running = False
        session.process.terminate()
        time.sleep(1)
        if session.process.poll() is None:
            session.process.kill()
        session.add_log(ms("⏹ Stopped by user"))
        
        if session.current_file:
            end_run_session(user_id, session.current_file)
        
        time.sleep(0.3)
        bot.edit_message_text(ms("⏹ File stopped!"), message.chat.id, msg.message_id, parse_mode='HTML')
    except Exception as e:
        bot.edit_message_text(f"{ms('❌ Error:')} {e}", message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# VIEW LOGS
# ============================================================
@bot.message_handler(func=lambda m: m.text == ms("📜 View Logs"))
def view_logs_cmd(message):
    user_id = message.chat.id
    
    msg = send_loading_animation(message, LOADING_FRAMES[:4], 0.2)
    
    with lock:
        if user_id not in user_sessions:
            bot.edit_message_text(ms("❌ No session!"), message.chat.id, msg.message_id, parse_mode='HTML')
            return
        session = user_sessions[user_id]
    
    logs = session.get_logs(25)
    if not logs or logs == ms("📭 No logs yet."):
        bot.edit_message_text(ms("📭 No logs yet.\n▶️ Run a file first."), message.chat.id, msg.message_id, parse_mode='HTML')
        return
    
    time.sleep(0.3)
    
    if len(logs) > 4000:
        chunks = [logs[i:i+4000] for i in range(0, len(logs), 4000)]
        bot.edit_message_text(f"{ms('📜 Logs (Part 1/{}')}{len(chunks)}{ms(')')}\n```\n{chunks[0]}\n```", message.chat.id, msg.message_id, parse_mode='HTML')
        for i, chunk in enumerate(chunks[1:3], 2):
            bot.send_message(message.chat.id, f"{ms('📜 Logs (Part {}/{}')}{i}{len(chunks)}{ms(')')}\n```\n{chunk}\n```", parse_mode='HTML')
    else:
        bot.edit_message_text(f"{ms('📜 Recent Logs:')}\n```\n{logs}\n```", message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# CREDITS
# ============================================================
@bot.message_handler(func=lambda m: m.text == ms("💰 Credits"))
def credits_cmd(message):
    user_id = message.chat.id
    
    msg = send_loading_animation(message, LOADING_FRAMES[:4], 0.2)
    
    credits = get_credits(user_id)
    
    text = f"""
{ms('💰 Your Credits')}
━━━━━━━━━━━━━━━━━━━━━
{ms('👤 User:')} {message.from_user.first_name}
{ms('💳 Credits:')} {credits}
{ms('📌 How to get more:')}
• {ms('🎁 Daily Bonus: 2 credits/24h')}
• {ms('🤝 Refer & Earn: +2 credits/referral')}
• {ms('👑 Contact admin for extra credits')}
━━━━━━━━━━━━━━━━━━━━━
"""
    
    time.sleep(0.3)
    bot.edit_message_text(text, message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# DAILY BONUS
# ============================================================
@bot.message_handler(func=lambda m: m.text == ms("🎁 Daily Bonus"))
def daily_bonus_cmd(message):
    user_id = message.chat.id
    
    if is_banned(user_id):
        bot.reply_to(message, ms("🚫 You are banned!"), parse_mode='HTML')
        return
    
    msg = send_loading_animation(message, LOADING_FRAMES[:4], 0.2)
    
    if can_claim_daily_bonus(user_id):
        claimed, new_credits = claim_daily_bonus(user_id)
        if claimed:
            bot.edit_message_text(
                f"{ms('🎁 Daily Bonus Claimed!')}\n"
                f"{ms('✅ +2 credits added!')}\n"
                f"{ms('💰 Total credits:')} {new_credits}\n"
                f"{ms('⏳ Next bonus: 24 hours')}",
                message.chat.id,
                msg.message_id,
                parse_mode='HTML'
            )
        else:
            bot.edit_message_text(ms("❌ Failed to claim bonus."), message.chat.id, msg.message_id, parse_mode='HTML')
    else:
        next_time = get_next_bonus_time(user_id)
        bot.edit_message_text(
            f"{ms('⏳ Daily Bonus already claimed!')}\n"
            f"{ms('🕐 Next claim in:')} {next_time}",
            message.chat.id,
            msg.message_id,
            parse_mode='HTML'
        )

# ============================================================
# REFER & EARN
# ============================================================
@bot.message_handler(func=lambda m: m.text == ms("🤝 Refer & Earn"))
def refer_cmd(message):
    user_id = message.chat.id
    
    if is_banned(user_id):
        bot.reply_to(message, ms("🚫 You are banned!"), parse_mode='HTML')
        return
    
    msg = send_loading_animation(message, LOADING_FRAMES[:4], 0.2)
    
    ref_code = get_referral_code(user_id)
    bot_username = bot.get_me().username
    ref_link = f"https://t.me/{bot_username}?start={ref_code}"
    
    referral_count = get_referral_count(user_id)
    pending_count = get_pending_referrals(user_id)
    
    text = f"""
{ms('🤝 Refer & Earn Credits!')}
━━━━━━━━━━━━━━━━━━━━━
{ms('📊 Your Referrals:')} {referral_count}
{ms('⏳ Pending:')} {pending_count}
{ms('💰 Per Referral: +2 credits')}
━━━━━━━━━━━━━━━━━━━━━
{ms('🔗 Your Referral Link:')}
<code>{ref_link}</code>
━━━━━━━━━━━━━━━━━━━━━
{ms('📌 How it works:')}
1️⃣ {ms('Share your link with friends')}
2️⃣ {ms('They join using your link')}
3️⃣ {ms('You get +2 credits instantly!')}
━━━━━━━━━━━━━━━━━━━━━
{ms('👑 @SunrakuV2 | 📢 @Anishpy')}
"""
    
    # Create QR code button
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(ms("📋 Copy Link"), callback_data=f"copy_{user_id}"))
    markup.add(InlineKeyboardButton(ms("📱 QR Code"), callback_data=f"qr_{user_id}"))
    
    time.sleep(0.3)
    bot.edit_message_text(text, message.chat.id, msg.message_id, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith('copy_'))
def copy_link(call):
    user_id = int(call.data.split('_')[1])
    if call.from_user.id != user_id:
        bot.answer_callback_query(call.id, ms("⚠️ Not your link!"), show_alert=True)
        return
    
    ref_code = get_referral_code(user_id)
    bot_username = bot.get_me().username
    ref_link = f"https://t.me/{bot_username}?start={ref_code}"
    
    bot.answer_callback_query(call.id, ms("📋 Link copied!"), show_alert=True)
    bot.send_message(call.message.chat.id, f"{ms('🔗 Your Referral Link:')}\n<code>{ref_link}</code>", parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith('qr_'))
def generate_qr(call):
    user_id = int(call.data.split('_')[1])
    if call.from_user.id != user_id:
        bot.answer_callback_query(call.id, ms("⚠️ Not your link!"), show_alert=True)
        return
    
    bot.answer_callback_query(call.id, ms("📱 Generating QR..."), show_alert=True)
    
    try:
        import qrcode
        from io import BytesIO
        
        ref_code = get_referral_code(user_id)
        bot_username = bot.get_me().username
        ref_link = f"https://t.me/{bot_username}?start={ref_code}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(ref_link)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        bio = BytesIO()
        img.save(bio, 'PNG')
        bio.seek(0)
        
        bot.send_photo(
            call.message.chat.id,
            photo=bio,
            caption=f"{ms('📱 Your Referral QR Code')}\n<code>{ref_link}</code>",
            parse_mode='HTML'
        )
    except:
        bot.send_message(call.message.chat.id, ms("❌ QR generation failed. Try again."), parse_mode='HTML')

# ============================================================
# PROFILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == ms("👤 Profile"))
def profile_cmd(message):
    user_id = message.chat.id
    
    if is_banned(user_id):
        bot.reply_to(message, ms("🚫 You are banned!"), parse_mode='HTML')
        return
    
    msg = send_loading_animation(message, LOADING_FRAMES[:4], 0.2)
    
    credits = get_credits(user_id)
    referral_count = get_referral_count(user_id)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_files WHERE user_id = ?', (user_id,))
    total_files = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM user_files WHERE user_id = ? AND approved = 1', (user_id,))
    approved_files = c.fetchone()[0]
    conn.close()
    
    admin_status = ms("👑 Admin") if is_admin(user_id) else ms("👤 User")
    
    text = f"""
{ms('👤 Your Profile')}
━━━━━━━━━━━━━━━━━━━━━
{ms('🆔 ID:')} <code>{user_id}</code>
{ms('🎫 Role:')} {admin_status}
{ms('💰 Credits:')} {credits}
{ms('📁 Files:')} {total_files} ({ms('✅')} {approved_files} {ms('approved')})
{ms('🤝 Referrals:')} {referral_count}
━━━━━━━━━━━━━━━━━━━━━
"""
    
    time.sleep(0.3)
    bot.edit_message_text(text, message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# CONTACT
# ============================================================
@bot.message_handler(func=lambda m: m.text == ms("📞 Contact"))
def contact_cmd(message):
    msg = send_loading_animation(message, LOADING_FRAMES[:3], 0.2)
    
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(ms("👑 @SunrakuV2"), url="https://t.me/SunrakuV2"),
        InlineKeyboardButton(ms("📢 @Anishpy"), url="https://t.me/Anishpy"),
        InlineKeyboardButton(ms("📢 @VOUCH_R"), url="https://t.me/VOUCH_R")
    )
    
    time.sleep(0.3)
    bot.edit_message_text(
        f"{ms('📞 Contact & Support')}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"{ms('Click below to connect:')}",
        message.chat.id,
        msg.message_id,
        reply_markup=markup,
        parse_mode='HTML'
    )

# ============================================================
# ADMIN PANEL
# ============================================================
@bot.message_handler(func=lambda m: m.text == ms("👑 Admin Panel"))
def admin_panel_cmd(message):
    user_id = message.chat.id
    
    if not is_admin(user_id):
        bot.reply_to(message, ms("⚠️ Admin only!"), parse_mode='HTML')
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(ms("💰 Add Credits"), callback_data="admin_add_credits"),
        InlineKeyboardButton(ms("👑 Add Admin"), callback_data="admin_add_admin")
    )
    markup.add(
        InlineKeyboardButton(ms("📢 Broadcast"), callback_data="admin_broadcast"),
        InlineKeyboardButton(ms("📊 Stats"), callback_data="admin_stats")
    )
    markup.add(
        InlineKeyboardButton(ms("🚫 Ban User"), callback_data="admin_ban"),
        InlineKeyboardButton(ms("✅ Unban User"), callback_data="admin_unban")
    )
    markup.add(
        InlineKeyboardButton(ms("📋 Banned List"), callback_data="admin_banned_list")
    )
    markup.add(
        InlineKeyboardButton(ms("🔙 Back"), callback_data="admin_back")
    )
    
    bot.reply_to(message, ms("👑 Admin Panel"), reply_markup=markup, parse_mode='HTML')

# ============================================================
# ADMIN CALLBACKS
# ============================================================
@bot.callback_query_handler(func=lambda c: c.data == "admin_add_credits")
def admin_add_credits(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, ms("⚠️ Admin only!"), show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, ms("💰 Enter: user_id amount\nExample: `123456 10`"), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_add_credits)

def process_add_credits(message):
    if not is_admin(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        user_id = int(parts[0])
        amount = int(parts[1])
        add_credits(user_id, amount)
        bot.reply_to(message, f"{ms('✅ Added')} {amount} {ms('credits to')} <code>{user_id}</code>", parse_mode='HTML')
        bot.send_message(user_id, f"{ms('💰 +{} credits added!').format(amount)}\n{ms('Current balance:')} {get_credits(user_id)}", parse_mode='HTML')
    except:
        bot.reply_to(message, ms("❌ Invalid format! Use: user_id amount"), parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_add_admin")
def admin_add_admin(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, ms("⚠️ Admin only!"), show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, ms("👑 Enter user ID to add as admin:"), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_add_admin)

def process_add_admin(message):
    if not is_admin(message.from_user.id):
        return
    
    try:
        user_id = int(message.text.strip())
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO admins (user_id) VALUES (?)', (user_id,))
        conn.commit()
        conn.close()
        load_admins()
        bot.reply_to(message, f"{ms('✅')} <code>{user_id}</code> {ms('added as admin!')}", parse_mode='HTML')
        bot.send_message(user_id, ms("👑 You have been added as admin!"), parse_mode='HTML')
    except:
        bot.reply_to(message, ms("❌ Invalid user ID!"), parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_broadcast")
def admin_broadcast(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, ms("⚠️ Admin only!"), show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, ms("📢 Send broadcast message:"), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if not is_admin(message.from_user.id):
        return
    
    msg = bot.reply_to(message, ms("📢 Broadcasting..."))
    
    sent, failed = broadcast_message(message.text)
    
    bot.edit_message_text(
        f"{ms('✅ Broadcast done!')}\n"
        f"{ms('📤 Sent:')} {sent}\n"
        f"{ms('❌ Failed:')} {failed}",
        message.chat.id,
        msg.message_id,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda c: c.data == "admin_stats")
def admin_stats(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, ms("⚠️ Admin only!"), show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM user_files')
    total_files = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM user_files WHERE approved = 1')
    approved_files = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM admins')
    total_admins = c.fetchone()[0]
    conn.close()
    
    text = f"""
{ms('📊 System Stats')}
━━━━━━━━━━━━━━━━━━━━━
{ms('👥 Total Users:')} {total_users}
{ms('📁 Total Files:')} {total_files}
{ms('✅ Approved:')} {approved_files}
{ms('👑 Admins:')} {total_admins}
{ms('💰 Credits:')} {ms('10 default per user')}
━━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(call.message.chat.id, text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_ban")
def admin_ban(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, ms("⚠️ Admin only!"), show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, ms("🚫 Enter user ID to ban:"), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_ban)

def process_ban(message):
    if not is_admin(message.from_user.id):
        return
    
    try:
        user_id = int(message.text.strip())
        if user_id == OWNER_ID:
            bot.reply_to(message, ms("❌ Cannot ban owner!"), parse_mode='HTML')
            return
        ban_user(user_id)
        bot.reply_to(message, f"{ms('🚫 User')} <code>{user_id}</code> {ms('banned!')}", parse_mode='HTML')
        try:
            bot.send_message(user_id, ms("🚫 You have been banned!"), parse_mode='HTML')
        except:
            pass
    except:
        bot.reply_to(message, ms("❌ Invalid user ID!"), parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_unban")
def admin_unban(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, ms("⚠️ Admin only!"), show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, ms("✅ Enter user ID to unban:"), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_unban)

def process_unban(message):
    if not is_admin(message.from_user.id):
        return
    
    try:
        user_id = int(message.text.strip())
        unban_user(user_id)
        bot.reply_to(message, f"{ms('✅ User')} <code>{user_id}</code> {ms('unbanned!')}", parse_mode='HTML')
        try:
            bot.send_message(user_id, ms("✅ You have been unbanned!"), parse_mode='HTML')
        except:
            pass
    except:
        bot.reply_to(message, ms("❌ Invalid user ID!"), parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_banned_list")
def admin_banned_list(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, ms("⚠️ Admin only!"), show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE is_banned = 1')
    banned = c.fetchall()
    conn.close()
    
    if not banned:
        bot.send_message(call.message.chat.id, ms("📭 No banned users."), parse_mode='HTML')
    else:
        text = f"{ms('🚫 Banned Users:')}\n━━━━━━━━━━━━━━━━━━━━━\n"
        for user_id in banned:
            text += f"• <code>{user_id[0]}</code>\n"
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_back")
def admin_back(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    start_cmd(call.message)

# ============================================================
# START BOT
# ============================================================
print("""
╔═══════════════════════════════════════════════════╗
║   ☠️ 𝑺𝑼𝑵𝑹𝑨𝑲𝑼 — 𝑼𝑳𝑻𝑰𝑴𝑨𝑻𝑬 𝑭𝑰𝑳𝑬 𝑹𝑼𝑵𝑵𝑬𝑹 𝑩𝑶𝑻  ║
║   ✅ Upload .py files                            ║
║   ✅ Auto input detection                        ║
║   ✅ Credit System                               ║
║   ✅ Daily Bonus (2 credits/24h)                 ║
║   ✅ Refer & Earn (+2 credits)                   ║
║   ✅ 1 Credit = 7 Hours Run                      ║
║   ✅ Broadcast System                            ║
║   ✅ Admin Panel                                 ║
║   ✅ Mixed Serif Font (𝐀ɴɪsʜ style)              ║
║   👑 @SunrakuV2 | 📢 @Anishpy                   ║
╚═══════════════════════════════════════════════════╝
""")
print(f"✅ Bot running...")
print(f"👑 Owner: @SunrakuV2")

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"⚠️ Polling error: {e}")
        time.sleep(5)
