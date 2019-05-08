import sentry_sdk
from flask import Flask
from flask_restplus import Api
from sentry_sdk.integrations.flask import FlaskIntegration

from .namespaces.namespace import get_namespaces


def create_app() -> Flask:
    app = Flask(__name__)
    return app


def create_api(app: Flask) -> Api:
    api = Api()
    # This should be modified
    namespaces = get_namespaces()
    for ns in namespaces:
        api.add_namespace(ns)
    api.init_app(app)
    return api


def load_config(app: Flask) -> None:
    app.config.from_object('nivo_api.settings.Config')
    app.config.from_envvar('CONFIG_FILE', silent=True)


def setup_logging(app: Flask) -> None:
    # TODO
    pass


def init_sentry():
    # sentry is service that collect all exception in the app ans send it to sentry.io
    # the endpoint to contact sentry is set via SENTRY_DSN env var
    sentry_sdk.init(integrations=[FlaskIntegration()])


def init_app() -> Flask:
    init_sentry()
    app = create_app()
    api = create_api(app)
    load_config(app)
    setup_logging(app)
    return app

