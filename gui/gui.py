from data.data import User
from data.data_manager.managing_data import MovieLibrary
import recommendations.recommendations

class ConsoleInterface:
    def __init__(self):
        self.library = MovieLibrary()
        self.current_user = None

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


        user = User(user_id, name)
        self.library.add_user(user)

        print(f"\nПользователь {name} успешно зарегистрирован!")
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

    def _show_all_movies(self):
        """Показать все фильмы"""
        movies = self.library.list_movies()

        if not movies:
            print("Нет фильмов для отображения.")
            return

        self.print_header("ВСЕ ФИЛЬМЫ")
        print(f"Всего фильмов в библиотеке: {len(movies)}")

        # Отображаем фильмы
        for i, movie in enumerate(movies, 1):
            user_rating = self.current_user.ratings.get(movie.id)
            rating_text = f"Ваша оценка: {user_rating}/10" if user_rating else "Не оценено"

            print(f"\n{i}. {movie.title} ({movie.year})")
            print(f"   Режиссер: {movie.director}")
            print(f"   Жанры: {', '.join([g.value for g in movie.genres])}")
            print(f"   Рейтинг: {movie.rating:.1f}/10 | {rating_text}")

    def browse_movies(self):
        if not self.current_user:
            print("Сначала войдите в систему!")
            return

        self.print_header("ПРОСМОТР ФИЛЬМОВ")

        movies = self.library.list_movies()

        while True:
            print(f"\nВсего фильмов в библиотеке: {len(movies)}")
            print("\nВыберите действие:")
            print("1. Показать все фильмы")
            print("2. Фильтровать по жанру")
            print("3. Фильтровать по рейтингу (общественному)")
            print("4. Фильтровать по возможно вам понравиться")
            print("5. Вернуться в главное меню")

            choice = input("\nВаш выбор: ").strip()
            if choice == '1':
                self._show_all_movies()
            # elif choice == '2':
            #     self.
            # elif choice == '3':
            #     self.
            # elif choice == '4':
            #     self.
            elif choice == '5':
                break
            else:
                print("Неверный выбор!")

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

            print("\n" + "-" * 50)
            print("МЕНЮ ПРОФИЛЯ:")
            print("1. Изменить любимые жанры")
            print("2. Вернуться в главное меню")

            choice = input("\nВыберите действие: ").strip()
            # мне кажеться можно и без словаря
            if choice == '1':
                print('be')
            elif choice == '2':
                break
            else:
                print("Неверный выбор!")
                input("Нажмите Enter для продолжения...")


    def main_menu(self):
        actions = {
            '1': self.register_user,
            '2': self.login_user,
            '3': self.browse_movies,
            '4': self.view_profile,
            '5': 'exit'
        }

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
            elif choice in actions:
                actions[choice]()
            else:
                print("Неверный выбор!")
                input("Нажмите Enter для продолжения...")

def main():
    interface = ConsoleInterface()
    interface.main_menu()


if __name__ == "__main__":
    main()