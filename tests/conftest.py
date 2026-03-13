from pathlib import Path

import pytest


@pytest.fixture
def sample_database(tmp_path: Path):
    file_path = tmp_path / "database.db"

    print(f"Creating {file_path}")
    file_path.touch()

    yield Path(file_path)
