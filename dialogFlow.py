#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)
    res = json.dumps(res, indent=4)
    print(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    # testing: name of action in Dialogflow
    if req.get("queryResult").get("action") != "testing":
        return {}
    result = req.get("queryResult")
    parameters = result.get("parameters")
    # OpenWebURLs: name of Entities in Dialogflow
    zone = parameters.get("OpenWebURLs")

    cost = {'Youtube':'www.youtube.com','Google':'www.google.com', 'Gmail':'www.gmail.com'}
    speech = "The url for " + zone + " is " + str(cost[zone])
    return {
        "displayText": speech,
        "source": "PythonSpeechRecognition"  #PythonSpeechRecognition: name of Agent in Dialogflow
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))
    print ("Starting app on port %d" %(port))
    app.run(debug=True, port=port, host='0.0.0.0')