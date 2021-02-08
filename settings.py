import os

DEBUG = os.getenv('DEBUG', 'false') == 'true'
SECRET_KEY = os.getenv('SECRET_KEY')

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'discord_jira_bot')
MONGO_HOST = os.getenv('MONGO_HOST', 'mongo')
MONGO_PORT = int(os.getenv('MONGO_PORT', '27017'))
JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_USER_UNIQUE_KEY = os.getenv('JIRA_USER_UNIQUE_KEY', 'accountId')
