import uuid

import pytest
from sqlalchemy import text

from music2.common import db

# Make sure it's unique but repeatable so we can use it in two different tests
TABLE_NAME = f"table_test_{str(uuid.uuid4()).replace('-', '')}"

EXISTS_QUERY = text(
    "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename  = :table_name);"
).bindparams(table_name=TABLE_NAME)
COUNT_QUERY = text(f"SELECT COUNT(*) FROM {TABLE_NAME};")
CREATE_QUERY = text(f"CREATE TABLE {TABLE_NAME} (test_col text);")
INSERT_QUERY = text(f"INSERT INTO {TABLE_NAME} (test_col) VALUES ('test');")


# We do this test twice to ensure that the fixture runs in a single transaction
# scoped to an individual test
@pytest.mark.db
@pytest.mark.parametrize("iteration", [1, 2])
def test_db_session(db_session, iteration):
    assert db_session.execute(EXISTS_QUERY).scalar() is False
    db_session.execute(CREATE_QUERY)
    assert db_session.execute(EXISTS_QUERY).scalar() is True
    assert db_session.execute(COUNT_QUERY).scalar() == 0
    db_session.execute(INSERT_QUERY)
    assert db_session.execute(COUNT_QUERY).scalar() == 1


@pytest.mark.db
def test_db_session_commit_mocked(db_session, mocker):
    """
    When db marker is used, db_session.commit should be mocked out
    """
    assert isinstance(db_session.commit, mocker.MagicMock)


@pytest.mark.db
def test_get_db_session_commit_mocked(mocker):
    """
    When db marker is used, get_db_session().commit should be mocked out
    """
    session = db.get_db_session()
    assert isinstance(session.commit, mocker.MagicMock)


def test_get_db_session_raises_engine_connect():
    """
    When db marker is not used, Engine.connect() should fail
    """
    with pytest.raises(RuntimeError):
        db.get_db_engine().connect()


def test_get_db_session_raises_session():
    """
    When db marker is not used, Session() should fail
    """
    with pytest.raises(RuntimeError):
        db.get_db_session()
