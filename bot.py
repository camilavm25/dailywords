import os
import random

import discord
from dotenv import load_dotenv

# Define the Bot
class DailyWordsBot(discord.Bot):
    # On ready happens when the bot connects to Discord for the first time
    async def on_ready(self):
        print(f'{bot.user} has connected to Discord!')

    # Send a message after any message
    async def on_message(self, message):
        # Make sure that it wasn't the bot that sent it
        if message.author == self.user:
            return
        
        # Choose a word and remove it from the list
        word = random.choice(words)
        words.remove(word)

        # Save the remaining words to the text file
        os.remove("newwords.txt")
        with open("newwords.txt", "w") as f:
            if len(words) == 0:
                print("ERROR: WORD LIST EMPTY")
                return
            
            for (i, w) in enumerate(words, start = 0):
                if i == 0:
                    f.write(w)
                else:
                    f.write(f",{w}")

        # Print the word
        await message.channel.send(f"Today's word of the day is: {word}")

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