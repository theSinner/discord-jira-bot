import os
import random
import discord


TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content
    if content.startswith('/setusername'):
        username = content.replace('/setusername', '').strip()
        await message.channel.send('ok, %s' % (username))
    else:
        await message.channel.send('command not found')

client.run(TOKEN)

