from flask import Blueprint

harvester_bp = Blueprint('harvester', __name__)

@harvester_bp.route('/test')
def test():
    return "Blueprint funcionando!"