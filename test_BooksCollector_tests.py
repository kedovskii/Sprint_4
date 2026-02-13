import pytest
from main import BooksCollector

class TestBooksCollector:

    # add_new_book(name) - проверка отсутствия жанра при добавлении новой книги с названием < 40 символов
    # использую фикстуру collector
    @pytest.mark.parametrize("book_name", ["A", "XYZ"*13, "Обычная книга"])
    def test_add_new_book_short_name_added_with_empty_genre(self, collector, book_name):
        collector.add_new_book(book_name)
        assert (book_name in collector.books_genre) and (collector.books_genre[book_name] == "")

    # set_book_genre(name, genre) - проверка добавления одного из валидных жанров
    # использую фикстуру collector
    @pytest.mark.parametrize("valid_genre", ["Фантастика", "Ужасы", "Детективы", "Мультфильмы", "Комедии"])
    def test_set_book_genre_with_valid_genre(self, collector, valid_genre):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", valid_genre)
        assert collector.books_genre["Книга"] == valid_genre

    # set_book_genre(name, genre) - проверка добавления невалидного жанра (не из списка)
    # использую фикстуру collector
    @pytest.mark.parametrize("invalid_genre", ["Роман", "Стихи", "", "Биография"])
    def test_set_book_genre_with_invalid_genre_ignored(self, collector, invalid_genre):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", invalid_genre)
        assert collector.books_genre["Книга"] == ""

    # get_book_genre(name) - проверка возврата установленного жанра у существующей книги
    # использую фикстуру collector
    @pytest.mark.parametrize("book_name, genre",[("Книга A", "Мультфильмы"),("Книга B", "Фантастика"),("Книга C", "Комедии"),])
    def test_get_book_genre_existing_book_returns_value(self, collector, book_name, genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

    # get_book_genre(name) - проверка возврата жанра у несуществующей книги
    # использую фикстуру collector
    def test_get_book_genre_non_existing_returns_none(self, collector):
        assert collector.get_book_genre("Несуществующая книга") is None

    # get_books_with_specific_genre(genre) - проверка возврата списка книг с валидным жанром
    # использую фикстуру collector
    @pytest.mark.parametrize("book_name, genre",[("Книга A", "Мультфильмы"),("Книга B", "Фантастика"),("Книга C", "Комедии"),])
    def test_get_books_with_specific_genre_returns_books_of_valid_genre(self, collector, book_name, genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)

        result = collector.get_books_with_specific_genre(genre)
        assert result == [book_name]

    # get_books_genre() - проверка возврата словаря жанров
    # использую фикстуру prepared_collector
    def test_get_books_genre_returns_filled_mapping(self, prepared_collector):
        assert prepared_collector.get_books_genre() == {"Книга A": "Мультфильмы", "Книга B": "Ужасы", "Книга C": ""}

    # get_books_for_children() - проверка возврата книг с жанрами из genre, не входящими в genre_age_rating
    # использую фикстуру prepared_collector
    def test_get_books_for_children_only_non_rated(self, prepared_collector):
        result = prepared_collector.get_books_for_children()
        assert result == ["Книга A"]

    # add_book_in_favorites(name) - проверка добавления книги в избранное
    # использую фикстуру collector
    @pytest.mark.parametrize("book_name, genre", [("Книга A", "Мультфильмы"), ("Книга B", "Фантастика"), ("Книга C", "Комедии")])
    def test_add_book_in_favorites_adds_existing_book(self, collector, book_name, genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        collector.add_book_in_favorites(book_name)
        assert collector.get_list_of_favorites_books() == [book_name]

    # add_book_in_favorites(name) - проверка добавления книги в избранное даже без жанра
    # использую фикстуру collector
    def test_add_book_in_favorites_adds_even_without_genre(self, collector):
        collector.add_new_book("Без жанра")
        collector.add_book_in_favorites("Без жанра")
        assert collector.get_list_of_favorites_books() == ["Без жанра"]

# delete_book_from_favorites(name) - проверка удаления существующей в избранном книги
    # использую фикстуру collector
    @pytest.mark.parametrize("book_name", ["Книга A", "Книга B", "Книга C"])
    def test_delete_book_from_favorites_removes_existing(self, collector, book_name):
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert collector.get_list_of_favorites_books() == []

    # get_list_of_favorites_books() - проверка наличия книги в избранном списке
    # использую фикстуру collector
    @pytest.mark.parametrize("book_name, genre", [("Книга A", "Мультфильмы"), ("Книга B", "Фантастика"), ("Книга C", "Комедии")])
    def test_get_list_of_favorites_books(self, collector, book_name, genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.get_list_of_favorites_books()