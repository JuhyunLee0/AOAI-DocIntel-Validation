import os
import json
from services.AzureOpenAI import get_response_from_aoai_with_schema
from services.AzureAIDocIntel import get_response_from_ai_doc_intel, get_schema_from_model

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
    analyze_result = get_response_from_ai_doc_intel(target_file_path)

    if analyze_result is None:
        print("Unable to analyze Document")
        return None

    content = analyze_result["content"]
    doc = analyze_result["documents"][0]
    fields = doc["fields"]

    # getting response from openai with schema
    aoai_resp = get_response_from_aoai_with_schema(content, json.dumps(schema))

    if aoai_resp is None:
        print("Unable to get response from OpenAI")
        return None

    aoai_resp_json = json.loads(aoai_resp)

    data = []
    for key, value in fields.items():
        # create new dictionary
        element = {
            **value, # adding all existing values
            "name": key,
            "aoaiValue": aoai_resp_json[key],
        }
        data.append(element)
    print(data)
    return data
        
       
def get_test_data(file_path):
    """
    This function is responsible for getting the test data as a json
    """
    return [
        {
            "type":"number",
            "valueNumber":30000,
            "content":"30,000",
            "boundingRegions":[
                {
                    "pageNumber":1,
                    "polygon":[
                    2.2524023,
                    6.9898515,
                    2.7835,
                    6.9887,
                    2.7839031,
                    7.174599,
                    2.2528052,
                    7.1757507
                    ]
                }
            ],
            "confidence":0.866,
            "spans":[
                {
                    "offset":1087,
                    "length":6
                }
            ],
            "name":"amount",
            "aoaiValue":30000
        },
        {
            "type":"number",
            "valueNumber":38593847301,
            "content":"38593847301",
            "boundingRegions":[
                {
                    "pageNumber":1,
                    "polygon":[
                    6.3883986,
                    2.3584993,
                    7.432,
                    2.3591,
                    7.4319015,
                    2.5305007,
                    6.3883,
                    2.5299
                    ]
                }
            ],
            "confidence":0.964,
            "spans":[
                {
                    "offset":98,
                    "length":11
                }
            ],
            "name":"apn_number",
            "aoaiValue":38593847301
        },
        {
            "type":"string",
            "valueString":"Siyabonga Sithole",
            "content":"Siyabonga Sithole",
            "boundingRegions":[
                {
                    "pageNumber":1,
                    "polygon":[
                    3.3858023,
                    5.219143,
                    4.787001,
                    5.2206,
                    4.7867994,
                    5.414757,
                    3.3856003,
                    5.4132996
                    ]
                }
            ],
            "confidence":0.977,
            "spans":[
                {
                    "offset":579,
                    "length":17
                }
            ],
            "name":"borrower_name",
            "aoaiValue":"Siyabonga Sithole"
        },
        {
            "type":"string",
            "valueString":"Addullo Kholov",
            "content":"Addullo Kholov",
            "boundingRegions":[
                {
                    "pageNumber":1,
                    "polygon":[
                    3.7689576,
                    5.6128993,
                    4.936356,
                    5.6139064,
                    4.936198,
                    5.796607,
                    3.7688,
                    5.7956
                    ]
                }
            ],
            "confidence":0.974,
            "spans":[
                {
                    "offset":670,
                    "length":14
                }
            ],
            "name":"lender_name",
            "aoaiValue":"Addullo Kholov"
        },
        {
            "type":"date",
            "valueDate":"2024-12-25",
            "content":"December, 25, 2024",
            "boundingRegions":[
                {
                    "pageNumber":1,
                    "polygon":[
                    5.697604,
                    6.6023955,
                    7.2604,
                    6.6016,
                    7.2604966,
                    6.7914,
                    5.697701,
                    6.792196
                    ]
                }
            ],
            "confidence":0.843,
            "spans":[
                {
                    "offset":990,
                    "length":18
                }
            ],
            "name":"note_date",
            "aoaiValue":"2024-12-25"
        },
        {
            "type":"string",
            "valueString":"Fabrikam, Inc",
            "content":"Fabrikam, Inc",
            "boundingRegions":[
                {
                    "pageNumber":1,
                    "polygon":[
                    2.4165053,
                    6.411617,
                    3.4764237,
                    6.418007,
                    3.4752977,
                    6.6047873,
                    2.4153793,
                    6.5983973
                    ]
                }
            ],
            "confidence":0.97,
            "spans":[
                {
                    "offset":906,
                    "length":13
                }
            ],
            "name":"trustee",
            "aoaiValue":"Fabrikam, Inc"
        }
        ]





