#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☠️ SUNRAKU — FILE RUNNER BOT ☠️
✅ Upload .py files
✅ Auto input detection
✅ View Logs
✅ Credit System (10 credits free)
✅ Approve/Reject by Owner
✅ Run/Stop controls
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
from datetime import datetime
from telebot import TeleBot
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

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
                 (user_id INTEGER PRIMARY KEY, credits INTEGER DEFAULT 10)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_files
                 (user_id INTEGER, file_name TEXT, file_type TEXT, 
                  approved INTEGER DEFAULT 0, uploaded_at TEXT,
                  PRIMARY KEY (user_id, file_name))''')
    c.execute('''CREATE TABLE IF NOT EXISTS pending
                 (pending_id TEXT PRIMARY KEY, user_id INTEGER, 
                  file_name TEXT, file_path TEXT, submitted_at TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ============================================================
# DATA STORES
# ============================================================
user_sessions = {}
bot_scripts = {}
lock = threading.Lock()

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
    return 10  # Default 10 credits

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

def add_user(user_id):
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, credits) VALUES (?, 10)', (user_id,))
    conn.commit()
    conn.close()

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
        
    def add_log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {msg}")
        if len(self.logs) > 200:
            self.logs.pop(0)
            
    def get_logs(self, lines=20):
        return "\n".join(self.logs[-lines:]) if self.logs else "📭 No logs yet."

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
    session.add_log(f"⏳ Waiting for input...")
    
    try:
        logs = session.get_logs(15)
        if logs and logs != "📭 No logs yet.":
            bot.send_message(
                session.chat_id,
                f"📜 **Recent Logs:**\n```\n{logs}\n```",
                parse_mode='HTML'
            )
        
        prompt_msg = bot.send_message(
            session.chat_id,
            f"📥 **Input Required!**\n\n"
            f"Your file needs input:\n"
            f"```\n{prompt}\n```\n\n"
            f"💬 **Reply with the value.**\n"
            f"Type `/cancel` to cancel.",
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
            bot.reply_to(message, f"✅ **Input sent!**\n`{value[:100]}`")
            
            time.sleep(0.3)
            logs = session.get_logs(10)
            if logs and logs != "📭 No logs yet.":
                bot.send_message(
                    chat_id,
                    f"📜 **Updated Logs:**\n```\n{logs}\n```",
                    parse_mode='HTML'
                )
    except Exception as e:
        session.awaiting_input = False
        session.add_log(f"❌ Input error: {e}")
        bot.reply_to(message, f"❌ Error: {e}")

# ============================================================
# MAIN MENU
# ============================================================
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("📤 Upload File")
    btn2 = KeyboardButton("▶️ Run File")
    btn3 = KeyboardButton("⏹ Stop File")
    btn4 = KeyboardButton("📜 View Logs")
    btn5 = KeyboardButton("📊 My Files")
    btn6 = KeyboardButton("💰 Credits")
    btn7 = KeyboardButton("👤 Profile")
    btn8 = KeyboardButton("📞 Contact")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    return markup

# ============================================================
# START
# ============================================================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.chat.id
    add_user(user_id)
    
    with lock:
        if user_id not in user_sessions:
            user_sessions[user_id] = UserSession(user_id)
    
    credits = get_credits(user_id)
    
    welcome = f"""
☠️ <b>SUNRAKU — FILE RUNNER</b> ☠️
━━━━━━━━━━━━━━━━━━━━━
👤 <b>User:</b> {message.from_user.first_name}
💰 <b>Credits:</b> {credits}

📤 Upload .py file (1 credit per run)
▶️ Run approved file
📜 View live logs
━━━━━━━━━━━━━━━━━━━━━
👑 @SunrakuV2 | 📢 @Anishpy
"""
    bot.reply_to(message, welcome, reply_markup=main_menu(), parse_mode='HTML')

# ============================================================
# UPLOAD FILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == "📤 Upload File")
def upload_file_cmd(message):
    bot.reply_to(message, "📤 **Send your .py file**", parse_mode='HTML')
    bot.register_next_step_handler(message, handle_upload)

@bot.message_handler(content_types=['document'])
def handle_upload(message):
    user_id = message.chat.id
    
    if not message.document or not message.document.file_name.endswith('.py'):
        bot.reply_to(message, "❌ **Only .py files allowed!**", parse_mode='HTML')
        return
    
    if message.document.file_size > 5 * 1024 * 1024:
        bot.reply_to(message, "❌ **Max 5MB!**", parse_mode='HTML')
        return
    
    # Check if file already exists
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT file_name FROM user_files WHERE user_id = ? AND file_name = ?', 
              (user_id, message.document.file_name))
    if c.fetchone():
        conn.close()
        bot.reply_to(message, f"⚠️ **{message.document.file_name} already exists!**", parse_mode='HTML')
        return
    conn.close()
    
    msg = bot.reply_to(message, "⏳ **Downloading...**", parse_mode='HTML')
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        
        file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{message.document.file_name}")
        with open(file_path, 'wb') as f:
            f.write(downloaded)
        
        # Save to database (not approved yet)
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        c = conn.cursor()
        c.execute('INSERT INTO user_files (user_id, file_name, file_type, approved, uploaded_at) VALUES (?, ?, ?, ?, ?)',
                  (user_id, message.document.file_name, 'py', 0, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        # Send approval request to owner
        approve_markup = InlineKeyboardMarkup(row_width=2)
        approve_markup.add(
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}_{message.document.file_name}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user_id}_{message.document.file_name}")
        )
        
        bot.send_message(
            OWNER_ID,
            f"📩 **New File Upload**\n"
            f"👤 User: `{user_id}`\n"
            f"📁 File: `{message.document.file_name}`\n"
            f"💰 Credits: {get_credits(user_id)}",
            reply_markup=approve_markup,
            parse_mode='HTML'
        )
        
        bot.edit_message_text(
            f"✅ **Uploaded:** `{message.document.file_name}`\n"
            f"⏳ **Waiting for owner approval...**",
            message.chat.id,
            msg.message_id,
            parse_mode='HTML'
        )
        
    except Exception as e:
        bot.edit_message_text(f"❌ **Error:** {e}", message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# APPROVE/REJECT CALLBACKS
# ============================================================
@bot.callback_query_handler(func=lambda c: c.data.startswith('approve_'))
def approve_file(call):
    parts = call.data.split('_')
    user_id = int(parts[1])
    file_name = '_'.join(parts[2:])
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('UPDATE user_files SET approved = 1 WHERE user_id = ? AND file_name = ?', (user_id, file_name))
    conn.commit()
    conn.close()
    
    bot.answer_callback_query(call.id, "✅ Approved!")
    bot.edit_message_text(
        f"✅ **Approved:** `{file_name}`",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='HTML'
    )
    
    bot.send_message(
        user_id,
        f"✅ **Your file `{file_name}` has been approved!**\n"
        f"▶️ Use **Run File** button to start.",
        parse_mode='HTML'
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith('reject_'))
def reject_file(call):
    parts = call.data.split('_')
    user_id = int(parts[1])
    file_name = '_'.join(parts[2:])
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('DELETE FROM user_files WHERE user_id = ? AND file_name = ?', (user_id, file_name))
    conn.commit()
    conn.close()
    
    # Delete file
    file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{file_name}")
    if os.path.exists(file_path):
        os.remove(file_path)
    
    bot.answer_callback_query(call.id, "❌ Rejected!")
    bot.edit_message_text(
        f"❌ **Rejected:** `{file_name}`",
        call.message.chat.id,
        call.message.message_id,
        parse_mode='HTML'
    )
    
    bot.send_message(
        user_id,
        f"❌ **Your file `{file_name}` was rejected.**\n"
        f"📞 Contact @SunrakuV2 for details.",
        parse_mode='HTML'
    )

# ============================================================
# MY FILES
# ============================================================
@bot.message_handler(func=lambda m: m.text == "📊 My Files")
def my_files_cmd(message):
    user_id = message.chat.id
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT file_name, approved FROM user_files WHERE user_id = ?', (user_id,))
    files = c.fetchall()
    conn.close()
    
    if not files:
        bot.reply_to(message, "📭 **No files uploaded.**\n\nUse **Upload File** button.", parse_mode='HTML')
        return
    
    text = "📂 **Your Files:**\n━━━━━━━━━━━━━━━━━━━━━\n"
    for file_name, approved in files:
        status = "✅ Approved" if approved else "⏳ Pending"
        text += f"📄 {file_name} — {status}\n"
    
    bot.reply_to(message, text, parse_mode='HTML')

# ============================================================
# RUN FILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == "▶️ Run File")
def run_file_cmd(message):
    user_id = message.chat.id
    
    # Check credits
    credits = get_credits(user_id)
    if credits <= 0:
        bot.reply_to(message, "❌ **Insufficient credits!**\n💰 Contact @SunrakuV2 for more.", parse_mode='HTML')
        return
    
    # Get approved file
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT file_name FROM user_files WHERE user_id = ? AND approved = 1', (user_id,))
    files = c.fetchall()
    conn.close()
    
    if not files:
        bot.reply_to(message, "❌ **No approved files!**\n📤 Upload and wait for approval.", parse_mode='HTML')
        return
    
    if len(files) == 1:
        # Auto-run if only one file
        run_file(message, files[0][0])
        return
    
    # Multiple files - show selection
    markup = InlineKeyboardMarkup(row_width=1)
    for file_name in files:
        markup.add(InlineKeyboardButton(f"▶️ {file_name[0]}", callback_data=f"run_{user_id}_{file_name[0]}"))
    bot.reply_to(message, "📂 **Select file to run:**", reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda c: c.data.startswith('run_'))
def run_selected_file(call):
    parts = call.data.split('_')
    user_id = int(parts[1])
    file_name = '_'.join(parts[2:])
    
    if call.from_user.id != user_id:
        bot.answer_callback_query(call.id, "⚠️ Not your file!", show_alert=True)
        return
    
    bot.answer_callback_query(call.id)
    run_file(call.message, file_name)

def run_file(message, file_name):
    user_id = message.chat.id
    
    with lock:
        if user_id not in user_sessions:
            user_sessions[user_id] = UserSession(user_id)
        session = user_sessions[user_id]
    
    if session.is_running:
        bot.reply_to(message, "⚠️ **File already running!**\nUse **Stop File** first.", parse_mode='HTML')
        return
    
    # Check credits
    credits = get_credits(user_id)
    if credits <= 0:
        bot.reply_to(message, "❌ **No credits left!**\n💰 Contact @SunrakuV2.", parse_mode='HTML')
        return
    
    file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{file_name}")
    if not os.path.exists(file_path):
        bot.reply_to(message, f"❌ **File not found:** `{file_name}`", parse_mode='HTML')
        return
    
    # Deduct credit
    new_credits = deduct_credit(user_id)
    
    msg = bot.reply_to(message, f"🚀 **Starting:** `{file_name}`\n💰 Credits left: {new_credits}", parse_mode='HTML')
    
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
        session.add_log(f"✅ Started: {file_name}")
        
        # Log reader thread
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
        
        threading.Thread(target=read_logs, daemon=True).start()
        
        bot.edit_message_text(
            f"✅ **Running:** `{file_name}`\n"
            f"💰 Credits left: {new_credits}\n"
            f"📜 Use **View Logs** to see output",
            message.chat.id,
            msg.message_id,
            parse_mode='HTML'
        )
        
    except Exception as e:
        session.is_running = False
        session.add_log(f"❌ Run error: {e}")
        bot.edit_message_text(f"❌ **Error:** {e}", message.chat.id, msg.message_id, parse_mode='HTML')

# ============================================================
# STOP FILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == "⏹ Stop File")
def stop_file_cmd(message):
    user_id = message.chat.id
    
    with lock:
        if user_id not in user_sessions:
            bot.reply_to(message, "❌ No session!", parse_mode='HTML')
            return
        session = user_sessions[user_id]
    
    if not session.is_running:
        bot.reply_to(message, "⚠️ **No file running!**", parse_mode='HTML')
        return
    
    try:
        session.is_running = False
        session.process.terminate()
        time.sleep(1)
        if session.process.poll() is None:
            session.process.kill()
        session.add_log("⏹ Stopped by user")
        bot.reply_to(message, "⏹ **File stopped!**", parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ **Error:** {e}", parse_mode='HTML')

# ============================================================
# VIEW LOGS
# ============================================================
@bot.message_handler(func=lambda m: m.text == "📜 View Logs")
def view_logs_cmd(message):
    user_id = message.chat.id
    
    with lock:
        if user_id not in user_sessions:
            bot.reply_to(message, "❌ No session!", parse_mode='HTML')
            return
        session = user_sessions[user_id]
    
    logs = session.get_logs(25)
    if not logs or logs == "📭 No logs yet.":
        bot.reply_to(message, "📭 **No logs yet.**\n▶️ Run a file first.", parse_mode='HTML')
        return
    
    # Send in chunks if too long
    if len(logs) > 4000:
        chunks = [logs[i:i+4000] for i in range(0, len(logs), 4000)]
        for i, chunk in enumerate(chunks[:3]):
            bot.reply_to(message, f"📜 **Logs (Part {i+1}):**\n```\n{chunk}\n```", parse_mode='HTML')
    else:
        bot.reply_to(message, f"📜 **Recent Logs:**\n```\n{logs}\n```", parse_mode='HTML')

# ============================================================
# CREDITS
# ============================================================
@bot.message_handler(func=lambda m: m.text == "💰 Credits")
def credits_cmd(message):
    user_id = message.chat.id
    credits = get_credits(user_id)
    
    text = f"""
💰 <b>Your Credits</b>
━━━━━━━━━━━━━━━━━━━━━
👤 <b>User:</b> {message.from_user.first_name}
💳 <b>Credits:</b> {credits}

📌 <b>How to get more:</b>
• Contact @SunrakuV2
• Each run costs 1 credit
━━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, text, parse_mode='HTML')

# ============================================================
# PROFILE
# ============================================================
@bot.message_handler(func=lambda m: m.text == "👤 Profile")
def profile_cmd(message):
    user_id = message.chat.id
    credits = get_credits(user_id)
    
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM user_files WHERE user_id = ?', (user_id,))
    total_files = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM user_files WHERE user_id = ? AND approved = 1', (user_id,))
    approved_files = c.fetchone()[0]
    conn.close()
    
    text = f"""
👤 <b>Your Profile</b>
━━━━━━━━━━━━━━━━━━━━━
🆔 <b>ID:</b> <code>{user_id}</code>
💰 <b>Credits:</b> {credits}
📁 <b>Files:</b> {total_files} (✅ {approved_files} approved)
⏱ <b>Joined:</b> {datetime.now().strftime('%Y-%m-%d')}
━━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, text, parse_mode='HTML')

# ============================================================
# CONTACT
# ============================================================
@bot.message_handler(func=lambda m: m.text == "📞 Contact")
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
# ADMIN COMMANDS (Hidden)
# ============================================================
@bot.message_handler(commands=['addcredits'])
def add_credits_cmd(message):
    if message.from_user.id != OWNER_ID:
        return
    
    try:
        parts = message.text.split()
        user_id = int(parts[1])
        amount = int(parts[2])
        add_credits(user_id, amount)
        bot.reply_to(message, f"✅ Added {amount} credits to `{user_id}`", parse_mode='HTML')
        bot.send_message(user_id, f"💰 **+{amount} credits added!**\nCurrent balance: {get_credits(user_id)}", parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Usage: /addcredits user_id amount", parse_mode='HTML')

@bot.message_handler(commands=['broadcast'])
def broadcast_cmd(message):
    if message.from_user.id != OWNER_ID:
        return
    
    bot.reply_to(message, "📢 **Send broadcast message:**", parse_mode='HTML')
    bot.register_next_step_handler(message, process_broadcast)

def process_broadcast(message):
    if message.from_user.id != OWNER_ID:
        return
    
    msg = message.text
    sent = 0
    failed = 0
    
    for user_id in list(active_users):
        try:
            bot.send_message(user_id, f"📢 <b>Broadcast:</b>\n\n{msg}", parse_mode='HTML')
            sent += 1
        except:
            failed += 1
        time.sleep(0.1)
    
    bot.reply_to(message, f"✅ **Broadcast done!**\n📤 Sent: {sent}\n❌ Failed: {failed}", parse_mode='HTML')

# ============================================================
# START BOT
# ============================================================
print("""
╔═══════════════════════════════════════╗
║   ☠️ SUNRAKU — FILE RUNNER BOT        ║
║   ✅ Upload .py files                 ║
║   ✅ Auto input detection             ║
║   ✅ Credit System (10 free)          ║
║   ✅ Approve/Reject by Owner          ║
║   ✅ View Logs                        ║
║   👑 @SunrakuV2                       ║
║   📢 @Anishpy | @VOUCH_R              ║
╚═══════════════════════════════════════╝
""")
print(f"✅ Bot running...")
print(f"👑 Owner: @SunrakuV2")

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"⚠️ Polling error: {e}")
        time.sleep(5)
