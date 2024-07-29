import json
import math


def generate_number_facts(start, end):  # генерация JSON файла с математическими фактами о числах
    facts = {}
    for num in range(start, end + 1):
        facts[str(num)] = []

        if is_even(num):
            facts[str(num)].append("Четное число")
        else:
            facts[str(num)].append("Нечетное число")
        if is_prime(num):
            facts[str(num)].append("Простое число")
        if is_square_number(num):
            facts[str(num)].append("Квадрат целого числа")
        if is_cube_number(num):
            facts[str(num)].append("Куб целого числа")
        if is_fibonacci_number(num):
            facts[str(num)].append("Число Фибоначчи")
        if is_mersenne_prime(num):
            facts[str(num)].append("Число Мерсенна")
        if is_lucas_number(num):
            facts[str(num)].append("Число Люка")
        if is_harshad_number(num):
            facts[str(num)].append("Число Харшадха")
        if is_triangular_number(num):
            facts[str(num)].append("Треугольное число")
        if is_palindromic_number(num):
            facts[str(num)].append("Палиндромное число")
        if is_happy_number(num):
            facts[str(num)].append("Счастливое число")
        if is_twin_prime(num):
            facts[str(num)].append("Число-близнец")
        if is_wilson_prime(num):
            facts[str(num)].append("Число Вилсона")
        if is_fermat_number(num):
            facts[str(num)].append("Число Ферма")
        if is_sophie_germain_prime(num):
            facts[str(num)].append("Число Софи Жермен")
        if is_semiprime(num):
            facts[str(num)].append("Полупростое число")
        if is_perfect_number(num):
            facts[str(num)].append("Совершенное число")

    with open('number_facts_corrected.json', 'w', encoding='utf-8') as f:
        json.dump(facts, f, indent=4, ensure_ascii=False)

    print("JSON-файл с числовыми фактами успешно создан!")


def is_even(num):
    return num % 2 == 0


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def is_square_number(num):
    return int(num ** 0.5) ** 2 == num


def is_cube_number(num):
    return round(num ** (1 / 3)) ** 3 == num


def is_fibonacci_number(num):
    x1 = 5 * num ** 2 + 4
    x2 = 5 * num ** 2 - 4
    return int(x1 ** 0.5) ** 2 == x1 or int(x2 ** 0.5) ** 2 == x2


def is_triangular_number(num):
    n = (-1 + (1 + 8 * num) ** 0.5) / 2
    return n.is_integer()


def is_palindromic_number(num):
    return str(num) == str(num)[::-1]


def is_happy_number(num):
    def get_next(n):
        return sum(int(char) ** 2 for char in str(n))

    slow = num
    fast = get_next(num)
    while fast != 1 and slow != fast:
        slow = get_next(slow)
        fast = get_next(get_next(fast))
    return fast == 1


def is_harshad_number(num):
    if num == 0:
        return False
    return num % sum(int(char) for char in str(num)) == 0


def is_lucas_number(num):
    if num == 2 or num == 1:
        return True
    a, b = 2, 1
    while b < num:
        a, b = b, a + b
    return b == num


def is_twin_prime(num):
    return is_prime(num) and (is_prime(num - 2) or is_prime(num + 2))


def is_mersenne_prime(num):
    if not is_prime(num):
        return False
    p = 1
    while (1 << p) - 1 <= num:
        if (1 << p) - 1 == num:
            return True
        p += 1
    return False


def is_wilson_prime(num):
    if not is_prime(num):
        return False
    factorial = 1
    for i in range(1, num):
        factorial *= i
    return (factorial + 1) % (num * num) == 0


def is_fermat_number(num):
    i = 0
    while (2 ** (2 ** i) + 1) <= num:
        if (2 ** (2 ** i) + 1) == num:
            return True
        i += 1
    return False


def is_sophie_germain_prime(num):
    return is_prime(num) and is_prime(2 * num + 1)


def is_semiprime(num):
    count = 0
    for i in range(2, int(num ** 0.5) + 1):
        while num % i == 0:
            num //= i
            count += 1
        if count > 2:
            return False
    if num > 1:
        count += 1
    return count == 2


def is_perfect_number(num):
    if num < 2:
        return False
    sum_of_divisors = 1
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            sum_of_divisors += i
            if i != num // i:
                sum_of_divisors += num // i
    return sum_of_divisors == num


generate_number_facts(0, 10000)
