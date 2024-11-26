import random
import time
from typing import Tuple
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
)


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


class BullsAndCowsGUI(QWidget):
    def __init__(self) -> None:
        """Инициализация главного окна и игровых элементов."""
        super().__init__()

        self.secret_number = ""
        self.attempts = 0
        self.time_limit = 300  # Время на раунд (300 секунд)
        self.start_time = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.init_ui()

    def init_ui(self) -> None:
        """Инициализация интерфейса."""
        self.setWindowTitle("Быки и коровы")

        # Основной layout
        main_layout = QVBoxLayout()

        # Ввод длины числа
        self.length_label = QLabel("Введите длину секретного числа "
                                   "(от 2 до 10):")
        self.length_input = QLineEdit()
        self.length_input.setMaxLength(2)
        self.length_input.returnPressed.connect(self.start_game)

        # Ввод для догадки
        self.guess_label = QLabel("Введите ваше число:")
        self.guess_input = QLineEdit()
        self.guess_input.setMaxLength(10)
        self.guess_input.returnPressed.connect(self.submit_guess)

        # Отображение времени
        self.time_label = QLabel("Оставшееся время: 300 секунд")

        # Кнопка подсказки
        self.hint_button = QPushButton("Получить подсказки")
        self.hint_button.clicked.connect(self.give_hints)

        # Сообщения
        self.message_label = QLabel("")

        # Кнопка начала новой игры
        self.new_game_button = QPushButton("Начать новую игру")
        self.new_game_button.clicked.connect(self.start_game)
        self.new_game_button.setVisible(False)

        # Добавление всех элементов на окно
        main_layout.addWidget(self.length_label)
        main_layout.addWidget(self.length_input)
        main_layout.addWidget(self.guess_label)
        main_layout.addWidget(self.guess_input)
        main_layout.addWidget(self.time_label)
        main_layout.addWidget(self.hint_button)
        main_layout.addWidget(self.message_label)
        main_layout.addWidget(self.new_game_button)

        self.setLayout(main_layout)

    def start_game(self) -> None:
        """Начинает игру, генерирует секретное число и запускает таймер."""
        length = self.length_input.text()
        if not length.isdigit() or not 2 <= int(length) <= 10:
            self.show_message("Ошибка",
                              "Длина числа должна быть от 2 до 10.")
            return

        length = int(length)
        self.secret_number = get_secret_number(length)
        self.attempts = 0
        self.start_time = time.time()
        self.timer.start(1000)  # Таймер обновляется каждую секунду

        self.length_input.setVisible(False)
        self.length_label.setVisible(False)
        self.new_game_button.setVisible(False)

        self.guess_input.setVisible(True)
        self.guess_label.setVisible(True)
        self.time_label.setVisible(True)
        self.hint_button.setVisible(True)
        self.message_label.setVisible(True)

        self.update_timer()

    def update_timer(self) -> None:
        """Обновляет оставшееся время на таймере и завершает игру
        по истечении времени."""
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = self.time_limit - elapsed_time
        if remaining_time <= 0:
            self.timer.stop()
            self.show_message(
                "Время вышло",
                f"Вы не успели угадать число. Это было " 
                f"{self.secret_number}.",
            )
            self.end_game()
        else:
            self.time_label.setText(f"Оставшееся время: {remaining_time} "
                                    f"" f"секунд")

    def submit_guess(self) -> None:
        """Обрабатывает ввод числа от игрока."""
        guess = self.guess_input.text()
        if len(guess) != len(self.secret_number) or not guess.isdigit():
            self.show_message(
                "Ошибка", "Введите правильное число той же длины,"
                          " " "что и секретное."
            )
            return

        self.attempts += 1
        bulls, cows = check_guess(self.secret_number, guess)

        if bulls == len(self.secret_number):
            self.timer.stop()
            elapsed_time = int(time.time() - self.start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            self.show_message(
                "Поздравляю!",
                f"Вы угадали число {self.secret_number} за "
                f"{self.attempts} попыток!"
                f"\nВремя: {minutes} минут(ы) и {seconds} секунд(ы).",
            )
            self.end_game()
        else:
            self.message_label.setText(f"Быки: {bulls}, Коровы: {cows}")

    def give_hints(self) -> None:
        """Выводит подсказки, если игрок запросил их."""
        hints = []
        for i, digit in enumerate(self.guess_input.text()):
            if digit == self.secret_number[i]:
                hints.append(f"Цифра {digit} на правильном месте.")
            elif digit in self.secret_number:
                hints.append(f"Цифра {digit} есть, но не на этом месте.")
        if hints:
            self.show_message("Подсказки", "\n".join(hints))
        else:
            self.show_message("Подсказки",
                              "Нет подсказок для этого числа.")

    def show_message(self, title: str, message: str) -> None:
        """Отображает сообщение в виде окна."""
        QMessageBox.information(self, title, message)

    def end_game(self) -> None:
        """Завершает игру и позволяет начать новую."""
        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        self.guess_input.clear()
        self.guess_input.setVisible(False)
        self.guess_label.setVisible(False)
        self.time_label.setVisible(False)
        self.hint_button.setVisible(False)
        self.new_game_button.setVisible(True)

        # Выводим сообщение с информацией о времени
        self.show_message(
            "Конец игры",
            f"Вы потратили {minutes} минут(ы) и {seconds} "
            f"" f"секунд(ы) на игру.",
        )


def main() -> None:
    """Основная функция для запуска приложения."""
    app = QApplication([])  # Инициализация приложения
    window = BullsAndCowsGUI()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
