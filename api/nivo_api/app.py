from nivo_api.app_factory import init_app
from nivo_api.settings import Env

app = init_app()

if __name__ == '__main__':
    app.run(debug=app.config['ENV'] == Env.DEV)
