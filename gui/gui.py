from data.data import User, Genre, Movie
from data.data_manager.managing_data import MovieLibrary
from data.data import TestData
import recommendations.recommendations


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
            print("3. Просмотр фильмов")
            print("4. Профиль")
            print("5. Выход")

            if not self.current_user:
                print("\n⚠ Сначала войдите в систему или зарегистрируйтесь!")

            choice = input("\nВыберите действие: ").strip()

            if choice == '5':
                print("\nСпасибо за использование системы!")
                break
            elif choice == '3' and not self.current_user:
                print("\n⚠ Для этого действия требуется авторизация!")
                input("Нажмите Enter для продолжения...")
            elif choice == '1':
                self.register_user()
            elif choice == '2':
                self.login_user()
            elif choice == '3':
                self.browse_movies()
            elif choice == '4':
                self.view_profile()
            else:
                print("Неверный выбор!")
                input("Нажмите Enter для продолжения...")


def main():
    interface = ConsoleInterface()
    interface.main_menu()


if __name__ == "__main__":
    main()