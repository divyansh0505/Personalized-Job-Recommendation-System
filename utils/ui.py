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

            st.markdown(f"**{row['Title']}**  \n{row['Description']}  \n---")

            # Create a unique key
            bookmark_key = f"bookmark_{idx}"

            # Handle button click
            if st.button("❌ Remove Bookmark" if is_bookmarked else "🔖 Bookmark", key=bookmark_key):
                if is_bookmarked:
                    st.session_state.bookmarked_jobs.remove(job_dict)
                    st.success(f"Removed bookmark: {row['Title']}")
                else:
                    st.session_state.bookmarked_jobs.append(job_dict)
                    st.success(f"Bookmarked: {row['Title']}")
                
                # Avoid needing double-click by forcing rerun with updated state
                st.rerun()
