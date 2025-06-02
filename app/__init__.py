from flask import Flask, render_template
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Importar DEPOIS de criar o app para evitar imports circulares
    from app.scanner.core import harvester_bp
    
    # Registrar blueprint
    app.register_blueprint(harvester_bp, url_prefix='/api/harvester')
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app