from mongoengine import StringField, Document


class UsernameRelation(Document):
    discord_user_id = StringField(required=True)
    discord_username = StringField(required=True)
    jira_username = StringField(required=True, unique=True)
