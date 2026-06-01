import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities state before each test."""
    original = copy.deepcopy(app_module.activities)
    yield
    # restore original state
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


@pytest.fixture
def client(reset_activities):
    """Provide a TestClient for the FastAPI app."""
    with TestClient(app_module.app) as c:
        yield c
