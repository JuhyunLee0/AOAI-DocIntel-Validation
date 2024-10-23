# AOAI-DocIntel-Validation

⚠️ if you are coming from the [article](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/maximizing-data-extraction-precision-with-dual-llms-integration/ba-p/4236728), please refer to the [article branch](https://github.com/JuhyunLee0/AOAI-DocIntel-Validation/tree/article)

<img src="readme_files/main.gif" alt="main image" width="800"/>

This app leverages Azure OpenAI GPT4 model and Azure AI Studio Document Intelligence Model to do extraction and compare the output to get better accuracy on the extraction.

## Requirements

- python 3.11 or above
- Azure OpenAI GPT4 deployment
- Azure AI Studio Document Deployment with Generative Model
    - for more detail look, please visit https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/document-field-extraction-with-generative-ai/ba-p/4222950

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
