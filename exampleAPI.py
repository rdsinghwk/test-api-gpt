from flask import Flask, request, jsonify
import random 

app = Flask(__name__)


@app.route("/m3-ai", methods=["GET"])
def get_happiness():
  location = request.args.get("location")
  happiness_percent = get_happiness_from_location(location)
  return jsonify({
      "happiness_percent": happiness_percent
  })

def get_happiness_from_location(location):
  if location==None or location=="":
    happiness_percent = 0
  else:
    happiness_percent = random.randint(0, 100)
  return happiness_percent

@app.route("/maia", methods=["GET"])
def get_thanks():
  happiness_score = request.args.get("happiness_score")
  returnText = "Thanks. Received " + str(happiness_score)
  return jsonify({
      "happiness_received": returnText
  })

@app.route("/maia-rs", methods=["POST"])
def symptoms():
    data = request.get_json()
    userId = data['userID']
    symptoms = data['symptoms']
    returnText = "Thanks. Symptoms recorded successfully" # Add number later
    return jsonify({
      "message": returnText
    })

@app.route("/maia-rm", methods=["POST"])
def midas():
    data = request.get_json()
    userId = data['userID']
    symptoms = data['midas']
    returnText = "Thanks. MIDAS assessment recorded successfully" # Add number later
    return jsonify({
      "message": returnText
    })

@app.route("/maia-rh", methods=["POST"])
def hit6():
    data = request.get_json()
    userId = data['userID']
    symptoms = data['hit6']
    returnText = "Thanks. Hit-6 assessment recorded successfully" # Add number later
    return jsonify({
      "message": returnText
    })

if __name__ == "__main__":
  app.run()