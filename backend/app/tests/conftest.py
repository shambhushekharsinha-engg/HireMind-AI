import sys
from pathlib import Path

# Ensure backend root directory is always on sys.path regardless of execution CWD
backend_dir = str(Path(__file__).resolve().parent.parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import app.models.all_models  # noqa: F401 - Register all SQLAlchemy models in Base.metadata
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
