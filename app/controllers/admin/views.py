from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for
import io
import csv

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')


@admin_bp.route('/reset', methods=['GET'])
def reset():
    from app.models import Matches
    Matches.deleteAll()
    matches = Matches.query.all()
    return render_template('admin.html', matches=matches), 200

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
                in_person_team = team_prefs[team]['in person']
                for mentor in mentor_prefs:
                    in_person_mentor = mentor_prefs[mentor]['in person']
                    shared_expertise = team_prefs[team]['expertise'] & mentor_prefs[mentor]['expertise']
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

    def stable_matching(team_order, mentor_order):
        matches = {}
        team_free = set(team_order.keys())
        mentor_free = set(mentor_order.keys())
        team_proposed = {team: set() for team in team_order}
        while len(team_free) > 0:
            current_team = team_free.pop()
            potential_mentor = None
            for mentor in team_order[current_team]:
                if mentor not in team_proposed[current_team]:
                    potential_mentor = mentor
                    break
            if potential_mentor == None:
                break
            if potential_mentor in mentor_free:
                mentor_free.remove(potential_mentor)
                matches[current_team] = potential_mentor
            else:
                for team in team_order:
                    if team in matches and matches[team] == potential_mentor:
                        alt_team = team
                        break
                if compare_pref(mentor_order, current_team, alt_team, potential_mentor):
                    team_free.add(alt_team)
                    matches.pop(alt_team)
                    matches[current_team] = potential_mentor
        return matches
    
    team = {1: {'commitment': 3, 'expertise': {'cs'}, 'in person': True},
                 2: {'commitment': 2, 'expertise': {'cs'}, 'in person': True},
                 3: {'commitment': 4, 'expertise': {'cs'}, 'in person': True}}
    mentor = {11: {'commitment': 5, 'expertise': {'cs'}, 'in person': True},
                   22: {'commitment': 2, 'expertise': {'cs'}, 'in person': True},
                   33: {'commitment': 3, 'expertise': {'cs'}, 'in person': True}}
    #team = TeamResponses.serialize()
    #mentor = MentorResponses.serialize()
    team_order = create_numerical_rankings(team, mentor)
    mentor_order = create_numerical_rankings(mentor, team)

    print(team_order)
    print(mentor_order)
    print(stable_matching(team_order, mentor_order))

    matches = stable_matching(team_order, mentor_order)

    for team,mentor in matches.items():
        team_row = TeamResponses.query.filter_by(id=team).first()
        mentor_row = MentorResponses.query.filter_by(id=mentor).first()
        team_email, mentor_email = None, None
        if team_row:
            team_email = team_email.email
        if mentor_row:
            mentor_email = mentor_email.email
        Matches.populate({team: [mentor, team_email, mentor_email]})

    matches = Matches.query.all()
    print(matches)
    for elem in matches:
        print(elem.team_id)
        print(elem.mentor_id)
    return render_template('admin.html', matches=matches), 200

@admin_bp.route('/', methods=['GET'])
def reset_hackers():
    from app.models import Matches
    matches = Matches.query.all()
    return render_template('admin.html', matches=matches), 200

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
    print(data)

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
    print(data)
    return "", 200