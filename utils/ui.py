import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    .stButton > button {
        background-color: #28a745;
        color: white;
        font-weight: bold;
        font-size: 16px;
        padding: 10px 24px;
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
    """Render the job selection UI components"""
    if 'job_dropdown' not in st.session_state:
        st.session_state.job_dropdown = []
    
    selected_titles = st.multiselect(
        "🎯 Select Job Titles to Filter (optional):",
        job_titles,
        default=st.session_state.job_dropdown,
        key="job_multiselect"
    )
    
    if selected_titles != st.session_state.job_dropdown:
        st.session_state.job_dropdown = selected_titles
    
    if st.button("🔄 Clear Filters"):
        st.session_state.job_dropdown = []
        st.rerun()
    
    return st.session_state.job_dropdown

def display_results(top_jobs):
    """Display the job recommendations"""
    st.subheader("🎯 Top Job Matches")
    for idx, row in top_jobs.iterrows():
        st.markdown(f"""
        <div style='padding: 10px 15px; border: 1px solid #ccc; border-radius: 8px; margin-bottom: 10px;'>
            <strong>{row['Title']}</strong><br>
            <span>{row['Description']}</span>
        </div>
        """, unsafe_allow_html=True)