from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import os

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
STRING_SESSION = os.getenv('STRING_SESSION')
GROUP_ID = int(os.getenv('GROUP_ID'))
SUDO_USERS = [int(id) for id in os.getenv('SUDO_USERS').split(',')]

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
bot_active = False

async def check_messages():
    global bot_active
    while bot_active:
        try:
            messages = await client.get_messages(GROUP_ID, limit=3)
            emoji_found = any(
                msg.text and ('🔮' in msg.text or '🎐' in msg.text)
                for msg in messages if hasattr(msg, 'text')
            )
            
            if emoji_found:
                for user_id in SUDO_USERS:
                    await client.send_message(
                        user_id,
                        "A limited 🔮 or celestial 🎐 waifu or Hus has appeared!"
                    )
                bot_active = False
            else:
                await client.send_message(GROUP_ID, "hlo")
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(1)

@client.on(events.NewMessage(chats=GROUP_ID))
async def handler(event):
    global bot_active
    if event.sender_id in SUDO_USERS:
        if '/go' in event.raw_text and not bot_active:
            bot_active = True
            await event.reply("Bot activated!")
            asyncio.create_task(check_messages())
        elif '/stop' in event.raw_text and bot_active:
            bot_active = False
            await event.reply("Bot deactivated!")

async def main():
    await client.start()
    print("Bot is running...")
    await client.run_until_disconnected()

asyncio.run(main())
