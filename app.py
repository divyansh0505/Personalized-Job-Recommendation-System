import streamlit as st
from utils.parse_resume import extract_text  

st.title("🔍 Personalized Job Recommendation System")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    st.success("Resume uploaded successfully!")
    
    # Display the text in the app
    st.text_area("Extracted Resume Text", resume_text, height=250)
    print("Extracted Text:", resume_text)

