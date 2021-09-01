from flask import Blueprint, Response, request, jsonify, make_response, render_template, redirect, url_for

landing_bp = Blueprint("", __name__)

@landing_bp.route('/', methods=['GET'])
def test():
    return "hi", 200