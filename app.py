from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

database.create_table()

@app.route("/")
def index():
    employees = database.get_all_employees()
    return render_template("index.html", employees=employees)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        department = request.form["department"].strip()
        salary = request.form["salary"].strip()
        joining_date = request.form["joining_date"]

        if not name:
            return render_template("add.html", error="Name is required.")

        database.add_employee(name, email, department, float(salary or 0), joining_date)
        return redirect(url_for ("index"))

    return render_template("add.html", error=None)

if __name__ == "__main__":
    app.run(debug=True)