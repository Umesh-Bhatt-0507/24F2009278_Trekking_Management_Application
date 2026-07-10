from flask import Flask
from controllers.trek_controller import trek
from controllers.staff_controller import staff
from controllers.admin_controller import admin
from controllers.user_controller import user
from extension import db

app=Flask(__name__)
app.config["SECRET_KEY"]="ashu"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///trek.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db.init_app(app)

from models.User import User
from models.Trek import Trek
from models.Booking import Booking
from models.StaffAssignment import StaffAssignment

app.register_blueprint(trek)
app.register_blueprint(staff)
app.register_blueprint(admin)
app.register_blueprint(user)

if __name__=='__main__':
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(role="admin").first()
        if not admin:
            admin=User(
                name="Admin",
                email="ashu@gmail.com",
                password="@1616856423Umesh",
                role="admin",
                status="approved"
            )
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)