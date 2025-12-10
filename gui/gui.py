from data.data import User, Genre, Movie
from data.data_manager.managing_data import MovieLibrary
from data.data import TestData
from recommendations.recommendations import genre_recommend, rating_recommend, similar_users_recommend


class ConsoleInterface:
    def __init__(self):
        self.library = MovieLibrary()
        self.current_user = None
        self._load_test_data()  # Загружаем тестовые данные

    def _load_test_data(self):
        """Загружаем тестовые фильмы в библиотеку"""
        test_movies = TestData.load_movies()
        for movie in test_movies:
            self.library.add_movie(movie)

    def clear_screen(self):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title):
        print("=" * 50)
        print(f"{title:^50}")
        print("=" * 50)

    def register_user(self):
        self.print_header("РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ")

        try:
            user_id = max([user.id for user in self.library.list_users()]) + 1
        except:
            user_id = 1

        name = input("Введите ваше имя: ").strip()
        if not name:
            print("Имя не может быть пустым!")
            input("Нажмите Enter для продолжения...")
            return

        print("\nВыберите любимые жанры (введите номера через запятую):")
        genres_list = list(Genre)
        for i, genre in enumerate(genres_list, 1):
            print(f"{i}. {genre.value}")

        selected_genres = []
        try:
            choices = input("Ваш выбор (например: 1,3,5): ").strip()
            if choices:
                choices = [int(c.strip()) for c in choices.split(',')]
                for choice in choices:
                    if 1 <= choice <= len(genres_list):
                        selected_genres.append(genres_list[choice - 1])
        except ValueError:
            print("Неверный формат ввода!")

        # Создаем пользователя
        user = User(user_id, name)
        for genre in selected_genres:
            user.add_favorite_genre(genre)

        self.library.add_user(user)

        print(f"\nПользователь {name} успешно зарегистрирован!")
        if selected_genres:
            print(f"Любимые жанры: {', '.join([g.value for g in selected_genres])}")
        input("Нажмите Enter для продолжения...")

    def login_user(self):
        self.print_header("ВХОД В СИСТЕМУ")

        users = self.library.list_users()
        if not users:
            print("В системе пока нет пользователей.")
            choice = input("Хотите зарегистрироваться? (да/нет): ").lower()
            if choice == 'да':
                self.register_user()
            return

        print("\nСписок пользователей:")
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.name} (ID: {user.id})")

        try:
            choice = int(input("\nВыберите номер пользователя: "))
            if 1 <= choice <= len(users):
                self.current_user = users[choice - 1]
                print(f"\nДобро пожаловать, {self.current_user.name}!")
            else:
                print("Неверный номер!")
        except ValueError:
            print("Пожалуйста, введите число!")

        input("Нажмите Enter для продолжения...")

    def view_profile(self):
        if not self.current_user:
            print("Сначала войдите в систему!")
            input("Нажмите Enter для продолжения...")
            return

        while True:
            self.clear_screen()
            self.print_header(f"ПРОФИЛЬ: {self.current_user.name}")

            print(f" Имя: {self.current_user.name}")
            print(f" ID: {self.current_user.id}")
            print(f" ЛЮБИМЫЕ ЖАНРЫ ({len(self.current_user.favorite_genres)}):")
            if self.current_user.favorite_genres:
                for i, genre in enumerate(self.current_user.favorite_genres, 1):
                    print(f"  {i}. {genre.value}")
            else:
                print("  Жанры не указаны")

            print(f"\n ОЦЕНЕННЫХ ФИЛЬМОВ: {len(self.current_user.ratings)}")
            if self.current_user.ratings:
                for movie_id, rating in list(self.current_user.ratings.items())[:5]:  # Показываем первые 5
                    movie = self.library.get_movie(movie_id)
                    if movie:
                        print(f"  • {movie.title}: {rating}/10")

            print("\n" + "-" * 50)
            print("МЕНЮ ПРОФИЛЯ:")
            print("1. Изменить любимые жанры")
            print("2. Вернуться в главное меню")

            choice = input("\nВыберите действие: ").strip()

            if choice == '1':
                self._edit_genres()
            elif choice == '2':
                break
            else:
                print("Неверный выбор!")
                input("Нажмите Enter для продолжения...")

    def _edit_genres(self):
        """Редактирование любимых жанров пользователя"""
        self.clear_screen()
        self.print_header("РЕДАКТИРОВАНИЕ ЛЮБИМЫХ ЖАНРОВ")

        print("Текущие любимые жанры:")
        if self.current_user.favorite_genres:
            for genre in self.current_user.favorite_genres:
                print(f"  • {genre.value}")
        else:
            print("  Нет любимых жанров")

        print("\n1. Добавить жанры")
        print("2. Удалить жанры")
        print("3. Очистить все жанры")
        print("4. Назад")

        choice = input("\nВыберите действие: ").strip()

        if choice == '1':
            self._add_genres()
        elif choice == '2':
            self._remove_genres()
        elif choice == '3':
            self.current_user._favorite_genres.clear()
            print("Все жанры удалены!")
            input("Нажмите Enter для продолжения...")
        elif choice == '4':
            return
        else:
            print("Неверный выбор!")
            input("Нажмите Enter для продолжения...")

    def _add_genres(self):
        """Добавление жанров"""
        print("\nВыберите жанры для добавления (введите номера через запятую):")
        genres_list = list(Genre)
        for i, genre in enumerate(genres_list, 1):
            print(f"{i}. {genre.value}")

        try:
            choices = input("Ваш выбор: ").strip()
            if choices:
                choices = [int(c.strip()) for c in choices.split(',')]
                added_count = 0
                for choice in choices:
                    if 1 <= choice <= len(genres_list):
                        genre = genres_list[choice - 1]
                        if genre not in self.current_user.favorite_genres:
                            self.current_user.add_favorite_genre(genre)
                            added_count += 1

                if added_count > 0:
                    print(f"Добавлено {added_count} жанров!")
                else:
                    print("Не было добавлено новых жанров.")
        except ValueError:
            print("Неверный формат ввода!")

        input("Нажмите Enter для продолжения...")

    def _remove_genres(self):
        """Удаление жанров"""
        if not self.current_user.favorite_genres:
            print("Нет жанров для удаления!")
            input("Нажмите Enter для продолжения...")
            return

        print("\nВыберите жанры для удаления (введите номера через запятую):")
        for i, genre in enumerate(self.current_user.favorite_genres, 1):
            print(f"{i}. {genre.value}")

        try:
            choices = input("Ваш выбор: ").strip()
            if choices:
                choices = [int(c.strip()) for c in choices.split(',')]
                removed_count = 0
                # Сортируем в обратном порядке, чтобы индексы не сбивались при удалении
                for choice in sorted(choices, reverse=True):
                    if 1 <= choice <= len(self.current_user.favorite_genres):
                        self.current_user.favorite_genres.pop(choice - 1)
                        removed_count += 1

                if removed_count > 0:
                    print(f"Удалено {removed_count} жанров!")
                else:
                    print("Не было удалено ни одного жанра.")
        except ValueError:
            print("Неверный формат ввода!")

        input("Нажмите Enter для продолжения...")

    def browse_movies(self):
        """Просмотр и оценка фильмов"""
        if not self.current_user:
            print("Сначала войдите в систему!")
            input("Нажмите Enter для продолжения...")
            return

        while True:
            self.clear_screen()
            self.print_header("ПРОСМОТР И ОЦЕНКА ФИЛЬМОВ")

            all_movies = self.library.list_movies()

            print("СПИСОК ФИЛЬМОВ:\n")

            for i, movie in enumerate(all_movies, 1):
                # Проверяем, оценил ли пользователь этот фильм
                user_rating = self.current_user.ratings.get(movie.id)
                rating_text = f" (Ваша оценка: {user_rating}/10)" if user_rating else ""

                print(f"{i}. {movie.title} ({movie._year})")
                print(f" Жанры: {', '.join([g.value for g in movie.genres])}")
                print(f" Режиссер: {movie._director}")
                print(f" Рейтинг: {movie.rating}/10{rating_text}")
                print("-" * 40)

            print("\nВОЗМОЖНЫЕ ДЕЙСТВИЯ:")
            print("1. Оценить фильм")
            print("2. Получить рекомендации")
            print("3. Вернуться в главное меню")

            choice = input("\nВыберите действие: ").strip()

            if choice == '1':
                self._rate_movie(all_movies)
            elif choice == '2':
                self.get_recommendations()
            elif choice == '3':
                break
            else:
                print("Неверный выбор!")
                input("Нажмите Enter для продолжения...")

    def _rate_movie(self, all_movies):
        """Оценка выбранного фильма"""
        try:
            movie_num = int(input("\nВведите номер фильма для оценки: "))
            if 1 <= movie_num <= len(all_movies):
                movie = all_movies[movie_num - 1]

                # Проверяем, есть ли уже оценка
                current_rating = self.current_user.ratings.get(movie.id)
                if current_rating:
                    print(f"Вы уже оценили этот фильм на {current_rating}/10")
                    change = input("Хотите изменить оценку? (да/нет): ").lower()
                    if change != 'да':
                        return

                # Запрашиваем новую оценку
                while True:
                    try:
                        rating = float(input(f"Оцените фильм '{movie.title}' (0-10): "))
                        if 0 <= rating <= 10:
                            self.current_user.add_rating(movie, rating)
                            print(f"Спасибо! Вы оценили фильм '{movie.title}' на {rating}/10")
                            break
                        else:
                            print("Оценка должна быть от 0 до 10!")
                    except ValueError:
                        print("Пожалуйста, введите число!")
        except ValueError:
            print("Неверный номер фильма!")

        input("Нажмите Enter для продолжения...")

    def get_recommendations(self):
        """Получение рекомендаций по разным стратегиям"""
        if not self.current_user:
            print("Сначала войдите в систему!")
            input("Нажмите Enter для продолжения...")
            return

        while True:
            self.clear_screen()
            self.print_header("РЕКОМЕНДАЦИИ ФИЛЬМОВ")

            print("ВЫБЕРИТЕ СТРАТЕГИЮ РЕКОМЕНДАЦИЙ:")
            print("1. По любимым жанрам")
            print("2. По рейтингу фильмов")
            print("3. От похожих пользователей")
            print("4. Назад")

            choice = input("\nВыберите стратегию: ").strip()

            recommendations = []
            strategy_name = ""

            if choice == '1':
                # Рекомендации по жанрам
                strategy = genre_recommend(self.library)
                recommendations = strategy.recommend(self.current_user)
                strategy_name = "По вашим любимым жанрам"
            elif choice == '2':
                # Рекомендации по рейтингу
                strategy = rating_recommend(self.library)
                recommendations = strategy.recommend(self.current_user)
                strategy_name = "По рейтингу фильмов"
            elif choice == '3':
                # Рекомендации от похожих пользователей
                strategy = similar_users_recommend(self.current_user)
                recommendations = strategy.recommend()
                strategy_name = "От похожих пользователей"
            elif choice == '4':
                break
            else:
                print("Неверный выбор!")
                input("Нажмите Enter для продолжения...")
                continue

            # Вывод рекомендаций
            self.clear_screen()
            self.print_header(f"РЕКОМЕНДАЦИИ: {strategy_name}")

            if recommendations:
                print(f"Найдено {len(recommendations)} рекомендаций:\n")

                for i, movie in enumerate(recommendations[:10], 1):  # Показываем первые 10
                    print(f"{i}. {movie.title} ({movie._year})")
                    print(f"   Жанры: {', '.join([g.value for g in movie.genres])}")
                    print(f"   Режиссер: {movie._director}")
                    print(f"   Рейтинг: {movie.rating}/10")

                    # Проверяем, оценил ли уже пользователь этот фильм
                    if movie.id in self.current_user.ratings:
                        print(f"   ⚠ Вы уже оценили этот фильм")

                    print("-" * 40)

                if len(recommendations) > 10:
                    print(f"... и еще {len(recommendations) - 10} фильмов")

                # Предложение оценить рекомендованный фильм
                print("\nХотите оценить один из рекомендованных фильмов?")
                rate_choice = input("Введите номер фильма для оценки или 'нет' для возврата: ").strip()

                if rate_choice.lower() != 'нет':
                    try:
                        movie_num = int(rate_choice)
                        if 1 <= movie_num <= min(10, len(recommendations)):
                            movie = recommendations[movie_num - 1]
                            while True:
                                try:
                                    rating = float(input(f"Оцените фильм '{movie.title}' (0-10): "))
                                    if 0 <= rating <= 10:
                                        self.current_user.add_rating(movie, rating)
                                        print(f"Спасибо! Вы оценили фильм '{movie.title}' на {rating}/10")
                                        break
                                    else:
                                        print("Оценка должна быть от 0 до 10!")
                                except ValueError:
                                    print("Пожалуйста, введите число!")
                    except ValueError:
                        print("Неверный номер фильма!")
            else:
                print("К сожалению, по выбранной стратегии рекомендаций не найдено.")
                print("Попробуйте другую стратегию или добавьте больше оценок фильмов.")

            input("\nНажмите Enter для продолжения...")

    def main_menu(self):
        while True:
            self.clear_screen()
            self.print_header("КИНОТЕКА - СИСТЕМА РЕКОМЕНДАЦИЙ")

            if self.current_user:
                print(f"\nТекущий пользователь: {self.current_user.name}")
                print("-" * 50)

            print("\nГЛАВНОЕ МЕНЮ:")
            print("1. Регистрация нового пользователя")
            print("2. Вход в систему")
            print("3. Просмотр и оценка фильмов")
            print("4. Получить рекомендации")
            print("5. Профиль")
            print("6. Выход")

            if not self.current_user:
                print("\n⚠ Сначала войдите в систему или зарегистрируйтесь!")

            choice = input("\nВыберите действие: ").strip()

            if choice == '6':
                print("\nСпасибо за использование системы!")
                break
            elif choice in ['3', '4'] and not self.current_user:
                print("\n⚠ Для этого действия требуется авторизация!")
                input("Нажмите Enter для продолжения...")
            elif choice == '1':
                self.register_user()
            elif choice == '2':
                self.login_user()
            elif choice == '3':
                self.browse_movies()
            elif choice == '4':
                self.get_recommendations()
            elif choice == '5':
                self.view_profile()
            else:
                print("Неверный выбор!")
                input("Нажмите Enter для продолжения...")


def main():
    interface = ConsoleInterface()
    interface.main_menu()


if __name__ == "__main__":
    main()