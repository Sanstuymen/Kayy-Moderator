import os
import asyncio
import logging
import traceback

import discord
from discord.ext import commands

from config import (
    TOKEN,
    PREFIX,
    BOT_NAME,
    BOT_VERSION,
    BOT_ACTIVITY
)

from database import initialize


# ===========================
# Logging
# ===========================

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s"
)

logger = logging.getLogger(BOT_NAME)


# ===========================
# Discord Intents
# ===========================

intents = discord.Intents.default()

intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.voice_states = True
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_typing = False
intents.presences = False


# ===========================
# Bot Class
# ===========================

class KayModerator(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix=PREFIX,
            intents=intents,
            help_command=None,
            case_insensitive=True
        )

        self.logger = logger
        self.start_time = None

    async def setup_hook(self):

        self.logger.info("Initializing database...")

        await initialize()

        self.logger.info("Database initialized.")

        await self.load_all_extensions()

    async def load_all_extensions(self):

        loaded = 0

        for filename in os.listdir("./cogs"):

            if not filename.endswith(".py"):
                continue

            name = filename[:-3]

            try:

                await self.load_extension(f"cogs.{name}")

                self.logger.info(f"Loaded Cog: {name}")

                loaded += 1

            except Exception:

                self.logger.error(
                    traceback.format_exc()
                )

        self.logger.info(f"{loaded} Cog loaded.")
        
        bot = KayModerator()
        @bot.event
async def on_ready():

    logger.info("-" * 40)

    logger.info(f"Bot : {bot.user}")

    logger.info(f"ID  : {bot.user.id}")

    logger.info(f"Servers : {len(bot.guilds)}")

    logger.info(f"Users   : {len(bot.users)}")

    logger.info(f"Version : {BOT_VERSION}")

    logger.info("-" * 40)

    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=BOT_ACTIVITY
    )

    await bot.change_presence(activity=activity)

    print()

    logger.info("Bot is Ready.")
    
async def main():

    async with bot:

        await bot.start(TOKEN)


if __name__ == "__main__":

    asyncio.run(main())