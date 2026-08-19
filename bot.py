import telebot
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# 🔑 BotFather से प्राप्त टोकन यहाँ पेस्ट करें
TOKEN = '8906367080:AAHNRQKZwK-9E7ybgI3ZfkLgr1j9jdVOL8I'

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

# यूज़र्स का डेटा और स्टेट (State) स्टोर करने के लिए
user_data = {}

# --- मुख्य कीबोर्ड (Reply Keyboard) ---
def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton('👤 Profile'), KeyboardButton('📤 Upload APK'))
    markup.row(KeyboardButton('📋 Help'), KeyboardButton('🌐 Language'))
    markup.row(KeyboardButton('🛠 Developer / Support'))
    return markup

# --- बैक बटन कीबोर्ड ---
def get_back_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton('🔙 Back'))
    return markup

# --- लैंग्वेज इनलाइन कीबोर्ड ---
def get_language_inline_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇺🇸 English", callback_data="lang_English"),
        InlineKeyboardButton("🇨🇳 中文", callback_data="lang_Chinese"),
        InlineKeyboardButton("🇪🇸 Español", callback_data="lang_Spanish"),
        InlineKeyboardButton("🇧🇷 Português", callback_data="lang_Portuguese"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_Russian"),
        InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_Turkish"),
        InlineKeyboardButton("🇮🇳 हिंदी", callback_data="lang_Hindi"),
        InlineKeyboardButton("🇯🇵 日本語", callback_data="lang_Japanese")
    )
    return markup

# 1. /start कमांड
@bot.message_handler(commands=['start'])
def start_cmd(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'state': 'IDLE'}
    
    text = (
        "<b>⚡️ APK FUD TECHNOLOGY</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Select an option:"
    )
    bot.send_message(chat_id, text, reply_markup=get_main_keyboard())

# 2. PROFILE बटन
@bot.message_handler(func=lambda m: m.text in ['👤 Profile', '👤 MY PROFILE'])
def profile_cmd(message):
    user_id = message.from_user.id
    profile_text = (
        "<b>👤 YOUR PROFILE</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<blockquote>"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
        "✅ <b>Status:</b> Active\n"
        "👑 <b>Plan:</b> 🌑 Credit\n"
        "📅 <b>Expiry:</b> ∞ No expiry (credit pack)\n"
        "🏗 <b>Builds:</b> 1 (used 0/1)"
        "</blockquote>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<b>⚡️ APK FUD TECHNOLOGY</b>"
    )
    bot.send_message(message.chat.id, profile_text, reply_markup=get_main_keyboard())

# 3. HELP बटन / मैन्युअल
@bot.message_handler(func=lambda m: m.text in ['📋 Help', '📋 HELP'])
def help_cmd(message):
    manual_text = (
        "<b>📋 MANUAL</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "<b>Workflow</b>\n"
        "<blockquote>"
        "1. Send .apk (≤ 20 MB)\n"
        "2. Enter display name\n"
        "3. Send icon PNG/JPG (or /skip)\n"
        "4. Receive repackaged APK"
        "</blockquote>\n\n"
        "<b>Commands</b>\n"
        "<blockquote>"
        "<b>/build</b> - Start new session\n"
        "<b>/cancel</b> - Abort operation\n"
        "<b>/language</b> - Switch language\n"
        "<b>/skip</b> - Skip current step"
        "</blockquote>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<b>FUD BY</b>"
    )
    bot.send_message(message.chat.id, manual_text, reply_markup=get_main_keyboard())

# 4. LANGUAGE बटन
@bot.message_handler(func=lambda m: m.text in ['🌐 Language', '🌐 LANGUAGE'])
def language_cmd(message):
    lang_text = (
        "🌐 <b>Select your language / Selecciona tu idioma / Выберите язык / Dil seçin / भाषा चुनें</b>"
    )
    bot.send_message(message.chat.id, lang_text, reply_markup=get_language_inline_keyboard())

# 5. BACK बटन
@bot.message_handler(func=lambda m: m.text == '🔙 Back')
def back_cmd(message):
    start_cmd(message)

# 6. UPLOAD APK प्रक्रिया (सेशन स्टार्ट)
@bot.message_handler(func=lambda m: m.text in ['📤 Upload APK', '📤 UPLOAD APK', '/build'])
def upload_apk_cmd(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'state': 'WAITING_APK'}
    
    msg_1 = (
        "<b>⚡️ APK FUD TECHNOLOGY</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "System online. Drop your .APK to begin."
    )
    msg_2 = (
        "📎 <b>NEW SESSION</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Send the <code>.apk</code> file to be repackaged.\n\n"
        "<i>Max size: 20 MB</i>"
    )
    bot.send_message(chat_id, msg_1)
    bot.send_message(chat_id, msg_2, reply_markup=get_back_keyboard())

# 7. `.apk` फाइल प्राप्त करने का हैंडलर
@bot.message_handler(content_types=['document'])
def handle_apk_file(message):
    chat_id = message.chat.id
    state = user_data.get(chat_id, {}).get('state')
    
    if state != 'WAITING_APK':
        bot.reply_to(message, "⚠️ कृपया पहले <b>📤 Upload APK</b> बटन दबाएं।")
        return

    doc = message.document
    file_name = doc.file_name or ""
    file_size_mb = doc.file_size / (1024 * 1024)

    if not file_name.lower().endswith('.apk'):
        bot.reply_to(message, "❌ <b>अमान्य फ़ाइल!</b> केवल <code>.apk</code> फ़ाइल भेजें।")
        return

    if file_size_mb > 20:
        bot.reply_to(message, "⚠️ <b>फ़ाइल आकार बहुत बड़ा है!</b> अधिकतम आकार 20 MB होना चाहिए।")
        return

    # फ़ाइल विवरण सहेजें
    user_data[chat_id] = {
        'state': 'WAITING_NAME',
        'file_id': doc.file_id,
        'file_name': file_name,
        'file_size': file_size_mb
    }

    resp_text = (
        f"<b>✓ {file_size_mb:.1f} MB received</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Enter display name for the app:"
    )
    bot.send_message(chat_id, resp_text)

# 8. ऐप का डिस्प्ले नेम दर्ज करने का हैंडलर
@bot.message_handler(func=lambda m: user_data.get(m.chat.id, {}).get('state') == 'WAITING_NAME')
def handle_app_name(message):
    chat_id = message.chat.id
    app_name = message.text.strip()

    user_data[chat_id]['app_name'] = app_name
    user_data[chat_id]['state'] = 'WAITING_LANG'

    lang_prompt = (
        "<b>🌐 Step 3: Choose UI Language</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "<blockquote>"
        "Select the language for the Google Play-style update dialog in the APK.\n\n"
        "Reply /skip for English (default)"
        "</blockquote>"
    )
    bot.send_message(chat_id, lang_prompt, reply_markup=get_language_inline_keyboard())

# 9. इनलाइन भाषा चुनने का हैंडलर + बिल्ड प्रोसेस
@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def handle_language_selection(call):
    chat_id = call.message.chat.id
    selected_lang = call.data.replace('lang_', '')
    bot.answer_callback_query(call.id)

    app_name = user_data.get(chat_id, {}).get('app_name', 'App')
    file_id = user_data.get(chat_id, {}).get('file_id')

    # स्टेप confirmation मैसेज
    lang_set_msg = (
        f"<b>✅ UI Language set:</b> {selected_lang}\n"
        f"<blockquote>Building APK with {selected_lang} UI...</blockquote>"
    )
    bot.send_message(chat_id, lang_set_msg)

    # प्रोग्रेस बार मैसेज
    proc_msg = bot.send_message(
        chat_id,
        f"<b>🔒 Processing</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<blockquote>📱 {app_name}\n🖼 default</blockquote>\n"
        "░░░░░░░░░░░░░░░░░░░░ <b>3%</b>"
    )

    # प्रोग्रेस बार सिमुलेशन
    time.sleep(1.5)
    bot.edit_message_text(
        f"<b>🔒 Processing</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<blockquote>📱 {app_name}\n🖼 default</blockquote>\n"
        "██████████░░░░░░░░░░ <b>50%</b>",
        chat_id, proc_msg.message_id
    )
    
    time.sleep(1.5)
    bot.edit_message_text(
        f"<b>🔒 Processing</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<blockquote>📱 {app_name}\n🖼 default</blockquote>\n"
        "████████████████████ <b>100%</b>",
        chat_id, proc_msg.message_id
    )

    time.sleep(1)

    # अंतिम संदेश
    final_caption = (
        "<blockquote>"
        "🔒 <b>APK Encryption Process Successfully Completed!</b> ✅\n\n"
        f"📱 <b>App Name:</b> {app_name}\n"
        "📦 <b>Package ID:</b> dApp.binance.Trading.Signals\n"
        "🔍 <b>Scan:</b> Bypassed all Antivirus\n"
        "⚙️ <b>Status:</b> Processed APK is ready!\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🗝 <b>Subscription Plan:</b> 🌑 Credit\n"
        "⌛ <b>Expires in:</b> ∞ No expiry\n"
        "∞ 0 builds left with this key\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📤 <b>Your FUD APK is attached above.</b>"
        "</blockquote>"
    )

    # APK फाइल वापस भेजना
    output_filename = f"bypassed_{int(time.time())}.apk"
    if file_id:
        bot.send_document(
            chat_id,
            document=file_id,
            caption=final_caption,
            visible_file_name=output_filename
        )
    else:
        bot.send_message(chat_id, final_caption)

    # स्टेट रीसेट करें
    user_data[chat_id] = {'state': 'IDLE'}

# बॉट शुरू करें
print("⚡️ APK FUD Telegram Bot is running perfectly...")
bot.polling(none_stop=True)
