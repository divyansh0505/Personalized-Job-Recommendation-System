import streamlit as st
from utils.parse_resume import extract_text  
import pandas as pd
from utils.match_jobs import recommend_jobs

st.title("🔍 Personalized Job Recommendation System")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    st.success("Resume uploaded successfully!")
    # Display the text in the app
    st.text_area("Extracted Resume Text", resume_text, height=250)

    print("Extracted Text:", resume_text)
    job_df = pd.read_csv("data/job_listings.csv")


    # Get top matching jobs
    top_jobs = recommend_jobs(resume_text, job_df)

    # Display recommended jobs
    st.subheader("🎯 Top Job Matches")
    for idx, row in top_jobs.iterrows():
        st.markdown(f"**{row['Title']}**")
        st.write(row["Description"])
        st.markdown("---")




