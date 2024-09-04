import os
import json
import re
import time
import requests

docintel_endpoint = os.getenv("AZURE_AI_DOC_INTEL_ENDPOINT")
docintel_key = os.getenv("AZURE_AI_DOC_INTEL_KEY")
docintel_custom_model_name = os.getenv("AZURE_AI_DOC_INTEL_MODE_NAME")

def get_schema_from_model():
    """
    This function is responsible for getting the schema from the custom trained model
    """

    url = f"{docintel_endpoint}documentintelligence/documentModels/{docintel_custom_model_name}"
    headers = {
        "Ocp-Apim-Subscription-Key": docintel_key
    }
    params = {
        "api-version": "2024-07-31-preview"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        resp = response.json()
        # print(resp)
        field_schema = resp["docTypes"][docintel_custom_model_name]["fieldSchema"]
        return field_schema
    except Exception as e:
        print(f"Error: {e}")

    return None


def get_response_from_ai_doc_intel(target_file):
    # get file from documents folder in the main directory
    with open(target_file, "rb") as f:
        url = f"{docintel_endpoint}documentintelligence/documentModels/{docintel_custom_model_name}:analyze"
        headers = {
            "Ocp-Apim-Subscription-Key": docintel_key,
            "Content-Type": "application/octet-stream"
        }
        params  = {
            "api-version": "2024-07-31-preview",
            "outputContentFormat": "markdown"
        }
        sumbit_analysis = requests.post(url, params=params , headers=headers, data=f)

        if sumbit_analysis.status_code != 202:
            print(f"Error: {sumbit_analysis.json()}")
            return None

        # get the operation location
        operation_location = sumbit_analysis.headers["Operation-Location"]
        print(operation_location)

        # do while loop til the analysis is done
        while True:
            response = requests.get(operation_location, headers={"Ocp-Apim-Subscription-Key": docintel_key})

            if response.status_code != 200:
                print(f"Error: {response.json()}")
                return None
            
            analysis_results = response.json()

            if analysis_results["status"] == "running":
                # wait for 5 seconds
                print("Analysis is still running...")
                time.sleep(5)
                continue
            
            if analysis_results["status"] != "succeeded":
                print(f"Error: {analysis_results}")
                return None
            
            return analysis_results["analyzeResult"]

