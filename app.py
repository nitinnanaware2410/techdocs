import openai
import streamlit as st
from keys.openAIkey import openai_key
import os

import sys


# Set the path for 'keys' folder
if getattr(sys, 'frozen', False):  # This checks if running as an executable
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the keys folder and import the key
key_file_path = os.path.join(app_path, 'keys', 'openAIkey.py')
sys.path.append(os.path.join(app_path, 'keys'))  # Add keys folder to sys path
# Set your OpenAI API key
openai.api_key = openai_key

# Function to generate document section using OpenAI's API

def generate_document(section_type, input_data):
    """
    Generates a section (HLD or LLD) based on input data using ChatCompletion API.
    
    Args:
    - section_type (str): Either 'HLD' or 'LLD' specifying the type of document.
    - input_data (str): Description of the migration requirements.
    
    Returns:
    - str: Generated document section.
    """
    if section_type == "HLD":
        prompt = f"""
        Create a high-level design (HLD) document for the following project: {input_data}.
        Include:
        - Overview of the current and target architectures
        - Migration strategy (phased approach, cutover, etc.)
        - Non-functional requirements (e.g., performance, security)
        - Risk analysis and mitigation strategies.
        - create a diagram to illustrate
        """
    elif section_type == "LLD":
        prompt = f"""
        Create a low-level design (LLD) document for the following project: {input_data}.
        Include:
        - Detailed migration steps
        - Security configurations (firewall, user roles, etc.)
        - Monitoring and optimization guidelines
        - Rollback and contingency plans.
        """
    else:
        raise ValueError("Invalid section type. Choose 'HLD' or 'LLD'.")

    # Use ChatCompletion for the new API format
    response = openai.chat.completions.create(
        model="gpt-4-turbo",  # Or "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are an experence architech who will be responsible for providing the design documents."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.8
    )
    
    # Access the content attribute directly
    document_section = response.choices[0].message.content.strip()
    return document_section
# Streamlit UI
st.title("HLD/LLD Document Generator")

# Collect user input
input_data = st.text_area("Enter Project Details", placeholder="Describe your project requirements here...")
generate_hld = st.checkbox("Generate HLD")
generate_lld = st.checkbox("Generate LLD")

# Button to trigger document generation
if st.button("Generate Document") and input_data:
    if generate_hld:
        st.subheader("High-Level Design (HLD)")
        hld_text = generate_document("HLD", input_data)
        st.write(hld_text)

    if generate_lld:
        st.subheader("Low-Level Design (LLD)")
        lld_text = generate_document("LLD", input_data)
        st.write(lld_text)
else:
    st.write("Please enter project details and select at least one document type to generate.")

# Option to download the results
if generate_hld or generate_lld:
    hld_text = generate_document("HLD", input_data) if generate_hld else ""
    lld_text = generate_document("LLD", input_data) if generate_lld else ""
    doc_content = f"## High-Level Design (HLD)\n\n{hld_text}\n\n## Low-Level Design (LLD)\n\n{lld_text}"
    
    # Streamlit download button
    st.download_button(
        label="Download Document",
        data=doc_content,
        file_name="design_document.md",
        mime="text/markdown"
    )

