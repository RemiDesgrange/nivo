from flask import Flask
from flask_restplus import Api

from .namespaces.namespace import get_namespaces
from .settings import Env



def create_app() -> Flask:
    app = Flask(__name__)
    return app


def create_api(app: Flask) -> Api:
    api = Api()
    #register all the namespaces
    namespaces = get_namespaces()
    for ns in namespaces:
        api.add_namespace(ns)
    api.init_app(app)
    return api

def load_config(app: Flask) -> None:
    app.config.from_object('nivo-api.settings.Config')
    app.config.from_envvar('CONFIG_FILE', silent=True)

def setup_logging(app: Flask) -> None:
    #TODO
    pass

if __name__ == '__main__':
    app = create_app()
    api = create_api(app)
    load_config(app)
    setup_logging(app)
    app.run(debug=app.config['ENV'] == Env.DEV)


