import streamlit as st

st.title("🔍 Personalized Job Recommendation System")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])
if uploaded_file:
    st.success("Resume uploaded successfully!")
    # You'll extract text later
