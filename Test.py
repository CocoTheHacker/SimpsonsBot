from flask import Flask, request, redirect
import requests
from twilio.twiml.messaging_response import MessagingResponse
import random
app = Flask(__name__)
import json
import couchdb
from re import *
user = "MrCoco"
password = "Nhialiscool123"
couchserver = couchdb.Server("http://%s:%s@localhost:5984/" % (user, password))
# Make quote
def get_quote():
    r = requests.get("https://frinkiac.com/api/random")
    if r.status_code == 200:
        json = r.json()
        # Extract the episode number and timestamp from the API response
        # and convert them both to strings.
        timestamp, episode, _ = map(str, json["Frame"].values())

        image_url = "https://frinkiac.com/meme/" + episode + "/" + timestamp
        # Combine each line of subtitles into one string.
        caption = "\n".join([subtitle["Content"] for subtitle in json["Subtitles"]])
        return image_url, caption

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    inbound_user = request.form.get("From")
    inbound_message = request.form.get("Body")
    inbound_message = inbound_message.lower().strip()
    image_url, caption = get_quote()
    """Respond to incoming calls with a MMS message."""
    f = open("Users.json",'w')
    dbname = 'user' + inbound_user
    if dbname in couchserver:
        db = couchserver[dbname]
    else:
        db = couchserver.create(dbname)
        db = couchserver[dbname]
    if inbound_message == 'send':
        rareity = random.randint(1,50)
        resp = MessagingResponse()
        msg = resp.message(caption)
        msg.media(image_url)
        
        # Common Simpson
        if rareity == 1 | 2 | 3:
            resp = MessagingResponse()
            msg = resp.message(caption + "\n\nThis is a Common Simpson")
            msg.media(image_url)
            1
            # Uncommon Simpson
        elif rareity == 4 | 5 | 6 | 7:
            resp = MessagingResponse()
            msg = resp.message(caption + "\n\nThis is a Uncommon Simpson")
            msg.media(image_url)
            
            # Epic Simpson
        elif rareity == 9:
            msg.media(image_url)
            resp = MessagingResponse()
            msg = resp.message(caption + "\n\nThis is an Epic Simpson")
            
            # Legendary Simpson
        elif  rareity == 48 | 49 | 50:
            resp = MessagingResponse()
            msg = resp.message(caption + "\n\nThe is a Legendary Simpson")
            msg.media(image_url)
            
            # Random Simpson
        else:
            randomz = ["\n\nThis is a Uncommon Simpson","\n\nThis is a Uncommon Simpson","\n\nThis is an Epic Simpson",]
            choice = random.choice(randomz)
            resp = MessagingResponse()
            msg = resp.message(caption + choice)
            msg.media(image_url)

        return str(resp)
    else:
        resp = MessagingResponse()
        msg = resp.message("Start by messaging \"Send\"")
        return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
