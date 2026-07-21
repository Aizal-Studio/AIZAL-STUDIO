from flask import Flask, render_template, request, redirect, url_for, send_file
from db import get_connection
from datetime import datetime
app = Flask(__name__)

# ==========================
# Home Page
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# About Page
# ==========================
@app.route("/about")
def about():
    return render_template("about.html")


# ==========================
# Courses Page
# ==========================
@app.route("/courses")
def courses():
    return render_template("courses.html")


# ==========================
# Services Page
# ==========================
@app.route("/services")
def services():
    return render_template("services.html")


# ==========================
# Portfolio Page
# ==========================
@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


# ==========================
# Contact Page
# ==========================
@app.route("/contact")
def contact():
    return render_template("contact.html")

# ==========================
# Admissions
# ==========================

@app.route("/admissions", methods=["GET", "POST"])
def admissions():

    if request.method == "POST":

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO admissions
        (
            full_name,
            father_name,
            email,
            phone,
            city,
            qualification,
            course,
            status,
            apply_date
        )
        VALUES (?,?,?,?,?,?,?,?,?)
        """, (

            request.form["full_name"],
            request.form["father_name"],
            request.form["email"],
            request.form["phone"],
            request.form["city"],
            request.form["qualification"],
            request.form["course"],
            "Pending",
            datetime.now().strftime("%Y-%m-%d")

        ))

        connection.commit()
        connection.close()

        return render_template(
            "admissions.html",
            success="Your admission form has been submitted successfully!"
        )

    return render_template("admissions.html")
# ==========================
# Verify Certificate
# ==========================
@app.route("/verify", methods=["GET", "POST"])
def verify():

    if request.method == "POST":

        certificate_id = request.form["certificate_id"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE certificate_id = ?",
            (certificate_id,)
        )

        student = cursor.fetchone()

        connection.close()

        return render_template(
            "verify.html",
            student=student
        )

    return render_template("verify.html")


# ==========================
# Admin Login
# ==========================
@app.route("/admin/login")
def admin_login():
    return render_template("admin/login.html")


# ==========================
# Admin Dashboard
# ==========================
@app.route("/admin/dashboard")
def dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    # Total Students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Valid Certificates
    cursor.execute("SELECT COUNT(*) FROM students WHERE status='Valid'")
    valid_certificates = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "admin/dashboard.html",
        total_students=total_students,
        valid_certificates=valid_certificates
    )

# ==========================
# View Students
# ==========================
@app.route("/admin/students")
def view_students():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM students
        ORDER BY id DESC
    """)

    students = cursor.fetchall()

    connection.close()

    return render_template(
        "admin/students.html",
        students=students
    )

# ==========================
# View Admissions
# ==========================

@app.route("/admin/admissions")
def view_admissions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM admissions
        ORDER BY id DESC
    """)

    admissions = cursor.fetchall()

    connection.close()

    return render_template(
        "admin/admissions.html",
        admissions=admissions
    )

# ==========================
# Approve Admission
# ==========================

@app.route("/admin/admission/approve/<int:id>")
def approve_admission(id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Admission Record
        cursor.execute(
            "SELECT * FROM admissions WHERE id=?",
            (id,)
        )

        admission = cursor.fetchone()

        if admission is None:
            connection.close()
            return "Admission Not Found"

        # Agar pehle hi approve hai to dobara insert na karo
        if admission["status"] == "Approved":
            connection.close()
            return redirect("/admin/students")

        # Check student already exists
        cursor.execute("""
            SELECT id
            FROM students
            WHERE student_name=? AND father_name=? AND course=?
        """, (

            admission["full_name"],
            admission["father_name"],
            admission["course"]

        ))

        existing = cursor.fetchone()

        if existing is None:

            cursor.execute("""
                INSERT INTO students
                (
                    certificate_id,
                    student_name,
                    father_name,
                    phone,
                    email,
                    city,
                    course,
                    duration,
                    grade,
                    issue_date,
                    status
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (

                "",
                admission["full_name"],
                admission["father_name"],
                admission["phone"],
                admission["email"],
                admission["city"],
                admission["course"],
                "Pending",
                "Pending",
                None,
                "Pending"

            ))

        # Update Admission Status
        cursor.execute(
            "UPDATE admissions SET status=? WHERE id=?",
            ("Approved", id)
        )

        connection.commit()

    finally:
        connection.close()

    return redirect("/admin/students")


# ==========================
# Reject Admission
# ==========================

@app.route("/admin/admission/reject/<int:id>")
def reject_admission(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE admissions SET status=? WHERE id=?",
        ("Rejected", id)
    )

    connection.commit()
    connection.close()

    return redirect("/admin/admissions")

# ==========================
# Edit Student
# ==========================
@app.route("/admin/edit-student/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    connection = get_connection()
    cursor = connection.cursor()

    if request.method == "POST":

        cursor.execute("""
        UPDATE students
        SET
            certificate_id=?,
            student_name=?,
            father_name=?,
            phone=?,
            email=?,
            city=?,
            course=?,
            duration=?,
            grade=?,
            issue_date=?,
            status=?
        WHERE id=?
        """, (

            request.form["certificate_id"],
            request.form["student_name"],
            request.form["father_name"],
            request.form["phone"],
            request.form["email"],
            request.form["city"],
            request.form["course"],
            request.form["duration"],
            request.form["grade"],
            request.form["issue_date"],
            request.form["status"],
            id

        ))

        connection.commit()
        connection.close()

        return redirect("/admin/students")

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    connection.close()

    return render_template(
        "admin/edit_student.html",
        student=student
    )

# ==========================
# Delete Student
# ==========================
@app.route("/admin/delete-student/<int:id>")
def delete_student(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("view_students"))



# ==========================
# Add Student
# ==========================
@app.route("/admin/add-student", methods=["GET", "POST"])
def add_student():

    if request.method == "POST":

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO students
        (
            certificate_id,
            student_name,
            father_name,
            phone,
            email,
            city,
            course,
            duration,
            grade,
            issue_date,
            status
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (

            request.form["certificate_id"],
            request.form["student_name"],
            request.form["father_name"],
            request.form["phone"],
            request.form["email"],
            request.form["city"],
            request.form["course"],
            request.form["duration"],
            request.form["grade"],
            request.form["issue_date"],
            request.form["status"]

        ))

        connection.commit()
        connection.close()

        return render_template(
            "admin/add_student.html",
            success="Student Added Successfully!"
        )

    return render_template("admin/add_student.html")

# ==========================
# Run Application
# ==========================
if __name__ == "__main__":
    app.run(debug=True)