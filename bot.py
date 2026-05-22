# OS
import os
from dotenv import load_dotenv

# Discord
import discord
from discord.ext import commands

# Project
from DailyTimer import DailyTimer

# Define the Bot
class DailyWordsBot(discord.Bot):
    # On ready happens when the bot connects to Discord for the first time
    async def on_ready(self):
        # TODO: Store this in/read from a file somehow (probably JSON)
        # Map of Guild ID -> Channel ID
        self.channel_dict = {}        

        # TODO: Remove this when the above is done (debug only for test server)
        self.channel_dict[1412296315811139647] = 1412296316528099381

        # Add the timer cog
        self.add_cog(DailyTimer(self, "newwords.txt"))

        print(f"{bot.user} has connected to Discord!")
        print(f"Connected to {len(bot.guilds)} guilds.")

    # When a guild is joined, default the channel to something it can post in
    async def on_guild_join(self, guild: discord.Guild):
        self.channel_dict[guild.id] = next((c for c in guild.text_channels if c.can_send()), None).id

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
    if ctx.author is not ctx.guild.owner:
        await ctx.respond(content = "You do not have permission to use this command.", ephemeral = True)
        return

    bot.channel_dict[ctx.guild.id] = channel.id
    await ctx.respond(content = f"Set to {channel.mention}", ephemeral = True)

# Run the bot
bot.run(TOKEN)