import pytest
import config
from variance import create_app

@pytest.fixture
def app():
    app = create_app(config.UnitTestConfig)
    return app
