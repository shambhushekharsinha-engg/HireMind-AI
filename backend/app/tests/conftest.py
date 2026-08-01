import pytest
from app.database.session import engine
from app.database.base import Base
import app.models.all_models

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Ensure clean database schema with all latest columns before executing test suite.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
