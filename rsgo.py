from pyrogram import Client, filters, idle
import random
import time
import asyncio
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
import asyncio
from datetime import datetime, timedelta
import random

# Define session settings
SESSION_INTERVAL = 60 * 60  # Sessions are every hour (3600 seconds)
ROUNDS_PER_SESSION = 5
ROUND_INTERVAL = 300  # 5 minutes between each round
BET_AMOUNT = 1000  # Fixed bet amount for each round

# Store ongoing sessions and results
sessions = {}
results = {}

# Initialize the bot (Replace with your API details)
api_id = '7980140'
api_hash = 'db84e318c6894f560a4087c20c33ce0a'
bot_token = '6520550784:AAHZPv8eOS2Unc91jIVYSH5PB0z8SO36lUY'

bot = Client("betting_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

async def generate_result():
    """Generate a random result for each round."""
    return round(random.uniform(1.5, 3.0), 2)

async def run_round(session_id, channel_id):
    """Run a single round of betting."""
    round_result = await generate_result()
    win_amount = round(BET_AMOUNT * round_result, 2)
    result_msg = f"✈️ BET ✈️\nMultiplier: {round_result}x\n\n💰 Win: ₹{win_amount} 💰"
    
    # Post result to the channel
    await bot.send_message(chat_id=channel_id, text=result_msg)
    return win_amount

async def run_session(channel_id):
    """Conducts a full session with multiple rounds."""
    session_id = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sessions[channel_id] = session_id
    session_winnings = 0

    for round_num in range(1, ROUNDS_PER_SESSION + 1):
        await bot.send_message(chat_id=channel_id, text=f"🚨 PREPARE FOR SIGNAL {round_num} 🚨")
        await asyncio.sleep(2)  # Simulate a small delay before the round starts
        round_win = await run_round(session_id, channel_id)
        session_winnings += round_win
        await asyncio.sleep(ROUND_INTERVAL)  # Wait before the next round

    # Post session summary
    summary_msg = f"🏆 Session Summary 🏆\nTotal Winnings: ₹{session_winnings}\n\n{ROUNDS_PER_SESSION} Rounds Completed."
    await bot.send_message(chat_id=channel_id, text=summary_msg)

async def scheduler():
    """Continuously run sessions at set intervals."""
    while True:
        now = datetime.now()
        next_session_time = (now + timedelta(seconds=SESSION_INTERVAL)).strftime('%H:%M:%S')
        for channel_id in sessions.keys():
            await bot.send_message(chat_id=channel_id, text=f"⏳ Next session will start at {next_session_time}")
            await asyncio.sleep(SESSION_INTERVAL)
            await run_session(channel_id)

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Welcome to the Aviator Bot!\nUse /set_channel to configure a channel for sessions.")

@bot.on_message(filters.command("set_channel") & filters.private)
async def set_channel(client, message):
    """Allows the user to set a channel where the bot will post."""
    try:
        channel_id = int(message.text.split()[1])
        sessions[channel_id] = None  # No session yet
        await message.reply(f"Channel ID {channel_id} set! Sessions will be conducted here.")
    except (IndexError, ValueError):
        await message.reply("Invalid format! Use: /set_channel <channel_id>.")

@bot.on_message(filters.command("start_session") & filters.private)
async def start_session(client, message):
    """Manually start a betting session."""
    try:
        channel_id = int(message.text.split()[1])
        if channel_id not in sessions:
            await message.reply("Channel not set! Use /set_channel first.")
            return
        await message.reply("Starting session...")
        await run_session(channel_id)
    except (IndexError, ValueError):
        await message.reply("Invalid format! Use: /start_session <channel_id>.")

@bot.on_message(filters.command("status") & filters.private)
async def status(client, message):
    """Check the status of sessions."""
    status_msg = "Current Active Sessions:\n"
    for channel_id, session_id in sessions.items():
        if session_id:
            status_msg += f"Channel {channel_id}: Session {session_id} ongoing.\n"
        else:
            status_msg += f"Channel {channel_id}: No session running.\n"
    await message.reply(status_msg)

@bot.on_message(filters.command("stop_session") & filters.private)
async def stop_session(client, message):
    """Stop all active sessions."""
    sessions.clear()
    await message.reply("All sessions stopped.")

if __name__ == "__main__":
    # Start the scheduler and bot
    asyncio.get_event_loop().create_task(scheduler())
    bot.run()
