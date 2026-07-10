# Trek Management System

## About

The Trek Management System is a Flask-based web application developed to manage trekking activities. It allows three different types of users (Admin, Staff and User) to perform different operations according to their roles.

The project uses Flask for the backend, SQLite as the database and HTML/CSS for the frontend.

---

## Features

### Admin

- Login to admin dashboard
- Create new treks
- Edit trek information
- Delete treks
- Assign staff to treks
- Approve staff registrations
- Approve or blacklist users
- Search treks by name or ID
- Search staff by name or ID
- Search users by name or ID
- View all bookings

### Staff

- Login after admin approval
- View assigned treks
- Update trek status
- Update available slots
- View participants of assigned treks

### User

- Register and login
- Edit profile
- View all available treks
- Search treks by location
- Filter treks by difficulty
- Book treks
- Cancel bookings
- View booking history and booking status

---

## Technologies Used

- Python
- Flask
- SQLAlchemy
- SQLite
- HTML
- CSS

---

## Database Tables

The project contains four tables.

### Users

Stores details of admin, staff and users.

### Treks

Stores all trek information.

### Bookings

Stores trek booking details of users.

### Staff Assignments

Stores which staff member is assigned to which trek.

---

## Project Structure

```
trekking_app/
│
├── app.py
├── extension.py
├── instance/
│   └── trek.db
│
├── models/
│   ├── User.py
│   ├── Trek.py
│   ├── Booking.py
│   └── StaffAssignment.py
│
├── controllers/
│   ├── admin.py
│   ├── staff.py
│   ├── user.py
│   └── trek.py
│
├── templates/
│
├── static/
│
└── README.md
```

---

## Installation

Clone the project.

```
git clone <repository_link>
```

Move into the project folder.

```
cd trekking_app
```

Install the required packages.

```
pip install flask flask_sqlalchemy
```

Run the project.

```
python app.py
```

Open the browser.

```
http://127.0.0.1:5000
```

---

## User Roles

### Admin

- Manage treks
- Manage users
- Manage staff
- Assign staff
- View bookings

### Staff

- View assigned treks
- Update trek details
- View participants

### User

- Register
- Book treks
- Cancel bookings
- View booking history
- Search treks

---

## Database Relationships

- One user can create multiple treks.
- One trek can have many bookings.
- One user can make multiple bookings.
- One staff member can be assigned to multiple treks.

---

## Future Improvements

Some features that can be added later are:

- Online payment
- Email notifications
- Trek images
- Password encryption
- Mobile responsive interface
- User reviews and ratings
- OTP verification

---

## Developed By

College Mini Project

Trek Management System using Flask and SQLite.