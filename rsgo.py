from pyrogram import Client, filters, idle
import random
import asyncio
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = "7980140"  # Your API ID
API_HASH = "db84e318c6894f560a4087c20c33ce0a"  # Your API Hash
BOT_TOKEN = "6520550784:AAHZPv8eOS2Unc91jIVYSH5PB0z8SO36lUY"  # Your bot token

bot = Client("aviator_betting_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

bet_amount = 1000  # Fixed bet amount
session_times = ["10:00", "11:00", "9:40"]  # Define session start times (You can customize this)
channels_to_post = ["@anehow", "-1002454896752"]

# Function to generate a random multiplier result for the round
def generate_round_result():
    return round(random.uniform(1.0, 3.0), 2)  # Generate random multiplier between 1.0x and 3.0x

# Function to calculate winnings based on the bet and multiplier
def calculate_winnings(bet, multiplier):
    return round(bet * multiplier, 2)

# Function to run a betting session (5 rounds in each session)
async def run_session():
    for channel in channels_to_post:
        # Send session start message
        await bot.send_message(channel, "✅ **Session started!**")

        await asyncio.sleep(1)

        # Simulate bet and result posting
        multiplier = generate_round_result()  # Example multiplier
        winnings = calculate_winnings(bet_amount, multiplier)

        # Use the online image link and format the message with winnings
        image_url = 'https://i.ibb.co/VxTXbYD/image.jpg'  # Using the provided image link
        caption = f"🚀 **Multiplier**: {multiplier}x\n💸 **Winnings**: ₹{winnings}"

        # Send the image with the caption
        await bot.send_photo(channel, image_url, caption=caption)

        # Delay for the next round (e.g., 60 seconds)
        await asyncio.sleep(60)

    # After all rounds, post session summary
    for channel in channels_to_post:
        # Example of a session summary with custom URL button
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📊 Check Stats", url="https://example.com")]]
        )
        await bot.send_message(channel,  f"📊 **Session Summary**: \nTotal winnings after 5 rounds: ₹{winnings}\nSession ended.", reply_markup=markup)

async def schedule_sessions():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in session_times:
            await run_session()
        await asyncio.sleep(60)  

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Welcome to the Aviator Betting Bot!")

async def start_bot():
    await bot.start()
    asyncio.create_task(run_session())  # No arguments needed here
    await idle()

if __name__ == "__main__":
    bot.run(start_bot())
