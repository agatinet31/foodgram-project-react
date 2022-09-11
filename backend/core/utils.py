def is_not_empty_query(query):
    """Проверка наличия записей в QyerySet."""
    return query.all().count() > 0
