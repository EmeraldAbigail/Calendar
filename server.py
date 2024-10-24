from flask_app.models.user import User
from flask_app.controllers import users_controller
from flask_app.controllers import events_controller
from flask_app.controllers import login_reg_controller
from flask_app.controllers import items_controller
#server.py

from flask_app import app

if __name__ == "__main__":
    app.run (debug=True)