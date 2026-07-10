from flask import render_template,redirect , url_for,Blueprint,session,flash,request
from extension import db
from models.Trek import Trek
from models.User import User
from models.Booking import Booking
from models.StaffAssignment import StaffAssignment
staff=Blueprint("staff",__name__)
from datetime import datetime

@staff.route("/staff")
def show_staff():
    if session.get("role") != "staff":
        flash("Login first")
        return redirect("/login")

    worker = User.query.get_or_404(session["user_id"])

    if worker.status != "approved":
        return render_template("approval_wait.html")

    assignments = StaffAssignment.query.filter_by(staff_id=worker.id).all()

    return render_template(
        "staff.html",
        assignments=assignments,
        worker=worker
    )

@staff.route("/staff/update/<int:trek_id>", methods=["GET","POST"])
def update_trek(trek_id):
    if session.get("role") != "staff":
        return redirect("/login")
    trek = Trek.query.get(trek_id)

    if request.method=="POST":
        assignment = StaffAssignment.query.filter_by(
            trek_id=trek_id,
            staff_id=session["user_id"]
        ).first_or_404()

        assignment.trek.available_slots = int(request.form["available_slots"])
        assignment.trek.status = request.form["status"]

        db.session.commit()

        flash("Trek updated.")
        return redirect(url_for("staff.show_staff"))
    return render_template("staff_updater.html",trek=trek)

@staff.route("/staff/participants/<int:trek_id>")
def participants(trek_id):
    if session.get("role") != "staff":
        return redirect("/login")

    assignment = StaffAssignment.query.filter_by(
        trek_id=trek_id,
        staff_id=session["user_id"]
    ).first()

    bookings = Booking.query.filter_by(trek_id=trek_id).all()
    
    if bookings:
        return render_template(
            "participants.html",
            # trek=assignment.trek,
            bookings=bookings
        )
    flash("No participants")
    return redirect(url_for("staff.show_staff"))
