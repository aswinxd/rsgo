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

sync def fetch_forecast_image():
    # Function to fetch or generate the image link (this should be updated according to your API or scraping method)
    images = ["https://example.com/image1.png", "https://example.com/image2.png", "https://example.com/image3.png"]
    return random.choice(images)

async def post_forecast_message():
    global forecast_history

    # Simulate getting a new forecast (this part should fetch from an actual API or data source)
    forecast_value = round(random.uniform(1.5, 3.0), 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Keep track of the current forecast
    forecast_history.append({
        'forecast': forecast_value,
        'time': timestamp
    })

    # Only keep the last two forecasts for display
    if len(forecast_history) > 2:
        forecast_history = forecast_history[-2:]

    # Previous forecast data
    if len(forecast_history) > 1:
        previous_forecast = forecast_history[-2]
    else:
        previous_forecast = {'forecast': "N/A", 'time': "N/A"}

    # Fetch forecast image (this should connect to the appropriate image source)
    forecast_image_url = await fetch_forecast_image()

    # Format the message with next and previous forecasts
    forecast_message = (
        f"📊 **Next Forecast: {forecast_value}x**\n"
        f"🕒 **Previous Forecast: {previous_forecast['forecast']}x**\n"
        f"⏰ **Time: {timestamp}**\n\n"
        f"![Forecast Image]({forecast_image_url})\n"
        "💡 *Get ready for the next prediction!*"
    )

    # Post the message to the target channel
    await bot.send_message("your_channel_id", forecast_message)

# Command to start the forecasting process
@bot.on_message(filters.command("start_forecast"))
async def start_forecast(client: Client, message: Message):
    await message.reply("Starting forecast updates...")

    # Post forecasts every minute for demonstration (adjust this timing as needed)
    while True:
        await post_forecast_message()
        await asyncio.sleep(60)  # Post every 60 seconds (modify as needed)

if __name__ == "__main__":
    bot.run()
