from abc import ABC, abstractmethod # 1-ый класс у нас абстрактный
from data.data import Genre, Movie, User # импортируем типы данных из первого файла
from data.data_manager.managing_data import MovieLibrary

class recommendation_strategy(ABC):
    """
    у нас есть три стратегии реков: по жанру, по рейтингу, и по похожим юзерам
    для жанров: у нас есть пользователь у которого есть любимые жанры, значит рекомендуем фильмы с этими жанрами(смотрим на предпочтительные жанры юзера, выводим фильмы с такими же жанрами)
    для рейтингов: берем рейтинг фильмов, и выводим фильмы, которые имеют наибольший рейтинг
    для похожих пользователей: смотрим на юзеров, которые имеют определенные такие жанры как изначальный юзер, и предлагаем им такие же фильмы

    этот класс по идее должен собирать популярные фильмы, пользователей с их жанрами
    то есть нам передается класс User с его атрибутами favourite_genres(список)
    и также класс Movie с их rating

    1. юзер, его жанры и фильмы с их жанрами(одинаковыми)
    2. парсим список фильмов, сортируем от большего к меньшему
    3. берем пользователя с жанрами, по жанрам смотрим на других и предлагаем фильмы пользователей
    """

    @abstractmethod
    def recommend(self):
        pass

class genre_recommend(recommendation_strategy): # сюда мы передаем пользователя которому рекомендуем
    def __init__(self, user: User):
        self._usid = user.id # переменная для получения айди юза
        self._favourite_genres = user.favorite_genres # здесь это след список - [Genre.HORROR, Genre.THRILLER]


    def recommend(self): #конкретное возращение данных
        all_films_id = set() # делаем множество, ибо фильмы могут совпадать, будет круто
        for us_genre in self._favourite_genres:# O(n^3)??? как нибудь упростить | перебираем жанры юза
            for film in MovieLibrary.list_movies(): # перебираем фильмы
                for mov_genre in film[2]: # перебираем в них их жанры
                    if us_genre == mov_genre: # если жанр совпадает
                        all_films_id.add(film[0]) #возвращаем айди фильма
        movies = []
        for mov_id in all_films_id:
            our_movie = MovieLibrary.get_movie(mov_id)
            movies.append(our_movie)
        
        return movies