from abc import ABC, abstractmethod
from enum import Enum  # импортируем Enum, чтобы сделать фиксированный список жанров - для аккуратности кода

# Создаем список всех жанров фильмов, чтобы не писать их руками каждый раз
class Genre(Enum):
    ACTION = "Боевик"
    DRAMA = "Драма"
    COMEDY = "Комедия"
    FANTASY = "Фантастика"
    HORROR = "Хоррор"
    THRILLER = "Триллер"
    ROMANCE = "Мелодрама"
    ANIMATION = "Анимация"
    ADVENTURE = "Приключения"
    HISTORY = "История"

class BaseModel(ABC):
    @abstractmethod
    def __str__(self):  # обязуем все объекты уметь красиво выводиться через print()
        pass

# КЛАСС ФИЛЬМОВ
class Movie(BaseModel):
    def __init__(self, movie_id: int, title: str, genres: list[Genre],
                 director: str, year: int, rating: float):
        self._id = movie_id  # айди фильма, приватная переменная
        self._title = title  # название фильма
        self._genres = genres  # список жанров фильма
        self._director = director  # режиссёр
        self._year = year  # год выхода
        self._rating = rating  # рейтинг

    # геттеры, чтобы читать данные, а не трогать напрямую - по требованию
    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def genres(self):
        return self._genres

    @property
    def rating(self):
        return self._rating

# КЛАСС ПОЛЬЗОВАТЕЛЕЙ
class User(BaseModel):
    def __init__(self, user_id: int, name: str):
        self._id = user_id  # айди пользователя
        self._name = name  # имя пользователя
        self._ratings: dict[int, float] = {}  # оценки фильмов в виде {id фильма: оценка}
        self._favorite_genres: list[Genre] = []  # любимые жанры
    def __str__(self):
        return f"Пользователь {self._name} ID: {self._id})"

    @property
    def id(self):
        return self._id  # возвращаем айди
    @property
    def name(self):
        return self._name

    @property
    def favorite_genres(self):
        return self._favorite_genres  # возвращаем любимые жанры

    @property
    def ratings(self):
        return self._ratings  # возвращаем оценки

    # Добавление оценки фильму
    def add_rating(self, movie: Movie, rating: float):
        if 0 <= rating <= 10:  # проверяем, чтобы оценка была нормальная
            self._ratings[movie.id] = rating  # сохраняем оценку
        else:
            print("Оценка должна быть в диапазоне 0–10.")  

    # Добавление любимых фильмов
    def add_favorite_genre(self, genre: Genre):
        if genre not in self._favorite_genres:  # если жанра ещё нет
            self._favorite_genres.append(genre)

# ТЕСТОВЫЕ ДАННЫЕ
class TestData:

    @staticmethod
    def load_movies():
        test_movies = [
            Movie(1, "Стажёр", [Genre.COMEDY, Genre.DRAMA], "Нэнси Майерс", 2015, 7.1),
            Movie(2, "Бойцовский клуб", [Genre.DRAMA, Genre.THRILLER], "Финчер", 1999, 8.8),
            Movie(3, "Жизнь Пи", [Genre.ADVENTURE, Genre.FANTASY, Genre.DRAMA], "Энг Ли", 2012, 8.0),
            Movie(4, "Интерстеллар", [Genre.FANTASY, Genre.DRAMA], "Нолан", 2014, 8.6),
            Movie(5, "Шрек", [Genre.COMEDY, Genre.ANIMATION], "Адамсон", 2001, 7.9),
            Movie(6, "Оно", [Genre.HORROR], "Мушетти", 2017, 7.4),
            Movie(7, "Титаник", [Genre.ROMANCE, Genre.DRAMA], "Кэмерон", 1997, 7.8),
            Movie(8, "Паразиты", [Genre.THRILLER, Genre.DRAMA], "Пон Джун-хо", 2019, 8.6),
            Movie(9, "Зверополис", [Genre.ANIMATION, Genre.COMEDY, Genre.ADVENTURE], "Байрон Ховард", 2016, 8.0),
            Movie(10, "Поворот не туда", [Genre.HORROR, Genre.THRILLER], "Стивен С. Миллер", 2003, 5.5),
            Movie(11, "Форрест Гамп", [Genre.DRAMA, Genre.COMEDY], "Земекис", 1994, 8.8),
            Movie(12, "Чужой", [Genre.FANTASY, Genre.HORROR], "Ридли Скотт", 1979, 8.4),
            Movie(13, "12 лет рабства", [Genre.DRAMA, Genre.HISTORY], "Стив Маккуин", 2013, 8.1),
            Movie(14, "Джокер", [Genre.DRAMA, Genre.THRILLER], "Филлипс", 2019, 8.4),
            Movie(15, "Молчание ягнят", [Genre.THRILLER, Genre.DRAMA], "Джонатан Демме", 1991, 8.6),
            Movie(16, "Вышка", [Genre.DRAMA, Genre.THRILLER], "Рубен Остлунд", 2023, 7.8),
            Movie(17, "Дьявол носит Прада", [Genre.COMEDY, Genre.DRAMA], "Дэвид Фрэнкел", 2006, 7.0),
            Movie(18, "Анора", [Genre.FANTASY, Genre.DRAMA], "Жан-Пьер Жене", 2019, 6.9),
            Movie(19, "Оппенгеймер", [Genre.DRAMA, Genre.HISTORY], "Кристофер Нолан", 2023, 8.8),
            Movie(20, "Зеленая книга", [Genre.DRAMA, Genre.COMEDY], "Питер Фаррелли", 2018, 8.2),
        ]

        return test_movies
