import asyncio
import os
import google.generativeai as genai
from balethon import Client
from balethon.objects import Message

# --- کلیدها و توکن‌ها ---
BALE_TOKEN = os.getenv("BALE_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BALE_TOKEN or not GEMINI_API_KEY:
    raise ValueError("BALE_TOKEN or GEMINI_API_KEY environment variables are not set.")

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

bot = Client(BALE_TOKEN)

MASTER_PROMPT = """
شما یک دستیار آشپزی حرفه‌ای، خلاق و دوست‌داشتنی به نام "آشپزجمینی" هستید. وظیفه شما این است که با دریافت لیستی از مواد اولیه، یک دستور پخت کامل و خوشمزه ارائه دهید.
قوانین شما:
1. فقط و فقط از موادی که کاربر به شما می‌دهد استفاده کنید.
2. لحن شما باید دوستانه و دلگرم‌کننده باشد.
3. دستور پخت باید شامل دو بخش اصلی باشد: "مواد لازم" و "مراحل پخت".
4. مراحل پخت را به صورت شماره‌گذاری شده و واضح توضیح دهید.
5. در انتهای دستور پخت، یک نام خلاقانه و جذاب برای غذا پیشنهاد دهید.
"""

@bot.on_message()
async def message_handler(message: Message):
    if not message.text:
        return

    if message.text == "/start":
        await message.reply("سلام! 👋 من آشپز هوش مصنوعی هستم. هر موادی که تو خونه داری بهم بگو تا یه غذای عالی بهت پیشنهاد بدم.")
        return

    chat_id = message.chat.id
    user_ingredients = message.text

    processing_message = await bot.send_message(chat_id, "عالی! دارم فکر می‌کنم... 🤔🍳")

    try:
        full_prompt = MASTER_PROMPT + f"\n\nمواد اولیه کاربر: '{user_ingredients}'"
        response = await asyncio.to_thread(gemini_model.generate_content, full_prompt)
        text = response.candidates[0].content.parts[0].text
        await message.reply(text)

    except Exception as e:
        print(f"An error occurred: {e}")
        await message.reply("متاسفانه مشکلی در ارتباط با هوش مصنوعی پیش اومد. 😥")

    finally:
        await bot.delete_message(chat_id, processing_message.id)

if __name__ == "__main__":
    print("ربات آشپزجمینی (نسخه Balethon) با موفقیت اجرا شد...")
    bot.run()
