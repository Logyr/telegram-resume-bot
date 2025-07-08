import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
PAWAN_API_KEY = os.getenv("PAWAN_API_KEY")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def generate_resume(prompt: str) -> str:
    url = "https://api.pawan.krd/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {PAWAN_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I'm ResumeBot.\n\nSend your details in this format:\n"
        "Name: ...\nSkills: ...\nExperience: ...\n\nI'll make a beautiful resume for you!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await update.message.reply_text("⏳ Generating your resume...")
    resume = await generate_resume(f"Create an ATS-free colorful resume with this info:\n{user_input}")
    await update.message.reply_text(resume)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 Bot is running...")
app.run_polling()
