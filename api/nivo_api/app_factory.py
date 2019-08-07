import sentry_sdk
from flask import Flask
from flask_restplus import Api, Namespace
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.utils import find_modules, import_string


def create_app() -> Flask:
    app = Flask(__name__)
    return app


def create_api(app: Flask) -> Api:
    # We import dynamically the "namespaces" module, recursively. Because Namespace object are located in submodules.
    # Then we loop over everything that are in the module, and then we add the Namespace object.
    # This is super expensive but it only happened at boot time.
    api = Api()
    for ns in find_modules("nivo_api.namespaces", recursive=True):
        mod = import_string(ns)
        for _, cls in mod.__dict__.items():
            if isinstance(cls, Namespace):
                api.add_namespace(cls)
    api.init_app(app)
    return api


def load_config(app: Flask) -> None:
    app.config.from_object("nivo_api.settings.Config")
    app.config.from_envvar("CONFIG_FILE", silent=True)


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
    return api.app
