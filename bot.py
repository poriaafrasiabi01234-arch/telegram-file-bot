from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import uuid

TOKEN = "8057867786:AAGtLWeRYTx3Q0NQOZNr_QV9IAB86NxS9Ns"
BOT_USERNAME = "myfileidtest_bot"  # بدون @

admin_id = None
file_storage = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global admin_id

    user_id = update.effective_user.id

    # اگر هنوز ادمین نداریم
    if admin_id is None:
        admin_id = user_id
        await update.message.reply_text("تو الان ادمین شدی 👑")
        return

    # اگر لینک داشت
    if context.args:
        code = context.args[0]

        if code in file_storage:
            file_id, file_type = file_storage[code]
            caption = "جاااان پسر شاه باشه"

            if file_type == "video":
                await update.message.reply_video(file_id, caption=caption)
            elif file_type == "document":
                await update.message.reply_document(file_id, caption=caption)
            elif file_type == "photo":
                await update.message.reply_photo(file_id, caption=caption)
        else:
            await update.message.reply_text("لینک نامعتبره.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global admin_id

    if update.effective_user.id != admin_id:
        return

    message = update.message
    file_id = None
    file_type = None

    if message.video:
        file_id = message.video.file_id
        file_type = "video"
    elif message.document:
        file_id = message.document.file_id
        file_type = "document"
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_type = "photo"

    if file_id:
        code = str(uuid.uuid4())[:8]
        file_storage[code] = (file_id, file_type)

        link = f"https://t.me/{BOT_USERNAME}?start={code}"
        await update.message.reply_text(f"لینک آماده شد:\n{link}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_file))

app.run_polling()