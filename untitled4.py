import streamlit as st
import pandas as pd
import numpy as np
import io
from PIL import Image
import requests
from io import BytesIO

# Function definitions and parameter descriptions
# Add your existing parameter_mapping and parameter_descriptions here

def process_data(uploaded_file, partner_id, buffer_percent, grade, district_digits, block_digits, school_digits, student_digits, selected_param):
    # Add your implementation here
    pass

def main():
    st.title("Student ID Generator")

    # Initialize session state for buttons
    if 'buttons_initialized' not in st.session_state:
        st.session_state['buttons_initialized'] = True
        st.session_state['download_data'] = None
        st.session_state['download_mapped'] = None
        st.session_state['download_teachers'] = None

    # Display the image before parameter selection
    image_url = "https://github.com/pranay-raj-goud/Testing/blob/889f28dd72ee8e1402374d4abc69c22e05b7c21b/Pic.png?raw=true"  # URL to your image file
    try:
        # Fetch and display the image
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        st.image(image, caption='Parameters for Custom ID Generation', use_column_width=True)
    except Exception as e:
        st.error(f"Error loading image: {e}")

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        
        partner_id = st.number_input("Partner ID", min_value=0, value=0)
        buffer_percent = st.number_input("Buffer (%)", min_value=0.0, max_value=100.0, value=30.0)
        grade = st.number_input("Grade", min_value=1, value=1)
        district_digits = st.number_input("District ID Digits", min_value=1, value=2)
        block_digits = st.number_input("Block ID Digits", min_value=1, value=2)
        school_digits = st.number_input("School ID Digits", min_value=1, value=3)
        student_digits = st.number_input("Student ID Digits", min_value=1, value=4)
        
        selected_param = st.selectbox("Select Parameter Set", list(parameter_mapping.keys()))
        st.write(parameter_descriptions[selected_param])

        if st.button("Generate IDs"):
            data_expanded, data_mapped, teacher_codes = process_data(uploaded_file, partner_id, buffer_percent, grade, district_digits, block_digits, school_digits, student_digits, selected_param)

            # Save the data for download
            towrite1 = io.BytesIO()
            towrite2 = io.BytesIO()
            towrite3 = io.BytesIO()
            with pd.ExcelWriter(towrite1, engine='xlsxwriter') as writer:
                data_expanded.to_excel(writer, index=False)
            with pd.ExcelWriter(towrite2, engine='xlsxwriter') as writer:
                data_mapped.to_excel(writer, index=False)
            with pd.ExcelWriter(towrite3, engine='xlsxwriter') as writer:
                teacher_codes.to_excel(writer, index=False)
            
            towrite1.seek(0)
            towrite2.seek(0)
            towrite3.seek(0)
            
            # Update session state for download links
            st.session_state['download_data'] = towrite1
            st.session_state['download_mapped'] = towrite2
            st.session_state['download_teachers'] = towrite3

    # Always show download buttons
    if st.session_state['download_data'] is not None:
        st.download_button(label="Download Student IDs Excel", data=st.session_state['download_data'], file_name="Student_Ids.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
    if st.session_state['download_mapped'] is not None:
        st.download_button(label="Download Mapped Student IDs Excel", data=st.session_state['download_mapped'], file_name="Student_Ids_Mapped.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
    if st.session_state['download_teachers'] is not None:
        st.download_button(label="Download Teacher Codes Excel", data=st.session_state['download_teachers'], file_name="Teacher_Codes.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    main()
