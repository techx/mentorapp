from config import config_settings
from app import app
import requests

def send_email(email_type, mentor_email, team_emails):
    app.config.from_object(config_settings['production'])
    return requests.post(
        "https://api.mailgun.net/v3/my.hackmit.org/messages",
        auth=("api", app.config['MAILGUN_API']),
        data={"from": "Test User <mentor@my.hackmit.org>",
              "to": ["awzhang@mit.edu", "azhang581@gmail.com"],
              "subject": "test matches",
              "text": "eeeeeeeee"})