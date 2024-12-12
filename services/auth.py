import bcrypt
from repositories import employees

def register(name, email, password, job_title):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    employees.insert(name, email, hashed_password.decode("utf-8"), job_title)

def auth(email, password):
    user = employees.get_by_email(email)

    if bcrypt.checkpw(password.encode(), user[2].encode()):
        return user[0]
    else:
        return 0