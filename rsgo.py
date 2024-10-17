from pyrogram import Client, filters, idle
import random
import asyncio
from datetime import datetime
from pyrogram.errors import PeerIdInvalid

API_ID = "7980140"  # Your API ID
API_HASH = "db84e318c6894f560a4087c20c33ce0a"  # Your API Hash
BOT_TOKEN = "6520550784:AAHZPv8eOS2Unc91jIVYSH5PB0z8SO36lUY"  # Your bot token

bot = Client("aviator_betting_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

bet_amount = 1000  # Fixed bet amount
session_times = ["10:00", "11:00", "9:40"]  # Define session start times (You can customize this)
channels_to_post = ["@anehow", "-1002454896752"]  # Add your channel IDs or usernames here

# Function to generate a random multiplier result for the round
def generate_round_result():
    return round(random.uniform(1.0, 3.0), 2)  # Generate random multiplier between 1.0x and 3.0x

# Function to calculate winnings based on the bet and multiplier
def calculate_winnings(bet, multiplier):
    return round(bet * multiplier, 2)

# Function to run a betting session (5 rounds in each session)
async def run_session(session_time):
    for channel in channels_to_post:
        try:
            await bot.send_message(channel, f"🚨 Session started at {session_time} 🚨\nPrepare for the first signal...")
        except PeerIdInvalid:
            print(f"Failed to send message. Invalid Peer ID: {channel}")
            continue

    total_winnings = {channel: 0 for channel in channels_to_post}  # Keep track of winnings per channel

    for round_number in range(1, 6):
        multiplier = generate_round_result()
        winnings = calculate_winnings(bet_amount, multiplier)
        
        for channel in channels_to_post:
            total_winnings[channel] += winnings
            
            try:
                # Post round result
                await bot.send_message(
                    channel,
                    f"✈️ **Round {round_number} Signal**: \n🚀 Bet: ₹{bet_amount}\n🔥 Multiplier: {multiplier}x\n💰 Winnings: ₹{winnings}\nTotal so far: ₹{total_winnings[channel]}"
                )
            except PeerIdInvalid:
                print(f"Failed to send round {round_number} message. Invalid Peer ID: {channel}")
                continue
        
        await asyncio.sleep(5 * 60)  # Wait for 5 minutes between each round

    # Post session summary
    for channel in channels_to_post:
        try:
            await bot.send_message(
                channel,
                f"📊 **Session Summary**: \nTotal winnings after 5 rounds: ₹{total_winnings[channel]}\nSession ended. 🚀"
            )
        except PeerIdInvalid:
            print(f"Failed to send session summary. Invalid Peer ID: {channel}")

# Function to schedule sessions at specific times
async def schedule_sessions():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in session_times:
            await run_session(now)
        await asyncio.sleep(60)  # Check every minute if it's time for the next session

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Welcome to the Aviator Betting Bot! Sessions will be conducted at scheduled times in both public and private channels.\nFixed bet amount: ₹1000.")

async def start_bot():
    await bot.start()
    asyncio.create_task(run_session("Test Session"))
    await run_session("Test Session")
   # asyncio.create_task(schedule_sessions())  # Schedule the betting sessions
#    await idle()

if __name__ == "__main__":
    bot.run(start_bot())
