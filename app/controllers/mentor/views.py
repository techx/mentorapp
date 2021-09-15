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
    from app.models import Matches
    data = request.form
    print(data)
    for elem in data:
        Matches.populate({teamID: data[elem]})
    matches = Matches.query.all()
    return render_template('admin.html', matches=matches)

@mentor_bp.route('/delete/<teamID>', methods=['POST'])
def delete_mentor(teamID):
    from app.models import Matches
    Matches.delete([teamID])
    matches = Matches.query.all()
    return render_template('admin.html', matches=matches), 200

@mentor_bp.route('/get_responses_mentor', methods=['POST'])
def get_from_csv():
    from app.models import MentorResponses
    content = request.files['csv']
    stream = io.StringIO(content.stream.read().decode("UTF-8"), newline = None)
    csv_input = csv.reader(stream)
    counter = 0
    for elem in csv_input:
        if counter == 0: 
            counter += 1
            continue
        else:
            a = True if elem[5] == 'Virtual' else False
            MentorResponses.populate(elem[1], elem[2], int(elem[3].split(':')[0]), elem[4], a)
            counter += 1
    data = MentorResponses.serialize()
    print(data)
    return "", 200