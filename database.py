import aiosqlite
from config import DATABASE

class Database:

    def __init__(self):
        self.db = DATABASE

    async def connect(self):
        return await aiosqlite.connect(self.db)

    async def execute(self, query, values=()):
        async with aiosqlite.connect(self.db) as db:
            await db.execute(query, values)
            await db.commit()

    async def fetchone(self, query, values=()):
        async with aiosqlite.connect(self.db) as db:
            cursor = await db.execute(query, values)
            return await cursor.fetchone()

    async def fetchall(self, query, values=()):
        async with aiosqlite.connect(self.db) as db:
            cursor = await db.execute(query, values)
            return await cursor.fetchall()

db = Database()

async def initialize():
    async with aiosqlite.connect(DATABASE) as db:

        await db.executescript("""
        
CREATE TABLE IF NOT EXISTS guilds(

guild_id INTEGER PRIMARY KEY,

name TEXT,

owner_id INTEGER,

joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);  

CREATE TABLE IF NOT EXISTS settings(

guild_id INTEGER PRIMARY KEY,

welcome_channel INTEGER,

leave_channel INTEGER,

log_channel INTEGER,

ticket_category INTEGER,

verified_role INTEGER,

autorole INTEGER,

anti_link INTEGER DEFAULT 0,

anti_invite INTEGER DEFAULT 0,

anti_spam INTEGER DEFAULT 0,

anti_caps INTEGER DEFAULT 0,

anti_emoji INTEGER DEFAULT 0,

anti_toxic INTEGER DEFAULT 0,

anti_raid INTEGER DEFAULT 0

);

CREATE TABLE IF NOT EXISTS users(

user_id INTEGER,

guild_id INTEGER,

joins INTEGER DEFAULT 0,

messages INTEGER DEFAULT 0,

voice_time INTEGER DEFAULT 0,

PRIMARY KEY(user_id,guild_id)

);    

CREATE TABLE IF NOT EXISTS warnings(

id INTEGER PRIMARY KEY AUTOINCREMENT,

guild_id INTEGER,

user_id INTEGER,

moderator_id INTEGER,

reason TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS mutes(

guild_id INTEGER,

user_id INTEGER,

moderator_id INTEGER,

end_time INTEGER,

reason TEXT,

PRIMARY KEY(guild_id,user_id)

);  

CREATE TABLE IF NOT EXISTS tickets(

id INTEGER PRIMARY KEY AUTOINCREMENT,

guild_id INTEGER,

channel_id INTEGER,

owner_id INTEGER,

claimed_by INTEGER,

status TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS ticket_messages(

ticket_id INTEGER,

message_id INTEGER

);

CREATE TABLE IF NOT EXISTS logs(

id INTEGER PRIMARY KEY AUTOINCREMENT,

guild_id INTEGER,

action TEXT,

target_id INTEGER,

moderator_id INTEGER,

reason TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS giveaways(

message_id INTEGER PRIMARY KEY,

guild_id INTEGER,

channel_id INTEGER,

prize TEXT,

winner_count INTEGER,

end_time INTEGER,

ended INTEGER DEFAULT 0

);

CREATE TABLE IF NOT EXISTS verification(

guild_id INTEGER PRIMARY KEY,

verify_channel INTEGER,

verify_role INTEGER

);

CREATE TABLE IF NOT EXISTS automod(

guild_id INTEGER PRIMARY KEY,

spam_limit INTEGER DEFAULT 5,

caps_limit INTEGER DEFAULT 70,

emoji_limit INTEGER DEFAULT 10,

mention_limit INTEGER DEFAULT 5,

bad_words TEXT DEFAULT ''

);

CREATE TABLE IF NOT EXISTS tempbans(

guild_id INTEGER,

user_id INTEGER,

moderator_id INTEGER,

end_time INTEGER,

reason TEXT,

PRIMARY KEY(guild_id,user_id)

);

CREATE TABLE IF NOT EXISTS notes(

id INTEGER PRIMARY KEY AUTOINCREMENT,

guild_id INTEGER,

member_id INTEGER,

moderator_id INTEGER,

note TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE IF NOT EXISTS audit_cache(

message_id INTEGER PRIMARY KEY,

guild_id INTEGER,

channel_id INTEGER,

author_id INTEGER,

content TEXT

);

CREATE TABLE IF NOT EXISTS premium(

guild_id INTEGER PRIMARY KEY,

enabled INTEGER DEFAULT 0,

expires INTEGER

);

        """)

        await db.commit()