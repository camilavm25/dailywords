# OS
import os
import shutil
import json
from dotenv import load_dotenv

# Discord
import discord
from discord.ext import commands

# Project
from DailyTimer import DailyTimer

# Define the Bot
class DailyWordsBot(discord.Bot):
    channel_dict_filename: str = "channel_dict.json"

    # Save the channel dict to json
    def save_channels_to_json(self):
        # Make a backup
        channel_dict_backup_filename = self.channel_dict_filename + ".backup"
        
        # Remove it first if it exists
        if os.path.exists(channel_dict_backup_filename):
            os.remove(channel_dict_backup_filename)
        shutil.copyfile(self.channel_dict_filename, channel_dict_backup_filename)

        # Completely overwrite file
        if os.path.exists(self.channel_dict_filename):
            os.remove(self.channel_dict_filename)

        with open(self.channel_dict_filename, "w") as f:
            json.dump(self.channel_dict, f)

    # Load JSON to channel_dict
    def load_json_to_channels(self):
        # Clear the dict
        self.channel_dict = {}

        # Doesn't exist? Just make the file
        if not os.path.exists(self.channel_dict_filename):
            open(self.channel_dict_filename, "w").close()
            return

        # Load the file contents
        with open(self.channel_dict_filename, "r") as f:
            self.channel_dict = json.load(f)

    # On ready happens when the bot connects to Discord for the first time
    async def on_ready(self):
        # Read JSON data into the channel_dict
        # Map of Guild ID -> Channel ID
        self.load_json_to_channels()

        # Add the timer cog
        self.add_cog(DailyTimer(self, "newwords.txt"))

        # Print bot info
        print(f"{bot.user} has connected to Discord!")
        print(f"Connected to {len(bot.guilds)} guilds.")

    # When a guild is joined, default the channel to something it can post in
    async def on_guild_join(self, guild: discord.Guild):
        self.channel_dict[str(guild.id)] = next((c for c in guild.text_channels if c.can_send()), None).id
        self.save_channels_to_json()

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
bot = DailyWordsBot(intents = intents)

# Add a set channel command for this bot
@bot.command(name = "set_channel", description = "Sets the channel that messages are sent to")
async def dw_set_channel(ctx: commands.Context, channel: discord.TextChannel):
    # Check that the user running the command is the owner
    if ctx.author is not ctx.guild.owner:
        await ctx.respond(content = "You do not have permission to use this command.", ephemeral = True)
        return

    # Save the channels to the file
    bot.channel_dict[str(ctx.guild.id)] = channel.id
    bot.save_channels_to_json()

    # Respond to the interaction
    await ctx.respond(content = f"Set to {channel.mention}", ephemeral = True)

# Run the bot
bot.run(TOKEN)