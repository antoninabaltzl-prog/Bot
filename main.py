#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☠️ 𝑺𝑼𝑵𝑹𝑨𝑲𝑼 — 𝑷𝑹𝑬𝑴𝑰𝑼𝑴 𝑭𝑰𝑳𝑬 𝑹𝑼𝑵𝑵𝑬𝑹 𝑩𝑶𝑻 ☠️
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
# PREMIUM FONT
# ============================================================
def pf(text):
    bold_serif = {
        'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆',
        'H': '𝐇', 'I': '𝐈', 'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍',
        'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑', 'S': '𝐒', 'T': '𝐓', 'U': '𝐔',
        'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙'
    }
    small_caps = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ',
        'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ',
        'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ', 's': 's', 't': 'ᴛ', 'u': 'ᴜ',
        'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ',
        'A': 'ᴀ', 'B': 'ʙ', 'C': 'ᴄ', 'D': 'ᴅ', 'E': 'ᴇ', 'F': 'ꜰ', 'G': 'ɢ',
        'H': 'ʜ', 'I': 'ɪ', 'J': 'ᴊ', 'K': 'ᴋ', 'L': 'ʟ', 'M': 'ᴍ', 'N': 'ɴ',
        'O': 'ᴏ', 'P': 'ᴘ', 'Q': 'ǫ', 'R': 'ʀ', 'S': 's', 'T': 'ᴛ', 'U': 'ᴜ',
        'V': 'ᴠ', 'W': 'ᴡ', 'X': 'x', 'Y': 'ʏ', 'Z': 'ᴢ'
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
                converted.append(bold_serif.get(char.upper(), char))
            else:
                converted.append(small_caps.get(char.lower(), char))
        result.append(''.join(converted))
    return ' '.join(result)

# ============================================================
# BUTTON CONSTANTS
# ============================================================
BTN_UPLOAD = pf("📤 Upload File")
BTN_RUN = pf("▶️ Run File")
BTN_STOP = pf("⏹ Stop File")
BTN_LOGS = pf("📜 View Logs")
BTN_FILES = pf("📊 My Files")
BTN_CREDITS = pf("💰 Credits")
BTN_BONUS = pf("🎁 Daily Bonus")
BTN_REFER = pf("🤝 Refer & Earn")
BTN_PROFILE = pf("👤 Profile")
BTN_ADMIN = pf("👑 Admin Panel")
BTN_CONTACT = pf("📞 Contact")
BTN_INPUT = pf("💬 Send Input")
BTN_PIP = pf("📦 Pip Install")

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
# REFERRAL
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
        self.end_time = None
        self.speed = 0
        self.total_checks = 0
        self.awaiting_input = False
        self.input_prompt = ""
        self.files = []
        self.current_file = None
        
    def add_log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {msg}")
        if len(self.logs) > 500:
            self.logs.pop(0)
            
    def get_logs(self, lines=30):
        if not self.logs:
            return "📭 No logs yet."
        return "\n".join(self.logs[-lines:])
    
    def get_runtime(self):
        if self.start_time:
            end_time = self.end_time or datetime.now()
            diff = end_time - self.start_time
            return str(diff).split('.')[0]
        return "N/A"
    
    def get_speed(self):
        if self.start_time and self.total_checks > 0:
            end_time = self.end_time or datetime.now()
            runtime_seconds = max((end_time - self.start_time).total_seconds(), 1)
            speed = int((self.total_checks / runtime_seconds) * 60)
            self.speed = speed
            return speed
        return self.speed or 0

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
    session.add_log(f"⏳ Waiting for input...")
    
    try:
        logs = session.get_logs(15)
        if logs and logs != "📭 No logs yet.":
            bot.send_message(
                session.chat_id,
                f"{pf('📜 Recent Logs:')}\n```\n{logs}\n```",
                parse_mode='HTML'
            )
        
        prompt_msg = bot.send_message(
            session.chat_id,
            f"{pf('📥 Input Required!')}\n\n"
            f"{pf('Your file needs input:')}\n"
            f"```\n{prompt}\n```\n\n"
            f"{pf('💬 Reply with the value.')}\n"
            f"{pf('Type /cancel to cancel.')}",
            parse_mode='HTML'
        )
        
        bot.register_next_step_handler(prompt_msg, process_user_input, session.chat_id)
        
    except Exception as e:
        session.awaiting_input = False
        session.add_log(f"❌ Input error: {e}")

def process_user_input(message, chat_id):
    with lock:
        if chat_id not in user_sessions:
            return
        session = user_sessions[chat_id]
    
    if not session.awaiting_input:
        bot.reply_to(message, pf("⚠️ No input needed."))
        return
        
    if not session.process or not session.is_running:
        session.awaiting_input = False
        bot.reply_to(message, pf("⚠️ File stopped."))
        return
    
    value = message.text or ""
    
    if value.strip().lower() == "/cancel":
        session.awaiting_input = False
        bot.reply_to(message, pf("❎ Cancelled."))
        return
    
    try:
        if session.process.stdin:
            session.process.stdin.write(value + "\n")
            session.process.stdin.flush()
            session.awaiting_input = False
            session.add_log(f"✅ Input sent: {value[:40]}")
            bot.reply_to(message, f"{pf('✅ Input sent!')}\n`{value[:100]}`")
            
            time.sleep(0.3)
            logs = session.get_logs(10)
            if logs and logs != "📭 No logs yet.":
                bot.send_message(
                    chat_id,
                    f"{pf('📜 Updated Logs:')}\n```\n{logs}\n```",
                    parse_mode='HTML'
                )
    except Exception as e:
        session.awaiting_input = False
        session.add_log(f"❌ Input error: {e}")
        bot.reply_to(message, f"{pf('❌ Error:')} {e}")

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
        bot.reply_to(message, pf("🚫 You are banned!"), parse_mode='HTML')
        return
    
    add_user(user_id, message.from_user.username)
    
    with lock:
        if user_id not in user_sessions:
            user_sessions[user_id] = UserSession(user_id)
    
    if len(message.text.split()) > 1:
        ref_code = message.text.split()[1]
        if ref_code.startswith('SUNRAKU'):
            try:
                referrer_id = int(ref_code.replace('SUNRAKU', '')[:-3])
                if referrer_id != user_id and add_referral(referrer_id, user_id):
                    if credit_referral(referrer_id):
                        bot.send_message(referrer_id, pf("🎉 You got +2 credits!"), parse_mode='HTML')
                    bot.reply_to(message, pf("🎉 You were referred! Referrer got +2 credits!"), parse_mode='HTML')
            except:
                pass
    
    credits = get_credits(user_id)
    admin_status = pf("👑 Admin") if is_admin(user_id) else pf("👤 User")
    
    welcome = f"""
{pf('☠️ S U N R A K U — P R E M I U M  F I L E  R U N N E R')} ☠️
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
{pf('👤 User:')} {message.from_user.first_name}
{pf('🎫 Role:')} {admin_status}
{pf('💰 Credits:')} {credits}
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
{pf('✦ Upload .py file (1 credit/7h)')}
{pf('✦ Run approved file')}
{pf('✦ Daily Bonus: +2 credits (24h)')}
{pf('✦ Refer & Earn: +2 credits/ref')}
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
{pf('♛ @SunrakuV2')} | {pf('✦ @Anishpy')}
"""
    bot.reply_to(message, welcome, reply_markup=main_menu(user_id), parse_mode='HTML')

# ============================================================
# UPLOAD FILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_UPLOAD)
def upload_file_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, pf("🚫 You are banned!"), parse_mode='HTML')
        return
    bot.reply_to(message, pf("📤 Send your .py file"), parse_mode='HTML')
    bot.register_next_step_handler(message, handle_upload)

@bot.message_handler(content_types=['document'])
def handle_upload(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, pf("🚫 You are banned!"), parse_mode='HTML')
        return
    
    if not message.document or not message.document.file_name.endswith('.py'):
        bot.reply_to(message, pf("❌ Only .py files allowed!"), parse_mode='HTML')
        return
    
    if message.document.file_size > 5 * 1024 * 1024:
        bot.reply_to(message, pf("❌ Max 5MB!"), parse_mode='HTML')
        return
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT file_name FROM user_files WHERE user_id = ? AND file_name = ?', 
              (user_id, message.document.file_name))
    if c.fetchone():
        conn.close()
        bot.reply_to(message, pf(f"⚠️ {message.document.file_name} already exists!"), parse_mode='HTML')
        return
    conn.close()
    
    msg = bot.reply_to(message, pf("📤 Uploading..."), parse_mode='HTML')
    
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
            InlineKeyboardButton(pf("✅ Approve"), callback_data=f"approve_{user_id}_{message.document.file_name}"),
            InlineKeyboardButton(pf("❌ Reject"), callback_data=f"reject_{user_id}_{message.document.file_name}")
        )
        
        for admin_id in admin_ids:
            try:
                bot.send_message(
                    admin_id,
                    f"{pf('📩 New File Upload')}\n{pf('👤 User:')} <code>{user_id}</code>\n{pf('📁 File:')} <code>{message.document.file_name}</code>\n{pf('💰 Credits:')} {get_credits(user_id)}",
                    reply_markup=approve_markup,
                    parse_mode='HTML'
                )
            except:
                pass
        
        bot.edit_message_text(
            f"{pf('✅ Uploaded:')} <code>{message.document.file_name}</code>\n{pf('⏳ Waiting for admin approval...')}",
            message.chat.id,
            msg.message_id,
            parse_mode='HTML'
        )
    except Exception as e:
        bot.edit_message_text(f"{pf('❌ Error:')} {e}", message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# APPROVE/REJECT CALLBACKS
# ============================================================
@bot.callback_query_handler(func=lambda c: c.data.startswith('approve_'))
def approve_file(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, pf("⚠️ Admin only!"), show_alert=True)
        return
    parts = call.data.split('_')
    user_id = int(parts[1])
    file_name = '_'.join(parts[2:])
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('UPDATE user_files SET approved = 1 WHERE user_id = ? AND file_name = ?', (user_id, file_name))
    conn.commit()
    conn.close()
    bot.answer_callback_query(call.id, pf("✅ Approved!"))
    bot.edit_message_text(f"{pf('✅ Approved:')} <code>{file_name}</code>", call.message.chat.id, call.message.message_id, parse_mode='HTML')
    bot.send_message(user_id, f"{pf('✅ Your file')} <code>{file_name}</code> {pf('has been approved!')}\n{pf('▶️ Use Run File button to start.')}", parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith('reject_'))
def reject_file(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, pf("⚠️ Admin only!"), show_alert=True)
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
    bot.answer_callback_query(call.id, pf("❌ Rejected!"))
    bot.edit_message_text(f"{pf('❌ Rejected:')} <code>{file_name}</code>", call.message.chat.id, call.message.message_id, parse_mode='HTML')
    bot.send_message(user_id, f"{pf('❌ Your file')} <code>{file_name}</code> {pf('was rejected.')}\n{pf('📞 Contact @SunrakuV2 for details.')}", parse_mode='HTML')

# ============================================================
# RUN FILE - FIXED
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_RUN)
def run_file_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, pf("🚫 You are banned!"), parse_mode='HTML')
        return
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT file_name FROM user_files WHERE user_id = ? AND approved = 1', (user_id,))
    files = c.fetchall()
    conn.close()
    
    if not files:
        bot.reply_to(message, pf("❌ No approved files!\n📤 Upload and wait for approval."), parse_mode='HTML')
        return
    
    if len(files) == 1:
        file_name = files[0][0]
        if can_run_free(user_id, file_name):
            bot.reply_to(message, f"{pf('🔄 Free run!')}\n<code>{file_name}</code>\n{pf('⏳ 7-hour session active')}", parse_mode='HTML')
            run_file(message, file_name, free=True)
            return
        credits = get_credits(user_id)
        if credits <= 0:
            bot.reply_to(message, pf("❌ Insufficient credits!\n💰 Use Daily Bonus or Refer & Earn"), parse_mode='HTML')
            return
        bot.reply_to(message, f"{pf('🚀 Starting:')} <code>{file_name}</code> {pf('(1 credit)')}", parse_mode='HTML')
        run_file(message, file_name, free=False)
        return
    
    markup = InlineKeyboardMarkup(row_width=1)
    for file_name in files:
        markup.add(InlineKeyboardButton(f"▶️ {file_name[0]}", callback_data=f"run_{user_id}_{file_name[0]}"))
    bot.reply_to(message, pf("📂 Select file to run:"), reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith('run_'))
def run_selected_file(call):
    parts = call.data.split('_')
    user_id = int(parts[1])
    file_name = '_'.join(parts[2:])
    if call.from_user.id != user_id:
        bot.answer_callback_query(call.id, pf("⚠️ Not your file!"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    if can_run_free(user_id, file_name):
        bot.send_message(call.message.chat.id, f"{pf('🔄 Free run!')}\n<code>{file_name}</code>\n{pf('⏳ 7-hour session active')}", parse_mode='HTML')
        run_file(call.message, file_name, free=True)
        return
    credits = get_credits(user_id)
    if credits <= 0:
        bot.send_message(call.message.chat.id, pf("❌ Insufficient credits!\n💰 Use Daily Bonus or Refer & Earn"), parse_mode='HTML')
        return
    bot.send_message(call.message.chat.id, f"{pf('🚀 Starting:')} <code>{file_name}</code> {pf('(1 credit)')}", parse_mode='HTML')
    run_file(call.message, file_name, free=False)

def run_file(message, file_name, free=False):
    user_id = message.chat.id
    
    # Check if already running
    with lock:
        if user_id not in user_sessions:
            user_sessions[user_id] = UserSession(user_id)
        session = user_sessions[user_id]
    
    if session.is_running:
        bot.reply_to(message, pf("⚠️ File already running!\nUse Stop File first."), parse_mode='HTML')
        return
    
    file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{file_name}")
    if not os.path.exists(file_path):
        bot.reply_to(message, f"{pf('❌ File not found:')} <code>{file_name}</code>", parse_mode='HTML')
        return
    
    # Deduct credit if not free
    if not free:
        new_credits = deduct_credit(user_id)
    else:
        new_credits = get_credits(user_id)
    
    # Reset session
    session.logs = []
    session.total_checks = 0
    session.start_time = datetime.now()
    session.end_time = None
    session.current_file = file_name
    session.is_running = True
    session.is_approved = True
    session.awaiting_input = False
    
    msg = bot.reply_to(message, pf("🚀 Starting..."), parse_mode='HTML')
    
    try:
        # Start process with proper stdin
        session.process = subprocess.Popen(
            [sys.executable, "-u", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=UPLOAD_DIR
        )
        
        session.add_log(f"✅ Started: {file_name}")
        
        if not free:
            start_run_session(user_id, file_name)
        
        # Start log reader thread
        def read_logs():
            stdout = session.process.stdout
            partial_output = ""
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
                        partial_output += text
                        prompt_sent = False
                        
                        while "\n" in partial_output:
                            line, partial_output = partial_output.split("\n", 1)
                            line = line.rstrip("\r")
                            if line.strip():
                                session.add_log(line.strip())
                                session.total_checks += 1
                    else:
                        prompt = clean_prompt(partial_output)
                        if (
                            prompt
                            and not prompt_sent
                            and session.process.poll() is None
                            and looks_like_input(prompt)
                        ):
                            ask_user_for_input(session, prompt)
                            partial_output = ""
                            prompt_sent = True
                    
                    if session.process.poll() is not None:
                        break
                except Exception as e:
                    session.add_log(f"⚠️ Reader error: {e}")
                    break
            
            remaining = clean_prompt(partial_output)
            if remaining and not session.awaiting_input:
                session.add_log(remaining)
            
            return_code = session.process.poll()
            session.awaiting_input = False
            session.input_prompt = ""
            session.is_running = False
            session.end_time = datetime.now()
            
            if return_code == 0:
                session.add_log("✅ File finished")
            elif return_code is not None:
                session.add_log(f"⚠️ File exited with code {return_code}")
            
            end_run_session(user_id, file_name)
        
        threading.Thread(target=read_logs, daemon=True).start()
        time.sleep(0.5)
        bot.edit_message_text(
            f"{pf('✅ Running:')} <code>{file_name}</code>\n{pf('💰 Credits left:')} {new_credits}\n{pf('📜 Use View Logs to see output')}\n{pf('💬 Use Send Input if file asks for input')}",
            message.chat.id,
            msg.message_id,
            parse_mode='HTML'
        )
    except Exception as e:
        session.is_running = False
        session.add_log(f"❌ Run error: {str(e)}")
        bot.edit_message_text(f"{pf('❌ Error:')} {e}", message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# STOP FILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_STOP)
def stop_file_cmd(message):
    user_id = message.chat.id
    with lock:
        if user_id not in user_sessions:
            bot.reply_to(message, pf("❌ No session!"), parse_mode='HTML')
            return
        session = user_sessions[user_id]
    if not session.is_running:
        bot.reply_to(message, pf("⚠️ No file running!"), parse_mode='HTML')
        return
    try:
        session.is_running = False
        session.process.terminate()
        time.sleep(1)
        if session.process.poll() is None:
            session.process.kill()
        session.end_time = datetime.now()
        session.add_log("⏹ File stopped")
        if session.current_file:
            end_run_session(user_id, session.current_file)
        bot.reply_to(message, pf("⏹ File stopped!"), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"{pf('❌ Error:')} {e}", parse_mode='HTML')

# ============================================================
# VIEW LOGS
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_LOGS)
def view_logs_cmd(message):
    chat_id = message.chat.id
    with lock:
        if chat_id not in user_sessions:
            bot.reply_to(message, pf("❌ No session found!"), parse_mode='HTML')
            return
        session = user_sessions[chat_id]
    
    logs = session.get_logs(30)
    
    if not logs or logs == "📭 No logs yet.":
        if session.is_running:
            bot.reply_to(message, pf("⏳ File is running but no logs yet...\n\nCheck back in a moment."), parse_mode='HTML')
        else:
            bot.reply_to(message, pf("📭 No logs yet.\n\n▶️ Run a file to see output."), parse_mode='HTML')
        return
    
    if len(logs) > 4000:
        chunks = [logs[i:i+4000] for i in range(0, len(logs), 4000)]
        bot.reply_to(message, f"{pf('📜 Recent Logs (Part 1/{}')}{len(chunks)}{pf(')')}:\n```\n{chunks[0]}\n```", parse_mode='HTML')
        for i, chunk in enumerate(chunks[1:4], 2):
            bot.send_message(chat_id, f"{pf('📜 Logs (Part {}/{}')}{i}{len(chunks)}{pf(')')}:\n```\n{chunk}\n```", parse_mode='HTML')
    else:
        bot.reply_to(message, f"{pf('📜 Recent Logs:')}\n```\n{logs}\n```", parse_mode='HTML')

# ============================================================
# SEND INPUT
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_INPUT)
def send_input_cmd(message):
    user_id = message.chat.id
    with lock:
        if user_id not in user_sessions:
            bot.reply_to(message, pf("❌ No session!"), parse_mode='HTML')
            return
        session = user_sessions[user_id]
    
    if not session.is_running:
        bot.reply_to(message, pf("⚠️ No file running!\nRun a file first."), parse_mode='HTML')
        return
    
    if session.awaiting_input:
        bot.reply_to(message, pf("⏳ File is already waiting for input.\nJust reply with the value!"), parse_mode='HTML')
        return
    
    msg = bot.reply_to(message, pf("💬 Send input for your running file:"), parse_mode='HTML')
    session.awaiting_input = True
    bot.register_next_step_handler(msg, process_manual_input, user_id)

def process_manual_input(message, user_id):
    with lock:
        if user_id not in user_sessions:
            return
        session = user_sessions[user_id]
    
    if not session.awaiting_input:
        bot.reply_to(message, pf("⚠️ No input needed."), parse_mode='HTML')
        return
    
    if not session.process or not session.is_running:
        session.awaiting_input = False
        bot.reply_to(message, pf("⚠️ File stopped."), parse_mode='HTML')
        return
    
    value = message.text or ""
    if value.strip().lower() == "/cancel":
        session.awaiting_input = False
        bot.reply_to(message, pf("❎ Cancelled."), parse_mode='HTML')
        return
    
    try:
        if session.process.stdin:
            session.process.stdin.write(value + "\n")
            session.process.stdin.flush()
            session.awaiting_input = False
            session.add_log(f"✅ Manual input: {value[:40]}")
            bot.reply_to(message, f"{pf('✅ Input sent!')}\n`{value[:100]}`", parse_mode='HTML')
            time.sleep(0.3)
            logs = session.get_logs(10)
            if logs and logs != "📭 No logs yet.":
                bot.send_message(message.chat.id, f"{pf('📜 Updated Logs:')}\n```\n{logs}\n```", parse_mode='HTML')
    except Exception as e:
        session.awaiting_input = False
        session.add_log(f"❌ Input error: {e}")
        bot.reply_to(message, f"{pf('❌ Error:')} {e}", parse_mode='HTML')

# ============================================================
# PIP INSTALL
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_PIP)
def pip_install_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, pf("🚫 You are banned!"), parse_mode='HTML')
        return
    
    msg = bot.reply_to(message, pf("📦 Enter package name to install:\nExample: `requests`"), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_pip_install)

def process_pip_install(message):
    user_id = message.chat.id
    package = message.text.strip()
    
    if not package:
        bot.reply_to(message, pf("❌ No package name!"), parse_mode='HTML')
        return
    
    if package.lower() == "/cancel":
        bot.reply_to(message, pf("❎ Cancelled."), parse_mode='HTML')
        return
    
    msg = bot.reply_to(message, f"{pf('📦 Installing')} <code>{package}</code>...", parse_mode='HTML')
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package, "--quiet"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            bot.edit_message_text(
                f"{pf('✅')} <code>{package}</code> {pf('installed successfully!')}",
                message.chat.id,
                msg.message_id,
                parse_mode='HTML'
            )
        else:
            error = result.stderr or result.stdout
            bot.edit_message_text(
                f"{pf('❌ Failed to install')} <code>{package}</code>:\n```\n{error[:300]}\n```",
                message.chat.id,
                msg.message_id,
                parse_mode='HTML'
            )
    except subprocess.TimeoutExpired:
        bot.edit_message_text(f"{pf('⏱️ Installation timed out for')} <code>{package}</code>", message.chat.id, msg.message_id, parse_mode='HTML')
    except Exception as e:
        bot.edit_message_text(f"{pf('❌ Error:')} {e}", message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# CREDITS
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_CREDITS)
def credits_cmd(message):
    user_id = message.chat.id
    credits = get_credits(user_id)
    referral_count = get_referral_count(user_id)
    
    text = f"""
{pf('💰 Your Credits')}
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
{pf('👤 User:')} {message.from_user.first_name}
{pf('💳 Credits:')} {credits}
{pf('🤝 Referrals:')} {referral_count}
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
{pf('✦ How to get more:')}
{pf('  ▪ Daily Bonus: +2 credits (24h)')}
{pf('  ▪ Refer & Earn: +2 credits/ref')}
{pf('  ▪ Contact admin for extra')}
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
"""
    bot.reply_to(message, text, parse_mode='HTML')

# ============================================================
# DAILY BONUS
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_BONUS)
def daily_bonus_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, pf("🚫 You are banned!"), parse_mode='HTML')
        return
    
    if can_claim_daily_bonus(user_id):
        claimed, new_credits = claim_daily_bonus(user_id)
        if claimed:
            bot.reply_to(
                message,
                f"{pf('🎁 Daily Bonus Claimed!')}\n{pf('✅ +2 credits added!')}\n{pf('💰 Total credits:')} {new_credits}\n{pf('⏳ Next bonus: 24 hours')}",
                parse_mode='HTML'
            )
        else:
            bot.reply_to(message, pf("❌ Failed to claim bonus."), parse_mode='HTML')
    else:
        bot.reply_to(message, pf("⏳ Daily Bonus already claimed!\n🕐 Next claim in: 24 hours"), parse_mode='HTML')

# ============================================================
# REFER & EARN
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_REFER)
def refer_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, pf("🚫 You are banned!"), parse_mode='HTML')
        return
    
    ref_code = get_referral_code(user_id)
    bot_username = bot.get_me().username
    ref_link = f"https://t.me/{bot_username}?start={ref_code}"
    referral_count = get_referral_count(user_id)
    pending_count = get_pending_referrals(user_id)
    
    text = f"""
{pf('🤝 Refer & Earn Credits!')}
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
{pf('📊 Your Referrals:')} {referral_count}
{pf('⏳ Pending:')} {pending_count}
{pf('💰 Per Referral: +2 credits')}
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
{pf('🔗 Your Referral Link:')}
<code>{ref_link}</code>
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
{pf('✦ How it works:')}
{pf('  1. Share your link with friends')}
{pf('  2. They join using your link')}
{pf('  3. You get +2 credits instantly!')}
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(pf("📋 Copy Link"), callback_data=f"copy_{user_id}"))
    bot.reply_to(message, text, reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith('copy_'))
def copy_link(call):
    user_id = int(call.data.split('_')[1])
    if call.from_user.id != user_id:
        bot.answer_callback_query(call.id, pf("⚠️ Not your link!"), show_alert=True)
        return
    ref_code = get_referral_code(user_id)
    bot_username = bot.get_me().username
    ref_link = f"https://t.me/{bot_username}?start={ref_code}"
    bot.answer_callback_query(call.id, pf("📋 Link copied!"), show_alert=True)
    bot.send_message(call.message.chat.id, f"{pf('🔗 Your Referral Link:')}\n<code>{ref_link}</code>", parse_mode='HTML')

# ============================================================
# PROFILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_PROFILE)
def profile_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, pf("🚫 You are banned!"), parse_mode='HTML')
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
    
    admin_status = pf("👑 Admin") if is_admin(user_id) else pf("👤 User")
    
    text = f"""
{pf('👤 Your Profile')}
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
{pf('🆔 ID:')} <code>{user_id}</code>
{pf('🎫 Role:')} {admin_status}
{pf('💰 Credits:')} {credits}
{pf('📁 Files:')} {total_files} ({pf('✅')} {approved_files} {pf('approved')})
{pf('🤝 Referrals:')} {referral_count}
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
"""
    bot.reply_to(message, text, parse_mode='HTML')

# ============================================================
# MY FILES
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_FILES)
def my_files_cmd(message):
    user_id = message.chat.id
    if is_banned(user_id):
        bot.reply_to(message, pf("🚫 You are banned!"), parse_mode='HTML')
        return
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT file_name, approved FROM user_files WHERE user_id = ?', (user_id,))
    files = c.fetchall()
    conn.close()
    
    if not files:
        bot.reply_to(message, pf("📭 No files uploaded.\n\nUse Upload File button."), parse_mode='HTML')
        return
    
    text = f"{pf('📂 Your Files:')}\n◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈\n"
    for file_name, approved in files:
        status = pf("✅ Approved") if approved else pf("⏳ Pending")
        text += f"📄 {file_name} — {status}\n"
    bot.reply_to(message, text, parse_mode='HTML')

# ============================================================
# CONTACT
# ============================================================
@bot.message_handler(func=lambda m: m.text == BTN_CONTACT)
def contact_cmd(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(pf("♛ @SunrakuV2"), url="https://t.me/SunrakuV2"),
        InlineKeyboardButton(pf("✦ @Anishpy"), url="https://t.me/Anishpy"),
        InlineKeyboardButton(pf("✦ @VOUCH_R"), url="https://t.me/VOUCH_R")
    )
    bot.reply_to(
        message,
        f"{pf('📞 Contact & Support')}\n◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈\n{pf('Click below to connect:')}",
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
        bot.reply_to(message, pf("⚠️ Admin only!"), parse_mode='HTML')
        return
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(pf("💰 Add Credits"), callback_data="admin_add_credits"),
        InlineKeyboardButton(pf("👑 Add Admin"), callback_data="admin_add_admin")
    )
    markup.add(
        InlineKeyboardButton(pf("📢 Broadcast"), callback_data="admin_broadcast"),
        InlineKeyboardButton(pf("📊 Stats"), callback_data="admin_stats")
    )
    markup.add(
        InlineKeyboardButton(pf("🚫 Ban User"), callback_data="admin_ban"),
        InlineKeyboardButton(pf("✅ Unban User"), callback_data="admin_unban")
    )
    markup.add(
        InlineKeyboardButton(pf("📋 Banned List"), callback_data="admin_banned_list"),
        InlineKeyboardButton(pf("📁 All Files"), callback_data="admin_all_files")
    )
    markup.add(
        InlineKeyboardButton(pf("👥 Users List"), callback_data="admin_users_list")
    )
    bot.reply_to(message, pf("👑 Admin Panel"), reply_markup=markup, parse_mode='HTML')

# ============================================================
# ADMIN CALLBACKS
# ============================================================
@bot.callback_query_handler(func=lambda c: c.data == "admin_add_credits")
def admin_add_credits(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, pf("⚠️ Admin only!"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, f"{pf('💰 Enter: user_id amount')}\n{pf('Example:')} `123456 10`", parse_mode='HTML')
    bot.register_next_step_handler(msg, process_add_credits)

def process_add_credits(message):
    if not is_admin(message.from_user.id):
        return
    try:
        parts = message.text.split()
        user_id = int(parts[0])
        amount = int(parts[1])
        add_credits(user_id, amount)
        bot.reply_to(message, f"{pf('✅ Added')} {amount} {pf('credits to')} <code>{user_id}</code>", parse_mode='HTML')
        bot.send_message(user_id, f"{pf('💰 +{} credits added!').format(amount)}\n{pf('Current balance:')} {get_credits(user_id)}", parse_mode='HTML')
    except:
        bot.reply_to(message, f"{pf('❌ Invalid format! Use: user_id amount')}", parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_add_admin")
def admin_add_admin(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, pf("⚠️ Admin only!"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, pf("👑 Enter user ID to add as admin:"), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_add_admin)

def process_add_admin(message):
    if not is_admin(message.from_user.id):
        return
    try:
        user_id = int(message.text.strip())
        if user_id in admin_ids:
            bot.reply_to(message, f"{pf('⚠️')} <code>{user_id}</code> {pf('is already admin!')}", parse_mode='HTML')
            return
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        c.execute('INSERT INTO admins (user_id) VALUES (?)', (user_id,))
        conn.commit()
        conn.close()
        load_admins()
        bot.reply_to(message, f"{pf('✅')} <code>{user_id}</code> {pf('added as admin!')}", parse_mode='HTML')
        bot.send_message(user_id, pf("👑 You have been added as admin!"), parse_mode='HTML')
    except:
        bot.reply_to(message, pf("❌ Invalid user ID!"), parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_broadcast")
def admin_broadcast(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, pf("⚠️ Admin only!"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, pf("📢 Send broadcast message:"), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_broadcast)

def process_broadcast(message):
    if not is_admin(message.from_user.id):
        return
    msg = bot.reply_to(message, pf("📢 Broadcasting..."))
    users = get_all_users()
    sent = 0
    failed = 0
    for user_id in users:
        try:
            bot.send_message(user_id, f"{pf('📢 Broadcast:')}\n\n{message.text}", parse_mode='HTML')
            sent += 1
        except:
            failed += 1
        time.sleep(0.05)
    bot.edit_message_text(
        f"{pf('✅ Broadcast done!')}\n{pf('📤 Sent:')} {sent}\n{pf('❌ Failed:')} {failed}",
        message.chat.id,
        msg.message_id,
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda c: c.data == "admin_stats")
def admin_stats(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, pf("⚠️ Admin only!"), show_alert=True)
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
{pf('📊 System Stats')}
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
{pf('👥 Total Users:')} {total_users}
{pf('📁 Total Files:')} {total_files}
{pf('✅ Approved:')} {approved_files}
{pf('👑 Admins:')} {total_admins}
{pf('💰 Total Credits:')} {total_credits}
◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈
"""
    bot.send_message(call.message.chat.id, text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_ban")
def admin_ban(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, pf("⚠️ Admin only!"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, pf("🚫 Enter user ID to ban:"), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_ban)

def process_ban(message):
    if not is_admin(message.from_user.id):
        return
    try:
        user_id = int(message.text.strip())
        if user_id == OWNER_ID:
            bot.reply_to(message, pf("❌ Cannot ban owner!"), parse_mode='HTML')
            return
        if is_banned(user_id):
            bot.reply_to(message, f"{pf('⚠️')} <code>{user_id}</code> {pf('is already banned!')}", parse_mode='HTML')
            return
        ban_user(user_id)
        bot.reply_to(message, f"{pf('🚫 User')} <code>{user_id}</code> {pf('banned!')}", parse_mode='HTML')
        try:
            bot.send_message(user_id, pf("🚫 You have been banned!"), parse_mode='HTML')
        except:
            pass
    except:
        bot.reply_to(message, pf("❌ Invalid user ID!"), parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_unban")
def admin_unban(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, pf("⚠️ Admin only!"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    msg = bot.send_message(call.message.chat.id, pf("✅ Enter user ID to unban:"), parse_mode='HTML')
    bot.register_next_step_handler(msg, process_unban)

def process_unban(message):
    if not is_admin(message.from_user.id):
        return
    try:
        user_id = int(message.text.strip())
        if not is_banned(user_id):
            bot.reply_to(message, f"{pf('⚠️')} <code>{user_id}</code> {pf('is not banned!')}", parse_mode='HTML')
            return
        unban_user(user_id)
        bot.reply_to(message, f"{pf('✅ User')} <code>{user_id}</code> {pf('unbanned!')}", parse_mode='HTML')
        try:
            bot.send_message(user_id, pf("✅ You have been unbanned!"), parse_mode='HTML')
        except:
            pass
    except:
        bot.reply_to(message, pf("❌ Invalid user ID!"), parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_banned_list")
def admin_banned_list(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, pf("⚠️ Admin only!"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT user_id, username FROM users WHERE is_banned = 1')
    banned = c.fetchall()
    conn.close()
    
    if not banned:
        bot.send_message(call.message.chat.id, pf("📭 No banned users."), parse_mode='HTML')
    else:
        text = f"{pf('🚫 Banned Users:')}\n◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈\n"
        for user_id, username in banned:
            uname = f"@{username}" if username else "N/A"
            text += f"• <code>{user_id}</code> ({uname})\n"
        bot.send_message(call.message.chat.id, text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_users_list")
def admin_users_list(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, pf("⚠️ Admin only!"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT user_id, username, credits FROM users ORDER BY user_id')
    users = c.fetchall()
    conn.close()
    
    if not users:
        bot.send_message(call.message.chat.id, pf("📭 No users found."), parse_mode='HTML')
        return
    
    text = f"{pf('👥 Users List:')}\n◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈\n"
    for user_id, username, credits in users[:20]:
        uname = f"@{username}" if username else "N/A"
        text += f"• <code>{user_id}</code> | {uname} | 💰{credits}\n"
    
    if len(users) > 20:
        text += f"\n... and {len(users)-20} more users"
    
    bot.send_message(call.message.chat.id, text, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data == "admin_all_files")
def admin_all_files(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, pf("⚠️ Admin only!"), show_alert=True)
        return
    bot.answer_callback_query(call.id)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT user_id, file_name, approved FROM user_files ORDER BY user_id')
    files = c.fetchall()
    conn.close()
    
    if not files:
        bot.send_message(call.message.chat.id, pf("📭 No files found."), parse_mode='HTML')
        return
    
    text = f"{pf('📁 All Files:')}\n◈◆◈◆◈◆◈◆◈◆◈◆◈◆◈\n"
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
║   ☠️ 𝑺𝑼𝑵𝑹𝑨𝑲𝑼 — 𝑷𝑹𝑬𝑴𝑰𝑼𝑴 𝑭𝑰𝑳𝑬 𝑹𝑼𝑵𝑵𝑬𝑹 𝑩𝑶𝑻              ║
║   ✦ Upload .py files                                        ║
║   ✦ Auto input detection                                    ║
║   ✦ View Logs                                               ║
║   ✦ Credit System (10 free)                                 ║
║   ✦ 1 Credit = 7 Hours Run                                  ║
║   ✦ Daily Bonus (+2 credits/24h)                            ║
║   ✦ Refer & Earn (+2 credits/ref)                           ║
║   ✦ Admin Panel                                             ║
║   ✦ Premium Font (𝐀ɴɪsʜ style)                              ║
║   ♛ @SunrakuV2 | ID: 8641613327                            ║
║   ✦ @Anishpy | @VOUCH_R                                    ║
╚═══════════════════════════════════════════════════════════════╝
""")
print(f"✅ Bot running...")
print(f"👑 Owner ID: {OWNER_ID}")

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"⚠️ Polling error: {e}")
        time.sleep(5)
