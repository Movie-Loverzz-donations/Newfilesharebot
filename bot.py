#(©)Codexbotz @Codeflix_Bots

from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
import logging

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCESUB_CHANNEL, FORCESUB_CHANNEL2, FORCESUB_CHANNEL3, CHANNEL_ID, PORT

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="my_bot",  # Add a name for the bot
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TG_BOT_TOKEN,
            workers=TG_BOT_WORKERS
        )
        self.LOGGER = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        print(f"Bot started as {usr_bot_me.username}")

        # Handle Force Sub Channel links
        await self.handle_force_sub_channels()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER.warning(e)
            self.LOGGER.warning(f"Make sure bot is Admin in DB Channel, and double-check the CHANNEL_ID value. Current value: {CHANNEL_ID}")
            self.LOGGER.info("\nBot stopped. Join https://t.me/weebs_support for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER.info(f"Bot running..!\n\nCreated by \nhttps://t.me/Animes_X_Hunters")
        self.LOGGER.info(r""" \n\n       
  _____ ____  _____  ______ ______ _      _______   ______   ____ _______ _____ 
 / ____/ __ \|  __ \|  ____|  ____| |    |_   _\ \ / /  _ \ / __ \__   __/ ____|
| |   | |  | | |  | | |__  | |__  | |      | |  \ V /| |_) | |  | | | | | (___  
| |   | |  | | |  | |  __| |  __| | |      | |   > < |  _ <| |  | | | |  \___ \ 
| |___| |__| | |__| | |____| |    | |____ _| |_ / . \| |_) | |__| | | |  ____) |
 \_____\____/|_____/|______|_|    |______|_____/_/ \_\____/ \____/  |_| |_____/ 
                                                                                
                                                                                
                                          """)
        self.username = usr_bot_me.username

        # Web response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

        # Keep the bot running
        await self.idle()

    async def handle_force_sub_channels(self):
        # Handle Force Sub Channel 1
        if FORCESUB_CHANNEL:
            await self.export_invite_link(FORCESUB_CHANNEL)

        # Handle Force Sub Channel 2
        if FORCESUB_CHANNEL2:
            await self.export_invite_link(FORCESUB_CHANNEL2)

        # Handle Force Sub Channel 3
        if FORCESUB_CHANNEL3:
            await self.export_invite_link(FORCESUB_CHANNEL3)

    async def export_invite_link(self, channel_id):
        try:
            link = (await self.get_chat(channel_id)).invite_link
            if not link:
                await self.export_chat_invite_link(channel_id)
                link = (await self.get_chat(channel_id)).invite_link
            setattr(self, f"invitelink{'' if channel_id == FORCESUB_CHANNEL else '2' if channel_id == FORCESUB_CHANNEL2 else '3'}", link)
        except Exception as e:
            self.LOGGER.warning(e)
            self.LOGGER.warning("Bot can't export invite link from Force Sub Channel!")
            self.LOGGER.warning(f"Please double-check the {channel_id} value and make sure the bot is admin in the channel with invite users via link permission. Current Force Sub Channel Value: {channel_id}")
            self.LOGGER.info("\nBot stopped. Join https://t.me/weebs_support for support")
            sys.exit()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER.info("Bot stopped.")

    def run(self):
        import asyncio
        try:
            asyncio.run(self.start())  # Ensure this is called appropriately
        except (KeyboardInterrupt, SystemExit):
            self.LOGGER.info("Bot stopped manually.")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
