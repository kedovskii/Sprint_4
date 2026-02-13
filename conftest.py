import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()


@pytest.fixture
def prepared_collector(collector):
    #- 'Книга A' — жанр 'Мультфильмы' (детский, без возрастного рейтинга)
    #- 'Книга B' — жанр 'Ужасы' (в списке genre_age_rating)
    #- 'Книга C' — без жанра
    collector.add_new_book("Книга A")
    collector.add_new_book("Книга B")
    collector.add_new_book("Книга C")

    collector.set_book_genre("Книга A", "Мультфильмы")
    collector.set_book_genre("Книга B", "Ужасы")

    return collector