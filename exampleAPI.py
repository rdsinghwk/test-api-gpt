from flask import Flask, request, jsonify
import random 
import json

app = Flask(__name__)

def load_data_map(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

data_map_pcs = load_data_map('pcs-codes.json')
data_map_modifiers = load_data_map('modifiers.json')
data_map_cms = load_data_map('icm-codes.json')
 
@app.route('/ground_mod', methods=['GET'])
def ground_mod():
    gptcode = request.args.get('doccode').strip('"')
    gptvalue = request.args.get('docvalue')

    matchValue = data_map_modifiers.get(gptcode)
    if not matchValue is None:
        if(matchValue == gptvalue.strip('"')):
            returnValue = [{"key": gptcode, "value": matchValue, "message": "good match"}]
            return jsonify(returnValue)
        else:
            returnValue = [{"key": gptcode, "value": matchValue+"--"+gptvalue, "message": "partial match"}]
            return jsonify(returnValue)
    else:
        return jsonify({"error": "No matching key-value pairs found"}), 404

@app.route('/ground_cms', methods=['GET'])
def ground_cms():
    gptcode = request.args.get('doccode').strip('"')
    gptvalue = request.args.get('docvalue')

    matchValue = data_map_cms.get(gptcode)
    if not matchValue is None:
        if(matchValue == gptvalue.strip('"')):
            returnValue = [{"key": gptcode, "value": matchValue, "message": "good match"}]
            return jsonify(returnValue)
        else:
            returnValue = [{"key": gptcode, "value": matchValue+"--"+gptvalue, "message": "partial match"}]
            return jsonify(returnValue)
    else:
        return jsonify({"error": "No matching key-value pairs found"}), 404

@app.route('/ground_pcs', methods=['GET'])
def ground_pcs():
    gptcode = request.args.get('doccode').strip('"')
    gptvalue = request.args.get('docvalue')

    matchValue = data_map_pcs.get(gptcode)
    if not matchValue is None:
        if(matchValue == gptvalue.strip('"')):
            returnValue = [{"key": gptcode, "value": matchValue, "message": "good match"}]
            return jsonify(returnValue)
        else:
            returnValue = [{"key": gptcode, "value": matchValue+"--"+gptvalue, "message": "partial match"}]
            return jsonify(returnValue)
    else:
        return jsonify({"error": "No matching key-value pairs found"}), 404
    

def checkValueExists(visit_number, keyName):
    return (keyName in patient_records[visit_number])

@app.route("/m3-ai", methods=["GET"])
def get_happiness():
  location = request.args.get("location")
  userName = request.args.get("user")
  happiness_percent = get_happiness_from_location(location)
  return jsonify({
      "user_id": userName,
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