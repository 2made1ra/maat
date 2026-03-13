from pathlib import Path


def test_create_database(sample_database):
    assert sample_database.exists()
    assert sample_database.is_file()
