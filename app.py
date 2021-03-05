from flask import Flask, render_template, request
import os
import aiml
from autocorrect import spell
import time
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BRAIN_FILE="./pretrained_model/aiml_pretrained_model.dump"
k = aiml.Kernel()

if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles="./pretrained_model/learningFileList.aiml", commands="load aiml")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/get", methods=['GET'])
def get_bot_response():
    query = request.args.get('msg')
    question = " ".join(query)
    response = k.respond(question)
    if response:
        time.sleep(1)
        return (str(response))
    else:
        return (str(":)"))


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
