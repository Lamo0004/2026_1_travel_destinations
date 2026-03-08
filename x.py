from flask import request, make_response
import mysql.connector
import re # Libeary to regular expressions (also called Regex)
from functools import wraps

# Denne fil ved ikke noget om browseren

################################ 
def db():
    try:
        db = mysql.connector.connect(
            host = "mariadb",
            user = "root",  
            password = "password",
            database = "2026_1_travel_destinations"
        )
        cursor = db.cursor(dictionary=True)
        return db, cursor
    except Exception as e:
        print(e, flush=True)
        raise Exception("Database under maintenance", 500)


################################ 
# Funktion som clear cache i browseren – så man ikke kan klikke på tilbage-pil og blive logget ind igen efter log ud
def no_cache(view):
    @wraps(view)
    def no_cache_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache_view


################ Validation first name ################ 
USER_FIRST_NAME_MIN = 2
USER_FIRST_NAME_MAX = 20
REGEX_USER_FIRST_NAME = f"^.{{{USER_FIRST_NAME_MIN},{USER_FIRST_NAME_MAX}}}$"
def validate_user_first_name():
    user_first_name = request.form.get("user_first_name", "").strip()
    if not re.match(REGEX_USER_FIRST_NAME, user_first_name):
        raise Exception("company_exception user_first_name")
    return user_first_name


################ Validation last name ################ 
USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20
REGEX_USER_LAST_NAME = f"^.{{{USER_LAST_NAME_MIN},{USER_LAST_NAME_MAX}}}$"
def validate_user_last_name():
    user_last_name = request.form.get("user_last_name", "").strip()
    if not re.match(REGEX_USER_LAST_NAME, user_last_name):
        raise Exception("company_exception user_last_name")
    return user_last_name


################ Validation email ################ 
REGEX_USER_EMAIL = "^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
def validate_user_email():
    user_email = request.form.get("user_email", "").strip()
    if not re.match(REGEX_USER_EMAIL, user_email):
        raise Exception("company_exception user_email")
    return user_email


################ Validation password ################ 
USER_PASSWORD_MIN = 8
USER_PASSWORD_MAX = 50
REGEX_USER_PASSWORD = f"^.{{{USER_PASSWORD_MIN},{USER_PASSWORD_MAX}}}$"
def validate_user_password():
    user_password = request.form.get("user_password", "").strip()
    if not re.match(REGEX_USER_PASSWORD, user_password):
        raise Exception("company_exception user_password")
    return user_password




