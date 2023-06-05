from bot import DATABASE_URL, BOT_USERNAME
from bot.database import Database

db = Database(DATABASE_URL, BOT_USERNAME)
