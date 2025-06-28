import os
import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from prompts import prompt
from gemini_interface import tanya_gemini
from utils import ekstrak_teks

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def is_url(teks: str) -> bool:
    return teks.startswith("http://") or teks.startswith("https://")

def is_malicious(teks: str) -> bool:
    return bool(re.search(r"<script|SELECT\s.+\sFROM|DROP\s+TABLE|--", teks, re.IGNORECASE))

def parse_gemini_response(hasil: str):
    kategori, penjelasan, confidence = "", "", ""
    for line in hasil.split("\n"):
        if line.lower().startswith("kategori:"):
            kategori = line.split(":", 1)[1].strip()
        elif line.lower().startswith("penjelasan:"):
            penjelasan = line.split(":", 1)[1].strip()
        elif "confidence" in line.lower():
            confidence = line.split(":", 1)[1].strip()
    return kategori, penjelasan, confidence 

def emoji_kategori(kategori):
    k = kategori.lower()
    if "hoax" in k:
        return "🔴"
    elif "misleading" in k:
        return "🟠"
    elif "clickbait" in k:
        return "🟡"
    elif "valid" in k:
        return "🟢"
    return "❓"

def build_main_menu():
    keyboard = [[
        InlineKeyboardButton("🔤 Teks Berita", callback_data="input_teks"),
        InlineKeyboardButton("🌐 Link Berita", callback_data="input_link"),
    ]]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = (
        "🤖 *Detektor Hoax*\n\n"
        "Saya adalah asisten cerdas yang siap membantumu mendeteksi apakah sebuah berita tergolong:\n"
        "🔴 *Hoax* | 🟠 *Misleading* | 🟡 *Clickbait* | 🟢 *Valid*\n\n"
        "Silakan pilih jenis input yang ingin kamu kirim:"
    )
    await update.message.reply_text(welcome, parse_mode="Markdown", reply_markup=build_main_menu())
    context.user_data["mode"] = None

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "input_teks":
        context.user_data["mode"] = "teks"
        await query.message.reply_text("📝 Silakan kirimkan *teks berita* yang ingin dianalisis:", parse_mode="Markdown")

    elif query.data == "input_link":
        context.user_data["mode"] = "link"
        await query.message.reply_text("🔗 Silakan kirimkan *link berita (URL)* yang ingin dianalisis:", parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if is_malicious(user_input):
        await update.message.reply_text("🚫 Input mengandung karakter mencurigakan. Mohon kirim teks atau link yang benar.")
        return

    if len(user_input) > 3000:
        await update.message.reply_text("⚠️ Teks terlalu panjang. Mohon kirim teks berita yang lebih singkat.")
        return

    if context.user_data.get("mode") is None:
        context.user_data["mode"] = "link" if is_url(user_input) else "teks"

    await update.message.reply_text("🤖🔎 Sedang menganalisis... Mohon tunggu sebentar.")

    try:
        if context.user_data["mode"] == "link":
            if not is_url(user_input):
                await update.message.reply_text("🔗 Link tidak valid. Pastikan diawali dengan http:// atau https://")
                return

            teks_berita = ekstrak_teks(user_input)
            if teks_berita.startswith("[Gagal"):
                await update.message.reply_text(f"❌ Gagal mengambil isi berita dari link.\n\n{teks_berita}")
                return
        else:
            teks_berita = user_input

        hasil = tanya_gemini(prompt(teks_berita))
        kategori, penjelasan, confidence = parse_gemini_response(hasil)
        icon = emoji_kategori(kategori)

        respon = (
            f"📊 *Hasil Analisis:*\n\n"
            f"*Kategori:* {icon} `{kategori}`\n"
            f"*Confidence:* `{confidence}`\n\n"
            f"*Penjelasan:*\n_{penjelasan}_"
        )

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 Analisis Berita Lain", callback_data="kembali_ke_menu")]
        ])

        await update.message.reply_text(respon, parse_mode="Markdown", reply_markup=reply_markup)

    except Exception as e:
        print(f"[ERROR] {e}")
        await update.message.reply_text("⚠️ Terjadi kesalahan saat memproses. Silakan coba lagi.")

async def kembali_ke_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Silakan pilih jenis berita yang ingin kamu analisis:", reply_markup=build_main_menu())
    context.user_data["mode"] = None


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button, pattern="^input_"))
    app.add_handler(CallbackQueryHandler(kembali_ke_menu, pattern="^kembali_ke_menu$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot aktif. Tekan CTRL+C untuk berhenti.")
    app.run_polling()
