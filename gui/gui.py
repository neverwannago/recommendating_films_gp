from data.data import User
from data.data_manager.managing_data import MovieLibrary

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
            print("3. Выход")

            if not self.current_user:
                print("\n⚠ Сначала войдите в систему или зарегистрируйтесь!")

            choice = input("\nВыберите действие: ").strip()

            if choice == '1':
                self.register_user()
            elif choice == '2':
                self.login_user()
            elif choice == '3':
                print("\nСпасибо за использование системы!")
                break
            else:
                print("Неверный выбор!")
                input("Нажмите Enter для продолжения...")


def main():
    interface = ConsoleInterface()
    interface.main_menu()


if __name__ == "__main__":
    main()