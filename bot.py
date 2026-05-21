# OS
import os
import random
import datetime

# Time zone
from zoneinfo import ZoneInfo

# Discord
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

# Translator
from googletrans import Translator

TIME = datetime.time(hour = 6, minute = 0, tzinfo = ZoneInfo("America/New_York"))

# Timer class
class DailyTimer(commands.Cog):
    # Start the timer Cog
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()
        self.new_word_task.start()
        

    # Have it run daily
    #@tasks.loop(time = TIME)
    @tasks.loop(seconds = 5.0)
    async def new_word_task(self):
        # Choose a word and remove it from the list
        word = random.choice(words)
        words.remove(word)

        # Save the remaining words to the text file
        os.remove("newwords.txt")
        with open("newwords.txt", "w") as f:
            # Don't overwrite if the list is empty
            if len(words) == 0:
                print("ERROR: WORD LIST EMPTY")
                return
            
            # First element does not need leading comma
            for (i, w) in enumerate(words, start = 0):
                if i == 0:
                    f.write(w)
                else:
                    f.write(f",{w}")

        # Translate the word
        german  = await self.translator.translate(text = word, src = 'en', dest = 'de')
        spanish = await self.translator.translate(text = word, src = 'en', dest = 'es')
        telugu  = await self.translator.translate(text = word, src = 'en', dest = 'te')

        # Prepare the response
        response = f"Today's word of the day is:\n"
        response += f"\tEnglish: **{word}**\n"
        response += f"\tGerman: **{german.text}**\n"
        response += f"\tSpanish: **{spanish.text}**\n"
        response += f"\tTelugu: **{telugu.text}** (*{telugu.pronunciation}*)\n"

        # Get the channel
        # TODO: Allow user to select channel
        for guild in bot.guilds:
            for channel in guild.channels:
                if channel.name == "general":
                    await channel.send(response)
                    break

        print(word)


# Define the Bot
class DailyWordsBot(discord.Bot):
    # On ready happens when the bot connects to Discord for the first time
    async def on_ready(self):
        self.add_cog(DailyTimer(self))
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

# Load the word list
words = []
with open("newwords.txt", "r") as f:
    for line in f:
        l = line.split(",")

        for word in l:
            w = word.strip()
            words.append(w)

# Initialize the bot
bot = DailyWordsBot(command_prefix = "&", intents = intents)

# Run the bot
bot.run(TOKEN)