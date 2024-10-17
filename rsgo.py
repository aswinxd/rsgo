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
channels_to_post = ["@anehow", "-1002454896752"]

from PIL import Image, ImageDraw, ImageFont

# Function to edit image and place bet info
def edit_image(multiplier, winnings):
    img_path = 'rspg.jpg'  # Your image path
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font.ttf", 36)  # Adjust to your preferred font file

    # Coordinates for text placement (adjust these values as per your image layout)
    multiplier_pos = (240, 30)  # Multiplier on the first rectangle
    winnings_pos = (240, 140)   # Winnings on the second rectangle
    
    # Text content
    multiplier_text = f"{multiplier}x"
    winnings_text = f"₹{winnings}"

    # Add text to image in the appropriate positions
    draw.text(multiplier_pos, multiplier_text, font=font, fill="white")
    draw.text(winnings_pos, winnings_text, font=font, fill="white")

    # Save the new image with bet information
    edited_image_path = "rspg.jpg"
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
    for channel in channels_to_post:
        # Send session start message
        await bot.send_message(channel, "✅ **Session started!**")

        await asyncio.sleep(1)

        # Simulate bet and result posting
        multiplier = 1.6  # Example multiplier
        winnings = bet_amount * multiplier

        await bot.send_message(channel, f"🚀 Bet: **{multiplier}x**")

        await asyncio.sleep(2)

        # Edit the image with bet info and post it
        edited_image = edit_image(multiplier, winnings)
        await bot.send_photo(channel, edited_image)

        # Delay for next round (60 seconds for example)
        await asyncio.sleep(round_intervals)

    # After all rounds, post session summary
    for channel in channels_to_post:
        # Example of a session summary with custom URL button
        markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📊 Check Stats", url="https://example.com")]]
        )
        await bot.send_message(channel,  f"📊 **Session Summary**: \nTotal winnings after 5 rounds: ₹{total_winnings[channel]}\nSession ended.", reply_markup=markup)

async def schedule_sessions():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in session_times:
            await run_session(now)
        await asyncio.sleep(60)  

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Welcome")

async def start_bot():
    await bot.start()
    asyncio.create_task(run_session())  # No arguments
    await idle()
  #  await run_session("Test Session")
   # asyncio.create_task(schedule_sessions())  # Schedule the betting sessions
#    await idle()

if __name__ == "__main__":
    bot.run(start_bot())
