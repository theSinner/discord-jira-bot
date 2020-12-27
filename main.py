from quart import Quart, make_response, request
from settings import (
    MONGO_DB_NAME,
    MONGO_HOST,
    MONGO_PORT,
    SECRET_KEY,
    DISCORD_TOKEN,
    DEBUG
)
import mongoengine
import asyncio
from discord.ext import commands
import threading
import json
from controllers.discord import send_message, set_relation, send_event

bot = commands.Bot(command_prefix='$')

conn = mongoengine.connect(
    MONGO_DB_NAME,
    host=MONGO_HOST,
    port=MONGO_PORT
)

app = Quart(__name__)
app.secret_key = SECRET_KEY


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='setusername')
async def _list(ctx, arg):
    await ctx.send(arg)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    content = message.content
    print(content)
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


# @app.before_serving
# async def before_serving():
#     loop = asyncio.get_event_loop()
#     await bot.login(DISCORD_TOKEN)
#     loop.create_task(bot.connect())


@app.route("/callback/jira/<issue_key>", methods=["POST"])
async def callback_jira(issue_key):
    data = json.loads(await request.get_data())
    await send_event(
        bot,
        data
    )
    return 'OK', 200


@app.route("/<username>", methods=["GET"])
async def send_msg(username):
    await send_message(
        bot, username, 'salam %s' % username)
    return 'OK', 200


bot.loop.create_task(app.run_task('0.0.0.0', debug=DEBUG))

bot.run(DISCORD_TOKEN)
