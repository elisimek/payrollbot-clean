import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta, UTC
import os
from dotenv import load_dotenv

# Load environment variables from Render or .env please savegit s
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1091068729779040397
ROLE_ID = 1386865314205138954

# Scheduled time: July 5, 2025 at 7:00 PM UTC
START_TIME = datetime(2025, 7, 5, 19, 0, 0, tzinfo=UTC)
next_scheduled_time = START_TIME

# Constants
TWO_WEEKS_IN_SECONDS = 14 * 24 * 60 * 60

# Discord setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    global next_scheduled_time
    print(f"✅ Logged in as {bot.user}")

    # Adjust next_scheduled_time in case of restarts
    now = datetime.now(UTC)
    while next_scheduled_time <= now:
        next_scheduled_time += timedelta(seconds=1209600)

    print(f"🗓️ Next scheduled reminder at: {next_scheduled_time}")
    biweekly_reminder.start()

@tasks.loop(seconds=TWO_WEEKS_IN_SECONDS)
async def biweekly_reminder():
    global next_scheduled_time
    now = datetime.now(UTC).replace(second=0, microsecond=0)

    # Send the message if we're within the target window
    if 0 <= (now - next_scheduled_time).total_seconds() < 60:
        try:
            channel = await bot.fetch_channel(CHANNEL_ID)
            await channel.send(
                f"<@&{ROLE_ID}> 🚨🚨🚨URGENT🚨🚨🚨 \n🕛 Please be sure all payroll information is correct and up to date by midnight tonight!!\n\n‼️ For every individual day you worked that is incorrectly logged, email siddharth@paradigmrobotics.tech:\n\n1) mm/dd\n2) all start/stop times for that day\n\n💕 Thank you!! 💕",
                allowed_mentions=discord.AllowedMentions(roles=True)
            )
            print(f"📤 Reminder sent at {now}")
        except Exception as e:
            print(f"❌ Failed to send reminder: {e}")

        # Schedule the next run
        next_scheduled_time += timedelta(seconds=1209600)
        print(f"🗓️ Next reminder scheduled for: {next_scheduled_time}")

bot.run(TOKEN)