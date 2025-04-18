class UserNotFoundException(Exception):
    detail = 'Incorrect username'

class UsernameIsTakenException(Exception):
    detail = "Incorrect username"

class WeakPasswordException(Exception):
    detail = "Weak password"

class IncorrectAuthPasswordException(Exception):
    detail = "Incorrect password"

class TokenExpired(Exception):
    detail = "Token expired"

class TokenIncorrect(Exception):
    detail = "Token Incorrect"
