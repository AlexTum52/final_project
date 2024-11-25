import random
from typing import Tuple


def get_secret_number(length: int) -> str:
    """Генерирует секретное число заданной длины с уникальными цифрами.

    Args:
        length: Длина секретного числа (от 2 до 10).

    Returns:
        Секретное число в виде строки.

    Raises:
        ValueError: Если длина числа вне диапазона [2, 10].
    """
    if not 2 <= length <= 10:
        raise ValueError("Длина числа должна быть от 2 до 10.")
    digits = list(range(10))
    random.shuffle(digits)
    return "".join(map(str, digits[:length]))


def check_guess(secret: str, guess: str) -> Tuple[int, int]:
    """Проверяет угаданное число и возвращает кол-во быков и коров.

    Args:
        secret: Секретное число.
        guess: Угаданное число.

    Returns:
        Кортеж (быки, коровы).

    Raises:
        ValueError: Если длины чисел не совпадают.
    """
    if len(secret) != len(guess):
        raise ValueError("Длины чисел должны совпадать.")
    bulls = cows = 0
    for i, digit in enumerate(guess):
        if digit == secret[i]:
            bulls += 1
        elif digit in secret:
            cows += 1
    return bulls, cows


def get_hints(secret: str, guess: str, request_hints: bool) -> list[str]:
    """Возвращает подсказки, если запрос есть."""
    if not request_hints:
        return []
    hints = []
    secret_set = set(secret)
    for i, digit in enumerate(guess):
        if digit in secret_set:
            if digit == secret[i]:
                hints.append("Цифра {} на правильном месте.".format(digit))
            else:
                hints.append(
                    "Цифра {} есть, но не на этом месте.".format(digit)
                )
    return hints


def play_bulls_and_cows():
    """Основной цикл игры."""
    game_stats = {"games_played": 0, "total_attempts": 0}
    while True:
        try:
            length = int(
                input("Введите длину секретного числа (от 2 до 10): ")
            )
            if not 2 <= length <= 10:
                raise ValueError("Длина числа должна быть от 2 до 10.")
            break
        except ValueError as e:
            print(f"Ошибка: {e}")

    secret_number = get_secret_number(length)
    attempts = []
    print("Игра началась!")
    game_stats["games_played"] += 1

    while True:
        try:
            guess = input(f"Введите {length}-значное число: ")
            if (
                len(guess) != length
                or not guess.isdigit()
                or len(set(guess)) != length
            ):
                raise ValueError(
                    "Некорректный ввод. Введите "
                    f"{length}-значное число с уникальными цифрами."
                )
            bulls, cows = check_guess(secret_number, guess)
            request_hints = (
                input("Хотите подсказки? (да/нет): ").lower() == "да"
            )
            hints = get_hints(secret_number, guess, request_hints)
            attempts.append((guess, bulls, cows))
            game_stats["total_attempts"] += 1

            print(f"Быки: {bulls}, Коровы: {cows}")
            if hints:
                print("Подсказки:")
                for hint in hints:
                    print(hint)

            if bulls == length:
                print(
                    f"Поздравляю! Вы угадали число "
                    f"{secret_number} за {len(attempts)} попыток."
                )
                print("История попыток:")
                for attempt, bulls, cows in attempts:
                    print(
                        f"Попытка: {attempt}, Быки: {bulls}, "
                        f"Коровы: {cows}"
                    )
                break
        except ValueError as e:
            print(f"Ошибка: {e}")
    print(
        f"Статистика: Сыграно игр - "
        f"{game_stats['games_played']}, всего попыток - "
        f"{game_stats['total_attempts']}"
    )


if __name__ == "__main__":
    play_bulls_and_cows()
