# AOAI-DocIntel-Validation

⚠️ There have been modification since the [article](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/maximizing-data-extraction-precision-with-dual-llms-integration/ba-p/4236728), please refer to the [article branch](https://github.com/JuhyunLee0/AOAI-DocIntel-Validation/tree/article) if you want to follow along with the article.

----

<img src="readme_files/main.gif" alt="main image" width="800"/>

## Introduction

This app leverages below services + human in the loop to maximize the content extraction from document.
- Azure OpenAI
- Azure AI Studio - Document Intelligence
- Azure Document Intelligence Studio

In this Sample Application, we will use Azure AI Studio - Document Extraction Preview to define the desired extraction schema, then perform analysis to extract the json object.

At the same time, we are also leveraging the document intelligence studio to run High OCR capability to convert the image to the markdown format, then using the GPT model, extract the desired data.

these two seperate data extraction results will then be compared for human evaluation as the last step, to insure that the extracted values are accurate to maximum degree.

## Requirements

- python 3.11 or above.
- Azure OpenAI GPT4 deployment.
- Azure Document Intelligence Service.
- Azure AI Studio Document Deployment with Generative Model.
    - for detail steps, please visit https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/document-field-extraction-with-generative-ai/ba-p/4222950

## Installation

1. Clone the repository.
2. [optional] create virtual python environment
    - ```python -m venv .venv```
    - ```.venv/scripts/activate```
3. change the `sample.env` to `.env` and populate the key values
4. Install the required dependencies using the following command:
    - ```pip install -r requirements.txt```

## Usage

To run the application, use the following command:

```shell
streamlit run app.py
```

> [!WARNING]
> When the applocation starts, it may take some time to grab the analyzed data from the Azure AI Document Intelligence services (typically ~5 seconds)

## License

This project is licensed under the [MIT License](LICENSE).
