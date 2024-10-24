import os
import json
import re
import time
import requests
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import ContentFormat, AnalyzeResult

genai_docintel_endpoint = os.getenv("AZURE_GENAI_DOCINTEL_ENDPOINT")
genai_docintel_key = os.getenv("AZURE_GENAI_DOCINTEL_KEY")
genai_docintel_custom_model_name = os.getenv("AZURE_GENAI_DOCINTEL_CUSTOM_MODEL_NAME")

genai_docintel_client = DocumentIntelligenceClient(
    endpoint=genai_docintel_endpoint,
    credential=AzureKeyCredential(genai_docintel_key),
)

def get_schema_from_model():
    """
    Grab extraction schema using rest, this function may be converted to use the SDK once its available
    """

    url = f"{genai_docintel_endpoint}documentintelligence/documentModels/{genai_docintel_custom_model_name}"
    headers = {
        "Ocp-Apim-Subscription-Key": genai_docintel_key
    }
    params = {
        "api-version": "2024-07-31-preview"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        resp = response.json()
        print("Field Schema:")
        print(json.dumps(resp, indent=4))
        field_schema = resp["docTypes"][genai_docintel_custom_model_name]["fieldSchema"]
        return field_schema
    except Exception as e:
        print(f"Error: {e}")

    return None

def get_response_from_genai_docintel(target_file):
    with open(target_file, "rb") as f:
        poller = genai_docintel_client.begin_analyze_document(
            model_id=genai_docintel_custom_model_name,
            analyze_request=f,
            content_type="application/octet-stream",
            output_content_format=ContentFormat.MARKDOWN,
            # features=[DocumentAnalysisFeature.OCR_HIGH_RESOLUTION, "languages"]
        )
    result: AnalyzeResult = poller.result()

    return result

def get_response_genai_docintel_using_restapi(target_file):
    # get file from documents folder in the main directory
    with open(target_file, "rb") as f:
        url = f"{genai_docintel_endpoint}documentintelligence/documentModels/{genai_docintel_custom_model_name}:analyze"
        headers = {
            "Ocp-Apim-Subscription-Key": genai_docintel_key,
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
