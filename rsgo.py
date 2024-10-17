from pyrogram import Client, filters, idle
import random
import time
import asyncio
from PIL import Image, ImageDraw, ImageFont

API_ID = "7980140"
API_HASH = "db84e318c6894f560a4087c20c33ce0a"
BOT_TOKEN = "6520550784:AAHZPv8eOS2Unc91jIVYSH5PB0z8SO36lUY"

bot = Client("aviator_forecast_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

previous_results = []

def generate_forecast():
    if len(previous_results) > 2:
        previous_results.pop(0)
    next_multiplier = round(random.uniform(1.0, 2.0), 2)  # You can adjust the range as needed
    previous_results.append(next_multiplier)
    return next_multiplier

def create_forecast_image(forecast, previous_results, win_amount):
    # Create an image with the forecast data, like in the screenshot
    img = Image.new('RGB', (600, 300), color=(0, 0, 0))  # Black background
    draw = ImageDraw.Draw(img)

    # Load a custom font
    font = ImageFont.truetype("font.ttf", 40)

    # Add the bet details and previous results, similar to the screenshot
    draw.text((50, 50), f"✈️ BET ✈️", fill="white", font=font)
    draw.text((50, 120), f"💥 Next forecast: {forecast}x", fill="white", font=font)
    draw.text((50, 190), f"You have cashed out 💰\nWin: ₹{win_amount}", fill="green", font=font)

    img.save("forecast_image.png")

    return "forecast_image.png"

async def auto_post_forecast():
    while True:
        forecast = generate_forecast()
        win_amount = round(random.uniform(1000, 3000), 2)  # You can adjust the range as needed
        image_path = create_forecast_image(forecast, previous_results, win_amount)

        # Post the image and message
        await bot.send_photo(chat_id="@your_channel_or_group_id", 
                             photo=image_path, 
                             caption=f"✈️ BET ✈️\n💥 Next forecast: {forecast}x\n\nYou have cashed out 💰\nWin: ₹{win_amount}\n\n[Register](https://your-website-link)", 
                             parse_mode="Markdown")

        await asyncio.sleep(60)  # Adjust the posting interval

@bot.on_message(filters.command("forecast") & filters.private)
async def send_forecast(client, message):
    forecast = generate_forecast()
    win_amount = round(random.uniform(1000, 3000), 2)  # Random win amount for demonstration
    image_path = create_forecast_image(forecast, previous_results, win_amount)

    await message.reply_photo(photo=image_path, caption=f"✈️ BET ✈️\n💥 Next forecast: {forecast}x\n\nYou have cashed out 💰\nWin: ₹{win_amount}")

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("Welcome to the Aviator Forecast Bot! Use /forecast to get the next forecast.")

async def start_forecast_posting():
    await bot.start()
    asyncio.create_task(auto_post_forecast())
    await idle()

if __name__ == "__main__":
    bot.run(start_forecast_posting())
