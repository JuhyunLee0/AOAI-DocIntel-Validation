import os
import json
import Levenshtein
from services.AzureOpenAI import get_response_from_aoai_with_schema
from services.AzureGenAIDocIntel import get_schema_from_model, get_response_from_genai_docintel
from services.AzureAIDocIntel import get_response_from_docintel

# Function to grab the correct value from the selected field
def get_value_from_field(selected_field):
    if selected_field['type'] == 'string':
        return selected_field['valueString']
    elif selected_field['type'] == 'number':
        return str(selected_field['valueNumber'])
    elif selected_field['type'] == 'date':
        return selected_field['valueDate']
    else:
        return selected_field['content']

def calculate_similarity_score(val1, val2):
    """
    Calculate the similarity score between two strings using Levenshtein distance.

    :param val1: First string.
    :param val2: Second string.
    :return: Similarity score between 0.0 and 1.0.
    """
    # Compute the Levenshtein distance
    distance = Levenshtein.distance(val1, val2)
    
    # Normalize the distance to get a score between 0.0 and 1.0
    max_len = max(len(val1), len(val2))
    if max_len == 0:
        return 1.0  # Both strings are empty
    similarity_score = 1 - (distance / max_len)
    
    return similarity_score


def get_data(target_file_path):
    """
    This function is responsible for getting the data from doc intel and azure openai
    """
    # checking for custom schema first
    schema = get_schema_from_model()
    if schema is None:
        print("Unable to get schema from Azure Doc Intel")
        return None

    # getting response from doc intel
    analyze_result = get_response_from_genai_docintel(target_file_path)

    if analyze_result is None:
        print("Unable to analyze Document")
        return None

    doc = analyze_result["documents"][0]
    fields = doc["fields"]

    # getting conten from doc intel
    docintel_resp = get_response_from_docintel(target_file_path)
    content = docintel_resp["content"]

    # getting response from openai with schema
    aoai_resp = get_response_from_aoai_with_schema(content, json.dumps(schema))

    if aoai_resp is None:
        print("Unable to get response from OpenAI")
        return None

    aoai_resp_json = json.loads(aoai_resp)

    data = []
    for key, value in fields.items():
        # create new dictionary
        genaiDocIntelValue = get_value_from_field(value)
        element = {
            **value, # adding all existing values
            "name": key,
            "aoaiValue": aoai_resp_json[key],
            "genaiDocIntelValue": genaiDocIntelValue,
            "userValue": genaiDocIntelValue,
            "similarityScore":calculate_similarity_score(genaiDocIntelValue, aoai_resp_json[key])
        }
        data.append(element)
    print(data)
    return data


def get_test_data(file_path):
    """
    This function is responsible for getting the test data as a json
    """
    return [{'type': 'string', 'valueString': 'Dallas', 'content': 'Dallas', 'boundingRegions': [{'pageNumber': 1, 'polygon': [935, 346, 1083, 346, 1083, 392, 935, 392]}], 'confidence': 0.977, 'spans': [{'offset': 347, 'length': 6}], 'name': 'proposed_primary_insured_city_address', 'aoaiValue': 'Dallas', 'genaiDocIntelValue': 'Dallas', 'userValue': 'Dallas', 'similarityScore': 1.0}, {'type': 'string', 'valueString': 'Mack B. Cuban', 'content': 'Mack B. Cuban', 'boundingRegions': [{'pageNumber': 1, 'polygon': [426.68155, 305.15015, 823.9909, 301.89352, 824.33606, 343.99725, 427.02667, 347.25388]}], 'confidence': 0.97, 'spans': [{'offset': 269, 'length': 13}], 'name': 'proposed_primary_insured_name', 'aoaiValue': 'Mark B. Cuban', 'genaiDocIntelValue': 'Mack B. Cuban', 'userValue': 'Mack B. Cuban', 'similarityScore': 0.9230769230769231}, {'type': 'string', 'valueString': 'M', 'content': 'M', 'boundingRegions': [{'pageNumber': 1, 'polygon': [1034, 423, 1058, 423, 1058, 445, 1034, 445]}], 'confidence': 0.871, 'spans': [{'offset': 397, 'length': 1}], 'name': 'proposed_primary_insured_sex', 'aoaiValue': 'M', 'genaiDocIntelValue': 'M', 'userValue': 'M', 'similarityScore': 1.0}, {'type': 'string', 'valueString': '444-82-6666', 'content': '444-82-6666', 'boundingRegions': [{'pageNumber': 1, 'polygon': [1209.6837, 301.5024, 1538, 299, 1538.3201, 340.99756, 1210.0038, 343.49997]}], 'confidence': 0.961, 'spans': [{'offset': 301, 'length': 11}], 'name': 'proposed_primary_insured_ssn', 'aoaiValue': '444-82-6666', 'genaiDocIntelValue': '444-82-6666', 'userValue': '444-82-6666', 'similarityScore': 1.0}, {'type': 'string', 'valueString': 'TX', 'content': 'TX', 'boundingRegions': [{'pageNumber': 1, 'polygon': [385.8547, 408.5324, 440, 407, 441.15945, 447.9672, 387.01413, 449.4996]}], 'confidence': 0.971, 'spans': [{'offset': 362, 'length': 2}], 'name': 'proposed_primary_insured_state_address', 'aoaiValue': 'TX', 'genaiDocIntelValue': 'TX', 'userValue': 'TX', 'similarityScore': 1.0}, {'type': 'string', 'valueString': '991 Richmond St.', 'content': '991 Richmond St.', 'boundingRegions': [{'pageNumber': 1, 'polygon': [409.55106, 353.00458, 839.99603, 348.61227, 840.463, 394.37283, 410.018, 398.76514]}], 'confidence': 0.97, 'spans': [{'offset': 323, 'length': 16}], 'name': 'proposed_primary_insured_street_address', 'aoaiValue': '791 Richmond St.', 'genaiDocIntelValue': '991 Richmond St.', 'userValue': '991 Richmond St.', 'similarityScore': 0.9375}, {'type': 'string', 'valueString': '75201', 'content': '75201', 'boundingRegions': [{'pageNumber': 1, 'polygon': [500.6468, 415.50385, 639, 414, 639.35864, 446.9961, 501.00543, 448.49994]}], 'confidence': 0.977, 'spans': [{'offset': 376, 'length': 5}], 'name': 'proposed_primary_insured_zipcode_address', 'aoaiValue': '15201', 'genaiDocIntelValue': '75201', 'userValue': '75201', 'similarityScore': 0.8}]