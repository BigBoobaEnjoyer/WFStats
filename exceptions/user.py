class UserNotFoundException(Exception):
    detail = 'Incorrect username'

class UsernameIsTakenException(Exception):
    detail = "Incorrect username"