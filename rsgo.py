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

def add_text_to_image(image_path, multiplier, winnings):
    # Open the image
    image = Image.open(image_path)

    # Define a font and size (use any appropriate font you want)
    font = ImageFont.truetype("font.ttf", 40)
    draw = ImageDraw.Draw(image)

    # Define text to add
    multiplier_text = f"1.3x"
    winnings_text = f"Win ₹{winnings}"

    # Add multiplier and winnings text at the respective positions
    draw.text((50, 50), multiplier_text, font=font, fill="white")  # Adjust the position as needed
    draw.text((50, 150), winnings_text, font=font, fill="white")

    # Save the modified image
    edited_image_path = "rspg.jpg"  # Set the correct path
    image.save(edited_image_path)

    return edited_image_path# Add your channel IDs or usernames here

# Function to generate a random multiplier result for the round
def generate_round_result():
    return round(random.uniform(1.0, 3.0), 2)  # Generate random multiplier between 1.0x and 3.0x

# Function to calculate winnings based on the bet and multiplier
def calculate_winnings(bet, multiplier):
    return round(bet * multiplier, 2)

# Function to run a betting session (5 rounds in each session)
async def run_session(session_time):
    for channel in channels_to_post:
        # Announce session start
        await bot.send_message(channel, f"🚨 Session started at {session_time} 🚨\nPrepare for the first signal...")
        await asyncio.sleep(1)  

        total_winnings = {channel: 0 for channel in channels_to_post}  

        for round_number in range(1, 6):
            multiplier = generate_round_result()
            winnings = calculate_winnings(bet_amount, multiplier)

            for channel in channels_to_post:
                total_winnings[channel] += winnings

                await bot.send_message(channel, f"✈️ **Round {round_number} Signal**: Bet {multiplier}x")
                await asyncio.sleep(1) 
                
                edited_image_path = add_text_to_image("rspg.jpg", multiplier, winnings)
                
                await bot.send_photo(channel, photo=edited_image_path)

            await asyncio.sleep(60) 

        for channel in channels_to_post:
            await bot.send_message(
                channel,
                f"📊 **Session Summary**: \nTotal winnings after 5 rounds: ₹{total_winnings[channel]}\nSession ended. 🚀"
            )
async def schedule_sessions():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in session_times:
            await run_session(now)
        await asyncio.sleep(60)  

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
