from data.data import Movie, User, Genre, TestData  # классы чтобы вообще прога поняла откуда у нас все это

# Класс-хранилище фильмов и пользователей, а также паттерн Singleton
class MovieLibrary:
    _instance = None

    # создаём объект только один раз
    def __new__(cls):
        if cls._instance is None:  # если ещё нет объекта
            cls._instance = super(MovieLibrary, cls).__new__(cls)  # создаём новый
            cls._instance._movies = {TestData.load_movies()}  # словарь фильмов
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
    


    def add_genre_to_user(self, user_id: int, genre: Genre): # выполняется при условии что пользователь есть
        us = self.get_user(user_id)#вроде же мы можем так написать, почему бы нет?

        if genre in us.favourite_genres:
            us.add_favourite_genre(genre) # 83 строчка в data.py, вроде должно работать

    def remove_genre_from_user(self, user_id: int, genre: Genre):
        us = self.get_user(user_id)

        if genre in us.favourite_genres:
            us.favourite.genres.remove(genre)# ну типа это у нас список поэтому тут remove можно поставить

    def get_us_fav_genres(self, user_id: int): # опять же работает при условии что юз есть 
        return self.get_user(user_id).favourite_genres