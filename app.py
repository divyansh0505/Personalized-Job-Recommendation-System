import streamlit as st
import pandas as pd
from utils.parse_resume import extract_text
from utils.match_jobs import recommend_jobs
from utils.ui import apply_custom_styles, job_selection_ui, display_results

def load_job_data():
    """Load and prepare job data"""
    job_df = pd.read_csv("data/job_listings.csv")
    job_titles = job_df["Title"].dropna().unique().tolist()
    job_titles.sort()
    return job_df, job_titles


def main():
    # Apply custom styles
    apply_custom_styles()
    
    # App title
    st.title("🔍 Personalized Job Recommendation System")
    
    # Load job data
    job_df, job_titles = load_job_data()
    
    # Resume upload section (only this appears first)
    uploaded_file = st.file_uploader("📄 Upload your resume", type=["pdf", "docx"])
    
    # Initialize session state
    if 'job_dropdown' not in st.session_state:
        st.session_state.job_dropdown = []
    
    # ONLY SHOW THE REST AFTER RESUME IS UPLOADED
    if uploaded_file:
        resume_text = extract_text(uploaded_file)
        st.success("✅ Resume uploaded and extracted successfully.")
        
        # Resume text dropdown
        with st.expander("📄 View Extracted Resume Text", expanded=False):
            st.text_area("Resume Content", resume_text, height=250, label_visibility="collapsed")
        
        # NOW SHOW THE JOB FILTERS (previously this was outside the if block)
        st.subheader("🔍 Filter Job Recommendations")
        clear_clicked, selected_titles = job_selection_ui(job_titles)
        
        if clear_clicked:
            st.session_state.job_dropdown = []
            st.experimental_rerun()
        
        # Process and show results
        filtered_df = job_df[job_df["Title"].isin(selected_titles)] if selected_titles else job_df
        top_jobs = recommend_jobs(resume_text, filtered_df)
        display_results(top_jobs)
    else:
        # Show nothing else until resume is uploaded
        st.info("ℹ️ Please upload your resume to see job filters and recommendations")

if __name__ == "__main__":
    main()