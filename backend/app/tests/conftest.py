import pytest
from app.database.base import Base
from app.database.session import engine


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Ensure clean database schema with all latest columns before executing test suite.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
