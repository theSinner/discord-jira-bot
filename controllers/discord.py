from models import UsernameRelation
import discord
import re
import requests
from settings import JIRA_BASE_URL, JIRA_USER_UNIQUE_KEY


def get_issue_url(issue):
    return f'{JIRA_BASE_URL}/browse/{issue["key"]}'


def get_comment_url(issue, comment):
    return f'{JIRA_BASE_URL}/browse/{issue["key"]}?focusedCommentId={comment["id"]}'


def get_event_assignees(data):
    user_list = []
    event_author = None
    if data['webhookEvent'] == 'comment_created' or data['webhookEvent'] == 'comment_updated':
        message = data['comment']['body']
        pattern = re.compile(r'\[~([a-zA-Z]*)\:(\S*)\]')
        for match in re.finditer(pattern, message):
            user_list.append(match.group(2))
        event_author = data['comment']['author'][JIRA_USER_UNIQUE_KEY]

    elif data['webhookEvent'] == 'jira:issue_created' or data['webhookEvent'] == 'jira:issue_updated':
        event_author = data['user'][JIRA_USER_UNIQUE_KEY]
        if 'watches' in data['issue'] and data['issue']['watches']['watchCount'] > 0:
            watchers_response = requests.get(data['issue']['self']).json()
            if watchers_response:
                for user in watchers_response['watchers']:
                    user_list.append(user[JIRA_USER_UNIQUE_KEY])
    if 'issue' in data:
        if 'assignee' in data['issue']['fields'] and data['issue']['fields']['assignee']:
            user_list.append(data['issue']['fields']
                            ['assignee'][JIRA_USER_UNIQUE_KEY])
        if 'reporter' in data['issue']['fields'] and data['issue']['fields']['reporter']:
            user_list.append(data['issue']['fields']
                            ['reporter'][JIRA_USER_UNIQUE_KEY])

    user_list = list(set(user_list))
    # if event_author and event_author in user_list:
    #     user_list.remove(event_author)
    return user_list


def create_comment_created_embed(data):
    embed = discord.Embed(
        title=f'{data["comment"]["author"]["displayName"]} added new comment to {data["issue"]["fields"]["summary"]}',
        description=data['comment']['body'],
        url=get_comment_url(data['issue'], data['comment']),
        color=0x27a877
    )
    embed.set_author(
        name=data['comment']['author']['displayName'],
        icon_url=data['comment']['author']['avatarUrls']['32x32'])
    embed.add_field(
        name="Project",
        value=data["issue"]["fields"]["project"]["name"],
        inline=True
    )
    embed.add_field(name="Issue", value=data["issue"]["key"], inline=True)
    embed.add_field(
        name="Status", value=data["issue"]["fields"]["status"]["name"], inline=True)
    embed.add_field(
        name="Priority", value=data["issue"]["fields"]["priority"]["name"], inline=True)
    return embed


def create_comment_edited_embed(data):
    embed = discord.Embed(
        title=f'{data["comment"]["author"]["displayName"]} updated a comment in {data["issue"]["fields"]["summary"]}',
        description=data['comment']['body'],
        url=get_comment_url(data['issue'], data['comment']),
        color=0xfbb829
    )
    embed.set_author(
        name=data['comment']['author']['displayName'],
        icon_url=data['comment']['author']['avatarUrls']['32x32'])
    embed.add_field(
        name="Project", value=data["issue"]["fields"]["project"]["name"], inline=True)
    embed.add_field(name="Issue", value=data["issue"]["key"], inline=True)
    embed.add_field(
        name="Status", value=data["issue"]["fields"]["status"]["name"], inline=True)
    embed.add_field(
        name="Priority", value=data["issue"]["fields"]["priority"]["name"], inline=True)
    return embed


def create_task_created_embed(data):
    embed = discord.Embed(
        title=f'{data["user"]["displayName"]} created a new task',
        description=data["issue"]["fields"]["summary"],
        url=get_issue_url(data["issue"]),
        color=0x00A0B0
    )
    embed.set_author(
        name=data['user']['displayName'],
        icon_url=data['user']['avatarUrls']['32x32']
    )
    embed.add_field(
        name="Project", value=data["issue"]["fields"]["project"]["name"], inline=True)
    embed.add_field(name="Issue", value=data["issue"]["key"], inline=True)
    embed.add_field(
        name="Status", value=data["issue"]["fields"]["status"]["name"], inline=True)
    embed.add_field(
        name="Priority", value=data["issue"]["fields"]["priority"]["name"], inline=True)
    if data["issue"]["fields"]["description"]:
        embed.add_field(
            name="Description",
            value=data["issue"]["fields"]["description"],
            inline=False
        )
    if data["issue"]["fields"]["labels"]:
        embed.add_field(
            name="Labels",
            value=', '.join(data["issue"]["fields"]["labels"]),
            inline=True
        )
    if data["issue"]["fields"]["assignee"]:
        embed.add_field(
            name="Assignee",
            value=data["issue"]["fields"]["assignee"]["displayName"],
            inline=True
        )
    if data["issue"]["fields"]["reporter"]:
        embed.add_field(
            name="Reporter",
            value=data["issue"]["fields"]["reporter"]["displayName"],
            inline=True
        )
    return embed


def create_task_edited_embed(data):
    embed = discord.Embed(
        title=f'{data["user"]["displayName"]} updated a task',
        description=data["issue"]["fields"]["summary"],
        url=get_issue_url(data["issue"]),
        color=0xE33258
    )
    embed.set_author(
        name=data['user']['displayName'],
        icon_url=data['user']['avatarUrls']['32x32'],
    )
    embed.add_field(
        name="Project", value=data["issue"]["fields"]["project"]["name"], inline=True)
    embed.add_field(name="Issue", value=data["issue"]["key"], inline=True)
    embed.add_field(
        name="Status", value=data["issue"]["fields"]["status"]["name"], inline=True)
    embed.add_field(
        name="Priority", value=data["issue"]["fields"]["priority"]["name"], inline=True)
    if data["issue"]["fields"]["description"]:
        embed.add_field(
            name="Description",
            value=data["issue"]["fields"]["description"],
            inline=False
        )
    if data["issue"]["fields"]["labels"]:
        embed.add_field(
            name="Labels",
            value=', '.join(data["issue"]["fields"]["labels"]),
            inline=True
        )
    if data["issue"]["fields"]["assignee"]:
        embed.add_field(
            name="Assignee",
            value=data["issue"]["fields"]["assignee"]["displayName"],
            inline=True
        )
    if data["issue"]["fields"]["reporter"]:
        embed.add_field(
            name="Reporter",
            value=data["issue"]["fields"]["reporter"]["displayName"],
            inline=True
        )
    if "changelog" in data and "items" in data['changelog'] and data["changelog"]['items']:
        embed.add_field(
            name="Change logs",
            value='‌',
            inline=False
        )
        for log in data["changelog"]['items']:
            embed.add_field(
                name="Field",
                value=log['field'].capitalize(),
                inline=True
            )
            if not log['fromString']:
                embed.add_field(
                    name="From",
                    value='Unassigned' if log['field'] == 'assignee' else 'Null',
                    inline=True
                )
            else:
                embed.add_field(
                    name="From",
                    value=log['fromString'],
                    inline=True
                )

            if not log['toString']:
                embed.add_field(
                    name="To",
                    value='Unassigned' if log['field'] == 'assignee' else 'Null',
                    inline=True
                )
            else:
                embed.add_field(
                    name="To",
                    value=log['toString'],
                    inline=True
                )
    return embed


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


def delete_relation(discord_user_id):
    UsernameRelation.objects.filter(
        discord_user_id=discord_user_id
    ).delete()

async def send_message(bot, jira_username, msg):
    username_relation = UsernameRelation.objects.filter(
        jira_username=jira_username
    ).first()
    if username_relation:
        user = await bot.fetch_user(int(username_relation.discord_user_id))
        await user.send(msg)


async def send_event(bot, data):
    assignees = get_event_assignees(data)
    username_relations = UsernameRelation.objects.filter(
        jira_username__in=assignees
    ).all()
    if username_relations:
        if data and data['webhookEvent']:
            embed = None
            if data['webhookEvent'] == 'comment_created' or (
                data['webhookEvent'] == 'jira:issue_updated' and\
                data["issue_event_type_name"] == "issue_commented"
            ):
                embed = create_comment_created_embed(data)
            elif data['webhookEvent'] == 'comment_updated' or (
                data['webhookEvent'] == 'jira:issue_updated' and\
                data["issue_event_type_name"] == "issue_comment_edited"
            ):
                embed = create_comment_edited_embed(data)
            elif data['webhookEvent'] == 'jira:issue_created':
                embed = create_task_created_embed(data)
            elif data['webhookEvent'] == 'jira:issue_updated' and\
                 data["issue_event_type_name"] == "issue_updated":
                embed = create_task_edited_embed(data)
            if embed is not None:
                for item in username_relations:
                    user = await bot.fetch_user(int(item.discord_user_id))
                    await user.send(embed=embed)
