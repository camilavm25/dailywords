# OS
import os
import random
import datetime

# Time zone
from zoneinfo import ZoneInfo

# Discord
import discord
from discord.ext import commands, tasks

# Translator
from googletrans import Translator

# Timer set for 6:00AM EST
TIME = datetime.time(hour = 6, minute = 0, tzinfo = ZoneInfo("America/New_York"))

# Timer class
class DailyTimer(commands.Cog):
    # Start the timer Cog
    def __init__(self, bot, filename):
        self.bot = bot
        self.filename = filename
        self.translator = Translator()

        # Load the word list
        self.words = []
        with open(self.filename, "r") as f:
            for line in f:
                l = line.split(",")

                for word in l:
                    w = word.strip()
                    self.words.append(w)

        # Run the cog
        self.new_word_task.start()


    # Have it run daily
    @tasks.loop(time = TIME)
    async def new_word_task(self):
        # Choose a word and remove it from the list
        word = random.choice(self.words)
        self.words.remove(word)

        # Save the remaining words to the text file
        os.remove(self.filename)
        with open(self.filename, "w") as f:
            # Don't overwrite if the list is empty
            if len(self.words) == 0:
                print("ERROR: WORD LIST EMPTY")
                return
            
            # First element does not need leading comma
            for (i, w) in enumerate(self.words, start = 0):
                if i == 0:
                    f.write(w)
                else:
                    f.write(f",{w}")

        # Translate the word
        german  = await self.translator.translate(text = word, src = 'en', dest = 'de')
        spanish = await self.translator.translate(text = word, src = 'en', dest = 'es')
        telugu  = await self.translator.translate(text = word, src = 'en', dest = 'te')

        # Get the date
        date = datetime.datetime.today().strftime('%A %d %B %Y')

        # Prepare the response
        response  = f"\tEnglish: **{word}**\n"
        response += f"\tGerman: **{german.text}**\n"
        response += f"\tSpanish: **{spanish.text}**\n"
        response += f"\tTelugu: **{telugu.text}** (*{telugu.pronunciation}*)\n"

        # Put it all together
        embed = discord.Embed(
            title = f"Word of the Day for {date}",
            description = response,
            color = discord.Color.green()
        )

        # Send it to every channel
        for guild_id in self.bot.channel_dict:
            channel_id = self.bot.channel_dict[guild_id]
            channel = self.bot.get_channel(channel_id)

            view = discord.ui.View()
            view.message = await channel.send(
                embed = embed,
                view = view
            )