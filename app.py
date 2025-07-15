import streamlit as st
import pandas as pd
from utils.parse_resume import extract_text
from utils.match_jobs import recommend_jobs
from utils.ui import apply_custom_styles, display_results,job_selection_ui
import io
import plotly
import plotly.express as px


def load_job_data():
    job_df = pd.read_csv("data/job_listings.csv")
    job_titles = job_df["Title"].dropna().unique().tolist()
    job_titles.sort()
    return job_df, job_titles

def main():
    # Apply custom styles
    apply_custom_styles()
    if "bookmarked_jobs" not in st.session_state:
        st.session_state.bookmarked_jobs = []

    # App title
    st.title("🔍 Personalized Job Recommendation System")
    
    # Load job data
    job_df, job_titles = load_job_data()
    
    # Resume upload section
    uploaded_file = st.file_uploader("📄 Upload your resume", type=["pdf", "docx"])
    
    # Only show filters and results after resume is uploaded
    if uploaded_file:
        resume_text = extract_text(uploaded_file)
        st.success("✅ Resume uploaded and extracted successfully.")
        
        # Resume text dropdown
        with st.expander("📄 View Extracted Resume Text", expanded=False):
            st.text_area("Resume Content", resume_text, height=250, label_visibility="collapsed")
        
        # Job filters section
                # Job filters section
        st.subheader("🔍 Filter Job Recommendations")

        # Category Filter (First apply)
        job_categories = job_df["Category"].dropna().unique().tolist()
        selected_categories = st.multiselect("📂 Filter by Job Categories (optional):", job_categories)

        # Title Filter
        selected_titles = job_selection_ui(job_titles)

        # Apply category and title filters
        filtered_df = job_df
        if selected_categories:
            filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]
        if selected_titles:
            filtered_df = filtered_df[filtered_df["Title"].isin(selected_titles)]

        # Apply keyword search filter
        search_query = st.text_input("🔎 Search within matched jobs (optional):").lower()
        if search_query:
            filtered_df = filtered_df[
                filtered_df["Title"].str.lower().str.contains(search_query) |
                filtered_df["Description"].str.lower().str.contains(search_query)
            ]

        # Run recommendations
        top_jobs = recommend_jobs(resume_text, filtered_df)
        display_results(top_jobs)


# Show chart if there are matched jobs
        fig = px.bar(top_jobs, x="Title", y="match_score", title="📈 Match Score per Job")
        st.plotly_chart(fig, use_container_width=True)
    

                


        

        # CSV download
        if not top_jobs.empty:
            csv = top_jobs.to_csv(index=False)
            st.download_button(
                label="📥 Download Top Matches",
                data=io.BytesIO(csv.encode()),
                file_name="top_job_matches.csv",
                mime="text/csv"
            )
        show_bookmarks = st.checkbox("📌 Show Bookmarked Jobs")

        if show_bookmarks and st.session_state.bookmarked_jobs:
            st.subheader("📌 Bookmarked Jobs")
            for job in st.session_state.bookmarked_jobs:
                st.markdown(f"**{job['Title']}**  \n{job['Description']}  \n---")
            if st.button("🗑 Clear All Bookmarks"):
                st.session_state.bookmarked_jobs = []
                st.success("All bookmarks removed!")
                st.rerun()    
            bookmarked_df = pd.DataFrame(st.session_state.bookmarked_jobs)
            csv_bookmarked = bookmarked_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Bookmarked Jobs",
                data=io.BytesIO(csv_bookmarked.encode()),
                file_name="bookmarked_jobs.csv",
                mime="text/csv"
            )     
        elif show_bookmarks:
            st.info("You have not bookmarked any jobs yet.")    

    else:
        st.info("ℹ️ Please upload your resume to see job filters and recommendations")

if __name__ == "__main__":
    main()