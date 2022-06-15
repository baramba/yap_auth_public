import random
import string

from app import bcrypt


def get_password_hash(password):
    return bcrypt.generate_password_hash(password).decode("utf-8")


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def message(status, message) -> dict:
    response_object = {"status": status, "message": message}
    return response_object


def validation_error(status, errors) -> dict:
    response_object = {"status": status, "errors": errors}

    return response_object


def err_resp(msg, reason, code):
    err = message(False, msg)
    err["error_reason"] = reason
    return err, code


def internal_err_resp():
    err = message(False, "Something went wrong during the process!")
    err["error_reason"] = "server_error"
    return err, 500
