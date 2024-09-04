import os
import json
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from openai import AzureOpenAI

azure_openai_ep = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
azure_openai_model = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
azure_openai_api_version = "2023-05-15"

client = AzureOpenAI(
    api_key=azure_openai_key,
    api_version=azure_openai_api_version,
    azure_endpoint=azure_openai_ep
)

def get_response_from_aoai(document_content: str):
    """Get a response from the GPT-4o model"""

    system_message = """
    ### you are AI assistant that helps extract information from given context.
    - context will be given by the user.
    - you will extract the relevant information using this json schema:
        ```json
        {
            "amount_of_consideration": {
                "type": "number"
            },
            "borrower_name": {
                "type": "string"
            },
            "trustor": {
                "type": "string"
            },
            "apn_number": {
                "type": "number"
            },
            "title_order_number": {
                "type": "number"
            }
        }
        ```
    - if you are unable to extract the information, return JSON with the keys and empty strings or 0 as values.
    """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": document_content}
    ]

    # print(messages)

    try:
        response = client.chat.completions.create(
            model=azure_openai_model, # The deployment name you chose when you deployed the GPT-35-Turbo or GPT-4 model.
            messages=messages,
            response_format={ "type": "json_object" },
        )
        response_message = response.choices[0].message
        return response_message.content
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def get_response_from_aoai_with_schema(document_content: str, schema: str):
    """Get a JSON response from the GPT-4o model with schema"""

    system_message = f"""
    ### you are AI assistant that helps extract information from given context.
    - context will be given by the user.
    - you will extract the relevant information using this json schema:
        ```json
        {schema}
        ```
    - if you are unable to extract the information, return JSON with the keys and empty strings or 0 as values.
    - if schema type is date, provide the date as a string in the format "YYYY-MM-DD".
    """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": document_content}
    ]

    try:
        response = client.chat.completions.create(
            model=azure_openai_model, # The deployment name you chose when you deploy GPT model
            messages=messages,
            response_format={ "type": "json_object" },
        )
        response_message = response.choices[0].message
        return response_message.content
    except Exception as e:
        print(f"Error: {e}")
        return None