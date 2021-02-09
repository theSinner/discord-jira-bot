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
from controllers.discord import (
    send_message,
    set_relation,
    send_event,
    delete_relation
)

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

@bot.command(name='connect')
async def connect(context, username):
    try:
        set_relation(
            str(context.author),
            str(context.author.id),
            username
        )
        await context.send('Your account connected to %s jira account successfuly!' % (username))
    except Exception as e:
        await context.send('Something went wrong')
        raise e

@bot.command(name='disconnect')
async def disconnect(context):
    try:
        delete_relation(
            str(context.author.id),
        )
        await context.send('Your account disconnected successfuly!')
    except Exception as e:
        await context.send('Something went wrong')
        raise e

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
