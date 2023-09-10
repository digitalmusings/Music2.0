#!/bin/env python

"""
Small module to create the Flask app and register all the submodules.

If executed directly, this module will start the dev server on port 8000.
"""

import flask

from .api.system import routes as system_routes

APP_NAME = "Music2.0"


def create_app():
    app = flask.Flask(__name__)
    app.register_blueprint(system_routes.bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=8080, debug=True)
