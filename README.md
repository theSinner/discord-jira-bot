# DISCORD JIRA BOT

It's a bot for the Discord platform to send tasks and comments (create and update) to people who should see them. :D

## Getting Started

### Create Discord Bot
First of all, you should create a Discord bot. To do this, you can follow this instruction or just search "How to create a discord bot".
After creating the bot, you should add it to your Discord server.

### Jira API Key
To get the updates and push them in Discord, we need to create a WebHook. This is a little bit different in various Jira versions, but generally, it is in the System settings and Advanced sections.
Create a new WebHook, add your needed permissions, and point it to your desired URL.

### Setting Variables
Here are the variables you should put in the environment variable:

#### JIRA_BASE_URL
This is your Jira base URL. If you use the Jira cloud, it's like `https://xxxxxx.atlassian.net/`

#### JIRA_USER_UNIQUE_KEY
It defines your unique id in Jira. Usually, it's `name` or `accountId`. If you use the Jira cloud, it's `accountId` by default.

#### DISCORD_TOKEN
The token you got from Discord API Portal.

#### Run
You can run it using docker-compose:

`$ docker-compose up -d`


### How to use
After running your bot, every user who wants the notifications in Discord needs to start a chat with the bot and send this message:

`/setusername YOUR_USER_UNIQUE_KEY`

YOUR_USER_UNIQUE_KEY is the user's unique key. The unique key is based on what you set in the `JIRA_USER_UNIQUE_KEY` variable.

For example, if you set `JIRA_USER_UNIQUE_KEY='accountId'`, users should replace their accountId value with the `YOUR_USER_UNIQUE_KEY` in the message.

### Contribute
It's a newborn project and needs a lot of changes to be perfect. Feel free to open a PR and make it better!
