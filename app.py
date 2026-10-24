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

@app.route("/edit/<int:employee_id>", methods=["GET", "POST"])
def edit(employee_id):
    employee = database.get_employee_by_id(employee_id)
    if employee is None:
        return "Employee Not Found", 404

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        department = request.form["department"].strip()
        salary = request.form["salary"].strip()
        joining_date = request.form["joining_date"]

        if not name:
            return render_template("edit.html", employee=employee, error="Name is required.")

        database.update_employee(employee_id, name, email, department, float(salary or 0), joining_date)
        return redirect(url_for("index"))

    return render_template("edit.html", employee=employee, error=None)

@app.route("/delete/<int:employee_id>", methods=["POST"])
def delete(employee_id):
    database.delete_employee(employee_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True) 