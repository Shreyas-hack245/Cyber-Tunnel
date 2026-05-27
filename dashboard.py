from flask import Flask, render_template, request, redirect, session
import subprocess

app = Flask(__name__)

app.secret_key = "cybertunnel_secret_key"

USERNAME = "admin"
PASSWORD = "cybertunnel"

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:

            session["user"] = username

            return redirect("/")

        else:

            error = "Invalid Credentials"

    return render_template(
        "login.html",
        error=error
    )

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")

@app.route("/")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    try:

        with open("logs/blocked_ips.log", "r") as file:

            logs = file.read()

            blocked_count = len(logs.splitlines())

    except:

        logs = "No blocked IPs yet."

        blocked_count = 0

    return render_template(
        "dashboard.html",
        logs=logs,
        blocked_count=blocked_count
    )

@app.route("/logs-data")
def logs_data():

    try:

        with open("logs/blocked_ips.log", "r") as file:

            return file.read()

    except:

        return "No logs available."

@app.route("/blocked")
def blocked():

    if "user" not in session:
        return redirect("/login")

    result = subprocess.getoutput(
        "iptables -L INPUT -n"
    )

    lines = result.splitlines()

    blocked_ips = []

    for line in lines:

        if "DROP" in line:

            parts = line.split()

            if len(parts) > 4:
                blocked_ips.append(parts[4])

    return render_template(
        "blocked.html",
        blocked_ips=blocked_ips
    )

@app.route("/geo")
def geo():

    if "user" not in session:
        return redirect("/login")

    geo_data = subprocess.getoutput(
        "geoiplookup 8.8.8.8"
    )

    return render_template(
        "geo.html",
        geo_data=geo_data
    )

@app.route("/threat")
def threat():

    if "user" not in session:
        return redirect("/login")

    threat_data = [
        {
            "ip": "185.220.101.1",
            "score": "95",
            "status": "Malicious"
        },
        {
            "ip": "8.8.8.8",
            "score": "0",
            "status": "Safe"
        }
    ]

    return render_template(
        "threat.html",
        threat_data=threat_data
    )

@app.route("/logs")
def logs():

    if "user" not in session:
        return redirect("/login")

    try:

        with open("logs/blocked_ips.log", "r") as file:

            log_data = file.read()

    except:

        log_data = "No logs available."

    return render_template(
        "logs.html",
        log_data=log_data
    )

app.run(host="0.0.0.0", port=5000)
