import re
from validate_email import validate_email

pass_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$"
user_regex = "^[a-zA-Z0-9_.-]+$"
F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'


def isEmailValid(email):
    is_valid = validate_email(email)
    return is_valid

def isUsernameValid(user):
    if re.search(user_regex, user):
        return True
    else:
        return False

def isPasswordValid(password):
    if re.search(pass_regex, password):
        return True
    else:
        return False
