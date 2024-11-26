from bulls_and_cows import get_secret_number, check_guess, get_hints


# Тест для генерации секретного числа (длина 3)
def test_get_secret_number_length_3():
    secret = get_secret_number(3)
    assert len(secret) == 3  # Длина числа должна быть 3
    assert len(set(secret)) == 3  # Все цифры должны быть уникальными
    assert secret.isdigit()  # Число должно состоять только из цифр


# Тест для check_guess с разными длинами чисел
def test_check_guess_length_5():
    bulls, cows = check_guess("98765", "98760")
    assert bulls == 4  # 4 быка
    assert cows == 0  # Нет коров

    bulls, cows = check_guess("98765", "12345")
    assert bulls == 0  # Нет быков
    assert cows == 0  # Нет коров


# Тест для get_hints с разными вариантами запросов
def test_get_hints_mixed():
    # Первая цифра правильная, вторая не на своем месте
    hints = get_hints("12345", "12543", True)
    assert "Цифра 1 на правильном месте." in hints
    assert "Цифра 5 есть, но не на этом месте." in hints

    # Все цифры на неправильных местах
    hints = get_hints("98765", "56789", True)
    assert "Цифра 5 есть, но не на этом месте." in hints
    assert "Цифра 6 есть, но не на этом месте." in hints
    assert "Цифра 7 есть, но не на этом месте." in hints
    assert "Цифра 8 есть, но не на этом месте." in hints
    assert "Цифра 9 есть, но не на этом месте." in hints


# Тест для check_guess с одной цифрой
def test_check_guess_one_digit():
    bulls, cows = check_guess("9", "9")
    assert bulls == 1  # Ожидаем 1 быка
    assert cows == 0  # Нет коров

    bulls, cows = check_guess("5", "3")
    assert bulls == 0  # Нет быков
    assert cows == 0  # Нет коров


# Тест для get_secret_number с минимальной длиной 2
def test_get_secret_number_length_2():
    secret = get_secret_number(2)
    assert len(secret) == 2  # Длина числа должна быть 2
    assert len(set(secret)) == 2  # Все цифры должны быть уникальными
    assert secret.isdigit()  # Число должно состоять только из цифр


# Тест для get_hints, когда запрос подсказок False
def test_get_hints_no_request():
    hints = get_hints("4567", "4675", False)
    assert hints == []  # Подсказки не запрашиваются, возвращаем пустой список


# Тест для генерации секретного числа (длина 4)
def test_get_secret_number_length_4():
    secret = get_secret_number(4)
    assert len(secret) == 4  # Длина числа должна быть 4
    assert len(set(secret)) == 4  # Все цифры должны быть уникальными
    assert secret.isdigit()  # Число должно состоять только из цифр


# Тест для check_guess с разными случаями (только быки)
def test_check_guess_only_bulls():
    bulls, cows = check_guess("54321", "54321")
    assert bulls == 5  # Все цифры на своих местах
    assert cows == 0  # Нет коров

# Тест для get_hints, когда запрос подсказок True
def test_get_hints_with_request():
    hints = get_hints("1234", "1245", True)
    assert "Цифра 1 на правильном месте." in hints
    assert "Цифра 2 на правильном месте." in hints
    assert "Цифра 4 есть, но не на этом месте." in hints
    assert len(hints) == 3  # Три подсказки
