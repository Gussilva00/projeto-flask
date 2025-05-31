from app import create_app

app = create_app()

# Adicione esta parte (temporária) para debug
@app.route('/routes')
def list_routes():
    import urllib.parse
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote(f"{rule.endpoint:50s} {methods:20s} {rule}")
        output.append(line)
    return '<br>'.join(sorted(output))

if __name__ == '__main__':
    app.run(debug=True)