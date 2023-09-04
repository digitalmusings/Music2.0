import pytest

from music2.app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app
