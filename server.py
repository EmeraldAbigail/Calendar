from flask_app.models.user import User
from flask_app.controllers import user_controller
from flask_app.controllers import login_reg_controller
# from flask_app.controllers import event_controller
# from flask_app.controllers import calendar_controller
#server.py

from flask_app import app

if __name__ == "__main__":
    app.run (debug=True)