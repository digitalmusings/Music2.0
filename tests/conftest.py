import pytest

# Import as music2_app so we can use the name `app` for other things
from music2 import app as music2_app
from music2.common import db


@pytest.fixture
def app():
    app = music2_app.create_app()
    return app


@pytest.fixture(autouse=True)
def db_session(mocker, request):
    """
    Fixture to run each test in a single session transaction.

    This fixture is automatically used per-test so that each test is completely
    independent.

    Ideally, most tests will mock out any database calls anyway, but this will
    allow us to create integration tests that actually hit the database without
    affecting the data.

    Any test that does wish to actually use the database must use the marker
    `db` to indicate this, otherwise attempting to connect will raise a
    RuntimeError.
    """

    # Make sure any code under test gets a fresh Session object (or exception)
    db.get_db_session.cache_clear()

    # Test to see if the current test function was given the db marker
    if any(m.name == "db" for m in request.node.iter_markers()) or (
        request.node.parent
        and any(m.name == "db" for m in request.node.parent.iter_markers())
    ):
        # Run the entire thing inside a transaction that we can rollback all at once
        # The session will be started inside this transaction and so everything it
        # does will be rolled back
        engine = db.get_db_engine()
        with engine.connect() as connection:
            with connection.begin() as transaction:
                # We don't want anyone to be able to commit any changes during tests
                # Replace with a MagicMock so that
                #   1) it pretends like it works and
                #   2) you can assert that it was called if you need to test that
                mocker.patch("sqlalchemy.orm.Session.commit")

                session = db.get_db_session()

                try:
                    yield session
                finally:
                    session.rollback()
    else:
        # This test is not marked as requiring DB access, throw an error if they try
        exc = RuntimeError("Non-DB test tried to access the DB")
        # Just in case code attempts to use Engine.connect directly
        mocker.patch("sqlalchemy.engine.base.Engine.connect", side_effect=exc)
        # This is what `get_db_session` uses
        mocker.patch("sqlalchemy.orm.Session", side_effect=exc)
        yield None
