from app import create_app
import sys
from pathlib import Path

# Configuração do path
sys.path.append(str(Path(__file__).parent))

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)