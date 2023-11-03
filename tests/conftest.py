# /myapplication/tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

# Add the project root directory to sys.path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from app.modules.database.base import Base

@pytest.fixture(scope="session")
def db_session():
    # Create an in-memory SQLite database for tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
