from pyrogram import Client, filters, idle
import random
import asyncio
from datetime import datetime
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw, ImageFont

API_ID = "7980140"  # Your API ID
API_HASH = "db84e318c6894f560a4087c20c33ce0a"  # Your API Hash
BOT_TOKEN = "6520550784:AAHZPv8eOS2Unc91jIVYSH5PB0z8SO36lUY"  # Your bot token

bot = Client("aviator_betting_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

bet_amount = 1000  # Fixed bet amount
session_times = ["10:00", "11:00", "9:40"]  # Define session start times (customizable)
channels_to_post = ["@anehow", "-1002454896752"]  # Channels to post the messages

round_intervals = 60  # Time between rounds in seconds

# Function to edit image and place bet info
def edit_image(multiplier, winnings):
    img_path = 'rsgo.jpg'  # Your image path
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font.ttf", 30)  # Adjust to your preferred font file

    multiplier_pos = (230, 85)  # Customize position as needed
    winnings_pos = (510, 85)  # Customize position as needed

    # Add text to image
    draw.text(multiplier_pos, f"{multiplier}x", font=font, fill="white")
    draw.text(winnings_pos, f"₹{winnings}", font=font, fill="white")

    # Save the new image with bet information
    edited_image_path = "rspg_edited.jpg"
    img.save(edited_image_path)
    
    return edited_image_path

# Function to generate a random multiplier result for the round
def generate_round_result():
    return round(random.uniform(1.0, 3.0), 2)  # Generate random multiplier between 1.0x and 3.0x

# Function to calculate winnings based on the bet and multiplier
def calculate_winnings(bet, multiplier):
    return round(bet * multiplier, 2)

# Function to run a betting session (5 rounds in each session)
async def run_session():
    total_winnings = {}  # Track total winnings per channel
    for channel in channels_to_post:
        total_winnings[channel] = 0  # Initialize winnings per channel

        # Send session start message
        await bot.send_message(channel, "✅ **Session started!**")
        await asyncio.sleep(1)

        # Simulate 5 rounds of bets
        for _ in range(5):
            multiplier = generate_round_result()
            winnings = calculate_winnings(bet_amount, multiplier)

            # Add winnings to total
            total_winnings[channel] += winnings

            # Post round info to channel
            await bot.send_message(channel, f"🚀 Bet: **{multiplier}x** | Win: ₹{winnings}")
            await asyncio.sleep(2)

            # Edit the image with bet info and post it
            edited_image = edit_image(multiplier, winnings)
            await bot.send_photo(channel, edited_image)

            # Delay for the next round
            await asyncio.sleep(round_intervals)

    # After all rounds, post session summary
    for channel in channels_to_post:
        # Example of a session summary with a custom URL button
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📊 Check Stats", url="https://example.com")]]
        )
        await bot.send_message(channel, f"📊 **Session Summary**: \nTotal winnings after 5 rounds: ₹{total_winnings[channel]}\nSession ended.", reply_markup=markup)

# Function to schedule betting sessions based on defined times
async def schedule_sessions():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in session_times:
            await run_session()
        await asyncio.sleep(60)  # Check every minute

# Command handler for /start
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Welcome to the Aviator Betting Bot! Stay tuned for upcoming sessions.")

# Start the bot and run the session scheduler
async def start_bot():
    await bot.start()
    asyncio.create_task(run_session())  # Start scheduling the betting sessions
    await idle()  # Keep the bot running

if __name__ == "__main__":
    bot.run(start_bot())
