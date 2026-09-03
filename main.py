#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☠️ 𝑺𝑼𝑵𝑹𝑨𝑲𝑼 — 𝑨𝑫𝑽𝑨𝑵𝑪𝑬𝑫 𝑭𝑰𝑳𝑬 𝑹𝑼𝑵𝑵𝑬𝑹 𝑩𝑶𝑻 ☠️
"""

import os
import sys
import time
import random
import json
import re
import select
import requests
import threading
import subprocess
import shutil
import sqlite3
from datetime import datetime, timedelta
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# ============================================================
# ENVIRONMENT VARIABLE
# ============================================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ BOT_TOKEN environment variable not set!")
    sys.exit()

bot = TeleBot(BOT_TOKEN, parse_mode='HTML')
OWNER_CHAT_ID = 8641613327

# ============================================================
# PREMIUM FONT (𝐀ɴɪsʜ style)
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
BTN_UPLOAD = "📤 Upload File"
BTN_RUN = "▶️ Run File"
BTN_STOP = "⏹ Stop File"
BTN_LOGS = "📜 View Logs"
BTN_STATUS = "📊 Live Status"
BTN_SPEED = "⚡ Speed"
BTN_PIP = "📦 Install Pip"
BTN_FILES = "📂 My Files"
BTN_INPUT = "💬 Send Input"
BTN_DEV = "👑 Dev"
BTN_CREDITS = "💰 Credits"
BTN_BONUS = "🎁 Daily Bonus"
BTN_REFER = "🤝 Refer & Earn"
BTN_PROFILE = "👤 Profile"
BTN_ADMIN = "👑 Admin Panel"
BTN_CONTACT = "📞 Contact"

# ============================================================
# GLOBALS
# ============================================================
user_sessions = {}
lock = threading.Lock()
# Always use absolute paths. If cwd is changed to UPLOAD_DIR while
# starting a file, a relative "uploads/file.py" becomes
# "/app/uploads/uploads/file.py".
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE_PATH = os.path.join(DATA_DIR, 'bot.db')
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

admin_ids = {OWNER_CHAT_ID}

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
    c.execute('INSERT OR IGNORE INTO admins (user_id) VALUES (?)', (OWNER_CHAT_ID,))
    conn.commit()
    conn.close()

init_db()

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

def get_all_users():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT user_id FROM users')
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

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
# USER SESSION MANAGER
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
        self.exit_code = None
        self.last_run_error = ""
        self.speed = 0
        self.total_checks = 0
        self.installed_packages = []
        self.awaiting_input = False
        self.input_prompt = ""
        self.files = []
        self.lock = threading.Lock()
        
    def add_log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {msg}")
        if len(self.logs) > 200:
            self.logs.pop(0)
            
    def get_logs(self, lines=25):
        return "\n".join(self.logs[-lines:]) if self.logs else "No logs yet."
        
    def get_runtime(self):
        if self.start_time:
            end_time = self.end_time or datetime.now()
            diff = end_time - self.start_time
            return str(diff).split('.')[0]
        return "N/A"
        
    def get_speed(self):
        if self.start_time:
            end_time = self.end_time or datetime.now()
            runtime_seconds = max((end_time - self.start_time).total_seconds(), 1)
            speed = int((self.total_checks / runtime_seconds) * 60)
            self.speed = speed
            return speed
        return self.speed or 0

# ============================================================
# ANSI CLEANER + INPUT DETECTION
# ============================================================
ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
INPUT_PROMPT_RE = re.compile(
    r"(chat\s*id|user\s*name|username|password|token|email|phone|"
    r"number|choice|select|option|proxy|path|file|url|key|code|"
    r"confirm|yes/no|enter|input|➜|:\s*$)",
    re.IGNORECASE
)

def clean_console_prompt(text):
    text = ANSI_ESCAPE_RE.sub("", text)
    text = text.replace("\x00", "").strip()
    return text[-700:] if len(text) > 700 else text

def looks_like_input_prompt(text):
    return bool(text and INPUT_PROMPT_RE.search(text))

def ask_user_for_process_input(session, prompt):
    prompt = clean_console_prompt(prompt)
    if not prompt or session.awaiting_input:
        return
        
    session.awaiting_input = True
    session.input_prompt = prompt
    session.add_log(f"⏳ Waiting for input: {prompt[:50]}...")
    
    try:
        full_log = session.get_logs(30)
        if full_log and full_log != "No logs yet.":
            log_chunks = [full_log[i:i+3500] for i in range(0, len(full_log), 3500)]
            for chunk_number, chunk in enumerate(log_chunks, start=1):
                header = "📜 FULL FILE LOG"
                if len(log_chunks) > 1:
                    header += f" ({chunk_number}/{len(log_chunks)})"
                bot.send_message(session.chat_id, f"{header}\n\n<code>{chunk}</code>", parse_mode='HTML')
        
        prompt_message = bot.send_message(
            session.chat_id,
            f"📥 <b>Input Required!</b>\n\n"
            f"Your file needs input:\n"
            f"<code>{prompt}</code>\n\n"
            f"💬 Reply with the value.\n"
            f"I will send it to the running file automatically.",
            parse_mode='HTML'
        )
        bot.register_next_step_handler(prompt_message, send_process_input)
    except Exception as e:
        session.awaiting_input = False
        session.add_log(f"❌ Could not request input: {e}")

# ============================================================
# FILE MANAGEMENT
# ============================================================
def add_file_to_session(session, file_path, file_name, approved=False):
    session.files = [
        entry for entry in session.files
        if entry.get("path") != file_path
    ]
    session.files.append({
        "path": file_path,
        "name": file_name,
        "approved": approved
    })

def discover_user_files(session):
    try:
        for file_name in os.listdir(UPLOAD_DIR):
            if not file_name.endswith(".py"):
                continue
            if not file_name.startswith(f"{session.chat_id}_"):
                continue
            file_path = os.path.join(UPLOAD_DIR, file_name)
            if not os.path.isfile(file_path):
                continue
            if not any(entry.get("path") == file_path for entry in session.files):
                add_file_to_session(session, file_path, file_name, approved=False)
    except OSError:
        pass

def get_file_entry(session, index):
    if index < 0 or index >= len(session.files):
        return None
    entry = session.files[index]
    if not os.path.exists(entry.get("path", "")):
        return None
    return entry

def file_manager_markup(session):
    markup = InlineKeyboardMarkup(row_width=2)
    for index, entry in enumerate(session.files):
        if not os.path.exists(entry.get("path", "")):
            continue
        selected = "⭐ " if entry.get("path") == session.file_path else ""
        approved = "✅" if entry.get("approved") else "⏳"
        label = f"{approved} {selected}{index + 1}. {entry.get('name', 'file')}"
        markup.add(
            InlineKeyboardButton(
                label[:60],
                callback_data=f"select_file_{session.chat_id}_{index}"
            ),
            InlineKeyboardButton(
                "🗑️",
                callback_data=f"delete_file_{session.chat_id}_{index}"
            )
        )
    return markup

def file_manager_text(session):
    existing = [
        entry for entry in session.files
        if os.path.exists(entry.get("path", ""))
    ]
    if not existing:
        return (
            "📂 <b>MY FILES</b>\n\n"
            "No uploaded files found.\n"
            "Use UPLOAD FILE to add one."
        )
    lines = ["📂 <b>MY FILES</b>", "", "Tap a file button to select it:"]
    for index, entry in enumerate(session.files):
        if not os.path.exists(entry.get("path", "")):
            continue
        selected = " ⭐ SELECTED" if entry.get("path") == session.file_path else ""
        status = "✅ APPROVED" if entry.get("approved") else "⏳ PENDING"
        lines.append(f"{index + 1}. {entry.get('name', 'file')} — {status}{selected}")
    lines.append("")
    lines.append("Selected file can be run with RUN FILE.")
    return "\n".join(lines)

# ============================================================
# APPROVAL SYSTEM
# ============================================================
def send_approval_request(user_chat_id, file_name, file_path):
    msg = f"""
📩 <b>NEW FILE UPLOADED - APPROVAL NEEDED</b>
━━━━━━━━━━━━━━━━━━━━━
👤 <b>User ID:</b> <code>{user_chat_id}</code>
📁 <b>File:</b> <code>{file_name}</code>
📂 <b>Path:</b> <code>{file_path}</code>
━━━━━━━━━━━━━━━━━━━━━
Click Approve to allow user to run this file.
"""
    markup = InlineKeyboardMarkup(row_width=2)
    btn_approve = InlineKeyboardButton(
        text="✅ APPROVE",
        callback_data=f"approve_{user_chat_id}_{file_path}"
    )
    btn_reject = InlineKeyboardButton(
        text="❌ REJECT",
        callback_data=f"reject_{user_chat_id}"
    )
    markup.add(btn_approve, btn_reject)
    try:
        for admin_id in admin_ids:
            bot.send_message(admin_id, msg, reply_markup=markup, parse_mode='HTML')
        return True
    except Exception as e:
        print(f"Approval send error: {e}")
        return False

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_"))
def approve_file(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
        return
    
    data = call.data.split("_")
    user_chat_id = int(data[1])
    file_path = "_".join(data[2:])
    
    with lock:
        if user_chat_id not in user_sessions:
            bot.answer_callback_query(call.id, "❌ User session not found!")
            return
        session = user_sessions[user_chat_id]
        session.is_approved = True
        for entry in session.files:
            if entry.get("path") == file_path:
                entry["approved"] = True
        session.add_log("✅ File approved by owner")
    
    bot.edit_message_text(
        f"✅ <b>File Approved!</b>\n👤 User: <code>{user_chat_id}</code>\n📁 File: <code>{os.path.basename(file_path)}</code>\n\nUser can now run the file.",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='HTML'
    )
    
    try:
        bot.send_message(
            user_chat_id,
            f"✅ <b>Your file has been approved!</b>\n\n<code>{os.path.basename(file_path)}</code>\nClick <b>RUN FILE</b> to start.",
            parse_mode='HTML'
        )
    except:
        pass
    
    bot.answer_callback_query(call.id, "✅ Approved!")

@bot.callback_query_handler(func=lambda call: call.data.startswith("reject_"))
def reject_file(call):
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "⚠️ Admin only!", show_alert=True)
        return
    
    user_chat_id = int(call.data.split("_")[1])
    
    with lock:
        if user_chat_id in user_sessions:
            session = user_sessions[user_chat_id]
            session.is_approved = False
            for entry in session.files:
                if entry.get("path") == session.file_path:
                    entry["approved"] = False
            session.add_log("❌ File rejected by owner")
    
    bot.edit_message_text(
        f"❌ <b>File Rejected!</b>\n👤 User: <code>{user_chat_id}</code>\n\nFile has been rejected by owner.",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='HTML'
    )
    
    try:
        bot.send_message(
            user_chat_id,
            "❌ <b>Your file has been rejected by the owner.</b>\n\nPlease contact @SunrakuV2 for approval.",
            parse_mode='HTML'
        )
    except:
        pass
    
    bot.answer_callback_query(call.id, "❌ Rejected!")

# ============================================================
# MAIN MENU
# ============================================================
def get_main_menu(user_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if is_admin(user_id):
        buttons = [
            BTN_UPLOAD, BTN_RUN, BTN_STOP, BTN_LOGS,
            BTN_STATUS, BTN_SPEED, BTN_PIP, BTN_FILES,
            BTN_INPUT, BTN_CREDITS, BTN_BONUS, BTN_REFER,
            BTN_PROFILE, BTN_ADMIN, BTN_CONTACT, BTN_DEV
        ]
    else:
        buttons = [
            BTN_UPLOAD, BTN_RUN, BTN_STOP, BTN_LOGS,
            BTN_STATUS, BTN_SPEED, BTN_PIP, BTN_FILES,
            BTN_INPUT, BTN_CREDITS, BTN_BONUS, BTN_REFER,
            BTN_PROFILE, BTN_CONTACT, BTN_DEV
        ]
    
    for i in range(0, len(buttons), 2):
        row = buttons[i:i+2]
        markup.add(*[KeyboardButton(btn) for btn in row])
    
    return markup

# ============================================================
# START COMMAND
# ============================================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    add_user(chat_id, message.from_user.username)
    
    with lock:
        if chat_id not in user_sessions:
            user_sessions[chat_id] = UserSession(chat_id)
    
    if len(message.text.split()) > 1:
        ref_code = message.text.split()[1]
        if ref_code.startswith('SUNRAKU'):
            try:
                referrer_id = int(ref_code.replace('SUNRAKU', '')[:-3])
                if referrer_id != chat_id and add_referral(referrer_id, chat_id):
                    if credit_referral(referrer_id):
                        bot.send_message(referrer_id, pf("🎉 You got +2 credits!"), parse_mode='HTML')
                    bot.reply_to(message, pf("🎉 You were referred! Referrer got +2 credits!"), parse_mode='HTML')
            except:
                pass
    
    credits = get_credits(chat_id)
    admin_status = pf("👑 Admin") if is_admin(chat_id) else pf("👤 User")
    
    welcome_msg = f"""
☠️ <b>SUNRAKU — PREMIUM FILE RUNNER</b> ☠️
━━━━━━━━━━━━━━━━━━━━━
👤 <b>User:</b> {message.from_user.first_name}
🎫 <b>Role:</b> {admin_status}
💰 <b>Credits:</b> {credits}
━━━━━━━━━━━━━━━━━━━━━
📤 Upload your .py file (1 credit/7h)
▶️ Run approved file
📜 View live logs
📊 Live Status
⚡ Speed
📦 Install pip packages
📂 Manage your files
💬 Send input to running file
🎁 Daily Bonus: +2 credits (24h)
🤝 Refer & Earn: +2 credits/ref
━━━━━━━━━━━━━━━━━━━━━
👑 @SunrakuV2 | 📢 @Anishpy | @VOUCH_R
"""
    bot.reply_to(message, welcome_msg, reply_markup=get_main_menu(chat_id), parse_mode='HTML')

# ============================================================
# UPLOAD FILE
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_UPLOAD)
def upload_file(message):
    msg1 = bot.reply_to(
        message,
        "📤 <b>Send your .py file now.</b>\n\n"
        "No token or Chat ID is needed here. "
        "After approval, the file will ask for each input in Telegram.",
        parse_mode='HTML'
    )
    bot.register_next_step_handler(msg1, handle_file_upload)

# ============================================================
# MY FILES
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_FILES)
def show_my_files(message):
    chat_id = message.chat.id
    with lock:
        if chat_id not in user_sessions:
            user_sessions[chat_id] = UserSession(chat_id)
        session = user_sessions[chat_id]
    
    discover_user_files(session)
    bot.reply_to(
        message,
        file_manager_text(session),
        reply_markup=file_manager_markup(session),
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("select_file_"))
def select_user_file(call):
    try:
        parts = call.data.split("_")
        requested_chat_id = int(parts[-2])
        file_index = int(parts[-1])
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "❌ Invalid file selection.")
        return
    
    if call.message.chat.id != requested_chat_id:
        bot.answer_callback_query(call.id, "❌ This file menu is not yours.")
        return
    
    session = user_sessions.get(requested_chat_id)
    if not session:
        bot.answer_callback_query(call.id, "❌ Session not found.")
        return
    
    if session.is_running:
        bot.answer_callback_query(call.id, "⏹ Stop the running file first.")
        return
    
    entry = get_file_entry(session, file_index)
    if not entry:
        bot.answer_callback_query(call.id, "❌ File no longer exists.")
        return
    
    session.file_path = entry["path"]
    session.is_approved = bool(entry.get("approved"))
    session.start_time = None
    session.end_time = None
    session.total_checks = 0
    session.speed = 0
    session.add_log(f"📂 Selected file: {entry.get('name', 'file')}")
    
    bot.answer_callback_query(call.id, "✅ File selected.")
    bot.edit_message_text(
        file_manager_text(session),
        call.message.chat.id,
        call.message.message_id,
        reply_markup=file_manager_markup(session),
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("delete_file_"))
def delete_user_file(call):
    try:
        parts = call.data.split("_")
        requested_chat_id = int(parts[-2])
        file_index = int(parts[-1])
    except (ValueError, IndexError):
        bot.answer_callback_query(call.id, "❌ Invalid file selection.")
        return
    
    if call.message.chat.id != requested_chat_id:
        bot.answer_callback_query(call.id, "❌ This file menu is not yours.")
        return
    
    session = user_sessions.get(requested_chat_id)
    if not session:
        bot.answer_callback_query(call.id, "❌ Session not found.")
        return
    
    entry = get_file_entry(session, file_index)
    if not entry:
        bot.answer_callback_query(call.id, "❌ File no longer exists.")
        return
    
    if session.is_running and entry["path"] == session.file_path:
        bot.answer_callback_query(call.id, "⏹ Stop this file before deleting it.")
        return
    
    file_path = os.path.abspath(entry["path"])
    upload_root = os.path.abspath(UPLOAD_DIR) + os.sep
    if not file_path.startswith(upload_root):
        bot.answer_callback_query(call.id, "❌ Unsafe file path.")
        return
    
    try:
        os.remove(file_path)
        deleted_name = entry.get("name", "file")
        was_selected = session.file_path == entry["path"]
        session.files.pop(file_index)
        
        if was_selected:
            session.file_path = None
            session.is_approved = False
            session.start_time = None
            session.end_time = None
            session.total_checks = 0
            session.speed = 0
            for fallback in reversed(session.files):
                if os.path.exists(fallback.get("path", "")):
                    session.file_path = fallback["path"]
                    session.is_approved = bool(fallback.get("approved"))
                    break
        
        session.add_log(f"🗑️ Deleted file: {deleted_name}")
        bot.answer_callback_query(call.id, "🗑️ File deleted.")
        bot.edit_message_text(
            file_manager_text(session),
            call.message.chat.id,
            call.message.message_id,
            reply_markup=file_manager_markup(session),
            parse_mode='HTML'
        )
    except OSError as e:
        bot.answer_callback_query(call.id, f"❌ Delete failed: {e}")

# ============================================================
# INSTALL PIP
# ============================================================
PACKAGE_SPEC_RE = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._-]*(?:\[[A-Za-z0-9_,.-]+\])?"
    r"(?:(?:==|!=|~=|>=|<=|>|<)[A-Za-z0-9.*+!_-]+)?$"
)

@bot.message_handler(commands=['pip'])
@bot.message_handler(func=lambda msg: msg.text == BTN_PIP)
def install_pip_button(message):
    chat_id = message.chat.id
    with lock:
        if chat_id not in user_sessions:
            user_sessions[chat_id] = UserSession(chat_id)
        session = user_sessions[chat_id]
    
    if not session.file_path or not os.path.exists(session.file_path):
        bot.reply_to(
            message,
            "📦 <b>Pehle apni .py file upload ya select karo.</b>\n\n"
            "Uske baad is button se us file ki requirements install kar sakte ho.",
            parse_mode='HTML'
        )
        return
    
    prompt = bot.reply_to(
        message,
        f"📦 <b>Packages for:</b> <code>{os.path.basename(session.file_path)}</code>\n\n"
        "Package names space se separate karke bhejo.\n\n"
        "Example:\n<code>requests pyTelegramBotAPI</code>\n"
        "or:\n<code>requests==2.32.3</code>\n\n"
        "Type /cancel to cancel.",
        parse_mode='HTML'
    )
    bot.register_next_step_handler(prompt, install_pip_packages)

def install_pip_packages(message):
    chat_id = message.chat.id
    with lock:
        if chat_id not in user_sessions:
            user_sessions[chat_id] = UserSession(chat_id)
        session = user_sessions[chat_id]
    
    if not session.file_path or not os.path.exists(session.file_path):
        bot.reply_to(message, "📦 <b>File not found. Upload/select your file first.</b>", parse_mode='HTML')
        return
    
    package_text = (message.text or "").strip()
    if package_text.lower() == "/cancel":
        bot.reply_to(message, "❎ <b>Pip installation cancelled.</b>", parse_mode='HTML')
        return
    
    packages = package_text.split()
    if not packages:
        bot.reply_to(message, "❌ <b>No package name received.</b>", parse_mode='HTML')
        return
    
    if len(packages) > 20 or any(not PACKAGE_SPEC_RE.fullmatch(pkg) for pkg in packages):
        bot.reply_to(
            message,
            "❌ <b>Invalid package list.</b>\n\n"
            "Use normal PyPI names only, for example:\n"
            "<code>requests flask==3.0.3</code>",
            parse_mode='HTML'
        )
        return
    
    package_list = " ".join(packages)
    bot.reply_to(
        message,
        f"⏳ <b>Installing:</b> <code>{package_list}</code>\n\nPlease wait...",
        parse_mode='HTML'
    )
    
    def pip_worker():
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--disable-pip-version-check",
                    *packages
                ],
                capture_output=True,
                text=True,
                timeout=180
            )
            output = (result.stdout or "") + (result.stderr or "")
            output = output.strip() or "No output returned."
            if len(output) > 3500:
                output = output[-3500:]
            
            if result.returncode == 0:
                title = "✅ Pip installation completed."
                session.installed_packages.extend(packages)
                session.add_log(f"📦 Packages installed: {package_list}")
            else:
                title = f"❌ Pip installation failed (exit code {result.returncode})."
                session.add_log(f"❌ Pip installation failed: {package_list}")
            
            bot.send_message(message.chat.id, f"{title}\n\n<code>{output}</code>", parse_mode='HTML')
        except subprocess.TimeoutExpired:
            bot.send_message(message.chat.id, "⏱️ Pip installation timed out after 180 seconds.", parse_mode='HTML')
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Pip error: {e}", parse_mode='HTML')
    
    threading.Thread(target=pip_worker, daemon=True).start()

# ============================================================
# 🔥 FILE UPLOAD HANDLER - FIXED
# ============================================================
@bot.message_handler(content_types=['document'])
def handle_file_upload(message):
    chat_id = message.chat.id
    
    if not message.document:
        bot.reply_to(message, "❌ <b>Please send a .py document file.</b>", parse_mode='HTML')
        return
    
    if not message.document.file_name.endswith('.py'):
        bot.reply_to(message, "❌ <b>Only .py files are allowed!</b>", parse_mode='HTML')
        return
    
    if message.document.file_size > 5 * 1024 * 1024:
        bot.reply_to(message, "❌ <b>File too large! Max 5MB.</b>", parse_mode='HTML')
        return
    
    with lock:
        if chat_id not in user_sessions:
            user_sessions[chat_id] = UserSession(chat_id)
        session = user_sessions[chat_id]
        session.is_approved = False
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Keep the uploaded file inside UPLOAD_DIR and use an absolute path.
        original_name = os.path.basename(message.document.file_name)
        safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", original_name)
        if not safe_name or safe_name == "." or safe_name == "..":
            bot.reply_to(message, "❌ <b>Invalid file name.</b>", parse_mode='HTML')
            return
        file_path = os.path.join(UPLOAD_DIR, f"{chat_id}_{safe_name}")
        
        with open(file_path, 'wb') as f:
            f.write(downloaded_file)
        
        # Store the same absolute path that will be passed to Popen.
        session.file_path = file_path
        add_file_to_session(
            session,
            file_path,
            message.document.file_name,
            approved=False
        )
        session.add_log(f"📤 File uploaded: {message.document.file_name}")
        
        success = send_approval_request(
            chat_id, 
            message.document.file_name, 
            file_path
        )
        
        if success:
            bot.reply_to(
                message, 
                f"✅ <b>File uploaded successfully!</b>\n<code>{message.document.file_name}</code>\n\n⏳ <b>Waiting for owner approval...</b>\nYou will be notified when approved.",
                parse_mode='HTML'
            )
        else:
            bot.reply_to(
                message, 
                f"⚠️ <b>File uploaded but approval failed!</b>\nPlease contact @SunrakuV2 manually.",
                parse_mode='HTML'
            )
    except Exception as e:
        bot.reply_to(message, f"❌ <b>Upload failed:</b> {str(e)}", parse_mode='HTML')

# ============================================================
# 🔥 RUN FILE - FIXED
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_RUN)
def run_file(message):
    chat_id = message.chat.id
    
    with lock:
        if chat_id not in user_sessions:
            user_sessions[chat_id] = UserSession(chat_id)
        session = user_sessions[chat_id]
    
    if not session.is_approved:
        bot.reply_to(message, "❌ <b>File not approved!</b>\n\nUpload a file and wait for owner approval.", parse_mode='HTML')
        return
    
    if session.is_running:
        bot.reply_to(message, "⚠️ <b>File is already running!</b>\nClick <b>STOP FILE</b> first.", parse_mode='HTML')
        return
    
    # Normalize once more in case this session was created before the
    # absolute-path fix was deployed.
    file_path = os.path.abspath(session.file_path) if session.file_path else None
    session.file_path = file_path
    
    if not file_path or not os.path.exists(file_path):
        session.add_log("❌ No file found! Upload a .py file.")
        bot.reply_to(message, "❌ <b>No file found!</b>\n\nUpload a .py file first.", parse_mode='HTML')
        return
    
    file_name = os.path.basename(file_path)
    
    # Check credits
    if not can_run_free(chat_id, file_name):
        credits = get_credits(chat_id)
        if credits <= 0:
            bot.reply_to(message, "❌ <b>Insufficient credits!</b>\n💰 Use Daily Bonus or Refer & Earn", parse_mode='HTML')
            return
        new_credits = deduct_credit(chat_id)
    else:
        new_credits = get_credits(chat_id)
    
    try:
        # Reset logs for new run
        session.logs = []
        session.total_checks = 0
        session.start_time = datetime.now()
        session.end_time = None
        session.exit_code = None
        session.last_run_error = ""
        
        # Use the same launch model as the old working bot: pass the
        # absolute script path and inherit the bot's current directory.
        # This matches the old working bot exactly. Do not set
        # cwd=UPLOAD_DIR; that caused the /uploads/uploads/<file> problem.
        session.process = subprocess.Popen(
            [sys.executable, "-u", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1,
            env={**os.environ, "PYTHONUNBUFFERED": "1"}
        )
        session.is_running = True
        session.speed = 0
        session.add_log(f"▶️ File started: {file_name}")
        session.add_log(f"📂 Running from: {os.getcwd()}")
        
        # Start 7-hour session
        start_run_session(chat_id, file_name)
        
        def read_logs():
            # Keep a local reference. session.process can change after a
            # stop/restart; the reader must never monitor a different run.
            process = session.process
            stdout = process.stdout
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
                        prompt = clean_console_prompt(partial_output)
                        if (
                            prompt
                            and not prompt_sent
                            and process.poll() is None
                            and looks_like_input_prompt(prompt)
                        ):
                            ask_user_for_process_input(session, prompt)
                            partial_output = ""
                            prompt_sent = True
                    if process.poll() is not None:
                        break
                except Exception as e:
                    session.last_run_error = str(e)
                    session.add_log(f"⚠️ Log reader error: {e}")
                    break
            
            remaining = clean_console_prompt(partial_output)
            if remaining and not session.awaiting_input:
                session.add_log(remaining)
            
            # Wait for the real child exit instead of declaring it stopped
            # while it is still shutting down.
            return_code = process.poll()
            if return_code is None:
                try:
                    return_code = process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    session.add_log(
                        "⚠️ Output reader ended, but the file is still running."
                    )
                    return

            if session.process is not process:
                return

            session.exit_code = return_code
            session.awaiting_input = False
            session.input_prompt = ""
            session.is_running = False
            session.end_time = datetime.now()
            
            if return_code == 0:
                session.add_log("✅ File finished successfully")
            elif return_code is not None:
                session.add_log(f"⚠️ File exited with code {return_code}")
            
            end_run_session(chat_id, file_name)
        
        threading.Thread(target=read_logs, daemon=True).start()
        
        bot.reply_to(
            message,
            f"✅ <b>File started!</b>\n<code>{file_name}</code>\n💰 <b>Credits left:</b> {new_credits}\n\n📜 Click <b>VIEW LOGS</b> to see output.\n📊 Click <b>LIVE STATUS</b> to check progress.",
            parse_mode='HTML'
        )
        
    except Exception as e:
        session.is_running = False
        session.add_log(f"❌ Run error: {str(e)}")
        bot.reply_to(message, f"❌ <b>Error:</b> {str(e)}", parse_mode='HTML')

# ============================================================
# STOP FILE
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_STOP)
def stop_file(message):
    chat_id = message.chat.id
    
    with lock:
        if chat_id not in user_sessions:
            bot.reply_to(message, "❌ No session found!", parse_mode='HTML')
            return
        session = user_sessions[chat_id]
    
    if not session.is_running:
        bot.reply_to(message, "⚠️ <b>No file is running!</b>", parse_mode='HTML')
        return
    
    try:
        session.is_running = False
        session.process.terminate()
        time.sleep(1)
        if session.process.poll() is None:
            session.process.kill()
        session.end_time = datetime.now()
        file_name = os.path.basename(session.file_path) if session.file_path else "unknown"
        session.add_log(f"⏹ File stopped by user")
        end_run_session(chat_id, file_name)
        bot.reply_to(message, "⏹ <b>File stopped successfully!</b>", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ <b>Stop error:</b> {str(e)}", parse_mode='HTML')

# ============================================================
# VIEW LOGS
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_LOGS)
def view_logs(message):
    chat_id = message.chat.id
    
    with lock:
        if chat_id not in user_sessions:
            bot.reply_to(message, "❌ No session found!", parse_mode='HTML')
            return
        session = user_sessions[chat_id]
    
    logs = session.get_logs(30)
    
    if not logs or logs == "No logs yet.":
        if session.is_running:
            bot.reply_to(
                message,
                "⏳ <b>File is running but no logs yet...</b>\n\nCheck back in a moment.",
                parse_mode='HTML'
            )
        else:
            bot.reply_to(
                message,
                "📭 <b>No logs yet.</b>\n\n▶️ Run a file to see output.",
                parse_mode='HTML'
            )
        return
    
    if len(logs) > 4000:
        chunks = [logs[i:i+4000] for i in range(0, len(logs), 4000)]
        bot.reply_to(
            message,
            f"📜 <b>Recent Logs (Part 1/{len(chunks)}):</b>\n<code>{chunks[0]}</code>",
            parse_mode='HTML'
        )
        for i, chunk in enumerate(chunks[1:4], 2):
            bot.send_message(
                chat_id,
                f"📜 <b>Logs (Part {i}/{len(chunks)}):</b>\n<code>{chunk}</code>",
                parse_mode='HTML'
            )
    else:
        bot.reply_to(
            message,
            f"📜 <b>Recent Logs:</b>\n<code>{logs}</code>",
            parse_mode='HTML'
        )

# ============================================================
# LIVE STATUS
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_STATUS)
def show_live_status(message):
    chat_id = message.chat.id
    
    with lock:
        if chat_id not in user_sessions:
            bot.reply_to(message, "❌ <b>No session found!</b>\n\nPlease /start first.", parse_mode='HTML')
            return
        session = user_sessions[chat_id]
    
    if session.process and session.process.poll() is not None and session.is_running:
        session.exit_code = session.process.poll()
        session.is_running = False
        session.end_time = session.end_time or datetime.now()
    
    status_icon = "🟢" if session.is_running else "🔴"
    status_text = "RUNNING" if session.is_running else "STOPPED"
    approved_text = "✅ Approved" if session.is_approved else "⏳ Pending Approval"
    file_name = os.path.basename(session.file_path) if session.file_path else "None"
    runtime = session.get_runtime()
    speed = session.get_speed()
    input_state = "⏳ Waiting" if session.awaiting_input else "No"
    exit_text = str(session.exit_code) if session.exit_code is not None else "N/A"
    
    status_msg = f"""
📊 <b>LIVE STATUS</b>
━━━━━━━━━━━━━━━━━━━━━
📁 <b>File:</b> <code>{file_name}</code>
{status_icon} <b>Status:</b> <code>{status_text}</code>
✅ <b>Approval:</b> <code>{approved_text}</code>
⏱ <b>Runtime:</b> <code>{runtime}</code>
📊 <b>Checks:</b> <code>{session.total_checks}</code>
⚡ <b>Speed:</b> <code>{speed}</code> checks/min
💬 <b>Input:</b> <code>{input_state}</code>
↩️ <b>Exit code:</b> <code>{exit_text}</code>
📜 <b>Logs:</b> <code>{len(session.logs)}</code> lines
━━━━━━━━━━━━━━━━━━━━━
👑 @SunrakuV2 | 📢 @Anishpy | @VOUCH_R
"""
    bot.reply_to(message, status_msg, parse_mode='HTML')

# ============================================================
# SPEED
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_SPEED)
def show_speed(message):
    chat_id = message.chat.id
    
    with lock:
        if chat_id not in user_sessions:
            bot.reply_to(message, "❌ <b>No session found!</b>\n\nPlease /start first.", parse_mode='HTML')
            return
        session = user_sessions[chat_id]
    
    if not session.start_time:
        bot.reply_to(
            message,
            "⚠️ <b>No file has been run yet!</b>\n\nStart a file first using <b>RUN FILE</b>.",
            parse_mode='HTML'
        )
        return
    
    if session.process and session.process.poll() is not None and session.is_running:
        session.is_running = False
        session.end_time = session.end_time or datetime.now()
    
    runtime = session.get_runtime()
    speed = session.get_speed()
    run_state = "🟢 Running" if session.is_running else "🔴 Stopped/Finished"
    performance = "🚀 Fast" if speed > 100 else "🐢 Slow" if speed < 30 else "⚡ Average"
    
    speed_msg = f"""
⚡ <b>SPEED REPORT</b>
━━━━━━━━━━━━━━━━━━━━━
📊 <b>State:</b> <code>{run_state}</code>
📊 <b>Total Checks:</b> <code>{session.total_checks}</code>
⏱ <b>Runtime:</b> <code>{runtime}</code>
⚡ <b>Speed:</b> <code>{speed}</code> checks/min
📈 <b>Performance:</b> <code>{performance}</code>
━━━━━━━━━━━━━━━━━━━━━
👑 @SunrakuV2 | 📢 @Anishpy | @VOUCH_R
"""
    bot.reply_to(message, speed_msg, parse_mode='HTML')

# ============================================================
# SEND INPUT
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_INPUT)
@bot.message_handler(commands=['input'])
def request_process_input(message):
    chat_id = message.chat.id
    
    with lock:
        session = user_sessions.get(chat_id)
    
    if not session or not session.process or not session.is_running:
        bot.reply_to(
            message,
            "⚠️ <b>No running file is waiting for input.</b>",
            parse_mode='HTML'
        )
        return
    
    if session.awaiting_input:
        bot.reply_to(
            message,
            "⏳ <b>File is already waiting for input.</b>\nJust reply with the value!",
            parse_mode='HTML'
        )
        return
    
    prompt = bot.reply_to(
        message,
        "💬 <b>Send the next input value for your running file.</b>\n\n"
        "The value will be sent to its input prompt.\n"
        "Type /cancel to cancel.",
        parse_mode='HTML'
    )
    session.awaiting_input = True
    session.input_prompt = "Manual input requested"
    bot.register_next_step_handler(prompt, send_process_input)

def send_process_input(message):
    chat_id = message.chat.id
    
    with lock:
        session = user_sessions.get(chat_id)
    
    if not session or not session.process or not session.is_running:
        bot.reply_to(message, "⚠️ <b>The file is no longer running.</b>", parse_mode='HTML')
        return
    
    value = message.text or ""
    
    if value.strip().lower() == "/cancel":
        session.awaiting_input = False
        bot.reply_to(message, "❎ <b>Input cancelled.</b>", parse_mode='HTML')
        return
    
    try:
        if session.process.stdin is None:
            raise RuntimeError("stdin pipe is not available")
        
        session.process.stdin.write(value + "\n")
        session.process.stdin.flush()
        session.awaiting_input = False
        session.input_prompt = ""
        session.add_log(f"💬 Input sent from Telegram: {value[:40]}")
        
        bot.reply_to(message, f"✅ <b>Input sent to the running file.</b>\n`{value[:100]}`", parse_mode='HTML')
        
        time.sleep(0.5)
        logs = session.get_logs(15)
        if logs and logs != "No logs yet.":
            bot.send_message(
                chat_id,
                f"📜 <b>Updated Logs:</b>\n<code>{logs}</code>",
                parse_mode='HTML'
            )
    except (BrokenPipeError, OSError, ValueError) as e:
        session.awaiting_input = False
        session.input_prompt = ""
        session.is_running = False
        session.end_time = session.end_time or datetime.now()
        session.add_log(f"❌ Input error: {e}")
        bot.reply_to(message, "❌ <b>File closed its input channel or has stopped.</b>", parse_mode='HTML')

# ============================================================
# CREDITS
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_CREDITS)
def credits_cmd(message):
    user_id = message.chat.id
    credits = get_credits(user_id)
    referral_count = get_referral_count(user_id)
    
    text = f"""
💰 <b>Your Credits</b>
━━━━━━━━━━━━━━━━━━━━━
👤 <b>User:</b> {message.from_user.first_name}
💳 <b>Credits:</b> {credits}
🤝 <b>Referrals:</b> {referral_count}
━━━━━━━━━━━━━━━━━━━━━
📌 <b>How to get more:</b>
  ▪ Daily Bonus: +2 credits (24h)
  ▪ Refer & Earn: +2 credits/ref
  ▪ Contact admin for extra
━━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, text, parse_mode='HTML')

# ============================================================
# DAILY BONUS
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_BONUS)
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
                f"🎁 <b>Daily Bonus Claimed!</b>\n✅ <b>+2 credits added!</b>\n💰 <b>Total credits:</b> {new_credits}\n⏳ <b>Next bonus: 24 hours</b>",
                parse_mode='HTML'
            )
        else:
            bot.reply_to(message, "❌ Failed to claim bonus.", parse_mode='HTML')
    else:
        bot.reply_to(message, "⏳ Daily Bonus already claimed!\n🕐 Next claim in: 24 hours", parse_mode='HTML')

# ============================================================
# REFER & EARN
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_REFER)
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
🤝 <b>Refer & Earn Credits!</b>
━━━━━━━━━━━━━━━━━━━━━
📊 <b>Your Referrals:</b> {referral_count}
⏳ <b>Pending:</b> {pending_count}
💰 <b>Per Referral: +2 credits</b>
━━━━━━━━━━━━━━━━━━━━━
🔗 <b>Your Referral Link:</b>
<code>{ref_link}</code>
━━━━━━━━━━━━━━━━━━━━━
📌 <b>How it works:</b>
  1. Share your link with friends
  2. They join using your link
  3. You get +2 credits instantly!
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
@bot.message_handler(func=lambda msg: msg.text == BTN_PROFILE)
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
    
    admin_status = "👑 Admin" if is_admin(user_id) else "👤 User"
    
    text = f"""
👤 <b>Your Profile</b>
━━━━━━━━━━━━━━━━━━━━━
🆔 <b>ID:</b> <code>{user_id}</code>
🎫 <b>Role:</b> {admin_status}
💰 <b>Credits:</b> {credits}
📁 <b>Files:</b> {total_files} (✅ {approved_files} approved)
🤝 <b>Referrals:</b> {referral_count}
━━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, text, parse_mode='HTML')

# ============================================================
# CONTACT
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_CONTACT)
def contact_cmd(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("👑 @SunrakuV2", url="https://t.me/SunrakuV2"),
        InlineKeyboardButton("📢 @Anishpy", url="https://t.me/Anishpy"),
        InlineKeyboardButton("📢 @VOUCH_R", url="https://t.me/VOUCH_R")
    )
    bot.reply_to(
        message,
        "📞 <b>Contact & Support</b>\n━━━━━━━━━━━━━━━━━━━━━\nClick below to connect:",
        reply_markup=markup,
        parse_mode='HTML'
    )

# ============================================================
# DEV
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_DEV)
def dev_cmd(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("👑 @SunrakuV2", url="https://t.me/SunrakuV2"),
        InlineKeyboardButton("📢 @Anishpy", url="https://t.me/Anishpy"),
        InlineKeyboardButton("📢 @VOUCH_R", url="https://t.me/VOUCH_R")
    )
    bot.reply_to(
        message,
        "👑 <b>Developer & Channels</b>\n━━━━━━━━━━━━━━━━━━━━━\nClick below to connect:",
        reply_markup=markup,
        parse_mode='HTML'
    )

# ============================================================
# ADMIN PANEL
# ============================================================
@bot.message_handler(func=lambda msg: msg.text == BTN_ADMIN)
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
    bot.reply_to(message, "👑 <b>Admin Panel</b>", reply_markup=markup, parse_mode='HTML')

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
            bot.send_message(user_id, f"📢 <b>Broadcast:</b>\n\n{message.text}", parse_mode='HTML')
            sent += 1
        except:
            failed += 1
        time.sleep(0.05)
    bot.edit_message_text(
        f"✅ <b>Broadcast done!</b>\n📤 Sent: {sent}\n❌ Failed: {failed}",
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
📊 <b>System Stats</b>
━━━━━━━━━━━━━━━━━━━━━
👥 Total Users: {total_users}
📁 Total Files: {total_files}
✅ Approved: {approved_files}
👑 Admins: {total_admins}
💰 Total Credits: {total_credits}
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
        if user_id == OWNER_CHAT_ID:
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
        text = "🚫 <b>Banned Users:</b>\n━━━━━━━━━━━━━━━━━━━━━\n"
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
    
    text = "👥 <b>Users List:</b>\n━━━━━━━━━━━━━━━━━━━━━\n"
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
    
    text = "📁 <b>All Files:</b>\n━━━━━━━━━━━━━━━━━━━━━\n"
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
║   ☠️ SUNRAKU — ADVANCED FILE RUNNER BOT                      ║
║   ✅ Upload .py files                                        ║
║   ✅ Approval System                                         ║
║   ✅ Run/Stop/Logs/Status/Speed                              ║
║   ✅ LIVE STATUS + SPEED FIXED                               ║
║   ✅ Credit System (10 free)                                 ║
║   ✅ 1 Credit = 7 Hours Run                                  ║
║   ✅ Daily Bonus (+2 credits/24h)                            ║
║   ✅ Refer & Earn (+2 credits/ref)                           ║
║   ✅ Admin Panel (Full Control)                              ║
║   ✅ Premium Font (𝐀ɴɪsʜ style)                              ║
║   👑 @SunrakuV2 | ID: 8641613327                            ║
║   📢 @Anishpy | @VOUCH_R                                    ║
╚═══════════════════════════════════════════════════════════════╝
""")
print(f"✅ Bot is running...")
print(f"👑 Owner ID: {OWNER_CHAT_ID}")
print(f"📢 Channel: @Anishpy | @VOUCH_R")

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"⚠️ Polling error: {e}")
        time.sleep(5)
        continue
