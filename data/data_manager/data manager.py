# Класс-хранилище фильмов и пользователей, а также паттерн Singleton
class MovieLibrary:
    _instance = None  # переменная для одного экземпляра

    # создаём объект только один раз
    def __new__(cls):
        if cls._instance is None:  # если ещё нет объекта
            cls._instance = super(MovieLibrary, cls).__new__(cls)  # создаём новый
            cls._instance._movies = {}  # словарь фильмов
            cls._instance._users = {}  # словарь пользователей
        return cls._instance  # возвращаем один и тот же объект

    # добавить фильм
    def add_movie(self, movie: Movie):
        self._movies[movie.id] = movie

    # получить фильм по айди
    def get_movie(self, movie_id: int):
        return self._movies.get(movie_id)

    # вернуть все фильмы списком
    def list_movies(self):
        return list(self._movies.values())

    # добавить пользователя
    def add_user(self, user: User):
        self._users[user.id] = user

    # получить пользователя по айди
    def get_user(self, user_id: int):
        return self._users.get(user_id)

    # вернуть всех пользователей списком
    def list_users(self):
        return list(self._users.values())
