from mafia_resources.api.config import PORT
from mafia_resources.api.service import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
