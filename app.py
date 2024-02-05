from flask import Flask , render_template , jsonify , request 
from chatbot import predict_class, get_response
import json
import re

intents = json.load(open("C:/Users/saich/OneDrive/Desktop/chat app - Backup/intents.json",encoding="utf-8"))

app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    ints = predict_class(text)
    print(ints)
    response = get_response(ints,intents)
    message = {"answer" : response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)





