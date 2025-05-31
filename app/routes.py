from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('index.html')
@main_bp.route('/test-frontend')
def test_frontend():
    return render_template('index.html')