from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for

mentor_bp = Blueprint("mentor", __name__, url_prefix='/mentor')

@mentor_bp.route('/test', methods=['GET'])
def test():
    return "hello world", 200

@mentor_bp.route('/<teamID>', methods=['GET'])
def get_mentor(teamID):
    return teamID, 200

@mentor_bp.route('/<teamID>/<mentorID>', methods=['POST'])
def add_mentor(teamID, mentorID):
    return teamID, 200

@mentor_bp.route('/<teamID>/<newMentorID>', methods=['PUT'])
def update_mentor(teamID, newMentorID):
    return newMentorID, 200

@mentor_bp.route('/<teamID>', methods=['DELETE'])
def delete_mentor(teamID):
    return teamID, 200
