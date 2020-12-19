from models import UsernameRelation
import discord


def create_comment_embed(data):
    pass


def create_task_embed(data):
    pass


def set_relation(discord_username, discord_user_id, jira_username):
    jira_already_exists = UsernameRelation.objects.filter(
        jira_username=jira_username,
        discord_user_id__ne=discord_user_id
    ).first()
    if jira_already_exists:
        raise Exception

    discord_already_exists = UsernameRelation.objects.filter(
        discord_username=discord_username
    ).first()

    if discord_already_exists:
        discord_already_exists.jira_username = jira_username
        discord_already_exists.save()
        return
    else:
        relation = UsernameRelation(
            discord_user_id=discord_user_id,
            discord_username=discord_username,
            jira_username=jira_username
        )
        relation.save()


async def send_message(bot, jira_username, msg):
    username_relation = UsernameRelation.objects.filter(
        jira_username=jira_username
    ).first()
    if username_relation:
        user = await bot.fetch_user(int(username_relation.discord_user_id))
        await user.send(msg)


async def send_embed(bot, jira_username, msg):
    username_relation = UsernameRelation.objects.filter(
        jira_username=jira_username
    ).first()
    if username_relation:
        user = await bot.fetch_user(int(username_relation.discord_user_id))
        embed = discord.Embed(
            title=msg, description="Desc", color=0x00ff00)
        embed.add_field(name="Field1", value="hi", inline=False)
        embed.add_field(name="Field2", value="hi2", inline=False)
        await user.send(embed=embed)
