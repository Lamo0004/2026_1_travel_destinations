from flask import Flask, render_template, request, jsonify, session, redirect
import x
import uuid
import time
from datetime import datetime
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from icecream import ic
ic.configureOutput(prefix=f'*-*-*-*-* | ', includeContext=True)

app = Flask(__name__)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

############################## Tjekker log ind
# def require_login():
#     user = session.get("user")
#     if not user:
#         raise Exception("not_logged_in")
#     return user

############################## 
@app.template_filter('timestamp_to_date')
def timestamp_to_date(ts):
    return datetime.utcfromtimestamp(int(ts)).strftime('%Y-%m-%d')

##############################
@app.get("/signup")
@x.no_cache
def show_signup():
    try:
        user = session.get("user", "")
        return render_template("page_signup.html", user=user, x=x)
    except Exception as ex:
        ic(ex)
        return "ups"


##############################
@app.post("/api-create-user")
def api_create_user(): 
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        user_hashed_password = generate_password_hash(user_password)
        #ic(user_hashed_password) #scrypt:32768:8:1$WmPlPlYX3rBxYNYU$2491db0ce0456ff9acb80ab93cd6c924150d1d4be8c9b53ba2d7160042b20a87d78074bf9fefd87483f74aeb269b461837edfda4017d340ea44855b99799d653

        user_pk = uuid.uuid4().hex
        user_created_at = int(time.time()) #

        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s);"
        cursor.execute(q, (user_pk, user_first_name, user_last_name, user_email, user_hashed_password, user_created_at))
        db.commit()

        form_signup = render_template("___form_signup.html", x=x)

        return f"""
        <browser mix-replace="form">{form_signup}</browser> 
        <browser mix-redirect="/login"></browser>
        """

    except Exception as ex:
        ic(ex)
        if "company_exception user_first_name" in str(ex):
            error_message = f"user first name must be {x.USER_FIRST_NAME_MIN} to {x.USER_FIRST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error",  message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        if "company_exception user_last_name" in str(ex):
            error_message = f"user last name must be {x.USER_LAST_NAME_MIN} to {x.USER_LAST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error",  message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        if "company_exception user_email" in str(ex):
            error_message = f"email invalid"
            ___tip = render_template("___tip.html", status="error",  message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        if "company_exception user_password" in str(ex):
            error_message = f"user password must be {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error",  message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "Duplicate entry" in str(ex) and "user_email" in str(ex):
            error_message = "Email already exists"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error",  message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close() # Locals referer til alt inde i try eller except 
        if "db" in locals(): db.close() 


##############################
@app.get("/login")
@x.no_cache
def show_login():
    try:
        user = session.get("user", "")
        if not user: return render_template("page_login.html", user=user, x=x)
        return redirect("/profile")
    except Exception as ex:
        ic(ex)
        return "ups"


##############################
@app.post("/api-login")
def api_login(): 
    try:
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()

        if not user: 
            error_message = "Invalid credentials 1"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        if not check_password_hash(user["user_password"], user_password):
            error_message = "Invalid credentials 2"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        user.pop("user_password")
        session["user"] = user

        return f"""<browser mix-redirect="/profile"></browser>"""

    except Exception as ex:
        ic(ex)
        if "company_exception user_email" in str(ex):
            error_message = f"email invalid"
            ___tip = render_template("___tip.html", status="error",  message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        if "company_exception user_password" in str(ex):
            error_message = f"user password must be {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error",  message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error",  message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close() # Locals referer til alt inde i try eller except 
        if "db" in locals(): db.close() 


##############################
@app.get("/profile")
@x.no_cache
def show_profile():
    try:
        user = session.get("user", "")
        if not user: return redirect("/login")
        return render_template("page_profile.html", user=user, x=x)
    except Exception as ex:
        ic(ex)
        return "ups"


##############################
@app.get("/logout")
def logout():
    try:
        session.clear()
        return redirect("/login")
    except Exception as ex:
        ic(ex)
        return "ups"


##############################
@app.get("/")
def show_home():
    try:
        return render_template("page_home.html")
    except Exception as ex:
        ic(ex)
        return "ups"
    

##############################
@app.get("/destinations")
def show_destinations():
    try:
        return render_template("page_destinations.html")
    except Exception as ex:
        ic(ex)
        return "ups" 


##############################
@app.get("/api/destinations")
def api_get_destinations():
    try:
        db, cursor = x.db()
        q = "SELECT * FROM destinations"
        cursor.execute(q)
        destinations = cursor.fetchall()

        return jsonify(destinations)

    except Exception as ex:
        ic(ex)
        error_message = {"error": "System under maintenance"}
        return jsonify(error_message), 500


##############################
@app.get("/api-create-destination")
def show_create_destination():
    try:
        return render_template("page_create.html", x=x)
    except Exception as ex:
        ic(ex)
        return "ups"


##############################
@app.post("/api-create-destination")
def api_create_destination():
    try:
        destination_pk = uuid.uuid4().hex
        destination_title = x.validate_destination_title()
        destination_description = request.form.get("description", "").strip()
        destination_country = x.validate_destination_country()
        destination_location = request.form.get("location", "").strip()
        date_from_str = request.form.get("date_from", "").strip()
        date_to_str = request.form.get("date_to", "").strip()
        destination_created_at = int(time.time())
        
        destination_date_from = None
        destination_date_to = None

        if date_from_str:
            destination_date_from = int(datetime.strptime(date_from_str, "%Y-%m-%d").timestamp())
        
        if date_to_str:
            destination_date_to = int(datetime.strptime(date_to_str, "%Y-%m-%d").timestamp())

        # Check at date_from ikke er efter date_to
        if destination_date_from > destination_date_to:
            return "Start date cannot be after end date", 400

        db, cursor = x.db()

        q = """
        INSERT INTO destinations (
            destination_pk,
            destination_title,
            destination_description,
            destination_country,
            destination_location,
            destination_date_from,
            destination_date_to,
            destination_created_at
        ) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(q, (
            destination_pk,
            destination_title,
            destination_description,
            destination_country,
            destination_location,
            destination_date_from,
            destination_date_to,
            destination_created_at
        ))

        db.commit()

        return '<browser mix-redirect="/destinations"></browser>'

    except Exception as ex:
        ic(ex)

        if "company_exception destination_title" in str(ex):
            error_message = f"Destination title must be {x.DESTINATION_TITLE_MIN} to {x.DESTINATION_TITLE_MAX} characters"
            ___tip = render_template("___tip.html", status="error",  message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        if "company_exception destination_country" in str(ex):
            error_message = f"Country must be {x.DESTINATION_COUNTRY_MIN} to {x.DESTINATION_COUNTRY_MAX} characters"
            ___tip = render_template("___tip.html", status="error",  message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400
        
        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error",  message=error_message)
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.delete("/api/destinations/<destination_pk>")
def delete_destination(destination_pk):
    try:
        # require_login()

        db, cursor = x.db()
        q = "DELETE FROM destinations WHERE destination_pk = %s"
        cursor.execute(q, (destination_pk,))
        db.commit()

        return "", 204

    except Exception as ex:
        ic(ex)
        return "System error", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

    
##############################
@app.get("/edit-destination/<destination_pk>")
def show_edit_destination(destination_pk):
    try:
        db, cursor = x.db()
        q = "SELECT * FROM destinations WHERE destination_pk = %s"
        cursor.execute(q, (destination_pk,))
        destination = cursor.fetchone()

        if not destination:
            return "Destination not found", 404

        return render_template("page_create.html", destination=destination, edit=True, x=x)
        return '<browser mix-redirect="/destinations"></browser>'
    except Exception as ex:
        ic(ex)
        return "System error", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


##############################
@app.post("/api-update-destination/<destination_pk>")
def api_update_destination(destination_pk):
    try:
        # Hent data fra formular
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        country = request.form.get("country", "").strip()
        location = request.form.get("location", "").strip()
        date_from_str = request.form.get("date_from", "").strip()
        date_to_str = request.form.get("date_to", "").strip()

        # Tjek at alle påkrævede felter er udfyldt
        if not title or not country or not date_from_str or not date_to_str:
            return "Missing required fields", 400

        # Konverter dato til epoch timestamp
        date_from = int(datetime.strptime(date_from_str, "%Y-%m-%d").timestamp())
        date_to = int(datetime.strptime(date_to_str, "%Y-%m-%d").timestamp())

        # Check at date_from ikke er efter date_to
        if date_from > date_to:
            return "Start date cannot be after end date", 400

        db, cursor = x.db()

        q = """
        UPDATE destinations SET
            destination_title=%s,
            destination_description=%s,
            destination_country=%s,
            destination_location=%s,
            destination_date_from=%s,
            destination_date_to=%s
        WHERE destination_pk=%s
        """

        cursor.execute(q, (title, description, country, location, date_from, date_to, destination_pk))
        db.commit()

        form_create = render_template("___form_create.html", x=x)

        return f"""
        <browser mix-replace="form">{form_create}</browser> 
        <browser mix-redirect="/destinations"></browser>
        """

        return redirect("/destinations")

    except Exception as ex:
        ic(ex)
        return "System error", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



