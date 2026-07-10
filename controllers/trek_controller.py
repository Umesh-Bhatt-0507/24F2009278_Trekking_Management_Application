from flask import Blueprint
from flask import request,session,redirect,render_template,url_for,flash
from models.User import User
from extension import db
trek = Blueprint("trek", __name__)

@trek.route("/")
def home():
    return render_template("home.html")

@trek.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        user=User.query.filter_by(email=email,password=password).first()
        if user:
            role = user.role
            session["role"] =role
            session["user_id"]=user.id
            if role == "admin":
                return redirect("/admin")

            elif role == "staff":
                return redirect("/staff")
            else:
                return redirect("/user")
        else:
            flash('Wrong email or password')
            return redirect(url_for("trek.login")) 
    return render_template("login.html")


@trek.route('/register',methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]
        role=request.form["role"]
        print(request.form["role"])
        res=User.query.filter_by(email=email).first()
        if res:
            flash("Email already exists")
            return redirect(url_for("trek.register"))
        new_user=User(
            name=name,
            email=email,
            password=password,
            role=role,
            status="approved" if role=="user" else "pending",
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("trek.login"))
    return render_template("register.html")