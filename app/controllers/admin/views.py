from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')

@admin_bp.route('/test', methods=['GET'])
def match():

    def create_numerical_rankings(team_prefs, mentor_prefs): 
        # team_prefs {'A': {'commitment': _, 'expertise': _, 'in person': _}, 'B': ...}
        # mentor_prefs {'a': {'commitment': _, 'expertise': _, 'in person': _}, 'b': ...}
        commitment_difference = [0, 1, 2, 3, -1, -2, -3]
        team_order = {}
        for team in team_prefs:
            team_order[team] = []
            mediocre_prefs = []
            bad_prefs = []
            for i in commitment_difference:
                commitment_level = team_prefs[team]["commitment"] + i
                in_person_team = team_prefs[team]['in person']
                for mentor in mentor_prefs:
                    in_person_mentor = mentor_prefs[mentor]['in person']
                    shared_expertise = set(team_prefs[team]['expertise']) & set(mentor_prefs[mentor]['expertise'])
                    if (mentor_prefs[mentor]["commitment"] == commitment_level) and len(shared_expertise) and (in_person_team == in_person_mentor):
                        team_order[team].append(mentor)
                    
                    elif (mentor_prefs[mentor]["commitment"] == commitment_level):
                        mediocre_prefs.append(mentor)
                    else:
                        bad_prefs.append(mentor)



        return
    

    return "", 200

@admin_bp.route('/match', methods=['GET'])
def match():
    return "", 200

@admin_bp.route('/reset', methods=['GET'])
def reset_hackers():
    return "", 200

@admin_bp.route('/export_to_csv', methods=['GET'])
def export_to_csv():
    return "", 200

@admin_bp.route('/import_from_feather', methods=['GET'])
def import_from_feather():
    return "", 200
