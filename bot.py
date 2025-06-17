import os
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
from search_references import cari_Ref_Berita

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ==================== Helper Functions ====================

def is_url(teks: str) -> bool:
    return teks.startswith("http://") or teks.startswith("https://")

def parse_gemini_response(hasil: str):
    kategori = ""
    penjelasan = ""
    confidence = ""

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

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🔤 Teks Berita", callback_data="input_teks"),
            InlineKeyboardButton("🌐 Link Berita", callback_data="input_link"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Silakan pilih jenis berita yang ingin kamu analisis:",
        reply_markup=reply_markup
    )
    context.user_data["mode"] = None  # Reset mode

# ==================== Command Handler ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖*Bot Detektor Berita Hoax!*\n\n"
        "Saya bisa bantu kamu menganalisis berita apakah itu hoax, clickbait, misleading, atau valid.\n\n"
        "Silakan pilih jenis berita yang ingin kamu analisis:",
        parse_mode="Markdown"
    )
    await show_main_menu(update, context)

# ==================== Inline Button Handler ====================

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "input_teks":
        context.user_data["mode"] = "teks"
        await query.message.reply_text("📥 Silakan kirimkan *teks berita* yang ingin kamu analisis:", parse_mode="Markdown")

    elif query.data == "input_link":
        context.user_data["mode"] = "link"
        await query.message.reply_text("📥 Silakan kirimkan *link berita (URL)* yang ingin kamu analisis:", parse_mode="Markdown")

# ==================== Message Handler ====================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    # Deteksi otomatis jika belum pilih mode
    if context.user_data.get("mode") is None:
        if is_url(user_input):
            context.user_data["mode"] = "link"
        else:
            context.user_data["mode"] = "teks"

    try:
        await update.message.reply_text("🕵️‍♂️ Sedang menganalisis... Mohon tunggu sebentar.")

        if context.user_data["mode"] == "link":
            if not is_url(user_input):
                await update.message.reply_text("⚠️ Tautan tidak valid. Mohon kirim link yang benar (diawali http:// atau https://).")
                return
            teks_berita = ekstrak_teks(user_input)
            if teks_berita.startswith("[Gagal"):
                await update.message.reply_text(f"❌ Gagal mengambil isi berita dari link.\n\n{teks_berita}")
                return
        else:
            teks_berita = user_input

        prompt_ = prompt(teks_berita)
        hasil = tanya_gemini(prompt_)
        kategori, penjelasan, confidence = parse_gemini_response(hasil)
        icon = emoji_kategori(kategori)

        respon = (
            f"📊 *Hasil Analisis:*\n\n"
            f"*Kategori:* {icon} `{kategori}`\n"
            f"*Confidence:* `{confidence}`\n\n"
            f"*Penjelasan:*\n_{penjelasan}_"
        )

        await update.message.reply_text(respon, parse_mode="Markdown")

    except Exception as e:
        print(f"[ERROR] {e}")
        await update.message.reply_text("⚠️ Terjadi kesalahan saat memproses berita. Silakan coba lagi.")

    # Tampilkan kembali menu
    await show_main_menu(update, context)

# ==================== App Initialization ====================

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot berjalan... tekan CTRL+C untuk menghentikan.")
    app.run_polling()
