import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, DocumentAnalysisFeature

docintel_endpoint = os.getenv("AZURE_AI_DOCINTEL_ENDPOINT")
docintel_key = os.getenv("AZURE_AI_DOCINTEL_KEY")
docintel_api_version = "2024-02-29-preview"

docintel_client = DocumentIntelligenceClient(
    endpoint=docintel_endpoint,
    credential=AzureKeyCredential(docintel_key),
    api_version=docintel_api_version
)

def get_response_from_docintel(target_file):
    
    with open(target_file, "rb") as f:
        poller = docintel_client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            content_type="application/octet-stream",
            features=[DocumentAnalysisFeature.OCR_HIGH_RESOLUTION]
        )
    result: AnalyzeResult = poller.result()

    return result
