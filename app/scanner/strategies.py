SCAN_STRATEGIES = {
    "default": {
        "command": "theHarvester -d {domain} -b dnsdumpster,hackertarget",
        "timeout": 120,
        "fallback_tips": ["Tente subdomínios como mail.{domain}"]
    },
    "protected": {
        "command": "theHarvester -d {domain} -b securitytrails",
        "timeout": 300,
        "fallback_tips": ["Use nosso scanner premium para este domínio"]
    }
}

def get_scan_strategy(domain):
    """Seleciona estratégia baseada no domínio"""
    if any(d in domain for d in ["google", "youtube", "facebook"]):
        return SCAN_STRATEGIES["protected"]
    return SCAN_STRATEGIES["default"]