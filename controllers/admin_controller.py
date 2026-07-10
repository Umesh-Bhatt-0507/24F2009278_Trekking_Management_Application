from flask import render_template,redirect , url_for,Blueprint,session,flash,request
from extension import db
from models.Trek import Trek
from models.User import User
from models.Booking import Booking
from models.StaffAssignment import StaffAssignment
admin=Blueprint("admin",__name__)
from datetime import datetime
from sqlalchemy import or_

@admin.route("/admin")
def showAdmin():
    if session.get("role") != "admin":
        flash("Login first")
        return redirect("/login")

    trek_search = request.args.get("trek_search", "")
    staff_search = request.args.get("staff_search", "")
    user_search = request.args.get("user_search", "")

    treks = Trek.query

    if trek_search:
        if trek_search.isdigit():
            treks = treks.filter(
                or_(
                    Trek.id == int(trek_search),
                    Trek.name.ilike(f"%{trek_search}%")
                )
            )
        else:
            treks = treks.filter(
                Trek.name.ilike(f"%{trek_search}%")
            )

    treks = treks.all()

    staff = User.query.filter_by(role="staff")

    if staff_search:
        if staff_search.isdigit():
            staff = staff.filter(
                or_(
                    User.id == int(staff_search),
                    User.name.ilike(f"%{staff_search}%")
                )
            )
        else:
            staff = staff.filter(
                User.name.ilike(f"%{staff_search}%")
            )

    staff = staff.all()

    users = User.query.filter_by(role="user")

    if user_search:
        if user_search.isdigit():
            users = users.filter(
                or_(
                    User.id == int(user_search),
                    User.name.ilike(f"%{user_search}%")
                )
            )
        else:
            users = users.filter(
                User.name.ilike(f"%{user_search}%")
            )

    users = users.all()

    bookings = Booking.query.all()

    return render_template(
        "admin.html",
        treks=treks,
        staff=staff,
        users=users,
        bookings=bookings
    )

@admin.route("/admin/newTrek", methods=["GET", "POST"])
def newTrek():
    if session.get("role") != "admin":
        flash("Login first")
        return redirect("/login")

    staff = User.query.filter_by(role="staff").all()

    if request.method == "POST":
        name = request.form["name"]
        location = request.form["location"]
        difficulty = request.form["difficulty"]
        duration = request.form["duration"]
        available_slots = request.form["available_slots"]
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d")
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d")
        status = request.form["status"]
        description = request.form["description"]
        staff_id = request.form["staff_id"]

        trek = Trek(
            user_id=session["user_id"],      # Admin who created the trek
            name=name,
            location=location,
            difficulty=difficulty,
            duration=duration,
            available_slots=available_slots,
            start_date=start_date,
            end_date=end_date,
            status=status,
            description=description
        )

        db.session.add(trek)
        db.session.commit()

        assignment = StaffAssignment(
            staff_id=staff_id,
            trek_id=trek.id
        )

        db.session.add(assignment)
        db.session.commit()

        flash("Trek created successfully.")
        return redirect(url_for("admin.showAdmin"))

    return render_template("add_new_trek.html", staff=staff)

@admin.route("/admin/trekDelete/<int:trekId>")
def deleteTrek(trekId):
    if session.get("role") != "admin":
        flash("Login first")
        return redirect("/login")
    StaffAssignment.query.filter_by(trek_id=trekId).delete()
    Booking.query.filter_by(trek_id=trekId).delete()
    trek=Trek.query.get_or_404(trekId)
    if trek:
        db.session.delete(trek)
        db.session.commit()
    flash("Trek Deleted Successfully")
    return redirect(url_for("admin.showAdmin"))

@admin.route("/admin/trekEdit/<int:trekId>", methods=["GET", "POST"])
def editTrek(trekId):
    if session.get("role") != "admin":
        flash("Login first")
        return redirect("/login")

    trek = Trek.query.get(trekId)
    staff = User.query.filter_by(role="staff").all()
    assignment = StaffAssignment.query.filter_by(trek_id=trek.id).first()

    if request.method == "POST":
        trek.name = request.form["name"]
        trek.location = request.form["location"]
        trek.difficulty = int(request.form["difficulty"])
        trek.duration = int(request.form["duration"])
        trek.available_slots = int(request.form["available_slots"])
        trek.start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d")
        trek.end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d")
        trek.status = request.form["status"]
        trek.description = request.form["description"]

        assignment = StaffAssignment.query.filter_by(trek_id=trek.id).first()

        if assignment:
            assignment.staff_id = int(request.form["staff_id"])
        else:
            assignment = StaffAssignment(
                staff_id=int(request.form["staff_id"]),
                trek_id=trek.id
            )
            db.session.add(assignment)

        db.session.commit()

        flash("Trek updated successfully.")
        return redirect(url_for("admin.showAdmin"))

    return render_template(
        "edit_trek.html",
        trek=trek,
        staff=staff,
        assignment=assignment
    )

@admin.route("/admin/blacklistUser/<int:user_id>")
def blacklist(user_id):
    if session.get("role") != "admin":
        flash("Login first")
        return redirect("/login")
    user=User.query.get_or_404(user_id)
    user.status="blacklisted"
    db.session.commit()
    return redirect(url_for("admin.showAdmin"))

@admin.route("/admin/blacklistUserRemove/<int:user_id>")
def remove_blacklist(user_id):
    if session.get("role") != "admin":
        flash("Login first")
        return redirect("/login")
    user=User.query.get_or_404(user_id)
    user.status="approved"
    db.session.commit()
    return redirect(url_for("admin.showAdmin"))