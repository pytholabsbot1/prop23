from flask import Flask, request, make_response
from gcalendar import *
from apscheduler.schedulers.background import BackgroundScheduler


################################### DEPENDENCIES


f_ = "/home/ubuntu/ascent/flask_server/client_secret_369937287240-6i29fcp4tgh9kk3rm4r6j9uqmbksnuue.apps.googleusercontent.com.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]
s = Create_Service(f_, "calendar", "v3", SCOPES)


# Whatsapp stuff
from wa import *


##### FLASK APP VIEWS ---------------------------------------- >


app = Flask(__name__)

sched = BackgroundScheduler(daemon=True)
sched.add_job(wa_sched_job, "interval", minutes=1)
sched.start()


@app.route("/schedule", methods=["POST"])
def schedule():
    if request.method == "POST":

        event = {
            "summary": request.form["stage"],
            "description": f'{request.form["name"]} : {request.form["mobile"]} \n airportenclave.com',
            "start": {
                "dateTime": request.form["dt"],
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": request.form["dt"],
                "timeZone": "Asia/Kolkata",
            },
        }

        res = (
            s.events()
            .insert(
                calendarId="il432o4h2mtbp25ehbui0aq4q4@group.calendar.google.com",
                body=event,
            )
            .execute()
        )

        print(res)
        return res


@app.route("/send_msg", methods=["POST"])
def send_msg():
    global driver, wa_status, wa_list

    if request.method == "POST":
        mob = request.form["mobile"]
        wa_list.append(mob)
        return "Added to List"


@app.route("/pic", methods=["GET"])
def pic():

    global driver
    data_ = driver.get_screenshot_as_png()
    response = make_response(data_)
    response.headers.set("Content-Type", "image/png")

    return response


@app.route("/close", methods=["GET"])
def close():
    global driver

    driver.quit()

    return "Exited"


if __name__ == "__main__":

    import logging

    logging.basicConfig(filename="error.log", level=logging.DEBUG)

    app.run(debug=True, use_reloader=False)
