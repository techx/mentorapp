from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for
import io
import csv

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')


@admin_bp.route('/reset', methods=['GET'])
def reset():
    from app.models import Matches, MentorResponses, TeamResponses
    Matches.deleteAll()
    MentorResponses.deleteAll()
    TeamResponses.deleteAll()
    matches = Matches.query.all()
    team = TeamResponses.query.all()
    mentor = MentorResponses.query.all()
    return render_template('admin.html', matches=matches, team=team, mentor=mentor), 200

@admin_bp.route('/match', methods=['GET'])
def match():
    from app.models import Matches, TeamResponses, MentorResponses

    def create_numerical_rankings(team_prefs, mentor_prefs): 
        # team_prefs {'A': {'commitment': _, 'expertise': _, 'in person': _}, 'B': ...}
        # mentor_prefs {'a': {'commitment': _, 'expertise': _, 'in person': _}, 'b': ...}
        commitment_difference = [0, 1, 2, 3, -1, -2, -3]
        team_order = {}
        for team in team_prefs:
            team_order[team] = []
            mediocre_prefs = []
            for i in commitment_difference:
                commitment_level = team_prefs[team]["commitment"] + i
                in_person_team = team_prefs[team]['virtual']
                for mentor in mentor_prefs:
                    in_person_mentor = mentor_prefs[mentor]['virtual']
                    shared_expertise = team_prefs[team]['interest'] & mentor_prefs[mentor]['interest']
                    if (mentor_prefs[mentor]["commitment"] == commitment_level) and len(shared_expertise) and (in_person_team == in_person_mentor):
                        team_order[team].append(mentor)
                    elif (mentor_prefs[mentor]["commitment"] == commitment_level):
                        mediocre_prefs.append(mentor)
            team_order[team] += mediocre_prefs

        return team_order

    def compare_pref(mentor_order, current_team, alt_team, mentor):
        for team in mentor_order[mentor]:
            if team == current_team:
                return True
            if team == alt_team:
                return False
        return False

    def other_prefer(team, mentor, matches):
        for team1 in matches:
            if matches[team1] == mentor and team1 != team:
                return team1
        return team

    def stable_matching(team_order, mentor_order):
        matches = {}
        team_free = set(team_order.keys())
        mentor_free = set(mentor_order.keys())
        team_proposed = {team: set() for team in team_order}
        while len(team_free) > 0:
            current_team = team_free.pop()
            team_free.add(current_team)
            potential_mentor = None
            for mentor in team_order[current_team]:
                if mentor not in team_proposed[current_team]:
                    potential_mentor = mentor
                    break
            if potential_mentor == None:
                break
            team_proposed[current_team].add(potential_mentor)
            alt_team= other_prefer(current_team, potential_mentor, matches) 
            if alt_team != current_team:
                if compare_pref(mentor_order, current_team, alt_team, potential_mentor):
                    team_free.add(alt_team)
                    matches.pop(alt_team)
                    team_free.remove(current_team)
                    matches[current_team] = potential_mentor
            else:
                matches[current_team] = potential_mentor
                team_free.remove(current_team)
                mentor_free.remove(potential_mentor)
        return matches

    team = TeamResponses.serialize()
    mentor = MentorResponses.serialize()
    team_order_og = create_numerical_rankings(team, mentor)
    team_order = create_numerical_rankings(team, mentor)
    mentor_order = create_numerical_rankings(mentor, team)
    matches = {}
    while (len(team_order) > len(mentor_order)):
        matches.update(stable_matching(team_order, mentor_order))
        team_order = {key:val for key,val in team_order.items() if not key in matches}
    matches.update(stable_matching(team_order, mentor_order))

    for team,mentor in matches.items():
        team_row = TeamResponses.query.filter_by(id=team).first()
        mentor_row = MentorResponses.query.filter_by(id=mentor).first()
        team_email, mentor_email = None, None
        if team_row:
            team_email = team_row.email
        if mentor_row:
            mentor_email = mentor_row.email
        Matches.populate({team: [mentor, team_email, mentor_email]})

    matches = Matches.query.all()
    team = TeamResponses.query.all()
    mentor = MentorResponses.query.all()
    return render_template('admin.html', matches=matches, team=team, mentor=mentor), 200

@admin_bp.route('/', methods=['GET'])
def reset_hackers():
    from app.models import Matches, TeamResponses, MentorResponses
    matches = Matches.query.all()
    team = TeamResponses.query.all()
    mentor = MentorResponses.query.all()
    return render_template('admin.html', matches=matches, team=team, mentor=mentor), 200

@admin_bp.route('/export_to_csv', methods=['GET'])
def export_to_csv():
    from app.models import Matches, TeamResponses, MentorResponses
    si = io.StringIO()
    cw = csv.writer(si)
    matches = Matches.query.all()
    cw.writerow(['team email', 'team_id', 'mentor email', 'mentor_id'])
    for elem in matches:
        cw.writerow([elem.team_email, elem.team_id, elem.mentor_email, elem.mentor_id])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output, 200

@admin_bp.route('/import_from_feather', methods=['GET'])
def import_from_feather():
    return "", 200

@admin_bp.route('/get_responses', methods=['POST'])
def get_from_csv():
    from app.models import MentorResponses, TeamResponses
    mentor_content = request.files['mentor']
    stream = io.StringIO(mentor_content.stream.read().decode("UTF-8"), newline = None)
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

    team_content = request.files['team']
    stream = io.StringIO(team_content.stream.read().decode("UTF-8"), newline = None)
    csv_input = csv.reader(stream)
    counter = 0
    for elem in csv_input:
        if counter == 0: 
            counter += 1
            continue
        else:
            a = True if elem[6] == 'Virtual' else False
            TeamResponses.populate(elem[1], elem[2], elem[3], int(elem[4].split(':')[0]), elem[5], a)
            counter += 1
    data = TeamResponses.serialize()
    return "", 200