from abc import ABC, abstractmethod # 1-ый класс у нас абстрактный
from data.data import Genre, Movie, User # импортируем типы данных из первого файла
from data.data_manager.managing_data import MovieLibrary

class recommendation_strategy(ABC):
    @abstractmethod
    def recommend(self, user: User): # закидываем пользователя, выводится будет здесь список
        pass

class genre_recommend(recommendation_strategy): 
    def __init__(self, lib: MovieLibrary): # мы можем просто закинуть сюда нашу movielibrary
        self.lib = lib

    def recommend(self, us: User):
        recs = []

        fav_us_genres = set(us.favorite_genres) # закидываем во множество любимые жанры юза
        all_movies = self.lib.list_movies()

        for movie in all_movies: # перебираем фильмы
            movie_genres = set(movie.genres) # делаем множество из жанров фильма 
            if fav_us_genres & movie_genres: # если жанры пользователя и жанры фильма, по сути, в одном множестве
                if movie.id not in us.ratings: # если фильм не оценен пользователем
                    recs.append(movie) # он нам подходит

        return recs
    
class rating_recommend(recommendation_strategy):
    def __init__(self, lib: MovieLibrary): # мы можем просто закинуть сюда нашу movielibrary
        self.lib = lib

    def recommend(self, us: User):
        all_movies = self.lib.list_movies()

        sorted_movies = sorted(all_movies, key= lambda m: m.rating, reverse=True) # чиста сортируем по лямбде, почему бы нет
        # реверс стоит ибо сортировка идет от меньшего к большему, а так наоборот

        return sorted_movies

