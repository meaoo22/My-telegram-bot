import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ====== YAHAN APNA TOKEN AUR ADMIN ID DAALEIN ======
BOT_TOKEN = "8889794883:AAG3hexs1Ulyslro6oNoAjd1WTnKFb4LDeE"
ADMIN_CHAT_ID = 6423085445  # 👈 Apna Telegram User ID (integer) yahan daalein

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Jo bhi user bheje:
       1. Wahi wapas user ko bhejo (bot ke naam se)
       2. Wahi admin ko forward karo (user ke naam ke saath)
    """
    message = update.effective_message
    chat_id = update.effective_chat.id
    user = update.effective_user

    if not message:
        return

    # User ka display name banao
    user_name = user.full_name or user.username or f"User {user.id}"
    user_mention = f"<a href='tg://user?id={user.id}'>{user_name}</a>"

    try:
        # ==========================================
        # 1️⃣ USER KO COPY BHEJEN (bot ke naam se)
        # ==========================================
        if message.text:
            await context.bot.send_message(
                chat_id=chat_id,
                text=message.text,
                entities=message.entities,
            )
        elif message.photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=message.photo[-1].file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
            )
        elif message.video:
            await context.bot.send_video(
                chat_id=chat_id,
                video=message.video.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                thumbnail=message.video.thumbnail.file_id if message.video.thumbnail else None,
            )
        elif message.document:
            await context.bot.send_document(
                chat_id=chat_id,
                document=message.document.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                filename=message.document.file_name,
                thumbnail=message.document.thumbnail.file_id if message.document.thumbnail else None,
            )
        elif message.audio:
            await context.bot.send_audio(
                chat_id=chat_id,
                audio=message.audio.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                duration=message.audio.duration,
                performer=message.audio.performer,
                title=message.audio.title,
                thumbnail=message.audio.thumbnail.file_id if message.audio.thumbnail else None,
            )
        elif message.voice:
            await context.bot.send_voice(
                chat_id=chat_id,
                voice=message.voice.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
                duration=message.voice.duration,
            )
        elif message.video_note:
            await context.bot.send_video_note(
                chat_id=chat_id,
                video_note=message.video_note.file_id,
                thumbnail=message.video_note.thumbnail.file_id if message.video_note.thumbnail else None,
            )
        elif message.sticker:
            await context.bot.send_sticker(
                chat_id=chat_id,
                sticker=message.sticker.file_id,
            )
        elif message.animation:
            await context.bot.send_animation(
                chat_id=chat_id,
                animation=message.animation.file_id,
                caption=message.caption,
                caption_entities=message.caption_entities,
            )
        elif message.location:
            await context.bot.send_location(
                chat_id=chat_id,
                latitude=message.location.latitude,
                longitude=message.location.longitude,
            )
        elif message.venue:
            await context.bot.send_venue(
                chat_id=chat_id,
                latitude=message.venue.location.latitude,
                longitude=message.venue.location.longitude,
                title=message.venue.title,
                address=message.venue.address,
            )
        elif message.contact:
            await context.bot.send_contact(
                chat_id=chat_id,
                phone_number=message.contact.phone_number,
                first_name=message.contact.first_name,
                last_name=message.contact.last_name,
                vcard=message.contact.vcard,
            )
        elif message.poll:
            await context.bot.send_poll(
                chat_id=chat_id,
                question=message.poll.question,
                options=[opt.text for opt in message.poll.options],
                type=message.poll.type,
                allows_multiple_answers=message.poll.allows_multiple_answers,
                is_anonymous=message.poll.is_anonymous,
            )
        elif message.dice:
            await context.bot.send_dice(
                chat_id=chat_id,
                emoji=message.dice.emoji,
            )
        else:
            await message.reply_text("❌ Is type ki file ko handle nahi kar sakta.")

        # ==========================================
        # 2️⃣ ADMIN KO FORWARD KAREIN (user ke naam se)
        # ==========================================
        if ADMIN_CHAT_ID:
            admin_info = f"👤 <b>User:</b> {user_mention}\n🆔 <b>ID:</b> <code>{user.id}</code>\n📌 <b>Type:</b> {get_media_type(message)}\n━━━━━━━━━━━━━━━"

            # Pehle info message bhejein
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_info,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )

            # Phir actual media forward karein (original sender ke saath)
            await message.forward(chat_id=ADMIN_CHAT_ID)

        logger.info(f"✅ Processed: {user_name} ({user.id})")

    except Exception as e:
        logger.error(f"Error: {e}")
        try:
            await message.reply_text(f"⚠️ Error: {str(e)[:200]}")
        except:
            pass


def get_media_type(message) -> str:
    """Message type batao — text, photo, video, file, etc."""
    if message.text:           return "📝 Text"
    if message.photo:          return "🖼 Photo"
    if message.video:          return "🎥 Video"
    if message.document:       return "📄 File"
    if message.audio:          return "🎵 Audio"
    if message.voice:          return "🎤 Voice"
    if message.video_note:     return "🌀 Video Note"
    if message.sticker:        return "🏷 Sticker"
    if message.animation:      return "🎞 GIF"
    if message.location:       return "📍 Location"
    if message.venue:          return "🏪 Venue"
    if message.contact:        return "📇 Contact"
    if message.poll:           return "📊 Poll"
    if message.dice:           return "🎲 Dice"
    return "❓ Unknown"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start command handler"""
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n\n"
        f"Main <b>Forward Cover Bot</b> hoon.\n\n"
        f"Jo bhi tu yahan forward karega / bhejega, "
        f"main wahi wapas bhej dunga <b>apne naam se</b> "
        f"(tera naam nahi dikhega).\n\n"
        f"Bas koi bhi video, photo, file ya text forward karo!",
        parse_mode="HTML"
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.COMMAND & filters.Regex(r'^/start$'), start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    logger.info("🤖 Forward Cover Bot started...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
