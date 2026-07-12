from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    Response
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)

from reportlab.lib import colors
from datetime import datetime

import random
import database

app = Flask(__name__)

# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = database.check_user(username, password)

        if user:

            voltage = random.randint(220, 240)
            current = round(random.uniform(1.5, 3.0), 2)

            power = round(voltage * current, 2)
            energy = round(power / 1000, 2)
            cost = round(energy * 8, 2)

            database.save_sensor_data(
                voltage,
                current,
                power,
                energy,
                cost
            )

            devices = database.get_devices()

            return render_template(
                "dashboard.html",
                username=username,
                voltage=voltage,
                current=current,
                power=power,
                energy=energy,
                cost=cost,
                devices=devices
            )

        return "Invalid Username or Password"

    return render_template("login.html")


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        database.add_user(
            username,
            email,
            password
        )

        return "Registration Successful!"

    return render_template("register.html")
# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    devices = database.get_devices()

    return render_template(
        "dashboard.html",
        username="Vinay",
        voltage=230,
        current=1.8,
        power=414,
        energy=4.3,
        cost=34.5,
        devices=devices
    )


# =========================
# HISTORY
# =========================

@app.route("/history")
def history():

    records = database.get_sensor_data()

    return render_template(
        "history.html",
        records=records
    )


# =========================
# ANALYTICS
# =========================

@app.route("/analytics")
def analytics():

    stats = database.get_statistics()

    return render_template(
        "analytics.html",
        voltage=round(stats[0], 2) if stats[0] else 0,
        current=round(stats[1], 2) if stats[1] else 0,
        power=round(stats[2], 2) if stats[2] else 0,
        energy=round(stats[3], 2) if stats[3] else 0,
        cost=round(stats[4], 2) if stats[4] else 0
    )


# =========================
# LIVE SENSOR API
# =========================

@app.route("/api/sensor")
def sensor_api():

    voltage = random.randint(220, 240)
    current = round(random.uniform(1.5, 3.0), 2)

    power = round(voltage * current, 2)
    energy = round(power / 1000, 2)
    cost = round(energy * 8, 2)

    return jsonify({
        "voltage": voltage,
        "current": current,
        "power": power,
        "energy": energy,
        "cost": cost,
        "time": datetime.now().strftime("%H:%M:%S")
    })
# =========================
# DEVICE CONTROL
# =========================

@app.route("/devices")
def devices():

    devices = database.get_devices()

    return render_template(
        "devices.html",
        devices=devices
    )


# =========================
# TOGGLE DEVICE
# =========================

@app.route("/toggle/<int:device_id>")
def toggle(device_id):

    database.toggle_device(device_id)

    return redirect("/devices")


# =========================
# SETTINGS
# =========================

@app.route("/settings")
def settings():

    return render_template("settings.html")


# =========================
# PROFILE
# =========================

@app.route("/profile")
def profile():

    return render_template(
        "profile.html",
        username="Vinay",
        energy=4.3,
        cost=34.5
    )


# =========================
# NOTIFICATIONS
# =========================

@app.route("/notifications")
def notifications():

    return render_template(
        "notifications.html"
    )

@app.route("/reports")
def reports():

    return render_template("reports.html")
# =========================
# MONTHLY BILL
# =========================

@app.route("/bill")
def bill():

    units = 128.5
    rate = 8

    total = round(units * rate, 2)

    return render_template(
        "bill.html",
        units=units,
        rate=rate,
        bill=total
    )
# =========================
# EXPORT CSV
# =========================

@app.route("/export/csv")
def export_csv():

    records = database.get_sensor_data()

    def generate():

        yield "Voltage,Current,Power,Energy,Cost,Timestamp\n"

        for row in records:

            yield f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=sensor_history.csv"
        }
    )


# =========================
# EXPORT PDF
# =========================

@app.route("/export/pdf")
def export_pdf():

    records = database.get_sensor_data()

    filename = "exports/energy_report.pdf"

    doc = SimpleDocTemplate(filename)

    data = [["Voltage", "Current", "Power", "Energy", "Cost", "Time"]]

    for row in records:
        data.append(list(row))

    table = Table(data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige)
    ]))

    doc.build([table])

    return "PDF Generated Successfully!"


# =========================
# RUN APPLICATION
# =========================






if __name__ == "__main__":

    app.run(debug=True)
