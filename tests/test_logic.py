from pathlib import Path
from maat.models import CategoryEnum, Review
from maat.repository import ReviewRepository

def test_create_database(sample_database):
    assert sample_database.exists()
    assert sample_database.is_file()

def test_repository_add_and_get_all(db_session):
    repo = ReviewRepository(db_session)

    # Check empty
    assert len(repo.get_all()) == 0

    # Add review
    review = repo.add(
        title="Dune",
        category=CategoryEnum.BOOK,
        score=9,
        text="A masterpiece of sci-fi."
    )

    assert review.id is not None
    assert review.title == "Dune"
    assert review.category == CategoryEnum.BOOK
    assert review.score == 9
    assert review.text == "A masterpiece of sci-fi."

    # Check get_all
    reviews = repo.get_all()
    assert len(reviews) == 1
    assert reviews[0].id == review.id

def test_repository_delete(db_session):
    repo = ReviewRepository(db_session)

    review1 = repo.add("Dune", CategoryEnum.BOOK, 9)
    review2 = repo.add("The Matrix", CategoryEnum.MOVIE, 10)

    assert len(repo.get_all()) == 2

    repo.delete(review1.id)

    reviews = repo.get_all()
    assert len(reviews) == 1
    assert reviews[0].id == review2.id

def test_repository_get_by_category(db_session):
    repo = ReviewRepository(db_session)

    repo.add("Dune", CategoryEnum.BOOK, 9)
    repo.add("1984", CategoryEnum.BOOK, 8)
    repo.add("The Matrix", CategoryEnum.MOVIE, 10)

    books = repo.get_by_category(CategoryEnum.BOOK)
    movies = repo.get_by_category(CategoryEnum.MOVIE)

    assert len(books) == 2
    assert len(movies) == 1
    assert movies[0].title == "The Matrix"
