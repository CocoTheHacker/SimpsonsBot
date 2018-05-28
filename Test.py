from flask import Flask, request, redirect
import requests
from twilio.twiml.messaging_response import MessagingResponse
import random

app = Flask(__name__)
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
    inbound_message = request.form.get("Body")
    inbound_message = inbound_message.lower().strip()
    image_url, caption = get_quote()
    """Respond to incoming calls with a MMS message."""
    repeats = 10
    if inbound_message == 'send':
        rareity = random.randint(1,10)
        resp = MessagingResponse()
        msg = resp.message(caption)
        msg.media(image_url)
        if rareity == 1 | 2 | 3:
            resp = MessagingResponse()
            msg = resp.message(caption + "\n\nThis is a Common Simpson")
            msg.media(image_url)
        elif rareity == 4 | 5 | 6 | 7:
            resp = MessagingResponse()
            msg = resp.message(caption + "\n\nThis is a Uncommon Simpson")
            msg.media(image_url)
        elif rareity == 8 | 9:
            resp = MessagingResponse()
            msg = resp.message(caption + "\n\nThis is an Epic Simpson")
        else:
            resp = MessagingResponse()
            msg = resp.message(caption + "\n\nThe is a Legendary Simpson")
            msg.media(image_url)
        return str(resp)




if __name__ == "__main__":
    app.run(debug=True)
