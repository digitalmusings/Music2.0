import pytest

from music2.common import db, exceptions


@pytest.mark.parametrize(
    "user, password, host, port, name, expected",
    [
        pytest.param(
            "skroob",
            "123456",
            "mrurl.net",
            654321,
            "luggage",
            "postgresql+psycopg2://skroob:123456@mrurl.net:654321/luggage",
            id="all-specified",
        ),
        pytest.param(
            "skroob",
            "123456",
            None,
            None,
            None,
            "postgresql+psycopg2://skroob:123456@localhost:5432/music",
            id="no-optional",
        ),
        pytest.param(
            None, "123456", None, None, None, exceptions.ConfigError, id="missing-user"
        ),
        pytest.param(
            "", "123456", None, None, None, exceptions.ConfigError, id="empty-user"
        ),
        pytest.param(
            "skroob",
            None,
            None,
            None,
            None,
            exceptions.ConfigError,
            id="missing-password",
        ),
        pytest.param(
            "skroob", "", None, None, None, exceptions.ConfigError, id="empty-password"
        ),
    ],
)
def test_get_db_url(user, password, host, port, name, expected):
    kwargs = {"user": user, "password": password}
    if host is not None:
        kwargs["host"] = host
    if port is not None:
        kwargs["port"] = port
    if name is not None:
        kwargs["name"] = name

    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            db.get_db_url(**kwargs)
    else:
        actual_url = db.get_db_url(**kwargs)
        assert actual_url == expected
