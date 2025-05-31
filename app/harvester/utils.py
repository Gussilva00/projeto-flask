import re

def validate_domain(domain):
    """Valida se o domínio está no formato correto"""
    pattern = r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$'
    return re.match(pattern, domain, re.IGNORECASE) is not None

def validate_input(data):
    """Valida os dados de entrada para a API"""
    required_fields = ['domain']
    for field in required_fields:
        if field not in data:
            return False
    return True