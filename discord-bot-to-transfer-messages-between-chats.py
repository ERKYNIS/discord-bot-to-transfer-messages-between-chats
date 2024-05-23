"""
Discord Bot создал nekitbelkin (https://taplink.cc/nekitbelkin)
"""

import configparser
import discord
import logging
import os
import requests
from datetime import datetime
from pprint import pprint

logging.getLogger().setLevel(logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

config = configparser.RawConfigParser()
config.sections()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'), encoding="utf-8")


@client.event
async def on_ready():
    logging.info(f'[BOT] Бот авторизовался как {client.user}')
    await client.wait_until_ready()


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.channel.id == int(config['BOT']['from_channel']):
        files = []
        for file in message.attachments:
            with open(f'files/{file.id}_' + file.filename, "wb+") as f:
                f.write(requests.get(file.url).content)
            files.append(discord.File(f'files/{file.id}_' + file.filename))
            f.close()
        await client.get_channel(int(config['BOT']['to_channel'])).send(content=message.content,
                                                                        files=files, embeds=message.embeds)

        for file in message.attachments:
            os.remove(f'files/{file.id}_' + file.filename)


if __name__ == "__main__":
    client.run(config['BOT']['token'])
