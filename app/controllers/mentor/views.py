from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for
import io
import csv

mentor_bp = Blueprint("mentor", __name__, url_prefix='/mentor')

@mentor_bp.route('/test', methods=['GET'])
def test():
    return "hello world", 200

@mentor_bp.route('/<teamID>', methods=['GET'])
def get_mentor(teamID):
    from app.models import Matches
    display = ''
    row = Matches.query.filter_by(team_id=teamID).first()
    if row:
        display = str(row.mentor_id)
    return display, 200

@mentor_bp.route('/<teamID>/<mentorID>', methods=['POST'])
def add_mentor(teamID, mentorID):
    from app.models import Matches
    display = ''
    row = Matches.query.filter_by(team_id=teamID).first()
    if not row:
        Matches.populate({teamID: mentorID})
        display = str(mentorID)
    return display, 200

@mentor_bp.route('/<teamID>', methods=['POST'])
def update_mentor(teamID):
    from app.models import Matches, MentorResponses, TeamResponses
    data = request.form
    team_email = Matches.query.filter_by(team_id=teamID).first().team_email
    for elem in data:
        mentor_email = MentorResponses.query.filter_by(id=int(data[elem])).first().email
        Matches.populate({teamID: [data[elem], team_email, mentor_email]})
    matches = Matches.query.all()
    mentor = MentorResponses.query.all()
    team = TeamResponses.query.all()
    return render_template('admin.html', matches=matches, mentor=mentor, team=team)

@mentor_bp.route('/delete/<teamID>', methods=['POST'])
def delete_mentor(teamID):
    from app.models import Matches, MentorResponses, TeamResponses
    Matches.delete([teamID])
    matches = Matches.query.all()
    mentor = MentorResponses.query.all()
    team = TeamResponses.query.all()
    return render_template('admin.html', matches=matches, mentor=mentor, team=team), 200

