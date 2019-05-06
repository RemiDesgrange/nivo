from flask import Flask
from flask_restplus import Api
from werkzeug.contrib.fixers import ProxyFix

from settings import load_config, Config

def create_app(config: Config):
    #TODO need setup logging
    app = Flask(config.app_name)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    return app


def create_api(config: Config, app: Flask):
    api = Api(**config.api)
    #register all the namespaces
    namespaces = get_namespaces()
    for ns in namespaces:
        api.add_namespace(ns)
    api.init_app(app)
    return api



if __name__ == '__main__':
    config = load_config()
    app = create_app(config)
    api = create_api(app)
    app.run(debug=config.debug)


