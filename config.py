from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

PREFIX = "!"

EMBED_COLOR = 0x5865F2

DATABASE = "database/bot.db"

BOT_NAME = "Kay Moderator"

BOT_VERSION = "1.0.0"

BOT_STATUS = "Melindungi Server"

BOT_ACTIVITY = "Moderating Server"

SUPPORT_GUILD = None

DEFAULT_SETTINGS = {
    "welcome_channel": None,
    "leave_channel": None,
    "log_channel": None,
    "ticket_category": None,
    "verified_role": None,
    "autorole": None,
    "anti_link": False,
    "anti_invite": False,
    "anti_spam": False,
    "anti_caps": False,
    "anti_emoji": False,
    "anti_toxic": False,
    "anti_raid": False
}