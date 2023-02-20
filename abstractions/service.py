def get_amount_point(
        amount: int,
) -> str:
    """
    Разбить цену точками
    :param amount: 10000
    return: 10.000
    """
    if amount < 10000:
        return str(amount)
    amount_list = []
    for element in str(amount):
        amount_list.append(element)
    last_1 = amount_list.pop(-1)
    last_2 = amount_list.pop(-1)
    last_3 = amount_list.pop(-1)
    amount_result = "".join(amount_list) + '.' + last_3 + last_2 + last_1
    return str(amount_result)
