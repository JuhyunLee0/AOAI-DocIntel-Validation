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

    # print(target_file_path)

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

    return data


def get_test_data(file_path):
    """
    This function is responsible for getting the test data as a json
    """

    test_json = os.path.join(os.getcwd(), "documents", "test.json")
    with open(test_json, "r") as f:
        data = json.load(f)
        return data

    return []