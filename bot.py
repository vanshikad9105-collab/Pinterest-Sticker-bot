import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

# 🔒 Paste your token here — keep it private!
BOT_TOKEN = "8074887465:AAErmDfmR2_Nw7dNVmO39kpywzw6RIzpNYA"

async def handle_pinterest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "pinterest.com" not in url:
        await update.message.reply_text("Please send a valid Pinterest link 📎")
        return

    await update.message.reply_text("Downloading from Pinterest...")

    try:
        # extract image url from pinterest
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        meta = soup.find("meta", property="og:image")
        image_url = meta["content"] if meta else None

        if not image_url:
            await update.message.reply_text("Couldn't find an image on that link 😕")
            return

        # download image
        resp = requests.get(image_url)
        img = Image.open(BytesIO(resp.content)).convert("RGBA")

        # convert to sticker format
        img.thumbnail((512, 512))
        out = BytesIO()
        img.save(out, format="WEBP")
        out.seek(0)

        await update.message.reply_sticker(sticker=out)
        await update.message.reply_text("Here’s your sticker! Tap 'Add to Stickers' to add it ✨")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_pinterest))
app.run_polling()
