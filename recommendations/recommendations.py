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

class similar_users_recommend(recommendation_strategy):
    def __init__(self, user: User):
        self.user = user
        self.library = MovieLibrary()
    
    def find_similar_users(self) -> list[User]:
        # похожие жанры = похожие пользователи
        all_users = self.library.list_users()
        similar = []
        
        for other_user in all_users:
            if other_user.id == self.user.id:
                continue
            
            # Считаем общие жанры
            common_genres = set(self.user.favorite_genres) & set(other_user.favorite_genres)
            if len(common_genres) > 0:
                similar.append(other_user)
        
        return similar
    
    def recommend(self) -> list[Movie]:
        # фильмы от похожих пользователей
        similar_users = self.find_similar_users()
        if not similar_users:
            return []
        
        # Фильмы, которые оценили похож пользователи
        result = []
        user_movie_ids = set(self.user.ratings.keys())
        
        for similar_user in similar_users:
            for movie_id in similar_user.ratings.keys():
                if movie_id not in user_movie_ids:
                    movie = self.library.get_movie(movie_id)
                    if movie and movie not in result:
                        result.append(movie)
        
        result.sort(key=lambda x: x.rating, reverse=True)
        return result

