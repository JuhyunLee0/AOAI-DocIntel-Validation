import streamlit as st
import fitz  # PyMuPDF
import os
import json
import pandas as pd
from dotenv import load_dotenv
from streamlit_pdf_viewer import pdf_viewer

load_dotenv(override=True)

from functions.get_data import get_data, get_data_with_highocr, get_test_data

# Set the page configuration
st.set_page_config(page_title="AOAI DocIntel Validator", layout="wide")

# this is static file path, you can change this to a dynamic file path
file_path = os.path.join(os.getcwd(), "documents", "sample-deed-of-trust.pdf")
pdf_path = os.path.join(os.getcwd(), "documents", "sample-deed-of-trust.pdf")

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

def load_data(file_path):
    # FOR TESTING ONLY
    # init_data = get_test_data(file_path) 
    # init_data = get_data_with_highocr(file_path)
    init_data = get_data(file_path)
    # for each element in the data, add a userValue key
    for element in init_data:
        element['userValue'] = get_value_from_field(element)
    return init_data

# store the data in the session state
if 'data' not in st.session_state:
    st.session_state['data'] = load_data(file_path)

data = st.session_state['data']


# Function to highlight text in PDF with a red box
def highlight_text_in_pdf(file_path, highlight_coords):
    pdf_file = os.path.join(os.getcwd(), "documents", "sample-deed-of-trust.pdf")
    doc = fitz.open(file_path)
    for coord in highlight_coords:
        page = doc.load_page(coord['pageNumber'] - 1)
        rect = fitz.Rect(coord['polygon'][0] * 72, coord['polygon'][1] * 72, coord['polygon'][4] * 72, coord['polygon'][5] * 72)
        annot = page.add_rect_annot(rect)
        annot.set_colors(stroke=(1, 0, 0))  # Red color
        annot.set_border(width=2)  # Border width
        annot.update()
    highlighted_file_path = "documents/temp.pdf"
    try:
        doc.save(highlighted_file_path)
    except Exception as e:
        print(f"Error saving PDF: {e}")
    return highlighted_file_path


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
    value_from_doc_intel = get_value_from_field(selected_field)
    low_confidence = selected_field['confidence'] < 0.8
    value_differs = value_from_doc_intel != str(selected_field['aoaiValue'])
    field_info = {
        "Label": ["Schema Given Name", "Confidence", "Value from Doc Intel", "Value from AOAI", "Content", "User given Value"],
        "Value": [selected_field['name'], selected_field['confidence'], value_from_doc_intel, selected_field['aoaiValue'], selected_field['content'], selected_field.get('userValue', '')]
    }

    df = pd.DataFrame(field_info)
    
    # Ensure all elements in the "Value" column are strings
    df['Value'] = df['Value'].astype(str)

    def highlight_style(row):
        if row['Label'] == 'Confidence':
            if low_confidence:
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
highlighted_file_path = highlight_text_in_pdf(file_path, highlight_coords)

# Display PDF on the right side
with col2:
    st.header("PDF Viewer")
    pdf_viewer(input=highlighted_file_path, width=700)

st.markdown("---")

# Add button to export data as JSON
if st.button("Export Data as JSON"):
    json_data = json.dumps(data, indent=4)
    st.download_button(label="Download JSON", data=json_data, file_name="data.json", mime="application/json")