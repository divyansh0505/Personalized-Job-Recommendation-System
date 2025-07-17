import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    .stButton > button {
        background-color: #28a745;
        color: white;
        font-weight: bold;
        font-size: 8px;
        padding: 6px 12px;
        border-radius: 8px;
        border: none;
        transition: 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #218838;
        cursor: pointer;
    }
    div[data-baseweb="select"] span {
        background-color: #d4edda !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

def job_selection_ui(job_titles):
    # Initialize session state
    if 'job_dropdown' not in st.session_state:
        st.session_state.job_dropdown = []
    
    # Create columns for better layout
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # Multiselect widget - use a unique key
        selected_titles = st.multiselect(
            "🎯 Select Job Titles to Filter (optional):",
            job_titles,
            default=st.session_state.job_dropdown,
            key="job_filter_widget"
        )
    
    with col2:
        # Clear filters button
        if st.button("🔄 Clear Filters", key="clear_filters_button"):
            st.session_state.job_dropdown = []
            st.rerun()
    
    # Update session state if selection changed
    if selected_titles != st.session_state.job_dropdown:
        st.session_state.job_dropdown = selected_titles
        st.rerun()
    
    return st.session_state.job_dropdown

def display_results(top_jobs):
    st.subheader("🎯 Top Job Matches")

    if top_jobs.empty:
        st.info("No matching jobs found.")
        return

    for idx, row in top_jobs.iterrows():
        with st.container():
            job_dict = row.to_dict()
            is_bookmarked = job_dict in st.session_state.bookmarked_jobs

            st.markdown(f"***{row['Title']}***  \n{row['Description']}")
            
            # Show match keywords if available
            if "Matched Keywords" in row and row["Matched Keywords"]:
                st.markdown(f"**🔑 Matched Keywords:** {row['Matched Keywords']}")

            # Optional: Show similarity score
            if "match_score" in row:
                st.markdown(f"**📊 Match Score:** {row['match_score']:.2f}")

            # Bookmark button
            bookmark_key = f"bookmark_{idx}"
            if st.button("❌ Remove Bookmark" if is_bookmarked else "🔖 Bookmark", key=bookmark_key):
                if is_bookmarked:
                    st.session_state.bookmarked_jobs.remove(job_dict)
                    st.success(f"Removed bookmark: {row['Title']}")
                else:
                    st.session_state.bookmarked_jobs.append(job_dict)
                    st.success(f"Bookmarked: {row['Title']}")
                st.rerun()

def display_bookmarks():
    st.subheader("🔖 Bookmarked Jobs")

    if not st.session_state.bookmarked_jobs:
        st.info("You haven't bookmarked any jobs yet.")
        return

    for idx, job in enumerate(st.session_state.bookmarked_jobs):
        with st.container():
            st.markdown(f"**{job['Title']}**  \n{job['Description']}  \n"
                        f"**🔑 Matched Keywords:** {job.get('Matched Keywords', '')}  \n"
                        f"**📊 Match Score:** {round(job.get('match_score', 0)*100)}%")
            st.markdown("---")

            if st.button(f"❌ Remove Bookmark", key=f"remove_{idx}"):
                st.session_state.bookmarked_jobs.remove(job)
                st.success(f"Removed bookmark: {job['Title']}")
                st.rerun()
