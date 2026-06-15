import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# ===== YANGI TOKENINGIZNI SHU YERGA YOZING =====
TOKEN = "8986331267:AAF3pEtrptL18JGuf2ksvdzS99KmHhQoqi8"

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

async def start(update: Update, context):
    await update.message.reply_text(
        "🎬 Salom! Botga xush kelibsiz!\n\n"
        "Instagram, YouTube yoki TikTok video havolasini yuboring."
    )

async def download_video(update: Update, context):
    url = update.message.text
    await update.message.reply_text("⏳ Video yuklanmoqda...")
    
    ydl_opts = {
        'format': 'best[height<=720]',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)
            
            with open(video_path, 'rb') as video_file:
                await update.message.reply_video(video=video_file, caption="✅ Yuklab olindi!")
            
            os.remove(video_path)
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {str(e)[:200]}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()