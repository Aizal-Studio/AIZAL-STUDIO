from flask import Flask, render_template, request, redirect, url_for, send_file
from db import get_connection
from datetime import datetime
import os

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

@app.route("/course/<course_name>")
def course_detail(course_name):

    courses = {

        "python": {
            "icon": "🐍",
            "title": "Python Programming",
            "description": "Learn Python from beginner to advanced with practical projects.",
            "instructor": "Beenish",
            "duration": "2 Months",
            "timing": "Mon - Fri | 7:00 PM - 8:30 PM",
            "mode": "Online & Physical",
            "level": "Beginner",
            "outline": [
                "Python Basics",
                "Variables & Data Types",
                "Loops & Functions",
                "File Handling",
                "OOP",
                "Projects"
            ]
        },

        "data-science": {
            "icon": "📊",
            "title": "Data Science",
            "description": "Learn Data Analysis, Visualization and Machine Learning.",
            "instructor": "Beenish",
            "duration": "3 Months",
            "timing": "Mon - Fri | 6:00 PM - 7:30 PM",
            "mode": "Online & Physical",
            "level": "Intermediate",
            "outline": [
                "Excel",
                "Python",
                "Pandas",
                "NumPy",
                "Visualization",
                "Machine Learning"
            ]
        },

        "web-development": {
            "icon": "🌐",
            "title": "Web Development",
            "description": "Build modern responsive websites using HTML, CSS, JavaScript & Flask.",
            "instructor": "Beenish",
            "duration": "3 Months",
            "timing": "Weekend",
            "mode": "Online & Physical",
            "level": "Beginner",
            "outline": [
                "HTML",
                "CSS",
                "JavaScript",
                "Flask",
                "SQLite",
                "Deployment"
            ]
        },

        "canva": {
            "icon": "🎨",
            "title": "Canva & Graphic Design",
            "description": "Create professional social media designs.",
            "instructor": "Beenish",
            "duration": "1 Month",
            "timing": "Weekend",
            "mode": "Online",
            "level": "Beginner",
            "outline": [
                "Canva Basics",
                "Branding",
                "Social Media",
                "Posters",
                "Presentations"
            ]
        },

        "ms-office": {
            "icon": "💼",
            "title": "MS Office",
            "description": "Professional Microsoft Office training.",
            "instructor": "Beenish",
            "duration": "1 Month",
            "timing": "Weekend",
            "mode": "Online & Physical",
            "level": "Beginner",
            "outline": [
                "Word",
                "Excel",
                "PowerPoint",
                "Projects"
            ]
        },

        "ai-tools": {
            "icon": "🤖",
            "title": "AI Tools",
            "description": "Master modern AI productivity tools.",
            "instructor": "Mam Amna",
            "duration": "1 Month",
            "timing": "Weekend",
            "mode": "Online",
            "level": "Beginner",
            "outline": [
                "ChatGPT",
                "Gemini",
                "Copilot",
                "AI Automation",
                "Prompt Engineering"
            ]
        },

        "ielts": {
            "icon": "🇬🇧",
            "title": "IELTS Preparation",
            "description": "Prepare for Academic & General IELTS.",
            "instructor": "Mam Fatima",
            "duration": "2 Months",
            "timing": "Mon - Fri",
            "mode": "Online & Physical",
            "level": "All Levels",
            "outline": [
                "Listening",
                "Reading",
                "Writing",
                "Speaking",
                "Mock Tests"
            ]
        },

        "spoken-english": {
            "icon": "🗣",
            "title": "Spoken English",
            "description": "Improve confidence in spoken English.",
            "instructor": "Mam Fatima",
            "duration": "2 Months",
            "timing": "Mon - Fri",
            "mode": "Online & Physical",
            "level": "Beginner",
            "outline": [
                "Daily Conversation",
                "Grammar",
                "Vocabulary",
                "Pronunciation",
                "Interview Skills"
            ]
        }

    }

    course = courses.get(course_name)

    if not course:
        return "Course Not Found", 404

    return render_template(
        "course_details.html",
        course=course
    )

# ==========================
# Course Details
# ==========================

COURSES = {

    "python": {
        "title": "Python Programming",
        "icon": "🐍",
        "instructor": "Beenish",
        "duration": "2 Months",
        "timing": "Monday - Friday | 5:00 PM - 7:00 PM",
        "mode": "Physical + Online",
        "level": "Beginner",
        "description": "Learn Python from beginner to advanced with practical projects.",
        "outline": [
            "Python Basics",
            "Variables & Data Types",
            "Functions",
            "Loops",
            "Object Oriented Programming",
            "SQLite Database",
            "Flask",
            "Final Project"
        ]
    },

    "data-science": {
        "title": "Data Science",
        "icon": "📊",
        "instructor": "Beenish",
        "duration": "3 Months",
        "timing": "Monday - Friday | 4:00 PM - 6:00 PM",
        "mode": "Physical + Online",
        "level": "Intermediate",
        "description": "Learn Data Analysis, Visualization and Machine Learning.",
        "outline": [
            "Python for Data Science",
            "Pandas",
            "NumPy",
            "Matplotlib",
            "Machine Learning",
            "Projects"
        ]
    },

    "web-development": {
        "title": "Web Development",
        "icon": "🌐",
        "instructor": "Beenish",
        "duration": "3 Months",
        "timing": "Monday - Friday | 6:00 PM - 8:00 PM",
        "mode": "Physical + Online",
        "level": "Beginner",
        "description": "HTML, CSS, JavaScript, Flask.",
        "outline": [
            "HTML",
            "CSS",
            "JavaScript",
            "Bootstrap",
            "Flask",
            "SQLite",
            "Deployment"
        ]
    },

    "ai-tools": {
        "title": "AI Tools",
        "icon": "🤖",
        "instructor": "Mam Amna",
        "duration": "1 Month",
        "timing": "Weekend Batch",
        "mode": "Physical + Online",
        "level": "Beginner",
        "description": "Master ChatGPT and AI productivity tools.",
        "outline": [
            "ChatGPT",
            "Gemini",
            "Copilot",
            "Prompt Engineering",
            "AI for Office Work"
        ]
    },

    "ielts": {
        "title": "IELTS Preparation",
        "icon": "🇬🇧",
        "instructor": "Mam Fatima",
        "duration": "2 Months",
        "timing": "Morning & Evening",
        "mode": "Physical",
        "level": "All Levels",
        "description": "Complete IELTS Preparation.",
        "outline": [
            "Speaking",
            "Writing",
            "Reading",
            "Listening",
            "Mock Tests"
        ]
    },

    "spoken-english": {
        "title": "Spoken English",
        "icon": "🗣",
        "instructor": "Mam Fatima",
        "duration": "2 Months",
        "timing": "Morning & Evening",
        "mode": "Physical",
        "level": "Beginner",
        "description": "Speak English confidently.",
        "outline": [
            "Daily Conversation",
            "Grammar",
            "Vocabulary",
            "Pronunciation"
        ]
    }

}

@app.route("/course/<course_name>")
def course_details(course_name):

    course = COURSES.get(course_name)

    if course is None:
        return "Course Not Found"

    return render_template(
        "course_details.html",
        course=course
    )

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)