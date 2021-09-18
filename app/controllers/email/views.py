from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for
from config import config_settings
import requests
import config
import os

email_bp = Blueprint("email", __name__, url_prefix='/email')

@email_bp.route('/send_emails', methods=['GET'])
def test():
    from app.models import Matches, MentorResponses, TeamResponses
    from app import app
    def send_email(mentor_email, team_email, team_id, mentor_id):
        app.config.from_object(config_settings['production'])
        basedir = os.path.abspath(os.path.dirname(__file__))
        data_file = os.path.join(basedir, 'matching.html')
        HtmlFile = open(data_file, 'r', encoding='utf-8')
        source_code = HtmlFile.read()   
        HtmlFile.close()
        return requests.post(
            "https://api.mailgun.net/v3/my.hackmit.org/messages",
            auth=("api", app.config['MAILGUN_API']),
            data={"from": "HackMIT <mentor@my.hackmit.org>",
                "to": [team_email],
                "cc": [mentor_email],
                "subject": "HackMIT <> Beginner-Mentor Pairing!",
                "html": source_code})

    all_matches = Matches.serialize()
    for row in all_matches:
        send_email(all_matches[row][2], all_matches[row][0], row, all_matches[row][1])
    
    matches = Matches.query.all()
    mentor = MentorResponses.query.all()
    team = TeamResponses.query.all()
    return render_template('admin.html', matches=matches, mentor=mentor, team=team), 200
