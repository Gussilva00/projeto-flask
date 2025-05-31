from flask import Flask
from flask_cors import CORS
from .routes import main_bp
from .harvester import harvester_bp  # Importação corrigida

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    app.config['SECRET_KEY'] = 'sua_chave_secreta'
    
    app.register_blueprint(main_bp)
    app.register_blueprint(harvester_bp, url_prefix='/api/harvester')
    
    return app