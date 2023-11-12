from flask import Flask, request, jsonify
import random 
app = Flask(__name__)

@app.route("/happiness", methods=["GET"])

def get_happiness():
  location = request.args.get("location")
  happiness_percent = get_happiness_from_location(location)
  return jsonify({
      "happiness_percent": happiness_percent
  })


def get_happiness_from_location(location):
  happiness_percent = random.randint(0, 100)
  return happiness_percent

if __name__ == "__main__":
  app.run()