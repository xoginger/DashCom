# telegram_bot.py
import logging
from datetime import datetime
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from models import db, User, Report

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update, context):
    await update.message.reply_text("Hola, soy DashCom Bot. Usa /help para ver comandos.")

async def help_command(update, context):
    await update.message.reply_text("Comandos: /start, /help, /id, /reporte")

async def id_command(update, context):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Tu chat_id es: {chat_id}")

async def reporte_command(update, context):
    chat_id = str(update.effective_chat.id)
    user = User.query.filter_by(chat_id=chat_id).first()
    if not user:
        await update.message.reply_text("No se encontró tu información.")
        return
    report_count = len(user.reports)
    await update.message.reply_text(f"Tienes {report_count} reportes registrados.")

async def handle_message(update, context):
    chat_id = str(update.effective_chat.id)
    content = update.message.text
    user = User.query.filter_by(chat_id=chat_id).first()
    if not user:
        user = User(chat_id=chat_id, name=update.effective_user.first_name)
        db.session.add(user)
        db.session.commit()
    report = Report(user_id=user.id, timestamp=datetime.utcnow(), content=content)
    db.session.add(report)
    db.session.commit()
    await update.message.reply_text("✅ Reporte registrado.")

def setup_bot(app_config):
    bot_app = ApplicationBuilder().token(app_config.TELEGRAM_BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("help", help_command))
    bot_app.add_handler(CommandHandler("id", id_command))
    bot_app.add_handler(CommandHandler("reporte", reporte_command))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return bot_app
