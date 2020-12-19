from models import UsernameRelation
import discord


def get_event_assignees(data):
    user_list = []
    if data['webhookEvent'] == 'comment_created':
        pass
    elif data['webhookEvent'] == 'comment_updated':
        pass
    elif data['webhookEvent'] == 'jira:issue_created':
        pass
    elif data['webhookEvent'] == 'jira:issue_updated':
        pass
    return user_list


def create_comment_created_embed(data):
    embed = discord.Embed(
        title=f'{data["comment"]["author"]["displayName"]} added new comment to {data["issue"]["fields"]["summary"]}',
        description=data['comment']['body'],
        url=data['comment']['self'],
        color=0x27a877
    )
    embed.set_author(
        name=data['comment']['author']['displayName'],
        icon_url=data['comment']['author']['avatarUrls']['32x32'],
        url=data['comment']['author']['self'])
    embed.add_field(
        name="Project", value=data["issue"]["fields"]["project"]["name"], inline=True)
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
        url=data['comment']['self'],
        color=0xfbb829
    )
    embed.set_author(
        name=data['comment']['author']['displayName'],
        icon_url=data['comment']['author']['avatarUrls']['32x32'],
        url=data['comment']['author']['self'])
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
        url=data['issue']['self'],
        color=0x00A0B0
    )
    embed.set_author(
        name=data['user']['displayName'],
        icon_url=data['user']['avatarUrls']['32x32'],
        url=data['user']['self'])
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
        url=data['issue']['self'],
        color=0xE33258
    )
    embed.set_author(
        name=data['user']['displayName'],
        icon_url=data['user']['avatarUrls']['32x32'],
        url=data['user']['self']
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
    if data["changelog"]['items']:
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
            if log['fromString'] is None:
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

            if log['toString'] is None:
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
            if data['webhookEvent'] == 'comment_created':
                embed = create_comment_created_embed(data)
            elif data['webhookEvent'] == 'comment_updated':
                embed = create_comment_edited_embed(data)
            elif data['webhookEvent'] == 'jira:issue_created':
                embed = create_task_created_embed(data)
            elif data['webhookEvent'] == 'jira:issue_updated':
                embed = create_task_edited_embed(data)
            if embed is not None:
                for item in username_relations:
                    user = await bot.fetch_user(int(item.discord_user_id))
                    await user.send(embed=embed)
