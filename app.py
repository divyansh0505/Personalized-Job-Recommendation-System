import streamlit as st
import pandas as pd
from utils.parse_resume import extract_text
from utils.match_jobs import recommend_jobs
from utils.ui import apply_custom_styles, display_results, job_selection_ui, display_bookmarks
from utils.bookmark_handler import save_bookmarks, load_bookmarks
import io
import plotly.express as px


def load_job_data():
    job_df = pd.read_csv("data/job_listings.csv")
    job_titles = job_df["Title"].dropna().unique().tolist()
    job_titles.sort()
    return job_df, job_titles


def main():
    apply_custom_styles()

    # Load bookmarks from disk only once
    if "bookmarked_jobs" not in st.session_state:
        st.session_state.bookmarked_jobs = load_bookmarks()

    st.title("🔍 Personalized Job Recommendation System")
    page = st.sidebar.selectbox("Choose a page:", ["Home", "Bookmarks"])

    if page == "Home":
        job_df, job_titles = load_job_data()

        uploaded_file = st.file_uploader("📄 Upload your resume", type=["pdf", "docx"])

        if uploaded_file:
            resume_text = extract_text(uploaded_file)
            st.success("✅ Resume uploaded and extracted successfully.")

            with st.expander("📄 View Extracted Resume Text", expanded=False):
                st.text_area("Resume Content", resume_text, height=250, label_visibility="collapsed")

            st.subheader("🔍 Filter Job Recommendations")

            job_categories = job_df["Category"].dropna().unique().tolist()
            selected_categories = st.multiselect("📂 Filter by Job Categories (optional):", job_categories)

            selected_titles = job_selection_ui(job_titles)

            filtered_df = job_df
            if selected_categories:
                filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]
            if selected_titles:
                filtered_df = filtered_df[filtered_df["Title"].isin(selected_titles)]

            search_query = st.text_input("🔎 Search within matched jobs (optional):").lower()
            if search_query:
                filtered_df = filtered_df[
                    filtered_df["Title"].str.lower().str.contains(search_query) |
                    filtered_df["Description"].str.lower().str.contains(search_query)
                ]

            top_jobs = recommend_jobs(resume_text, filtered_df)
            display_results(top_jobs)

            # Save updated bookmarks (in case user interacted with them)
            save_bookmarks(st.session_state.bookmarked_jobs)

            if not top_jobs.empty:
                fig = px.bar(top_jobs, x="Title", y="match_score", title="📈 Match Score per Job")
                st.plotly_chart(fig, use_container_width=True)

                csv = top_jobs.to_csv(index=False)
                st.download_button(
                    label="📥 Download Top Matches",
                    data=io.BytesIO(csv.encode()),
                    file_name="top_job_matches.csv",
                    mime="text/csv"
                )
        else:
            st.info("ℹ️ Please upload your resume to see job filters and recommendations")

    elif page == "Bookmarks":
        display_bookmarks()


if __name__ == "__main__":
    main()
