import streamlit as st
import os
import json
import pandas as pd
from dotenv import load_dotenv
from streamlit_pdf_viewer import pdf_viewer
from PIL import Image, ImageDraw

load_dotenv(override=True)

from functions.get_data import get_data, get_test_data, get_value_from_field
from functions.create_highlight import highlight_pdf, highlight_img

# this is static file path, you can change this to a dynamic file path
file_name = "test.png"
file_path = os.path.join(os.getcwd(), "documents", file_name)

# Set the page configuration
st.set_page_config(page_title="AOAI DocIntel Validator", layout="wide")

# loading data from various azure doc intel resources and azure openai
def load_data(file_path):
    # init_data = get_test_data(file_path) # for testing
    init_data = get_data(file_path)
    return init_data

# store the data in the session state
if 'data' not in st.session_state:
    st.session_state['data'] = load_data(file_path)

data = st.session_state['data']

# Streamlit app
st.title("AOAI Document Intelligence Validator")

# Create two columns
col1, col2 = st.columns([1, 1])

# Display list of fields on the left side
with col1:
    st.header("Fields")
    field_names = [field['name'] for field in data]
    selected_field_name = st.radio("Select a field to highlight", field_names)
    selected_field = next(field for field in data if field['name'] == selected_field_name)
    
    # add divider
    st.markdown("---")
    # Display additional information
    st.subheader("Field Information")
    
    # Create two columns
    inner_col1, inner_col2 = st.columns([5, 1])
    with inner_col1:
         # Add text input to select either aoaiValue or valueString
        user_value = st.text_input(key="userValue", label="User Value", placeholder="Enter value for userValue", value=selected_field.get('userValue', ''))
    with inner_col2:
        # Add button to save user input
        if st.button("Save"):
            selected_field['userValue'] = user_value

    # Save the user input back to the data dictionary
    if user_value:
        selected_field['userValue'] = user_value

    # Prepare data for DataFrame
    low_confidence = selected_field['confidence'] < 0.8
    value_differs = selected_field["genaiDocIntelValue"] != str(selected_field['aoaiValue'])
    field_info = {
        "Label": ["Schema Given Name", "Confidence From Doc Intel", "Similarity Score", "Value from Doc Intel", "Value from AOAI", "Content", "User given Value"],
        "Value": [selected_field['name'], selected_field['confidence'], selected_field["similarityScore"], selected_field["genaiDocIntelValue"], selected_field['aoaiValue'], selected_field['content'], selected_field.get('userValue', '')]
    }

    df = pd.DataFrame(field_info)
    
    # Ensure all elements in the "Value" column are strings
    df['Value'] = df['Value'].astype(str)

    def highlight_style(row):
        if row['Label'] == 'Confidence From Doc Intel':
            if low_confidence:
                return ['color: red'] * len(row)
            else:
                return ['color: green'] * len(row)
        if row['Label'] == 'Similarity Score':
            if selected_field["similarityScore"] < 0.95:
                return ['background-color: red'] * len(row)
            else:
                return ['background-color: green'] * len(row)
        if row['Label'] == 'Value from Doc Intel' or row['Label'] == 'Value from AOAI':
            if value_differs:
                return ['background-color: yellow'] * len(row)
        return [''] * len(row)

    styled_df = df.style.apply(highlight_style, axis=1)

    # Display the DataFrame
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

# Highlight selected text in PDF
selectedBoundingRegions = selected_field['boundingRegions']
box_coords = selectedBoundingRegions[0]['polygon']
highlight_coords = selected_field['boundingRegions']
highlighted_file_path = None
if file_path.endswith(".pdf"):
    highlighted_file_path = highlight_pdf(file_path, highlight_coords)
elif file_path.endswith(".png"):
    highlighted_file_path = highlight_img(file_path, highlight_coords)

# Display PDF on the right side
with col2:
    if file_path.endswith(".pdf"):
        st.header("PDF Viewer")
        pdf_viewer(input=highlighted_file_path, width=700)
    elif file_path.endswith(".jpg") or file_path.endswith(".jpeg") or file_path.endswith(".png"):
        st.header("Image Viewer")
        st.image(highlighted_file_path, width=700)    
    else:
        st.error("Invalid file format. Please upload a PDF or image file.")

st.markdown("---")

# Add button to export data as JSON
if st.button("Export Data as JSON"):
    json_data = json.dumps(data, indent=4)
    st.download_button(label="Download JSON", data=json_data, file_name="data.json", mime="application/json")