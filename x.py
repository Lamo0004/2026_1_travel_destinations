from flask import request, make_response
import mysql.connector
import re # Libeary to regular expressions (also called Regex)
from functools import wraps
import time
from datetime import datetime

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


################ Validation title ################ 
DESTINATION_TITLE_MIN = 2
DESTINATION_TITLE_MAX = 35
REGEX_DESTINATION_TITLE = f"^.{{{DESTINATION_TITLE_MIN},{DESTINATION_TITLE_MAX}}}$"
def validate_destination_title():
    destination_title = request.form.get("title", "").strip()
    if not re.match(REGEX_DESTINATION_TITLE, destination_title):
        raise Exception("company_exception destination_title")
    return destination_title


################ Validation country ################ 
DESTINATION_COUNTRY_MIN = 2
DESTINATION_COUNTRY_MAX = 50
REGEX_DESTINATION_COUNTRY = f"^.{{{DESTINATION_COUNTRY_MIN},{DESTINATION_COUNTRY_MAX}}}$"
def validate_destination_country():
    destination_country = request.form.get("country", "").strip()
    if not re.match(REGEX_DESTINATION_COUNTRY, destination_country):
        raise Exception("company_exception destination_country")
    return destination_country


################ Validation start and end dates ################ 
DATE_FROM_KEY = "date_from"
DATE_TO_KEY = "date_to"
DATE_FORMAT = "%Y-%m-%d"

def validate_destination_dates(date_from_str=None, date_to_str=None):
    if date_from_str is None:
        date_from_str = request.form.get(DATE_FROM_KEY, "").strip()
    if date_to_str is None:
        date_to_str = request.form.get(DATE_TO_KEY, "").strip()

    if not date_from_str or not date_to_str:
        raise Exception("company_exception date_missing")

    try:
        date_from = datetime.strptime(date_from_str, DATE_FORMAT)
        date_to = datetime.strptime(date_to_str, DATE_FORMAT)
    except ValueError:
        raise Exception("company_exception date_format_invalid")

    if date_from > date_to:
        raise Exception("company_exception date_from_after_date_to")

    return int(date_from.timestamp()), int(date_to.timestamp())

