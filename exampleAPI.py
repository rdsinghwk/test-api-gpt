from flask import Flask, request, jsonify
import random 
import json
#scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

#print(np.__version__)
#print(sklearn.__version__)
#print(json.__version__)
#print(random.__version__)

app = Flask(__name__)

def load_data_map(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

data_map_pcs = load_data_map('latest_pcs_codes_2024.json')
data_map_mod = load_data_map('modifiers.json')
#data_map_cms = load_data_map('icm-codes.json')
data_map_cms = load_data_map('latest_cms_codes_2024.json')

thresholdMatch = 0.5
thresholdScale = 0.6
topN = 10

#def ground(codes_to_check,referencePhrase,code_dict):
#    descriptions = list(codes_dict.values())
#
#    # Calculate TF-IDF vectors for the reference phrase and descriptions
#    vectorizer = TfidfVectorizer()
#    tfidf_matrix = vectorizer.fit_transform([reference_phrase] + descriptions)
#
#    # Calculate cosine similarity between reference phrase and each description
#    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
#
#    # Create a list of dictionaries with code, description, and similarity score
#    similarities = [
#        {"code": code, "description": description, "similarity_score": score}
#        for code, description, score in zip(codes_dict.keys(), descriptions, similarity_scores)
#    ]
#
#    # Sort by similarity score in descending order and get the top 10 matches
#    top_10_matches = sorted(similarities, key=lambda x: x["similarity_score"], reverse=True)[:topN]
#    top_10_codes = {item["code"] for item in top_10_matches}
#
#    # Check intersection with top 10 and entire dictionary
#    intersection_top_10 = [item for item in top_10_matches if item["code"] in codes_to_check]
#    intersection_top_10_codes = {item["code"] for item in intersection_top_10}
#
#    # Determine the threshold score for additional potential matches
#    if intersection_top_10:
#        lowest_intersection_score = min(item["similarity_score"] for item in intersection_top_10)
#        threshold_score = max(thresholdMatch, lowest_intersection_score * thresholdScale)
#    else:
#        threshold_score = thresholdMatch
#
#    # Add potential matches if not enough in the intersection with top 10
#    additional_potential_matches = [
#        item for item in top_10_matches
#        if item["code"] not in intersection_top_10_codes
#    ]
#
#    # Add matches with a score greater than the threshold if more are needed
#    additional_potential_matches += [
#        item for item in similarities
#        if item["code"] not in intersection_top_10_codes
#        and item["similarity_score"] >= threshold_score
#    ]
#
#    # Limit to ensure we are considering only distinct matches
#    potential_matches = list({item["code"]: item for item in additional_potential_matches}.values())
#
#    # Codes present in the entire dictionary but not in the top 10 matches
#    intersection_dict_not_in_top_10 = [
#        item for item in similarities if item["code"] in codes_to_check and item["code"] not in intersection_top_10_codes
#    ]
#
#    # Find the missing codes
#    missing_codes = list(codes_to_check.difference(codes_dict.keys()))
#
#    # Prepare the result as JSON
#    result = {
#        "Best matches": intersection_top_10,
#        "Potential matches": potential_matches[:10 - len(intersection_top_10)],  # Limit the number of additional matches
#        "Missing codes": missing_codes,
#        "Low accuracy matches": intersection_dict_not_in_top_10,
#    }
#
#    # Return result as JSON
#    result_json = json.dumps(result, indent=4)
#    return result_json
    
@app.route('/ground_mod', methods=['GET'])
def ground_mod():
    gptcodes = request.args.get('chatgcodes').strip('"').split(",") # interesting
    refphrase = request.args.get('docphrase')
#    topNRes = request.args.get('topN')
#    if not topNRes:
#        topNRes=topNResults
#        print(f"Top N:{topN}")

    return ground(set(gptcodes),refphrase, data_map_mod)    
#    gptcodes = request.args.get('doccode').strip('"').split(",") # interesting
#    matches = []
#    valueFound = False
#    codesNotFound=[]
#    for gptcode in gptcodes:
#        matchValue = data_map_modifiers.get(gptcode)
#        if not matchValue is None:
#            valueFound = True
#            matches.append({"key": gptcode, "value": matchValue})
#        else:
#            codesNotFound.append({"key":gptcode})
#          
#    print(codesNotFound)    
#    if(valueFound):
#        if(codesNotFound == []):
#            data = {"message": "Here are the matching codes","matches": matches}
#        else:    
#            data = {"message": "Here are the matching codes","matches": matches, "codesNotFound": codesNotFound}
#    else:
#        data = {"message": "Found no matching codes","codesNotFound": codesNotFound}
#    return data

@app.route('/ground_cms', methods=['GET'])
def ground_cms():
    gptcodes = request.args.get('chatgcodes').strip('"').split(",") # interesting
    refphrase = request.args.get('docphrase')
#    topNRes = request.args.get('topN')
#    if not topNRes:
#        topNRes=topNResults
#    print(f"Top N:{topNRes}")
    
    return ground(set(gptcodes),refphrase, data_map_cms)
    

#@app.route('/ground_cms', methods=['GET'])
#def ground_cms():
#    gptcodes = request.args.get('doccode').strip('"').split(",") # interesting
#    matches = []
#    valueFound = False
#    codesNotFound=[]
#    for gptcode in gptcodes:
#        matchValue = data_map_cms.get(gptcode)
#        if not matchValue is None:
#            valueFound = True
#            matches.append({"key": gptcode, "value": matchValue})
#        else:
#            codesNotFound.append({"key":gptcode})
#          
#    print(codesNotFound)    
#    if(valueFound):
#        if(codesNotFound == []):
#            data = {"message": "Here are the matching codes","matches": matches}
#        else:    
#            data = {"message": "Here are the matching codes","matches": matches, "codesNotFound": codesNotFound}
#    else:
#        data = {"message": "Found no matching codes","codesNotFound": codesNotFound}
#    return data

@app.route('/ground_pcs', methods=['GET'])
def ground_pcs():
    gptcodes = request.args.get('chatgcodes').strip('"').split(",") # interesting
    refphrase = request.args.get('docphrase')
    return ground(set(gptcodes),refphrase, data_map_pcs)

#    gptcodes = request.args.get('doccode').strip('"').split(",") # interesting
#    matches = []
#    valueFound = False
#    codesNotFound=[]
#    for gptcode in gptcodes:
#        matchValue = data_map_pcs.get(gptcode)
#        if not matchValue is None:
#            valueFound = True
#            matches.append({"key": gptcode, "value": matchValue})
#        else:
#            codesNotFound.append({"key":gptcode})
#          
#    print(codesNotFound)    
#    if(valueFound):
#        if(codesNotFound == []):
#            data = {"message": "Here are the matching codes","matches": matches}
#        else:    
#            data = {"message": "Here are the matching codes","matches": matches, "codesNotFound": codesNotFound}
#    else:
#        data = {"message": "Found no matching codes","codesNotFound": codesNotFound}
#    return data
    

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

def ground(codes_to_check,reference_phrase,codes_dict):
    print(type(codes_to_check))
    descriptions = list(codes_dict.values())

    # Calculate TF-IDF vectors for the reference phrase and descriptions
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([reference_phrase] + descriptions)

    # Calculate cosine similarity between reference phrase and each description
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Create a list of dictionaries with code, description, and similarity score
    similarities = [
        {"code": code, "description": description, "similarity_score": score}
        for code, description, score in zip(codes_dict.keys(), descriptions, similarity_scores)
    ]

    # Sort by similarity score in descending order and get the top 10 matches
    top_n_matches = sorted(similarities, key=lambda x: x["similarity_score"], reverse=True)[:topN]
    top_n_codes = {item["code"] for item in top_n_matches}

    # Check intersection with top 10 and entire dictionary
    intersection_top_n = [item for item in top_n_matches if item["code"] in codes_to_check]
    intersection_top_n_codes = {item["code"] for item in intersection_top_n}

    # Determine the threshold score for additional potential matches
    if intersection_top_n:
        lowest_intersection_score = min(item["similarity_score"] for item in intersection_top_n)
        threshold_score = max(thresholdMatch, lowest_intersection_score * thresholdScale)
    else:
        threshold_score = thresholdMatch

    # Add potential matches if not enough in the intersection with top 10
    additional_potential_matches = [
        item for item in top_n_matches
        if item["code"] not in intersection_top_n_codes
    ]

    # Add matches with a score greater than the threshold if more are needed
    additional_potential_matches += [
        item for item in similarities
        if item["code"] not in intersection_top_n_codes
        and item["similarity_score"] >= threshold_score
    ]

    # Limit to ensure we are considering only distinct matches
    potential_matches = list({item["code"]: item for item in additional_potential_matches}.values())

    # Codes present in the entire dictionary but not in the top 10 matches
    intersection_dict_not_in_top_n = [
        item for item in similarities if item["code"] in codes_to_check and item["code"] not in intersection_top_n_codes
    ]

    # Find the missing codes
    missing_codes = list(codes_to_check.difference(codes_dict.keys()))

    # Prepare the result as JSON
    result = {
        "Best matches": intersection_top_n,
        "Potential matches": potential_matches[:topN - len(intersection_top_n)],  # Limit the number of additional matches
        "Missing codes": missing_codes,
        "Low accuracy matches": intersection_dict_not_in_top_n,
    }

    # Return result as JSON
    result_json = json.dumps(result, indent=4)
    return result_json

if __name__ == "__main__":
  app.run()


## persistence code tbd
## Initialize dictionary to store patient visits
#patient_records = {
#    # Sample existing patient
#    "1029": {
#        "access_code": "secure123",
#        "presenting_condition": "severe pain in right knee, limited mobility",
#        "minutes_spent": 31,
#        "icd10_cm_codes": ["M25.561", "M17.11", "S83.231A"],
#        "additional_services": "X-ray 3 views",
#        "icd10_pcs_additional_services": ["BP2YZZZ"],
#        "complications": "foreign body accidentally left in body",
#        "icd10_pcs_presenting_condition": ["0QSJ0ZZ"],
#        "cpt_modifiers": ["22"]
#    }
#}
#
##API GET/POST
#@app.route("/getDetails", methods=["GET"])
#def get_details():
#  visit_number = request.args.get("visit_number")
#  if(check_existing_patient(visit_number)):
#    return release_patient_details(visit_number)
#  else:
#    returnText = "No user found with id: " + str(visit_number)
#    return jsonify({"details": returnText})
#
#@app.route("/data", methods=["POST"])
#def handle_data():
#    # Get the JSON data from the request
#    data = request.get_json()
#    
#    # Check if data was provided
#    if not data:
#        return jsonify({'error': 'No data provided'}), 400
#
#    visit_number = data.get("visit_number")
#    fieldKey = data.get("detail_key")
#    fieldValue = data.get("detail_value")
##    presenting_condition = data.get("presenting_condition")
#    store_field(visit_number,fieldKey,fieldValue)
#    returnText = "Thanks. Data recorded successfully" # Add number later
#    return jsonify({
#      "message": returnText
#    })
#
###API GET/POST  - Skip access code - just show for demo separately
##@app.route("/getDeepDetails", methods=["GET"])        
##def get_deep_details():
##    visit_number = request.args.get("visit_number")    
##    field_keys = request.args.get("case_field")
##    if(checkValueExists(visit_number,field_key)):
##        return 
#        
## Step 1: Check if patient exists
#def check_existing_patient(visit_number):
#    if visit_number in patient_records:
#        return True
#    return False
#
## Step 2: Request access code if patient exists
#def verify_access_code(visit_number, provided_code):
#    if patient_records[visit_number]['access_code'] == provided_code:
#        return True
#    return False
#
## Step 3: Release patient details in JSON format
#def release_patient_details(visit_number):
#    patient_data = patient_records[visit_number].copy()
#    # Remove access code from the released details
#    del patient_data['access_code']
#    return json.dumps(patient_data, indent=4)
#
## Step 4: If new patient, proceed with workflow
#def add_new_patient(visit_number, access_code):
#    patient_records[visit_number] = {'access_code': access_code}
#
## Workflow Functions (Similar to the previous version)
#def store_patient_visit_number(visit_number):
#    if not check_existing_patient(visit_number):
#        access_code = input("Enter a new access code for this patient: ")
#        add_new_patient(visit_number, access_code)
#        print(f"New patient visit {visit_number} stored.")
#    else:
#        print(f"Patient visit {visit_number} already exists.")
#
##Need to check if there is already one - then don't fill    
## Assume happy path always for now        
#def store_presenting_condition(visit_number, condition):
#    patient_records[visit_number]['presenting_condition'] = condition
#
##    if(checkValueExists(visit_number,'presenting_condition'))
##        return valueAlreadyFilledJson
##    else
##        patient_records[visit_number]['presenting_condition'] = condition
##        return valueAddedSuccessfullyJson
#def store_field(visit_number, field_key, field_value):
#    patient_records[visit_number][field_key] = field_value
#    
#def additional_services_check(visit_number, response, services=None):
#    if response.lower() == "yes" and services:
#        patient_records[visit_number]['additional_services'] = services
#    elif response.lower() == "no":
#        patient_records[visit_number]['additional_services'] = None
#
#def store_minutes_spent(visit_number, minutes):
#    patient_records[visit_number]['minutes_spent'] = minutes
#
#def store_icd10_cm_codes(visit_number, codes):
#    patient_records[visit_number]['icd10_cm_codes'] = codes
#
#def store_icd10_pcs_additional_services(visit_number, codes):
#    patient_records[visit_number]['icd10_pcs_additional_services'] = codes
#
#def complications_check(visit_number, response, complication=None):
#    if response.lower() == "yes" and complication:
#        patient_records[visit_number]['complications'] = complication
#    elif response.lower() == "no":
#        patient_records[visit_number]['complications'] = None
#
#def store_icd10_pcs_presenting_condition(visit_number, codes):
#    patient_records[visit_number]['icd10_pcs_presenting_condition'] = codes
#
#def store_cpt_modifiers(visit_number, modifiers):
#    patient_records[visit_number]['cpt_modifiers'] = modifiers
#
#def checkValueExists(visit_number, keyName):
#    return not (keyName not in patient_records[visit_number])