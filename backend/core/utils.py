def get_int(str):
    """Безопасное преобразование строки в в целое число."""
    try:
        return int(str)
    except TypeError:
        return None
