import random
import time
import sys
from typing import Tuple


def get_secret_number(length: int) -> str:
    """Генерирует секретное число заданной длины с уникальными цифрами.

    Args:
        length (int): Длина генерируемого числа.

    Returns:
        str: Секретное число.
    """
    digits = list(range(10))
    random.shuffle(digits)
    return "".join(map(str, digits[:length]))


def check_guess(secret: str, guess: str) -> Tuple[int, int]:
    """Проверяет угаданное число и возвращает количество быков и коров.

    Args:
        secret (str): Секретное число.
        guess (str): Число, введенное игроком.

    Returns:
        Tuple[int, int]: Кортеж с количеством быков и коров.
    """
    bulls = cows = 0
    for i, digit in enumerate(guess):
        if digit == secret[i]:
            bulls += 1
        elif digit in secret:
            cows += 1
    return bulls, cows


def get_hints(secret: str, guess: str, request_hints: bool) -> list[str]:
    """Возвращает подсказки, если запрос есть.

    Args:
        secret (str): Секретное число.
        guess (str): Число, введенное игроком.
        request_hints (bool): Флаг запроса подсказок.

    Returns:
        list[str]: Список подсказок.
    """
    if not request_hints:
        return []
    hints = []
    secret_set = set(secret)
    for i, digit in enumerate(guess):
        if digit in secret_set:
            if digit == secret[i]:
                hints.append(f"Цифра {digit} на правильном месте.")
            else:
                hints.append(f"Цифра {digit} есть, но не на этом месте.")
    return hints


def play_round(length: int) -> int:
    """Проводит один раунд игры с таймером.

    Args:
        length (int): Длина секретного числа.

    Returns:
        int: Количество попыток, потребовавшихся для угадывания числа.
    """
    secret_number = get_secret_number(length)
    attempts = []
    time_limit = 300  # Время на раунд (300 секунд)
    start_time = time.time()  # Время начала раунда

    print("Раунд начался! У вас есть 300 секунд.")

    while True:
        elapsed_time = time.time() - start_time
        remaining_time = time_limit - int(elapsed_time)

        if remaining_time <= 0:
            print(f"Время вышло! Секретное число было {secret_number}.")
            return len(attempts)

        try:
            guess = input(
                f"Осталось времени: {remaining_time} секунд. Введите "
                f"{length}-значное число: "
            )

            if (len(guess) != length or not guess.isdigit() or len(set(guess))
                    != length):
                raise ValueError(
                    f"Некорректный ввод. Введите "
                    f"{length}-значное число с уникальными цифрами."
                )

            bulls, cows = check_guess(secret_number, guess)
            request_hints = (input("Хотите подсказки? (да/нет): ").lower() ==
                             "да")
            hints = get_hints(secret_number, guess, request_hints)
            attempts.append((guess, bulls, cows))

            print(f"Быки: {bulls}, Коровы: {cows}")
            if hints:
                print("Подсказки:")
                for hint in hints:
                    print(hint)

            if bulls == length:
                round_time = int(time.time() - start_time)
                print(
                    f"Поздравляю! Вы угадали число {secret_number} за "
                    f"{len(attempts)} попыток и {round_time} секунд."
                )
                return len(attempts)

        except ValueError as e:
            print(f"Ошибка: {e}")


def play_bulls_and_cows() -> None:
    """Основной цикл игры с возможностью повторной игры."""
    game_stats = {"games_played": 0, "total_attempts": 0}

    while True:
        try:
            length = int(input("Введите длину секретного числа " 
                               "(от 2 до 10): "))
            if not 2 <= length <= 10:
                raise ValueError("Длина числа должна быть от 2 до 10.")
            break
        except ValueError as e:
            print(f"Ошибка: {e}")

    while True:
        attempts_this_round = play_round(length)
        game_stats["games_played"] += 1
        game_stats["total_attempts"] += attempts_this_round
        play_again = input("Сыграем еще раз? (да/нет): ").lower()
        if play_again != "да":
            break

    print(
        f"Статистика: Сыграно игр - {game_stats['games_played']}, "
        f"всего попыток - {game_stats['total_attempts']}"
    )


if __name__ == "__main__" and "pytest" not in sys.argv:
    play_bulls_and_cows()
