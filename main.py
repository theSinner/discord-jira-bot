from quart import Quart, make_response, request
from settings import (
    MONGO_DB_NAME,
    MONGO_HOST,
    MONGO_PORT,
    SECRET_KEY,
    DISCORD_TOKEN
)
import mongoengine
import asyncio
import discord
import threading
from controllers.discord import send_message, set_relation, send_embed

client = discord.Client()

conn = mongoengine.connect(
    MONGO_DB_NAME,
    host=MONGO_HOST,
    port=MONGO_PORT
)

app = Quart(__name__)
app.secret_key = SECRET_KEY


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
        try:
            set_relation(
                str(message.author),
                str(message.author.id),
                username
            )
            await message.channel.send('Your account connected to %s jira account successfuly!' % (username))
        except Exception as e:
            await message.channel.send('Something went wrong')
            raise e
    else:
        await message.channel.send('command not found')


@app.before_serving
async def before_serving():
    loop = asyncio.get_event_loop()
    await client.login(DISCORD_TOKEN)
    loop.create_task(client.connect())


@app.route("/callback/jira/<issue_key>", methods=["POST"])
async def callback_jira(issue_key):
    print(await request.get_data())
    username = 'amir2'
    await send_embed(
        client, username, 'salam %s' % username)
    return 'OK', 200


@app.route("/<username>", methods=["GET"])
async def send_msg(username):
    await send_message(
        client, username, 'salam %s' % username)
    return 'OK', 200

app.run(debug=True)
