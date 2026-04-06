from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from maat.models import Base

@pytest.fixture
def sample_database(tmp_path: Path):
    file_path = tmp_path / "database.db"

    print(f"Creating {file_path}")
    file_path.touch()

    yield Path(file_path)

@pytest.fixture
def db_session(tmp_path: Path):
    """Provides a clean in-memory SQLite database session for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
