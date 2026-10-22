from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

database.create_table()

@app.route("/")
def index():
    employees = database.get_all_employees()
    return render_template("index.html", employees=employees)

if __name__ == "__main__":
    app.run(debug=True)