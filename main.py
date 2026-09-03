#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☠️ 𝑺𝑼𝑵𝑹𝑨𝑲𝑼 — 𝑼𝑳𝑻𝑰𝑴𝑨𝑻𝑬 𝑭𝑰𝑳𝑬 𝑹𝑼𝑵𝑵𝑬𝑹 𝑩𝑶𝑻 ☠️
✅ Upload .py files
✅ Auto input detection
✅ Send Input (Manual)
✅ Pip Install
✅ View Logs
✅ Credit System (10 free)
✅ 1 Credit = 7 Hours Run
✅ Daily Bonus (2 credits/24h)
✅ Refer & Earn (+2 credits per referral)
✅ Admin Panel
✅ Add Admin System
✅ Broadcast System
✅ Ban/Unban System
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
# BUTTON CONSTANTS
# ============================================================
BTN_UPLOAD = "📤 Upload File"
BTN_RUN = "▶️ Run File"
BTN_STOP = "⏹ Stop File"
BTN_LOGS = "📜 View Logs"
BTN_FILES = "📊 My Files"
BTN_CREDITS = "💰 Credits"
BTN_BONUS = "🎁 Daily Bonus"
BTN_REFER = "🤝 Refer & Earn"
BTN_PROFILE = "👤 Profile"
BTN_ADMIN = "👑 Admin Panel"
BTN_CONTACT = "📞 Contact"
BTN_INPUT = "💬 Send Input"
BTN_PIP = "📦 Pip Install"

# ============================================================
# MIXED SERIF FONT CONVERTER
# ============================================================
def mixed_serif(text):
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
    
    words = str(text).split(' ')
    result = []
    for word in words:
        if not word:
            result.append('')
            continue
        converted = []
        for i, char in enumerate(word):
            if i == 0:
                converted.append(bold_serif.get(char, char))
            else:
                converted.append(light_serif.get(char, char))
        result.append(''.join(converted))
    return ' '.join(result)

def ms(text):
    return mixed_serif(text)

# ============================================================
# CONFIG
# ============================================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ BOT_TOKEN not set!")
    sys.exit()

bot = TeleBot(BOT_TOKEN, parse_mode='HTML')
OWNER_ID = 8641613327

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
                  username TEXT, referral_code TEXT, daily_bonus_date TEXT, 
                  is_banned INTEGER DEFAULT 0)''')
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
                  PRIMARY KEY (user_id, file_name))''')
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
lock = threading.Lock()

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
    return row[0] if row else 10

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
# DAILY BONUS
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

# ============================================================
# REFERRAL SYSTEM
# ============================================================
def get_referral_code(user_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT referral_code FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row and row[0]:
        return row[0]
    code = f"SUNRAKU{user_id}{random.randint(100,999)}"
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
    c.execute('INSERT OR REPLACE INTO running_sessions (user_id, file_name, start_time) VALUES (?, ?, ?)',
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
    return datetime.now() - start_time < timedelta(hours=7)

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
        if len(self.logs) > 500:
            self.logs.pop(0)
            
    def get_logs(self, lines=30):
        return "\n".join(self.logs[-lines:]) if self.logs else "📭 No logs yet."

# ============================================================
# LOADING ANIMATION
# ============================================================
def send_loading(message, frames=None, delay=0.2):
    if frames is None:
        frames = [
            "🔄 Loading ■□□□□□□□□□ 0%",
            "🔄 Loading ■■□□□□□□□□ 20%",
            "🔄 Loading ■■■□□□□□□□ 40%",
            "🔄 Loading ■■■■□□□□□□ 50%",
            "🔄 Loading ■■■■■□□□□□ 60%",
            "🔄 Loading ■■■■■■□□□□ 70%",
            "🔄 Loading ■■■■■■■□□□ 80%",
            "🔄 Loading ■■■■■■■■□□ 90%",
            "✅ Done! ■■■■■■■■■■ 100%"
        ]
    
    msg = bot.reply_to(message, frames[0])
    for frame in frames[1:]:
        time.sleep(delay)
        try:
            bot.edit_message_text(frame, message.chat.id, msg.message_id)
        except:
            pass
    return msg

START_FRAMES = [
    "🚀 Starting ■□□□□□□□□□ 0%",
    "🚀 Starting ■■□□□□□□□□ 20%",
    "🚀 Starting ■■■□□□□□□□ 40%",
    "🚀 Starting ■■■■□□□□□□ 50%",
    "🚀 Starting ■■■■■□□□□□ 60%",
    "🚀 Starting ■■■■■■□□□□ 70%",
    "🚀 Starting ■■■■■■■□□□ 80%",
    "🚀 Starting ■■■■■■■■□□ 90%",
    "✅ Ready! ■■■■■■■■■■ 100%"
]

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

def ask_user_for_input(session, prompt):
    if session.awaiting_input:
        return
    session.awaiting_input = True
    session.add_log("⏳ Waiting for input...")
    try:
        logs = session.get_logs(15)
        if logs and logs != "📭 No logs yet.":
            bot.send_message(session.chat_id, f"📜 Recent Logs:\n```\n{logs}\n```", parse_mode='HTML')
        prompt_msg = bot.send_message(
            session.chat_id,
            f"📥 Input Required!\n\nYour file needs input:\n```\n{prompt}\n```\n\n💬 Reply with the value.\nType /cancel to cancel.",
            parse_mode='HTML'
        )
        bot.register_next_step_handler(prompt_msg, process_input, session.chat_id)
    except Exception as e:
        session.awaiting_input = False
        session.add_log(f"❌ Input error: {e}")

def process_input(message, chat_id):
    with lock:
        if chat_id not in user_sessions:
            return
        session = user_sessions[chat_id]
    if not session.awaiting_input:
        bot.reply_to(message, "⚠️ No input needed.")
        return
    if not session.process or not session.is_running:
        session.awaiting_input = False
        bot.reply_to(message, "⚠️ File stopped.")
        return
    value = message.text or ""
    if value.strip().lower() == "/cancel":
        session.awaiting_input = False
        bot.reply_to(message, "❎ Cancelled.")
        return
    try:
        if session.process.stdin:
            session.process.stdin.write(value + "\n")
            session.process.stdin.flush()
            session.awaiting_input = False
            session.add_log(f"✅ Input sent: {value[:40]}")
            bot.reply_to(message, f"✅ Input sent!\n`{value[:100]}`")
            time.sleep(0.3)
            logs = session.get_logs(10)
            if logs and logs != "📭 No logs yet.":
                bot.send_message(chat_id, f"📜 Updated Logs:\n```\n{logs}\n```", parse_mode='HTML')
    except Exception as e:
        session.awaiting_input = False
        session.add_log(f"❌ Input error: {e}")
        bot.reply_to(message, f"❌ Error: {e}")

# ============================================================
# MAIN MENU
# ============================================================
def main_menu(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if is_admin(user_id):
        buttons = [
            BTN_UPLOAD, BTN_RUN, BTN_STOP, BTN_LOGS,
            BTN_INPUT, BTN_PIP, BTN_FILES, BTN_CREDITS,
            BTN_BONUS, BTN_REFER, BTN_PROFILE, BTN_ADMIN,
            BTN_CONTACT
        ]
    else:
        buttons = [
            BTN_UPLOAD, BTN_RUN, BTN_STOP, BTN_LOGS,
            BTN_INPUT, BTN_PIP, BTN_FILES, BTN_CREDITS,
            BTN_BONUS, BTN_REFER, BTN_PROFILE, BTN_CONTACT
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
        bot.reply_to(message, "🚫 You are banned from using this bot!", parse_mode='HTML')
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
                        bot.send_message(referrer_id, "🎉 You got +2 credits! Someone used your referral link!", parse_mode='HTML')
                    bot.reply_to(message, "🎉 You were referred! Referrer got +2 credits!", parse_mode='HTML')
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
    admin_status = "👑 Admin" if is_admin(user_id) else "👤 User"
    
    welcome = f"""
☠️ {ms('SUNRAKU — ULTIMATE FILE RUNNER BOT')} ☠️
━━━━━━━━━━━━━━━━━━━━━
👤 {ms('User:')} {message.from_user.first_name}
🎫 {ms('Role:')} {admin_status}
💰 {ms('Credits:')} {credits}
━━━━━━━━━━━━━━━━━━━━━
📤 {ms('Upload .py file (1 credit per 7h)')}
▶️ {ms('Run approved file')}
🎁 {ms('Daily Bonus: 2 credits (24h)')}
🤝 {ms('Refer & Earn: +2 credits per referral')}
━━━━━━━━━━━━━━━━━━━━━
👑 @SunrakuV2 | 📢 @Anishpy
"""
    
    time.sleep(0.3)
    bot.edit_message_text(welcome, message.chat.id, msg.message_id, parse_mode='HTML', reply_markup=main_menu(user_id))

# ============================================================
# UPLOAD FILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_UPLOAD)
def upload_file_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 You are banned!", parse_mode='HTML')
        return
    msg = send_loading(message, delay=0.15)
    bot.edit_message_text("📤 Send your .py file", message.chat.id, msg.message_id, parse_mode='HTML')
    bot.register_next_step_handler(message, handle_upload)

@bot.message_handler(content_types=['document'])
def handle_upload(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 You are banned!", parse_mode='HTML')
        return
    msg = bot.reply_to(message, "⏳ Processing...", parse_mode='HTML')
    if not message.document or not message.document.file_name.endswith('.py'):
        bot.edit_message_text("❌ Only .py files allowed!", message.chat.id, msg.message_id, parse_mode='HTML')
        return
    if message.document.file_size > 5 * 1024 * 1024:
        bot.edit_message_text("❌ Max 5MB!", message.chat.id, msg.message_id, parse_mode='HTML')
        return
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT file_name FROM user_files WHERE user_id = ? AND file_name = ?', (user_id, message.document.file_name))
    if c.fetchone():
        conn.close()
        bot.edit_message_text(f"⚠️ {message.document.file_name} already exists!", message.chat.id, msg.message_id, parse_mode='HTML')
        return
    conn.close()
    
    # Loading animation
    frames = [
        "📤 Uploading ■□□□□□□□□□ 0%",
        "📤 Uploading ■■□□□□□□□□ 20%",
        "📤 Uploading ■■■□□□□□□□ 40%",
        "📤 Uploading ■■■■□□□□□□ 50%",
        "📤 Uploading ■■■■■□□□□□ 60%",
        "📤 Uploading ■■■■■■□□□□ 70%",
        "📤 Uploading ■■■■■■■□□□ 80%",
        "📤 Uploading ■■■■■■■■□□ 90%",
        "✅ Uploaded! ■■■■■■■■■■ 100%"
    ]
    for frame in frames:
        time.sleep(0.15)
        try:
            bot.edit_message_text(frame, message.chat.id, msg.message_id)
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
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}_{message.document.file_name}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}_{message.document.file_name}")
        )
        for admin_id in admin_ids:
            try:
                bot.send_message(
                    admin_id,
                    f"📩 New File Upload\n👤 User: <code>{user_id}</code>\n📁 File: <code>{message.document.file_name}</code>\n💰 Credits: {get_credits(user_id)}",
                    reply_markup=approve_markup,
                    parse_mode='HTML'
                )
            except:
                pass
        bot.edit_message_text(
            f"✅ Uploaded: <code>{message.document.file_name}</code>\n⏳ Waiting for admin approval...",
            message.chat.id,
            msg.message_id,
            parse_mode='HTML'
        )
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {e}", message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# APPROVE/REJECT CALLBACKS
# ============================================================
@bot.callback_query_handler(func=lambda c: c.data.startswith('approve_'))
def approve_file(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
        return
    parts = call.data.split('_')
    user_id = int(parts[1])
    file_name = '_'.join(parts[2:])
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('UPDATE user_files SET approved = 1 WHERE user_id = ? AND file_name = ?', (user_id, file_name))
    conn.commit()
    conn.close()
    bot.answer_callback_query(call.id, "✅ Approved!")
    bot.edit_message_text(f"✅ Approved: <code>{file_name}</code>", call.message.chat.id, call.message.message_id, parse_mode='HTML')
    bot.send_message(user_id, f"✅ Your file <code>{file_name}</code> has been approved!\n▶️ Use Run File button to start.", parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith('reject_'))
def reject_file(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
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
    bot.answer_callback_query(call.id, "❌ Rejected!")
    bot.edit_message_text(f"❌ Rejected: <code>{file_name}</code>", call.message.chat.id, call.message.message_id, parse_mode='HTML')
    bot.send_message(user_id, f"❌ Your file <code>{file_name}</code> was rejected.\n📞 Contact @SunrakuV2 for details.", parse_mode='HTML')

# ============================================================
# RUN FILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_RUN)
def run_file_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 You are banned!", parse_mode='HTML')
        return
    
    msg = send_loading(message, delay=0.15)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT file_name FROM user_files WHERE user_id = ? AND approved = 1', (user_id,))
    files = c.fetchall()
    conn.close()
    
    if not files:
        bot.edit_message_text("❌ No approved files!\n📤 Upload and wait for approval.", message.chat.id, msg.message_id, parse_mode='HTML')
        return
    
    if len(files) == 1:
        file_name = files[0][0]
        if can_run_free(user_id, file_name):
            bot.edit_message_text(f"🔄 Free run!\n<code>{file_name}</code>\n⏳ 7-hour session active", message.chat.id, msg.message_id, parse_mode='HTML')
            run_file(message, file_name, free=True)
            return
        credits = get_credits(user_id)
        if credits <= 0:
            bot.edit_message_text("❌ Insufficient credits!\n💰 Use Daily Bonus or Refer & Earn", message.chat.id, msg.message_id, parse_mode='HTML')
            return
        bot.edit_message_text(f"🚀 Starting: <code>{file_name}</code> (1 credit)", message.chat.id, msg.message_id, parse_mode='HTML')
        run_file(message, file_name, free=False)
        return
    
    markup = InlineKeyboardMarkup(row_width=1)
    for file_name in files:
        markup.add(InlineKeyboardButton(f"▶️ {file_name[0]}", callback_data=f"run_{user_id}_{file_name[0]}"))
    bot.edit_message_text("📂 Select file to run:", message.chat.id, msg.message_id, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith('run_'))
def run_selected_file(call):
    parts = call.data.split('_')
    user_id = int(parts[1])
    file_name = '_'.join(parts[2:])
    if call.from_user.id != user_id:
        bot.answer_callback_query(call.id, "⚠️ Not your file!", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    if can_run_free(user_id, file_name):
        bot.send_message(call.message.chat.id, f"🔄 Free run!\n<code>{file_name}</code>\n⏳ 7-hour session active", parse_mode='HTML')
        run_file(call.message, file_name, free=True)
        return
    credits = get_credits(user_id)
    if credits <= 0:
        bot.send_message(call.message.chat.id, "❌ Insufficient credits!\n💰 Use Daily Bonus or Refer & Earn", parse_mode='HTML')
        return
    bot.send_message(call.message.chat.id, f"🚀 Starting: <code>{file_name}</code> (1 credit)", parse_mode='HTML')
    run_file(call.message, file_name, free=False)

def run_file(message, file_name, free=False):
    user_id = message.chat.id
    with lock:
        if user_id not in user_sessions:
            user_sessions[user_id] = UserSession(user_id)
        session = user_sessions[user_id]
    if session.is_running:
        bot.reply_to(message, "⚠️ File already running!\nUse Stop File first.", parse_mode='HTML')
        return
    file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{file_name}")
    if not os.path.exists(file_path):
        bot.reply_to(message, f"❌ File not found: <code>{file_name}</code>", parse_mode='HTML')
        return
    if not free:
        new_credits = deduct_credit(user_id)
    else:
        new_credits = get_credits(user_id)
    
    # Run animation
    frames = [
        "🚀 Starting ■□□□□□□□□□ 0%",
        "🚀 Starting ■■□□□□□□□□ 20%",
        "🚀 Starting ■■■□□□□□□□ 40%",
        "🚀 Starting ■■■■□□□□□□ 50%",
        "🚀 Starting ■■■■■□□□□□ 60%",
        "🚀 Starting ■■■■■■□□□□ 70%",
        "🚀 Starting ■■■■■■■□□□ 80%",
        "🚀 Starting ■■■■■■■■□□ 90%",
        "✅ Running! ■■■■■■■■■■ 100%"
    ]
    msg = bot.reply_to(message, frames[0])
    for frame in frames[1:]:
        time.sleep(0.15)
        try:
            bot.edit_message_text(frame, message.chat.id, msg.message_id)
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
        session.add_log(f"✅ Started: {file_name}")
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
                    session.add_log(f"⚠️ Reader error: {e}")
                    break
            remaining = clean_prompt(partial)
            if remaining and not session.awaiting_input:
                session.add_log(remaining)
            session.is_running = False
            session.awaiting_input = False
            if session.process.poll() == 0:
                session.add_log("✅ File finished")
            else:
                session.add_log(f"⚠️ Exited with code {session.process.poll()}")
            end_run_session(user_id, file_name)
        
        threading.Thread(target=read_logs, daemon=True).start()
        time.sleep(0.3)
        bot.edit_message_text(
            f"✅ Running: <code>{file_name}</code>\n💰 Credits left: {new_credits}\n📜 Use View Logs to see output",
            message.chat.id,
            msg.message_id,
            parse_mode='HTML'
        )
    except Exception as e:
        session.is_running = False
        session.add_log(f"❌ Run error: {e}")
        bot.edit_message_text(f"❌ Error: {e}", message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# STOP FILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_STOP)
def stop_file_cmd(message):
    user_id = message.chat.id
    with lock:
        if user_id not in user_sessions:
            bot.reply_to(message, "❌ No session!", parse_mode='HTML')
            return
        session = user_sessions[user_id]
    if not session.is_running:
        bot.reply_to(message, "⚠️ No file running!", parse_mode='HTML')
        return
    try:
        session.is_running = False
        session.process.terminate()
        time.sleep(1)
        if session.process.poll() is None:
            session.process.kill()
        session.add_log("⏹ Stopped by user")
        if session.current_file:
            end_run_session(user_id, session.current_file)
        bot.reply_to(message, "⏹ File stopped!", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}", parse_mode='HTML')

# ============================================================
# VIEW LOGS (FIXED - No stuck)
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_LOGS)
def view_logs_cmd(message):
    user_id = message.chat.id
    with lock:
        if user_id not in user_sessions:
            bot.reply_to(message, "❌ No session!", parse_mode='HTML')
            return
        session = user_sessions[user_id]
    
    # Direct reply without loading animation to avoid stuck
    logs = session.get_logs(30)
    if not logs or logs == "📭 No logs yet.":
        bot.reply_to(message, "📭 No logs yet.\n▶️ Run a file first.", parse_mode='HTML')
        return
    
    # Send logs directly
    if len(logs) > 4000:
        chunks = [logs[i:i+4000] for i in range(0, len(logs), 4000)]
        bot.reply_to(message, f"📜 Logs (Part 1/{len(chunks)})\n```\n{chunks[0]}\n```", parse_mode='HTML')
        for i, chunk in enumerate(chunks[1:3], 2):
            bot.send_message(message.chat.id, f"📜 Logs (Part {i}/{len(chunks)})\n```\n{chunk}\n```", parse_mode='HTML')
    else:
        bot.reply_to(message, f"📜 Recent Logs:\n```\n{logs}\n```", parse_mode='HTML')

# ============================================================
# SEND INPUT (Manual)
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_INPUT)
def send_input_cmd(message):
    user_id = message.chat.id
    with lock:
        if user_id not in user_sessions:
            bot.reply_to(message, "❌ No session!", parse_mode='HTML')
            return
        session = user_sessions[user_id]
    
    if not session.is_running:
        bot.reply_to(message, "⚠️ No file running!\nRun a file first.", parse_mode='HTML')
        return
    
    if session.awaiting_input:
        bot.reply_to(message, "⏳ File is already waiting for input.\nJust reply with the value!", parse_mode='HTML')
        return
    
    msg = bot.reply_to(message, "💬 Send input for your running file:", parse_mode='HTML')
    session.awaiting_input = True
    session.input_prompt = "Manual input"
    bot.register_next_step_handler(msg, process_manual_input, user_id)

def process_manual_input(message, user_id):
    with lock:
        if user_id not in user_sessions:
            return
        session = user_sessions[user_id]
    
    if not session.awaiting_input:
        bot.reply_to(message, "⚠️ No input needed.", parse_mode='HTML')
        return
    
    if not session.process or not session.is_running:
        session.awaiting_input = False
        bot.reply_to(message, "⚠️ File stopped.", parse_mode='HTML')
        return
    
    value = message.text or ""
    if value.strip().lower() == "/cancel":
        session.awaiting_input = False
        bot.reply_to(message, "❎ Cancelled.", parse_mode='HTML')
        return
    
    try:
        if session.process.stdin:
            session.process.stdin.write(value + "\n")
            session.process.stdin.flush()
            session.awaiting_input = False
            session.add_log(f"✅ Manual input: {value[:40]}")
            bot.reply_to(message, f"✅ Input sent!\n`{value[:100]}`", parse_mode='HTML')
            time.sleep(0.3)
            logs = session.get_logs(10)
            if logs and logs != "📭 No logs yet.":
                bot.send_message(message.chat.id, f"📜 Updated Logs:\n```\n{logs}\n```", parse_mode='HTML')
    except Exception as e:
        session.awaiting_input = False
        session.add_log(f"❌ Input error: {e}")
        bot.reply_to(message, f"❌ Error: {e}", parse_mode='HTML')

# ============================================================
# PIP INSTALL
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_PIP)
def pip_install_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 You are banned!", parse_mode='HTML')
        return
    
    msg = bot.reply_to(message, "📦 Enter package name to install:\nExample: `requests`", parse_mode='HTML')
    bot.register_next_step_handler(msg, process_pip_install)

def process_pip_install(message):
    user_id = message.chat.id
    package = message.text.strip()
    
    if not package:
        bot.reply_to(message, "❌ No package name!", parse_mode='HTML')
        return
    
    if package.lower() == "/cancel":
        bot.reply_to(message, "❎ Cancelled.", parse_mode='HTML')
        return
    
    msg = bot.reply_to(message, f"📦 Installing <code>{package}</code>...", parse_mode='HTML')
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package, "--quiet"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            bot.edit_message_text(
                f"✅ <code>{package}</code> installed successfully!",
                message.chat.id,
                msg.message_id,
                parse_mode='HTML'
            )
        else:
            error = result.stderr or result.stdout
            bot.edit_message_text(
                f"❌ Failed to install <code>{package}</code>:\n```\n{error[:300]}\n```",
                message.chat.id,
                msg.message_id,
                parse_mode='HTML'
            )
    except subprocess.TimeoutExpired:
        bot.edit_message_text(f"⏱️ Installation timed out for <code>{package}</code>", message.chat.id, msg.message_id, parse_mode='HTML')
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {e}", message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# CREDITS
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_CREDITS)
def credits_cmd(message):
    user_id = message.chat.id
    credits = get_credits(user_id)
    referral_count = get_referral_count(user_id)
    
    text = f"""
💰 {ms('Your Credits')}
━━━━━━━━━━━━━━━━━━━━━
👤 {ms('User:')} {message.from_user.first_name}
💳 {ms('Credits:')} {credits}
🤝 {ms('Referrals:')} {referral_count}
━━━━━━━━━━━━━━━━━━━━━
{ms('📌 How to get more:')}
• 🎁 {ms('Daily Bonus: 2 credits/24h')}
• 🤝 {ms('Refer & Earn: +2 credits/referral')}
• 👑 {ms('Contact admin for extra credits')}
━━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, text, parse_mode='HTML')

# ============================================================
# DAILY BONUS
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_BONUS)
def daily_bonus_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 You are banned!", parse_mode='HTML')
        return
    
    if can_claim_daily_bonus(user_id):
        claimed, new_credits = claim_daily_bonus(user_id)
        if claimed:
            bot.reply_to(
                message,
                f"🎁 {ms('Daily Bonus Claimed!')}\n✅ {ms('+2 credits added!')}\n💰 {ms('Total credits:')} {new_credits}\n⏳ {ms('Next bonus: 24 hours')}",
                parse_mode='HTML'
            )
        else:
            bot.reply_to(message, "❌ Failed to claim bonus.", parse_mode='HTML')
    else:
        bot.reply_to(message, "⏳ Daily Bonus already claimed!\n🕐 Next claim in: 24 hours", parse_mode='HTML')

# ============================================================
# REFER & EARN
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_REFER)
def refer_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 You are banned!", parse_mode='HTML')
        return
    
    ref_code = get_referral_code(user_id)
    bot_username = bot.get_me().username
    ref_link = f"https://t.me/{bot_username}?start={ref_code}"
    referral_count = get_referral_count(user_id)
    pending_count = get_pending_referrals(user_id)
    
    text = f"""
🤝 {ms('Refer & Earn Credits!')}
━━━━━━━━━━━━━━━━━━━━━
📊 {ms('Your Referrals:')} {referral_count}
⏳ {ms('Pending:')} {pending_count}
💰 {ms('Per Referral: +2 credits')}
━━━━━━━━━━━━━━━━━━━━━
🔗 {ms('Your Referral Link:')}
<code>{ref_link}</code>
━━━━━━━━━━━━━━━━━━━━━
📌 {ms('How it works:')}
1️⃣ {ms('Share your link with friends')}
2️⃣ {ms('They join using your link')}
3️⃣ {ms('You get +2 credits instantly!')}
━━━━━━━━━━━━━━━━━━━━━
"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📋 Copy Link", callback_data=f"copy_{user_id}"))
    bot.reply_to(message, text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith('copy_'))
def copy_link(call):
    user_id = int(call.data.split('_')[1])
    if call.from_user.id != user_id:
        bot.answer_callback_query(call.id, "⚠️ Not your link!", show_alert=True)
        return
    ref_code = get_referral_code(user_id)
    bot_username = bot.get_me().username
    ref_link = f"https://t.me/{bot_username}?start={ref_code}"
    bot.answer_callback_query(call.id, "📋 Link copied!", show_alert=True)
    bot.send_message(call.message.chat.id, f"🔗 Your Referral Link:\n<code>{ref_link}</code>", parse_mode='HTML')

# ============================================================
# PROFILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_PROFILE)
def profile_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 You are banned!", parse_mode='HTML')
        return
    
    credits = get_credits(user_id)
    referral_count = get_referral_count(user_id)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_files WHERE user_id = ?', (user_id,))
    total_files = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM user_files WHERE user_id = ? AND approved = 1', (user_id,))
    approved_files = c.fetchone()[0]
    conn.close()
    
    admin_status = "👑 Admin" if is_admin(user_id) else "👤 User"
    
    text = f"""
👤 {ms('Your Profile')}
━━━━━━━━━━━━━━━━━━━━━
🆔 {ms('ID:')} <code>{user_id}</code>
🎫 {ms('Role:')} {admin_status}
💰 {ms('Credits:')} {credits}
📁 {ms('Files:')} {total_files} (✅ {approved_files} {ms('approved')})
🤝 {ms('Referrals:')} {referral_count}
━━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, text, parse_mode='HTML')

# ============================================================
# MY FILES
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_FILES)
def my_files_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, "🚫 You are banned!", parse_mode='HTML')
        return
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT file_name, approved FROM user_files WHERE user_id = ?', (user_id,))
    files = c.fetchall()
    conn.close()
    
    if not files:
        bot.reply_to(message, "📭 No files uploaded.\n\nUse Upload File button.", parse_mode='HTML')
        return
    
    text = "📂 Your Files:\n━━━━━━━━━━━━━━━━━━━━━\n"
    for file_name, approved in files:
        status = "✅ Approved" if approved else "⏳ Pending"
        text += f"📄 {file_name} — {status}\n"
    bot.reply_to(message, text, parse_mode='HTML')

# ============================================================
# CONTACT
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_CONTACT)
def contact_cmd(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("👑 @SunrakuV2", url="https://t.me/SunrakuV2"),
        InlineKeyboardButton("📢 @Anishpy", url="https://t.me/Anishpy"),
        InlineKeyboardButton("📢 @VOUCH_R", url="https://t.me/VOUCH_R")
    )
    bot.reply_to(
        message,
        "📞 Contact & Support\n━━━━━━━━━━━━━━━━━━━━━\nClick below to connect:",
        reply_markup=markup,
        parse_mode='HTML'
    )

# ============================================================
# ADMIN PANEL
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_ADMIN)
def admin_panel_cmd(message):
    user_id = message.chat.id
    if not is_admin(user_id):
        bot.reply_to(message, "⚠️ Admin only!", parse_mode='HTML')
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("💰 Add Credits", callback_data="admin_add_credits"),
        InlineKeyboardButton("👑 Add Admin", callback_data="admin_add_admin")
    )
    markup.add(
        InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
        InlineKeyboardButton("📊 Stats", callback_data="admin_stats")
    )
    markup.add(
        InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban"),
        InlineKeyboardButton("✅ Unban User", callback_data="admin_unban")
    )
    markup.add(
        InlineKeyboardButton("📋 Banned List", callback_data="admin_banned_list"),
        InlineKeyboardButton("📁 All Files", callback_data="admin_all_files")
    )
    markup.add(
        InlineKeyboardButton("👥 Users List", callback_data="admin_users_list")
    )
    bot.reply_to(message, "👑 Admin Panel", reply_markup=markup, parse_mode='HTML')

# ============================================================
# ADMIN CALLBACKS
# ============================================================
@bot.callback_query_handler(func=lambda c: c.data == "admin_add_credits")
def admin_add_credits(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, "💰 Enter: user_id amount\nExample: `123456 10`", parse_mode='HTML')
    bot.register_next_step_handler(msg, process_add_credits)

def process_add_credits(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        user_id = int(parts[0])
        amount = int(parts[1])
        add_credits(user_id, amount)
        bot.reply_to(message, f"✅ Added {amount} credits to <code>{user_id}</code>", parse_mode='HTML')
        bot.send_message(user_id, f"💰 +{amount} credits added!\nCurrent balance: {get_credits(user_id)}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Invalid format! Use: user_id amount", parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_add_admin")
def admin_add_admin(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, "👑 Enter user ID to add as admin:", parse_mode='HTML')
    bot.register_next_step_handler(msg, process_add_admin)

def process_add_admin(message):
    if not is_admin(message.from_user.id):
        return
    try:
        user_id = int(message.text.strip())
        if user_id in admin_ids:
            bot.reply_to(message, f"⚠️ <code>{user_id}</code> is already admin!", parse_mode='HTML')
            return
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        c.execute('INSERT INTO admins (user_id) VALUES (?)', (user_id,))
        conn.commit()
        conn.close()
        load_admins()
        bot.reply_to(message, f"✅ <code>{user_id}</code> added as admin!", parse_mode='HTML')
        bot.send_message(user_id, "👑 You have been added as admin!", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Invalid user ID!", parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_broadcast")
def admin_broadcast(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, "📢 Send broadcast message:", parse_mode='HTML')
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if not is_admin(message.from_user.id):
        return
    msg = bot.reply_to(message, "📢 Broadcasting...")
    users = get_all_users()
    sent = 0
    failed = 0
    for user_id in users:
        try:
            bot.send_message(user_id, f"📢 {ms('Broadcast:')}\n\n{message.text}", parse_mode='HTML')
            sent += 1
        except:
            failed += 1
        time.sleep(0.05)
    bot.edit_message_text(
        f"✅ {ms('Broadcast done!')}\n📤 {ms('Sent:')} {sent}\n❌ {ms('Failed:')} {failed}",
        message.chat.id,
        msg.message_id,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda c: c.data == "admin_stats")
def admin_stats(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
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
    c.execute('SELECT SUM(credits) FROM users')
    total_credits = c.fetchone()[0] or 0
    conn.close()
    
    text = f"""
📊 {ms('System Stats')}
━━━━━━━━━━━━━━━━━━━━━
👥 {ms('Total Users:')} {total_users}
📁 {ms('Total Files:')} {total_files}
✅ {ms('Approved:')} {approved_files}
👑 {ms('Admins:')} {total_admins}
💰 {ms('Total Credits:')} {total_credits}
━━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(call.message.chat.id, text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_ban")
def admin_ban(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, "🚫 Enter user ID to ban:", parse_mode='HTML')
    bot.register_next_step_handler(msg, process_ban)

def process_ban(message):
    if not is_admin(message.from_user.id):
        return
    try:
        user_id = int(message.text.strip())
        if user_id == OWNER_ID:
            bot.reply_to(message, "❌ Cannot ban owner!", parse_mode='HTML')
            return
        if is_banned(user_id):
            bot.reply_to(message, f"⚠️ <code>{user_id}</code> is already banned!", parse_mode='HTML')
            return
        ban_user(user_id)
        bot.reply_to(message, f"🚫 User <code>{user_id}</code> banned!", parse_mode='HTML')
        try:
            bot.send_message(user_id, "🚫 You have been banned!", parse_mode='HTML')
        except:
            pass
    except:
        bot.reply_to(message, "❌ Invalid user ID!", parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_unban")
def admin_unban(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, "✅ Enter user ID to unban:", parse_mode='HTML')
    bot.register_next_step_handler(msg, process_unban)

def process_unban(message):
    if not is_admin(message.from_user.id):
        return
    try:
        user_id = int(message.text.strip())
        if not is_banned(user_id):
            bot.reply_to(message, f"⚠️ <code>{user_id}</code> is not banned!", parse_mode='HTML')
            return
        unban_user(user_id)
        bot.reply_to(message, f"✅ User <code>{user_id}</code> unbanned!", parse_mode='HTML')
        try:
            bot.send_message(user_id, "✅ You have been unbanned!", parse_mode='HTML')
        except:
            pass
    except:
        bot.reply_to(message, "❌ Invalid user ID!", parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_banned_list")
def admin_banned_list(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT user_id, username FROM users WHERE is_banned = 1')
    banned = c.fetchall()
    conn.close()
    
    if not banned:
        bot.send_message(call.message.chat.id, "📭 No banned users.", parse_mode='HTML')
    else:
        text = "🚫 Banned Users:\n━━━━━━━━━━━━━━━━━━━━━\n"
        for user_id, username in banned:
            uname = f"@{username}" if username else "N/A"
            text += f"• <code>{user_id}</code> ({uname})\n"
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_users_list")
def admin_users_list(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT user_id, username, credits FROM users ORDER BY user_id')
    users = c.fetchall()
    conn.close()
    
    if not users:
        bot.send_message(call.message.chat.id, "📭 No users found.", parse_mode='HTML')
        return
    
    text = "👥 Users List:\n━━━━━━━━━━━━━━━━━━━━━\n"
    for user_id, username, credits in users[:20]:
        uname = f"@{username}" if username else "N/A"
        text += f"• <code>{user_id}</code> | {uname} | 💰{credits}\n"
    
    if len(users) > 20:
        text += f"\n... and {len(users)-20} more users"
    
    bot.send_message(call.message.chat.id, text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_all_files")
def admin_all_files(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
        return
    bot.answer_callback_query(call.id)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT user_id, file_name, approved FROM user_files ORDER BY user_id')
    files = c.fetchall()
    conn.close()
    
    if not files:
        bot.send_message(call.message.chat.id, "📭 No files found.", parse_mode='HTML')
        return
    
    text = "📁 All Files:\n━━━━━━━━━━━━━━━━━━━━━\n"
    for user_id, file_name, approved in files[:30]:
        status = "✅" if approved else "⏳"
        text += f"• <code>{user_id}</code> | {status} {file_name}\n"
    
    if len(files) > 30:
        text += f"\n... and {len(files)-30} more files"
    
    bot.send_message(call.message.chat.id, text, parse_mode='HTML')

# ============================================================
# START BOT
# ============================================================
print("""
╔═══════════════════════════════════════════════════════════════╗
║   ☠️ 𝑺𝑼𝑵𝑹𝑨𝑲𝑼 — 𝑼𝑳𝑻𝑰𝑴𝑨𝑻𝑬 𝑭𝑰𝑳𝑬 𝑹𝑼𝑵𝑵𝑬𝑹 𝑩𝑶𝑻             ║
║   ✅ Upload .py files                                        ║
║   ✅ Auto input detection                                    ║
║   ✅ Send Input (Manual)                                     ║
║   ✅ Pip Install                                             ║
║   ✅ View Logs                                               ║
║   ✅ Credit System (10 free)                                 ║
║   ✅ 1 Credit = 7 Hours Run                                  ║
║   ✅ Daily Bonus (2 credits/24h)                             ║
║   ✅ Refer & Earn (+2 credits per referral)                  ║
║   ✅ Admin Panel                                             ║
║   ✅ Add Admin System                                        ║
║   ✅ Broadcast System                                        ║
║   ✅ Ban/Unban System                                        ║
║   ✅ Mixed Serif Font (𝐀ɴɪsʜ style)                          ║
║   👑 @SunrakuV2 | 📢 @Anishpy                               ║
╚═══════════════════════════════════════════════════════════════╝
""")
print(f"✅ Bot running...")
print(f"👑 Owner: @SunrakuV2")
print(f"📢 Channel: @Anishpy | @VOUCH_R")

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"⚠️ Polling error: {e}")
        time.sleep(5)
