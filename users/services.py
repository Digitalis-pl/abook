import secrets
import string


def make_random_password():
    character = string.ascii_letters + string.digits
    password = "".join(secrets.choice(character) for symbol in range(16))

    return password


print(make_random_password())
