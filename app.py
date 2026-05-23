import streamlit as st
from datetime import datetime
from utils.resume_parser import extract_text_from_pdf
from utils.llm_analyzer import analyze_resume

st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🤖",
    layout="wide"
)

# Store analysis history
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

# Custom CSS
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #1f2937;
}
.sub-title {
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 30px;
}
.metric-card {
    background-color: #f8fafc;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.05);
    text-align: center;
}
.card-title {
    font-size: 15px;
    color: #6b7280;
}
.card-value {
    font-size: 28px;
    font-weight: 800;
    color: #111827;
}
.analysis-box {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.06);
}
.sidebar-title {
    font-size: 24px;
    font-weight: 800;
    color: #111827;
}
</style>
""", unsafe_allow_html=True)

# Sidebar inputs
with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">🤖 AI Career Copilot</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Upload resume + job description anytime from here."
    )

    st.divider()

    # FIXED: Added unique key
    resume_file = st.file_uploader(
        "📄 Upload Resume PDF",
        type=["pdf"],
        key="resume_pdf_uploader"
    )

    # Added keys for stability
    job_title = st.text_input(
        "🏢 Job Title / Company",
        placeholder="Example: AI Engineer Intern - Google",
        key="job_title_input"
    )

    job_description = st.text_area(
        "💼 Paste Job Description",
        height=280,
        placeholder="Paste job description here...",
        key="job_description_input"
    )

    analyze_button = st.button(
        "🚀 Analyze Resume",
        use_container_width=True,
        key="analyze_button"
    )

    clear_history = st.button(
        "🗑️ Clear History",
        use_container_width=True,
        key="clear_history_button"
    )

    if clear_history:
        st.session_state.analysis_history = []
        st.success("History cleared.")

    st.divider()

    st.info("Phase 1 MVP: Resume analysis using LLM.")

# Main page
st.markdown(
    '<div class="main-title">AI Career Copilot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '''
    <div class="sub-title">
    Analyze resumes, compare job descriptions,
    and track previous job analysis history.
    </div>
    ''',
    unsafe_allow_html=True
)

# Metric cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="card-title">Current Phase</div>
        <div class="card-value">Phase 1</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="card-title">Total Analyses</div>
        <div class="card-value">
            {len(st.session_state.analysis_history)}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="card-title">Next Upgrade</div>
        <div class="card-value">RAG</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Analyze resume
if analyze_button:

    if resume_file is None:
        st.error(
            "Please upload your resume PDF from the sidebar."
        )

    elif not job_description.strip():
        st.error(
            "Please paste the job description in the sidebar."
        )

    else:
        with st.spinner("Analyzing resume with AI..."):

            resume_text = extract_text_from_pdf(
                resume_file
            )

            result = analyze_resume(
                resume_text,
                job_description
            )

        history_item = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "job_title": (
                job_title
                if job_title
                else "Untitled Job"
            ),
            "result": result,
            "resume_text": resume_text,
            "job_description": job_description
        }

        st.session_state.analysis_history.insert(
            0,
            history_item
        )

        st.success(
            "Analysis completed and saved to history!"
        )

# Display results/history
if st.session_state.analysis_history:

    latest = st.session_state.analysis_history[0]

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Latest Analysis",
        "📚 Previous Job History",
        "📄 Resume Text",
        "💼 Job Description"
    ])

    # Latest analysis
    with tab1:

        st.markdown(f"### {latest['job_title']}")

        st.caption(
            f"Analyzed on {latest['time']}"
        )

        st.markdown(
            '<div class="analysis-box">',
            unsafe_allow_html=True
        )

        st.markdown(latest["result"])

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # History
    with tab2:

        st.subheader(
            "Previous Job Analysis History"
        )

        for index, item in enumerate(
            st.session_state.analysis_history
        ):

            with st.expander(
                f"{index + 1}. "
                f"{item['job_title']} — "
                f"{item['time']}"
            ):

                st.markdown(item["result"])

                st.markdown(
                    "#### Job Description"
                )

                st.text_area(
                    "Saved Job Description",
                    item["job_description"],
                    height=180,
                    key=f"jd_{index}"
                )

    # Resume text
    with tab3:

        st.text_area(
            "Extracted Resume Text",
            latest["resume_text"],
            height=500,
            key="resume_text_display"
        )

    # Job description
    with tab4:

        st.text_area(
            "Latest Job Description Used",
            latest["job_description"],
            height=500,
            key="latest_jd_display"
        )

# Empty state
else:

    st.markdown("""
    <div class="analysis-box">
        <h3>Welcome 👋</h3>

        <p>
        Use the sidebar to upload your resume
        and paste a job description.
        </p>

        <p>
        Your previous job analyses will appear
        here after each run.
        </p>

        <ul>
            <li>ATS match score</li>
            <li>Matched skills</li>
            <li>Missing skills</li>
            <li>Resume weaknesses</li>
            <li>Career suggestions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)