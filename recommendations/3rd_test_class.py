from abc import ABC, abstractmethod
from data.data import Genre, Movie, User
from movie_library import MovieLibrary

class recommendation_strategy(ABC):
    @abstractmethod
    def recommend(self) -> list[Movie]:
        pass


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