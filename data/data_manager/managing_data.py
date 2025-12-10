from data.data import Movie, User # классы чтобы вообще прога поняла откуда у нас все это

# Класс-хранилище фильмов и пользователей, а также паттерн Singleton
class MovieLibrary:
    _instance = None

    # создаём объект только один раз
    def __new__(cls):
        if cls._instance is None:  # если ещё нет объекта
            cls._instance = super(MovieLibrary, cls).__new__(cls)  # создаём новый
            cls._instance._movies = {}  # словарь фильмов
            cls._instance._users = {}  # словарь пользователей
        return cls._instance  # возвращаем один и тот же объект

    def add_movie(self, movie: Movie):
        self._movies[movie.id] = movie

    def get_movie(self, movie_id: int):
        return self._movies.get(movie_id)

    def list_movies(self):
        return list(self._movies.values())

    def add_user(self, user: User):
        self._users[user.id] = user

    def get_user(self, user_id: int):
        return self._users.get(user_id)

    def list_users(self):
        return list(self._users.values())
