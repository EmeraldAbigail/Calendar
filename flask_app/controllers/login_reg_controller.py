from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# Route for Login/Registration
@app.route("/")
def index():
    return render_template("index.html")

# Route for user's registration information
@app.route("/user/register", methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect("/")  # Redirect on validation failure

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect("/main")
