class IncorrectAuthPasswordException(Exception):
    detail = "Incorrect password"

class TokenExpired(Exception):
    detail = "Token expired"

class TokenIncorrect(Exception):
    detail = "Token Incorrect"
