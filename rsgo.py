from pyrogram import Client, filters, idle
import random
import asyncio
from datetime import datetime
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw, ImageFont
import time
#MDB =
API_ID = "7980140"  
API_HASH = "db84e318c6894f560a4087c20c33ce0a"  
BOT_TOKEN = "6520550784:AAHZPv8eOS2Unc91jIVYSH5PB0z8SO36lUY"  
bot = Client("aviator_betting_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

bet_amount = 1000 
session_times = ["09:00", "11:00", "13:00", "15:00", "17:00", "19:00", "21:00", "23:00"] #international
channels_to_post = ["-1002396190461"] 
round_intervals = 60  
def edit_image(multiplier, winnings):
    img_path = 'rsgo.jpg'  
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font.ttf", 40)  
    multiplier_pos = (230, 86)  
    winnings_pos = (480, 86)  
    draw.text(multiplier_pos, f"{multiplier}x", font=font, fill="white")
    draw.text(winnings_pos, f"₹{winnings}", font=font, fill="white")
    edited_image_path = "rspg_edited.jpg"
    img.save(edited_image_path)
    return edited_image_path
    
def generate_round_result():
    return round(random.uniform(1.0, 3.0), 2) 

def calculate_winnings(bet, multiplier):
    return round(bet * multiplier, 2)
 
def edit_final_summary_image(total_winnings, round_results):
    img_path = 'summary.jpg'  
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("font.ttf", 40)
    smaller_font = ImageFont.truetype("font.ttf", 30)

    summary_pos = (50, 50)  
    final_profits_pos = (40, 500)
    rounds_start_pos = 200  
    round_spacing = 10 
    draw.text((50, 10), "cricket Signal Reports", font=font, fill="white")
    total_winnings_text = f"₹{total_winnings}"
    total_winnings_box = draw.textbbox((200, 50), total_winnings_text, font=font)
    draw.rectangle(total_winnings_box, fill="black")
    draw.rounded_rectangle(total_winnings_box, outline="green", width=3, radius=3)
    draw.text((200, 50), total_winnings_text, font=font, fill="white")
    for i, result in enumerate(round_results):
        round_text = f"{result}"
        round_pos = (30 + i * 100, rounds_start_pos)  
        round_box = draw.textbbox(round_pos, round_text, font=smaller_font)
        draw.rectangle(round_box, fill="black")
        draw.rounded_rectangle(round_box, outline="green", width=3, radius=3)
        draw.text(round_pos, round_text, font=smaller_font, fill="white")
    final_message_text = "final profits from this session"
    draw.text((10, 150), final_message_text, font=font, fill="white")
    oy_image_path = f"summary_ed.jpg"
    img.save(oy_image_path)
    return oy_image_path


async def run_session():
    total_winnings = {}
    round_results = {}
    for channel in channels_to_post:
        total_winnings[channel] = 0
        round_results[channel] = []

        await bot.send_message(channel, "✅ **Session starting round 1 soon**")
        await asyncio.sleep(15)
        for round_num in range(1, 6):
            await bot.send_message(channel, f" **Hold up! Starting round {round_num}...**")
            await asyncio.sleep(15)
            multiplier = generate_round_result()
            winnings = calculate_winnings(bet_amount, multiplier)
            total_winnings[channel] += winnings
            round_results[channel].append(f"{multiplier}x")
            await bot.send_message(channel, f"bet: {multiplier}x")
            await asyncio.sleep(30)
            edited_image = edit_image(multiplier, winnings)
            caption = f"Round {round_num} \nMultiplier: **{multiplier}x**\nWinnings: ₹{winnings}"
            markup = InlineKeyboardMarkup([[InlineKeyboardButton(" Check Stats", url="https://rsgo.win")]])
            await bot.send_photo(channel, edited_image, caption=caption, reply_markup=markup)
            await asyncio.sleep(round_intervals)

          
        final_summary_image = edit_final_summary_image(total_winnings[channel], round_results[channel])
        final_summary = "\n".join(round_results[channel])
        final_message = (
            f"📊 **Session Summary**: \n"
            f"{final_summary}\n"
            f"Total winnings after 5 rounds: ₹{total_winnings[channel]}\n"
            f"Session ended."
        )
        await bot.send_photo(channel, final_summary_image, caption=final_message, reply_markup=markup)


    
   #    ''' final_message = (
        #    f" **Session Summary**: \n"
     #       f"Total winnings after 5 rounds: ₹{total_winnings[channel]}\n"
   ###      await bot.send_photo(channel, final_summary_image, caption=final_message, reply_markup=markup)'''


'''async def run_session():
    total_winnings = {} 
    round_results = {}  

    for channel in channels_to_post:
        total_winnings[channel] = 0
        round_results[channel] = []  
        await bot.send_message(channel, "✅ **Session starting round 1 soon**")
        await asyncio.sleep(15)

        for round_num in range(1, 6):
            await bot.send_message(channel, f"🚀 **Hold up! Starting round {round_num}...**")
            await asyncio.sleep(10)

            multiplier = generate_round_result()
            winnings = calculate_winnings(bet_amount, multiplier)
            total_winnings[channel] += winnings

            round_results[channel].append(f"✅**Round {round_num}  ₹{winnings}**")

            await bot.send_message(channel, f"🚀 Bet: **{multiplier}x**")
            await asyncio.sleep(30)

            edited_image = edit_image(multiplier, winnings)
            caption = f"Round {round_num} 🚀\nMultiplier: **{multiplier}x**\nWinnings: ₹{winnings}"
            markup = InlineKeyboardMarkup([[InlineKeyboardButton("📊 Check Stats", url="https://rsgo.win")]])
            await bot.send_photo(channel, edited_image, caption=caption, reply_markup=markup)

            await asyncio.sleep(round_intervals)

        final_summary = "\n".join(round_results[channel])
        final_message = (
            f"📊 **Session Summary**: \n"
            f"{final_summary}\n"
            f"Total winnings after 5 rounds: ₹{total_winnings[channel]}\n"
            f"Session ended."
        )
        await bot.send_message(channel, final_message, reply_markup=markup)'''

         
async def schedule_sessions():
    while True:
        now = datetime.now().strftime("%H:%M")
        print(f"Current") 
        if now in session_times:
            print(f"Starting")  
            await run_session()
        await asyncio.sleep(30)

@bot.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type == "private":
        await message.reply("Welcome.")
    else:
        await message.reply("Welcome.")
        
async def start_bot():
    await bot.start()
    asyncio.create_task(schedule_sessions()) 
    await idle()  

if __name__ == "__main__":
    bot.run(start_bot())
