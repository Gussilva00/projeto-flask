from flask import Blueprint, jsonify, request
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Cria o blueprint
harvester_bp = Blueprint('harvester', __name__)

def ensure_dir():
    """Garante que o diretório de resultados existe"""
    Path('app/results').mkdir(exist_ok=True)

@harvester_bp.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    domain = data.get('domain', '').strip()
    
    if not domain:
        return jsonify({'error': 'Domain is required'}), 400
    
    try:
        ensure_dir()
        output_file = f'app/results/{domain}_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
        
        cmd = [
            'theHarvester',
            '-d', domain,
            '-b', 'securitytrails,dnsdumpster,hackertarget',
            '-f', output_file.replace('.json', '')
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if Path(output_file).exists():
            with open(output_file, 'r') as f:
                return jsonify(json.load(f))
                
        return jsonify({
            'hosts': list(set(
                line.split('Found:')[-1].strip() 
                for line in result.stdout.split('\n') 
                if 'Found:' in line
            )),
            'emails': list(set(
                line.strip() 
                for line in result.stdout.split('\n') 
                if '@' in line and '.' in line
            )),
            'raw_output': result.stdout
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@harvester_bp.route('/history', methods=['GET'])
def history():
    try:
        history = []
        for file in Path('app/results').glob('*.json'):
            with open(file, 'r') as f:
                data = json.load(f)
                history.append({
                    'domain': file.stem.split('_')[0],
                    'date': file.stem.split('_')[1],
                    'results': data
                })
        return jsonify(sorted(history, key=lambda x: x['date'], reverse=True))
    except Exception as e:
        return jsonify({'error': str(e)}), 500