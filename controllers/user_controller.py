from flask import render_template,redirect , url_for,Blueprint,session,flash,request
from extension import db
from models.Trek import Trek
from models.User import User
from models.Booking import Booking
from models.StaffAssignment import StaffAssignment
user=Blueprint("user",__name__)
from datetime import datetime

@user.route("/user")
def dashboard():
    if session.get("role") != "user":
        return redirect("/login")

    location = request.args.get("location")
    difficulty = request.args.get("difficulty")

    query = Trek.query.filter_by(status="open")

    if location:
        query = query.filter(Trek.location.ilike(f"%{location}%"))

    if difficulty:
        query = query.filter_by(difficulty=int(difficulty))

    treks = query.all()

    bookings = Booking.query.filter_by(
        user_id=session["user_id"]
    ).all()

    booked_treks = [
        booking.trek_id
        for booking in bookings
        if booking.status == "booked"
    ]

    return render_template(
        "user_dashboard.html",
        treks=treks,
        bookings=bookings,
        booked_treks=booked_treks
    )
@user.route("/user/book/<int:trek_id>")
def book(trek_id):
    if session.get("role") != "user":
        return redirect("/login")
    trek = Trek.query.get(trek_id)
    if trek.available_slots < 1:
        flash("No slots available.")
        return redirect(url_for("user.dashboard"))
    booking = Booking.query.filter_by(
        user_id=session["user_id"],
        trek_id=trek_id
    ).first()
    if booking:
        booking.status = "booked"
    else:
        booking = Booking(
            user_id=session["user_id"],
            trek_id=trek_id,
            status="booked"
        )
        db.session.add(booking)
    trek.available_slots -= 1
    db.session.commit()
    flash("Booking Successful")
    return redirect(url_for("user.dashboard"))

@user.route("/user/cancelBook/<int:trek_id>")
def cancelBook(trek_id):
    if session.get("role") != "user":
        return redirect("/login")

    booking = Booking.query.filter_by(
        user_id=session["user_id"],
        trek_id=trek_id
    ).first()

    booking.status = "cancelled"

    trek = Trek.query.get(trek_id)
    trek.available_slots += 1

    db.session.commit()

    flash("Booking cancelled successfully.")
    return redirect(url_for("user.dashboard"))

@user.route("/user/edit", methods=["GET", "POST"])
def editProfile():
    if session.get("role") != "user":
        return redirect("/login")
    current_user = User.query.get(session["user_id"])
    if request.method == "POST":
        existing = User.query.filter(
            User.email == request.form["email"],
            User.id != current_user.id
        ).first()

        if existing:
            flash("Email already exists.")
            return redirect(url_for("user.editProfile"))
        current_user.name = request.form["name"]
        current_user.email = request.form["email"]
        current_user.password = request.form["password"]

        

        db.session.commit()
        flash("Profile updated successfully.")
        return redirect(url_for("user.dashboard"))

    return render_template("edit_profile.html", user=current_user)