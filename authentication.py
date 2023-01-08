import database


def is_authenticated_user(user_id: int) -> bool:
    return user_id in database.get_authenticated_users()
