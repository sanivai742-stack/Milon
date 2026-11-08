import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

# আপনার বটের টোকেন
API_TOKEN = '9027972676:AAFsDj4wBDZfU-gUEfr29umXPyU67wG7Mqk'
bot = telebot.TeleBot(API_TOKEN)

# NP Network API কনফিগারেশন
NP_API_BASE_URL = 'https://www.npnetworkbd.com/api/user'
NP_API_KEY = 'NP-Y3JMHQEW9YMW5X47'

# ইউজার ব্যালেন্স ট্র্যাক করার ডিকশনারি
user_balances = {}

def get_user_balance(user_id):
    return user_balances.get(user_id, 0.0)

def add_user_balance(user_id, amount):
    current = user_balances.get(user_id, 0.0)
    user_balances[user_id] = round(current + amount, 2)

# মূল মেনু ডিজাইন
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("⚡ Get Virtual Number ⚡"),
        KeyboardButton("💎 My Wallet & Balance"),
        KeyboardButton("🚀 Invite & Earn (Refer)"),
        KeyboardButton("🛠️ 24/7 VIP Support")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🌟 *WELCOME TO ELITE OTP HUB* 🌟\n\n"
        "✨ Fast, Secure, and Automated Number Service.\n"
        "👇 Select an option from the sleek menu below to get started:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=get_main_menu())

# Get Number ক্লিক করলে প্রিমিয়াম সার্ভিস লিস্ট
@bot.message_handler(func=lambda message: message.text == "⚡ Get Virtual Number ⚡")
def handle_get_number(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🔥 FB Forgot Password"),
        KeyboardButton("⭐ Facebook Standard"),
        KeyboardButton("📸 Instagram Pro"),
        KeyboardButton("💬 WhatsApp Secure"),
        KeyboardButton("🔙 Main Menu")
    )
    bot.send_message(message.chat.id, "🎯 *Choose Your Desired Service Platform:*", parse_mode="Markdown", reply_markup=markup)

# সার্ভিস সিলেক্ট করার পর কান্ট্রি লিস্ট (নতুন প্রিমিয়াম ইমোজি সহ)
@bot.message_handler(func=lambda message: message.text in ["🔥 FB Forgot Password", "⭐ Facebook Standard", "📸 Instagram Pro", "💬 WhatsApp Secure"])
def handle_service_selection(message):
    # সার্ভিসের নাম থেকে ইমোজি বাদ দিয়ে শুধু মূল নাম রাখা
    service_name = message.text.split(' ', 1)[1]
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton(f"👑 Ethiopia - {service_name}"),
        KeyboardButton(f"💎 Italy - {service_name}"),
        KeyboardButton(f"🏆 France - {service_name}"),
        KeyboardButton(f"🎯 Cameroon - {service_name}"),
        KeyboardButton(f"🚀 Tajikistan - {service_name}"),
        KeyboardButton("🔙 Back to Services"),
        KeyboardButton("🔙 Main Menu")
    )
    bot.send_message(message.chat.id, f"🌍 *Select Target Country for {service_name}:*", parse_mode="Markdown", reply_markup=markup)

# সঠিক কান্ট্রি অনুযায়ী সরাসরি প্যানেল API থেকে নাম্বার ফেচ করা
@bot.message_handler(func=lambda message: any(c in message.text for c in ["Ethiopia", "Italy", "France", "Cameroon", "Tajikistan", "Change Number"]))
def handle_number_generation(message):
    text_input = message.text
    
    country_name = "Unknown"
    country_code = "ET"
    if "Ethiopia" in text_input:
        country_name = "Ethiopia"
        country_code = "ET"
    elif "Italy" in text_input:
        country_name = "Italy"
        country_code = "IT"
    elif "France" in text_input:
        country_name = "France"
        country_code = "FR"
    elif "Cameroon" in text_input:
        country_name = "Cameroon"
        country_code = "CM"
    elif "Tajikistan" in text_input:
        country_name = "Tajikistan"
        country_code = "TJ"

    phone_number = "No Number Available"
    
    try:
        api_url = f"{NP_API_BASE_URL}?key={NP_API_KEY}&action=getNumber&country={country_code}"
        response = requests.get(api_url, timeout=7)
        data = response.json()
        
        print("API Response Debug:", data)
        
        if isinstance(data, dict):
            for key in ['number', 'phone', 'msg', 'message', 'result']:
                if key in data and isinstance(data[key], str) and len(data[key]) > 4:
                    phone_number = data[key]
                    break
            if phone_number == "No Number Available" and 'data' in data and isinstance(data['data'], dict):
                phone_number = data['data'].get('number', 'No Number Available')
    except Exception as e:
        print(f"API Connection Error: {e}")

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        KeyboardButton(f"📋 Number: {phone_number}"),
        KeyboardButton("🔄 Check / Simulate OTP Received"),
        KeyboardButton("🔄 Request New Number"),
        KeyboardButton("🔙 Main Menu")
    )
    
    text = (
        f"╔═══════════════════════╗\n"
        f"  🛡️ **SESSION ACTIVE**\n"
        f"╚═══════════════════════╝\n\n"
        f"🌐 **Country:** `{country_name}`\n"
        f"⏳ **Status:** `Awaiting Incoming OTP...`\n\n"
        f"📱 **Virtual Number:**\n`{phone_number}`\n\n"
        f"💡 *Tip: Copy the number, use it on your app, then hit check OTP below!*"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# OTP রিসিভ হলে ব্যালেন্সে যোগ হওয়া
@bot.message_handler(func=lambda message: message.text == "🔄 Check / Simulate OTP Received")
def handle_otp_received(message):
    user_id = message.from_user.id
    
    add_user_balance(user_id, 0.1)
    current_balance = get_user_balance(user_id)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        KeyboardButton("🔄 Request New Number"),
        KeyboardButton("🔙 Main Menu")
    )
    
    text = (
        f"🎉 **OTP SUCCESSFULLY RECEIVED!** 🎉\n\n"
        f"📩 **Verification Code:** `482910`\n\n"
        f"💰 **Reward Added:** `+0.1 TK`\n"
        f"💎 **Total Balance:** `{current_balance} TK`"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

# ব্যালেন্স চেক মেনু
@bot.message_handler(func=lambda message: message.text == "💎 My Wallet & Balance")
def handle_balance(message):
    user_id = message.from_user.id
    balance = get_user_balance(user_id)
    text = (
        f"💼 **WALLET SUMMARY**\n\n"
        f"👤 **User ID:** `{user_id}`\n"
        f"💳 **Available Balance:** `{balance} TK`\n\n"
        f"✨ *Earn more by inviting friends through the referral section!*"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_menu())

# সাপোর্ট বাটন (সাপোর্ট আইডি 7143948308)
@bot.message_handler(func=lambda message: message.text == "🛠️ 24/7 VIP Support")
def handle_support(message):
    support_text = (
        "🎧 **VIP CUSTOMER SUPPORT**\n\n"
        "Facing any issues with numbers or balance? Connect with our administration directly:\n\n"
        "👉 [Click Here to Message Support](tg://user?id=7143948308)"
    )
    bot.send_message(message.chat.id, support_text, parse_mode="Markdown", reply_markup=get_main_menu())

# রেফার বাটন
@bot.message_handler(func=lambda message: message.text == "🚀 Invite & Earn (Refer)")
def handle_refer(message):
    bot_info = bot.get_me()
    bot_username = bot_info.username
    user_id = message.from_user.id
    referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    
    refer_text = (
        "🚀 **REFERRAL PROGRAM**\n\n"
        "Share your unique link with friends and grow your network instantly!\n\n"
        f"🔗 **Your Exclusive Link:**\n`{referral_link}`"
    )
    bot.send_message(message.chat.id, refer_text, parse_mode="Markdown", reply_markup=get_main_menu())

# ব্যাক এবং হোম মেনু হ্যান্ডলার
@bot.message_handler(func=lambda message: message.text in ["🔙 Main Menu", "🔙 Back to Services", "🔄 Request New Number"])
def handle_other_menus(message):
    txt = message.text
    if txt == "🔙 Back to Services":
        handle_get_number(message)
    else:
        bot.send_message(message.chat.id, "🌟 Main Dashboard:", reply_markup=get_main_menu())

if __name__ == '__main__':
    print("Elite OTP Bot is running successfully with updated design...")
    bot.infinity_polling()
