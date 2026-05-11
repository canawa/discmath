def check_if_boolean(expression_1, expression_2):
    if not isinstance(expression_1, int) or not isinstance(expression_2, int): # если не булевое
        raise ValueError('Введенные выражения не являются булевыми')

def inv(expression):
    """ Инверсия (Логическое НЕТ)"""
    if not isinstance(expression, int): # если не булевое
        raise ValueError('Ожидаются значения 0 или 1')
    return expression^1

def disj(expression_1, expression_2):
    """Дизъюнкция между двумя выражениями (Логическое ИЛИ)"""
    check_if_boolean(expression_1, expression_2)
    return expression_1 | expression_2

def conj(expression_1, expression_2):
    """Конъюнкция между двумя выражениями (Логическое И)"""
    check_if_boolean(expression_1, expression_2)
    return expression_1 & expression_2

def xor(expression_1, expression_2):
    """Сложение по модулю 2 между двумя выражениями (Логическое И)"""
    check_if_boolean(expression_1, expression_2)
    return expression_1 ^ expression_2

def eq(expression_1, expression_2):
    """Эквиваленция (Отрицание XOR)"""
    check_if_boolean(expression_1, expression_2)
    return inv(xor(expression_1, expression_2))

def imp(expression_1, expression_2):
    """Импликация (НЕ А ИЛИ Б)"""
    check_if_boolean(expression_1, expression_2)
    return disj(inv(expression_1), expression_2)

def pierce(expression_1, expression_2):
    """Стрелка пирса """
    check_if_boolean(expression_1,expression_2)
    return inv(disj(expression_1,expression_2))

def sheffer(expression_1, expression_2):
    """Штрих Шеффера"""
    check_if_boolean(expression_1, expression_2)
    return inv(conj(expression_1, expression_2))