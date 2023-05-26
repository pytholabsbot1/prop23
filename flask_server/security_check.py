import os, random, time
from datetime import datetime as dt
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "AC75291b3a693d2f5f1b9f4c206d8f7490"
auth_token = "b28f11707706fccc9c09ab73c167391f"
client = Client(account_sid, auth_token)


def init_call():
    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to="+918094011162",
        from_="+12057367447",
    )

    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to="+917978046572",
        from_="+12057367447",
    )

    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to="+918018603942",
        from_="+12057367447",
    )

    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to="+917205069140",
        from_="+12057367447",
    )

    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to="+916372236616",
        from_="+12057367447",
    )

    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to="+918249830656",
        from_="+12057367447",
    )


    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to="+917684875493",
        from_="+12057367447",
    )

    call = client.calls.create(
        url="http://demo.twilio.com/docs/voice.xml",
        to="+918117830156",
        from_="+12057367447",
    )


while True:
    if dt.now().hour > 22:
        points = sorted(random.sample([i * 30 for i in range(1, 13)], k=5))
        deviations = [points[0]] + [(points[i] - points[i - 1]) for i in range(1, 5)]

        for t in deviations:
            print("\n\n Starting Calls !!")
            init_call()
            print(f"running after {t} mins")
            time.sleep(t * 60)

    else:
        print(f"Its not time yet {dt.now().time()}")
        time.sleep(20 * 60)
