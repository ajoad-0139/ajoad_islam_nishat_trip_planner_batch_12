import os
from config import Config
from create_app import create_app

app = create_app(Config)

if __name__ == '__main__':
    app_env = os.getenv('APP_ENV', 'production')
    port = os.getenv('PORT', 5000)
    debug = False

    if app_env == 'development' :
        debug = True

    app.run(debug=debug, host='0.0.0.0', port=port)
