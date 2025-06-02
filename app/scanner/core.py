from flask import Blueprint, jsonify, request
import subprocess
import re
from pathlib import Path
from datetime import datetime

# 1. Primeiro definimos o blueprint
harvester_bp = Blueprint('harvester', __name__)

# Configurações
RESULTS_DIR = Path("app/results")
RESULTS_DIR.mkdir(exist_ok=True)

# Funções auxiliares
def remove_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def extract_valid_emails(text):
    email_regex = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
    return list(set(email.lower().strip() for email in email_regex.findall(text) if not email.startswith('*')))

def extract_valid_hosts(text):
    hosts = set()
    for line in text.split('\n'):
        if 'Found:' in line:
            host = line.split('Found:')[-1].strip()
            if '.' in host and not any(c in host for c in ['*', ' ']):
                hosts.add(host)
    return list(hosts)

# 2. Depois definimos as rotas que usam o blueprint
@harvester_bp.route('/scan', methods=['POST'])
def scan_domain():
    try:
        data = request.get_json()
        domain = data.get('domain', '').lower().strip()
        
        if not domain:
            return jsonify({"error": "Domain is required"}), 400

        cmd = [
            'theHarvester',
            '-d', domain,
            '-b', 'dnsdumpster,hackertarget',
            '-f', f'{RESULTS_DIR}/{domain}'
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        emails = extract_valid_emails(remove_ansi_codes(result.stdout))
        hosts = extract_valid_hosts(remove_ansi_codes(result.stdout))
        
        return jsonify({
            "domain": domain,
            "emails": emails,
            "hosts": hosts,
            "success": result.returncode == 0
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@harvester_bp.route('/test')
def test():
    return jsonify({"status": "API working"})