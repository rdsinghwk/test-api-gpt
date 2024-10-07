from flask import Flask, request, jsonify
import random 
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__)

def load_data_map(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

data_map_pcs = load_data_map('pcs-codes.json')
data_map_modifiers = load_data_map('modifiers.json')
#data_map_cms = load_data_map('icm-codes.json')
data_map_cms = load_data_map('latest_cms_codes.json')

thresholdMatch = 0.6
thresholdScale = 0.8
topN = 5

# Just to test connection
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
    gptcodes = request.args.get('doccode').strip('"').split(",") # interesting
    matches = []
    valueFound = False
    codesNotFound=[]
    for gptcode in gptcodes:
        matchValue = data_map_modifiers.get(gptcode)
        if not matchValue is None:
            valueFound = True
            matches.append({"key": gptcode, "value": matchValue})
        else:
            codesNotFound.append({"key":gptcode})
          
    print(codesNotFound)    
    if(valueFound):
        if(codesNotFound == []):
            data = {"message": "Here are the matching codes","matches": matches}
        else:    
            data = {"message": "Here are the matching codes","matches": matches, "codesNotFound": codesNotFound}
    else:
        data = {"message": "Found no matching codes","codesNotFound": codesNotFound}
    return data

@app.route('/ground_cms', methods=['GET'])
def ground_cms():
    gptcodes = request.args.get('chatgcodes').strip('"').split(",") # interesting
    refphrase = request.args.get('docphrase')
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
    gptcodes = request.args.get('doccode').strip('"').split(",") # interesting
    matches = []
    valueFound = False
    codesNotFound=[]
    for gptcode in gptcodes:
        matchValue = data_map_pcs.get(gptcode)
        if not matchValue is None:
            valueFound = True
            matches.append({"key": gptcode, "value": matchValue})
        else:
            codesNotFound.append({"key":gptcode})
          
    print(codesNotFound)    
    if(valueFound):
        if(codesNotFound == []):
            data = {"message": "Here are the matching codes","matches": matches}
        else:    
            data = {"message": "Here are the matching codes","matches": matches, "codesNotFound": codesNotFound}
    else:
        data = {"message": "Found no matching codes","codesNotFound": codesNotFound}
    return data
    

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
    top_10_matches = sorted(similarities, key=lambda x: x["similarity_score"], reverse=True)[:topN]
    top_10_codes = {item["code"] for item in top_10_matches}

    # Check intersection with top 10 and entire dictionary
    intersection_top_10 = [item for item in top_10_matches if item["code"] in codes_to_check]
    intersection_top_10_codes = {item["code"] for item in intersection_top_10}

    # Determine the threshold score for additional potential matches
    if intersection_top_10:
        lowest_intersection_score = min(item["similarity_score"] for item in intersection_top_10)
        threshold_score = max(thresholdMatch, lowest_intersection_score * thresholdScale)
    else:
        threshold_score = thresholdMatch

    # Add potential matches if not enough in the intersection with top 10
    additional_potential_matches = [
        item for item in top_10_matches
        if item["code"] not in intersection_top_10_codes
    ]

    # Add matches with a score greater than the threshold if more are needed
    additional_potential_matches += [
        item for item in similarities
        if item["code"] not in intersection_top_10_codes
        and item["similarity_score"] >= threshold_score
    ]

    # Limit to ensure we are considering only distinct matches
    potential_matches = list({item["code"]: item for item in additional_potential_matches}.values())

    # Codes present in the entire dictionary but not in the top 10 matches
    intersection_dict_not_in_top_10 = [
        item for item in similarities if item["code"] in codes_to_check and item["code"] not in intersection_top_10_codes
    ]

    # Find the missing codes
    missing_codes = list(codes_to_check.difference(codes_dict.keys()))

    # Prepare the result as JSON
    result = {
        "Best matches": intersection_top_10,
        "Potential matches": potential_matches[:10 - len(intersection_top_10)],  # Limit the number of additional matches
        "Missing codes": missing_codes,
        "Low accuracy matches": intersection_dict_not_in_top_10,
    }

    # Return result as JSON
    result_json = json.dumps(result, indent=4)
    return result_json

if __name__ == "__main__":
  app.run()