import flask

bp = flask.Blueprint("system", __name__, url_prefix="/system")


@bp.get("/ping")
def get_ping():
    """
    Hello world
    """

    return {"data": "pong"}
