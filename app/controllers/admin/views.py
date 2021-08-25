from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')

@admin_bp.route('/test', methods=['GET'])
def test():
    return "hello world", 200

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