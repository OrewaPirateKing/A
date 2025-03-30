import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
def get_env(name, required=True):
    value = os.getenv(name)
    if required and value is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return value

try:
    API_ID = int(get_env('API_ID'))
    API_HASH = get_env('API_HASH')
    STRING_SESSION = get_env('STRING_SESSION')
    GROUP_ID = int(get_env('GROUP_ID'))
    SUDO_USERS = [int(id.strip()) for id in get_env('SUDO_USERS').split(',') if id.strip()]
except ValueError as e:
    print(f"Configuration error: {e}")
    exit(1)

# Initialize client
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
bot_active = False

async def check_messages():
    global bot_active
    while bot_active:
        try:
            messages = await client.get_messages(GROUP_ID, limit=3)
            
            # Check for emojis
            emoji_found = any(
                msg.text and ('🔮' in msg.text or '🎐' in msg.text)
                for msg in messages if hasattr(msg, 'text')
            )
            
            if emoji_found:
                for user_id in SUDO_USERS:
                    await client.send_message(
                        user_id,
                        "A limited 🔮 or celestial 🎐 waifu or Hus has appeared in the group!"
                    )
                bot_active = False
            else:
                await client.send_message(GROUP_ID, "hlo")
                await asyncio.sleep(1)  # Check every second
                
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)

@client.on(events.NewMessage(chats=GROUP_ID))
async def handler(event):
    global bot_active
    if event.sender_id in SUDO_USERS:
        if '/go' in event.raw_text and not bot_active:
            bot_active = True
            await event.reply("✅ Bot activated! Monitoring messages...")
            asyncio.create_task(check_messages())
        elif '/stop' in event.raw_text and bot_active:
            bot_active = False
            await event.reply("🛑 Bot deactivated!")

async def main():
    await client.start()
    print("🤖 User client bot is running...")
    await client.run_until_disconnected()

asyncio.run(main())
