from flask import Flask, render_template, request, redirect
import schedule
import time
import threading
from plyer import notification
from database import init_db, add_task, get_all_tasks

app = Flask(__name__)

# 🔔 Notification function
def notify(task):
    notification.notify(
        title="⏰ Task Reminder",
        message=task,
        timeout=10
    )

# ⏳ Background scheduler
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form["task"]
        time_input = request.form["time"]

        # Save to DB
        add_task(task, time_input)

        # Schedule notification
        schedule.every().day.at(time_input).do(notify, task)

        return redirect("/")

    timetable = get_all_tasks()
    return render_template("index.html", timetable=timetable)

if __name__ == "__main__":
    init_db()

    # Load saved tasks into scheduler on startup
    for task, time_input in get_all_tasks():
        schedule.every().day.at(time_input).do(notify, task)

    threading.Thread(target=run_scheduler, daemon=True).start()
    app.run(debug=True)