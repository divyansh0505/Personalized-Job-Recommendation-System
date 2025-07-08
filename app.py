import streamlit as st
from utils.parse_resume import extract_text  
import pandas as pd
from utils.match_jobs import recommend_jobs

#st.image("logo.png", width=80) FOR LOGO
st.markdown(
    "<h3 style='color:#1f77b4;'>Welcome to <b>JobSense</b> — your personalized job recommender 🔍</h3>",
    unsafe_allow_html=True
)


st.title("🔍 Personalized Job Recommendation System")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded_file:
    resume_text = extract_text(uploaded_file)
    st.success("✅ Resume uploaded successfully!")

    
    st.markdown(
        "<h2 style='color:#1f77b4;'>🎯 Personalized Job Matches</h2>",
        unsafe_allow_html=True
    )

    #  Collapsible Resume Viewer
    with st.expander("📄 View Extracted Resume Text"):
        st.text_area("Resume Text", resume_text, height=250)

   
    job_df = pd.read_csv("data/job_listings.csv")
    top_jobs = recommend_jobs(resume_text, job_df)


    st.markdown("### 🔎 Top Recommended Jobs")
    if top_jobs.empty:
        st.warning("No matching jobs found. Try uploading a different resume.")
    else:
        for idx, row in top_jobs.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 5])     #width ratio

                with col1:
                    st.markdown("💼")

                with col2:
                    st.markdown(
                        f"<h4 style='margin-bottom: 0px;'>{row['Title']}</h4>",
                        unsafe_allow_html=True
                    )
                    st.write(row["Description"])
                st.markdown("---")






