# OS
import os

# Discord
import discord
from dotenv import load_dotenv

# Project
from DailyTimer import DailyTimer

# Define the Bot
class DailyWordsBot(discord.Bot):
    # On ready happens when the bot connects to Discord for the first time
    async def on_ready(self):
        self.add_cog(DailyTimer(self, "newwords.txt"))
        print(f'{bot.user} has connected to Discord!')

    # Send a message after any message
    async def on_message(self, message):
        # Make sure that it wasn't the bot that sent it
        if message.author == self.user:
            return

# Get the token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set the intents
intents = discord.Intents.default()
intents.messages = True

# Initialize the bot
bot = DailyWordsBot(command_prefix = "&", intents = intents)

# Run the bot
bot.run(TOKEN)