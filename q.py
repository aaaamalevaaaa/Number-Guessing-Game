import random
import math
import json
from colorama import init, Fore

init(autoreset=True)

error_messages = {  # словарь сообщений об ошибках
    "not_a_number": "Вы ввели не число. Пожалуйста, попробуйте еще раз.",
    "negative_number": "Число должно быть неотрицательным.",
    "max_less_than_min": "Максимальное значение должно быть больше минимального.",
    "wrong_guess": "Вы потратили попытку впустую."
}

achievements = {  # словарь ачивок
    "first_win": "Первая победа!",
    "five_wins": "5 побед!",
    "ten_wins": "10 побед!",
    "first_try": "С первой попытки!"
}


def get_non_negative_integer(prompt):  # проверка на ввод неотрицательного числа
    while True:
        try:
            number = int(input(prompt))
            if number < 0:
                print(Fore.RED + error_messages['negative_number'])
            else:
                return number
        except ValueError:
            print(Fore.RED + error_messages['not_a_number'])


def give_hint(number):  # использование подсказок
    try:
        with open('number_facts_corrected.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if str(number) in data and data[str(number)]:
                return random.choice(data[str(number)])
            else:
                return "Нет доступных фактов для этого числа."
    except FileNotFoundError:
        return "Файл с фактами не найден."
    except json.JSONDecodeError:
        return "Ошибка чтения файла с фактами."


def save_statistics(games_played, wins, losses, points, level, experience, achievements1):  # сохранение статистики
    data = {
        "games_played": games_played,
        "wins": wins,
        "losses": losses,
        "points": points,
        "level": level,
        "experience": experience,
        "achievements": achievements1
    }
    with open('statistics.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def load_statistics():  # загрузка статистики
    try:
        with open('statistics.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return (data.get('games_played', 0),
                    data.get('wins', 0),
                    data.get('losses', 0),
                    data.get('points', 0),
                    data.get('level', 1),
                    data.get('experience', 0),
                    data.get('achievements', []))
    except FileNotFoundError:
        return 0, 0, 0, 0, 1, 0, []


def display_statistics(games_played, wins, losses, points, level, experience):  # показ статистики
    print(Fore.CYAN + "+--------------------+-----------+")
    print(Fore.CYAN + f"| Сыграно игр        | {games_played:9d} |")
    print(Fore.CYAN + f"| Победы             | {wins:9d} |")
    print(Fore.CYAN + f"| Поражения          | {losses:9d} |")
    print(Fore.CYAN + f"| Очки               | {points:9d} |")
    print(Fore.CYAN + f"| Уровень            | {level:9d} |")
    print(Fore.CYAN + f"| Опыт               | {experience:9d} |")
    print(Fore.CYAN + "+--------------------+-----------+")


def choose_difficulty():  # уровни сложности
    print(Fore.YELLOW + "Выберите уровень сложности:")
    print("1. Легкий")
    print("2. Средний")
    print("3. Сложный")
    while True:
        choice = input("Введите 1, 2 или 3: ")
        if choice == '1':
            min_range, max_range = 10, 100
        elif choice == '2':
            min_range, max_range = 100, 1000
        elif choice == '3':
            min_range, max_range = 1000, 10000
        else:
            print(Fore.RED + "Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")
            continue

        range_size = random.randint(min_range, max_range)
        min_value = random.randint(1, 10000 - range_size)
        max_value = min_value + range_size
        return min_value, max_value


def play_game(mode):  # игра
    min_value, max_value = choose_difficulty()
    print(Fore.GREEN + f"Ваш диапазон чисел: от {min_value} до {max_value}")
    random_number = random.randint(min_value, max_value)
    attempts = math.ceil(math.log2(max_value - min_value + 1))
    hints_available = 2
    points = 0

    if mode == "да":
        attempts *= 2
        hints_available *= 2

    previous_guesses = set()
    initial_attempts = attempts
    last_guess = None

    while attempts > 0:
        print(Fore.YELLOW + f"У вас осталось {attempts} попыток.")
        user_guess = input("Введите вашу догадку (или 'п' для подсказки): ")

        if user_guess.lower() in ["п", "подсказка"]:
            if hints_available > 0:
                hint = give_hint(random_number)
                print(Fore.MAGENTA + hint)
                hints_available -= 1
                print(Fore.MAGENTA + f"(осталось {hints_available} подсказок)")
            else:
                print(Fore.RED + "Подсказки закончились. Попытка не потрачена.")
            continue

        try:
            user_guess = int(user_guess)
            if user_guess < min_value or user_guess > max_value:
                print(Fore.RED + f"Число должно быть в диапазоне от {min_value} до {max_value}.")
                attempts -= 1
                print(Fore.RED + error_messages['wrong_guess'])
            elif user_guess in previous_guesses:
                print(Fore.RED + "Вы уже пытались это число. Попытка потрачена впустую.")
                attempts -= 1
            else:
                if last_guess is not None:
                    if (random_number > last_guess > user_guess) or \
                            (random_number < last_guess < user_guess):
                        print(Fore.RED + "Попытка была потрачена впустую.")
                        attempts -= 1
                    else:
                        if user_guess < random_number:
                            print(Fore.BLUE + "Число больше.")
                        elif user_guess > random_number:
                            print(Fore.BLUE + "Число меньше.")
                        else:
                            print(Fore.GREEN + "Поздравляем! Вы угадали число!")
                            points += attempts * 10
                            return True, points, attempts == initial_attempts
                        attempts -= 1
                else:
                    if user_guess < random_number:
                        print(Fore.BLUE + "Загаданное число больше.")
                    elif user_guess > random_number:
                        print(Fore.BLUE + "Загаданное число меньше.")
                    else:
                        print(Fore.GREEN + "Поздравляем, вы угадали!")
                        points += attempts * 10
                        return True, points, attempts == initial_attempts
                    attempts -= 1

                previous_guesses.add(user_guess)
                last_guess = user_guess
        except ValueError:
            print(Fore.RED + error_messages['not_a_number'])
            attempts -= 1
            print(Fore.RED + error_messages['wrong_guess'])

    print(Fore.RED + f"Вы проиграли. Загаданное число было: {random_number}")
    return False, points, False


def update_statistics(won, points, first_try):  # обновление статистики
    games_played, wins, losses, total_points, level, experience, achieved = load_statistics()
    games_played += 1
    if won:
        wins += 1
        experience += points
    else:
        losses += 1
    total_points += points

    if won and wins == 1 and "first_win" not in achieved:
        achieved.append("first_win")
        print(Fore.GREEN + f"Достижение разблокировано: {achievements['first_win']}")
    if won and wins == 5 and "five_wins" not in achieved:
        achieved.append("five_wins")
        print(Fore.GREEN + f"Достижение разблокировано: {achievements['five_wins']}")
    if won and wins == 10 and "ten_wins" not in achieved:
        achieved.append("ten_wins")
        print(Fore.GREEN + f"Достижение разблокировано: {achievements['ten_wins']}")
    if won and first_try and "first_try" not in achieved:
        achieved.append("first_try")
        print(Fore.GREEN + f"Достижение разблокировано: {achievements['first_try']}")

    while experience >= level * 100:
        experience -= level * 100
        level += 1
        print(Fore.YELLOW + f"Поздравляем! Вы достигли уровня {level}!")

    save_statistics(games_played, wins, losses, total_points, level, experience, achieved)
    display_statistics(games_played, wins, losses, total_points, level, experience)


def main_menu():  # меню
    games_played, wins, losses, points, level, experience, achieved = load_statistics()
    while True:
        print(Fore.CYAN + "\n=== Главное меню ===")
        print("1. Играть")
        print("2. Посмотреть статистику")
        print("3. Выйти")
        choice = input("Выберите опцию: ")

        if choice == '1':
            mode = input("Включить режим для новичка? (да/нет(что угодно)): ").lower()
            won, points_earned, first_try = play_game(mode)
            update_statistics(won, points_earned, first_try)
        elif choice == '2':
            display_statistics(games_played, wins, losses, points, level, experience)
        elif choice == '3':
            print(Fore.YELLOW + "Спасибо за игру! До свидания!")
            break
        else:
            print(Fore.RED + "Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")


if __name__ == "__main__":  # запуск
    print(Fore.GREEN + 'Добро пожаловать в игру "Угадай число"!')
    main_menu()
