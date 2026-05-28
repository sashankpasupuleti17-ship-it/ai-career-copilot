import streamlit as st
from datetime import datetime

from utils.email_notifier import send_job_notification
from utils.job_tracker import search_it_jobs
from utils.resume_parser import extract_text_from_pdf
from utils.autofill_agent import open_application_page

from utils.llm_analyzer import (
    analyze_resume,
    answer_with_context
)

from utils.application_assistant import (
    save_user_profile,
    load_user_profile,
    generate_application_packet
)

from utils.rag_engine import (
    create_vector_store,
    retrieve_relevant_chunks
)

st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🤖",
    layout="wide"
)

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

if "latest_jobs" not in st.session_state:
    st.session_state.latest_jobs = []

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

with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">🤖 AI Career Copilot</div>',
        unsafe_allow_html=True
    )

    st.caption("Upload resume + job description anytime from here.")
    st.divider()

    resume_file = st.file_uploader(
        "📄 Upload Resume PDF",
        type=["pdf"],
        key="resume_pdf_uploader"
    )

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
    st.info("Phase 4: RAG + Jobs + Application Autofill")

st.markdown(
    '<div class="main-title">AI Career Copilot</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="sub-title">
    Analyze resumes, chat with your career assistant, track jobs, and prepare applications.
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="card-title">Current Phase</div>
        <div class="card-value">Phase 4</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="card-title">Total Analyses</div>
        <div class="card-value">{len(st.session_state.analysis_history)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="card-title">AI System</div>
        <div class="card-value">RAG + Jobs</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

if analyze_button:
    if resume_file is None:
        st.error("Please upload your resume PDF.")

    elif not job_description.strip():
        st.error("Please paste a job description.")

    else:
        with st.spinner("Analyzing resume with AI..."):
            resume_text = extract_text_from_pdf(resume_file)

            combined_text = f"""
Resume:
{resume_text}

Job Description:
{job_description}
"""

            collection = create_vector_store(combined_text)
            st.session_state.rag_collection = collection

            result = analyze_resume(
                resume_text,
                job_description
            )

        history_item = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "job_title": job_title if job_title else "Untitled Job",
            "result": result,
            "resume_text": resume_text,
            "job_description": job_description
        }

        st.session_state.analysis_history.insert(0, history_item)
        st.success("Analysis completed successfully!")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🔎 Live IT Jobs",
    "📊 Latest Analysis",
    "💬 Ask Career Copilot",
    "📚 Previous Job History",
    "📄 Resume Text",
    "💼 Job Description",
    "📝 Application Autofill"
])

with tab1:
    st.subheader("Live USA IT Job Tracker")

    job_keyword = st.text_input(
        "Search Role",
        value="AI Engineer Intern",
        key="job_search_keyword"
    )

    job_location = st.text_input(
        "Location",
        value="United States",
        key="job_search_location"
    )

    if st.button("Find Jobs", key="find_jobs_button"):
        with st.spinner("Searching live IT jobs..."):
            jobs = search_it_jobs(
                keyword=job_keyword,
                location=job_location,
                results_per_page=10
            )

        if isinstance(jobs, dict) and "error" in jobs:
            st.error(jobs["error"])

        elif not jobs:
            st.warning("No jobs found. Try another keyword or location.")

        else:
            st.session_state.latest_jobs = jobs
            st.success(f"Found {len(jobs)} jobs.")

    if st.session_state.latest_jobs:
        if st.button("Send These Jobs to My Email", key="email_jobs_button"):
            email_status = send_job_notification(st.session_state.latest_jobs)
            st.info(email_status)

        for index, job in enumerate(st.session_state.latest_jobs, start=1):
            with st.container():
                st.markdown(f"### {index}. {job['title']}")
                st.write(f"**Company:** {job['company']}")
                st.write(f"**Location:** {job['location']}")
                st.write(f"**Posted Date:** {job['created']}")

                if job.get("is_recent"):
                    st.success("🔥 Posted within last 48 hours")

                with st.expander("Job Description"):
                    st.write(job["description"])

                st.link_button(
                    "Apply Now",
                    job["apply_link"]
                )

                st.divider()

with tab2:
    if st.session_state.analysis_history:
        latest = st.session_state.analysis_history[0]

        st.markdown(f"### {latest['job_title']}")
        st.caption(f"Analyzed on {latest['time']}")
        st.markdown('<div class="analysis-box">', unsafe_allow_html=True)
        st.markdown(latest["result"])
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Upload resume + job description from sidebar to see latest analysis.")

with tab3:
    st.subheader("Ask questions about your resume and job description")

    question = st.text_input(
        "Ask a question",
        placeholder="Example: What skills am I missing?",
        key="rag_question"
    )

    if st.button("Ask AI", key="ask_rag_button"):
        if "rag_collection" not in st.session_state:
            st.error("Please analyze a resume first.")

        elif not question.strip():
            st.error("Please enter a question.")

        else:
            with st.spinner("Retrieving relevant context..."):
                context = retrieve_relevant_chunks(
                    st.session_state.rag_collection,
                    question
                )

                answer = answer_with_context(
                    question,
                    context
                )

            st.markdown("### Answer")
            st.markdown(answer)

            with st.expander("Retrieved Context"):
                st.write(context)

with tab4:
    st.subheader("Previous Job Analysis History")

    if st.session_state.analysis_history:
        for index, item in enumerate(st.session_state.analysis_history):
            with st.expander(
                f"{index + 1}. {item['job_title']} — {item['time']}"
            ):
                st.markdown(item["result"])

                st.markdown("#### Job Description")

                st.text_area(
                    "Saved Job Description",
                    item["job_description"],
                    height=180,
                    key=f"jd_{index}"
                )
    else:
        st.info("No resume analysis history yet.")

with tab5:
    if st.session_state.analysis_history:
        latest = st.session_state.analysis_history[0]

        st.text_area(
            "Extracted Resume Text",
            latest["resume_text"],
            height=500,
            key="resume_text_display"
        )
    else:
        st.info("Upload and analyze a resume first.")

with tab6:
    if st.session_state.analysis_history:
        latest = st.session_state.analysis_history[0]

        st.text_area(
            "Latest Job Description Used",
            latest["job_description"],
            height=500,
            key="latest_jd_display"
        )
    else:
        st.info("Paste and analyze a job description first.")

with tab7:
    st.subheader("Application Autofill Assistant")

    saved_profile = load_user_profile()

    st.markdown("### Save Your Common Application Details")

    full_name = st.text_input(
        "Full Name",
        value=saved_profile.get("full_name", ""),
        key="profile_full_name"
    )

    email = st.text_input(
        "Email",
        value=saved_profile.get("email", ""),
        key="profile_email"
    )

    phone = st.text_input(
        "Phone",
        value=saved_profile.get("phone", ""),
        key="profile_phone"
    )

    linkedin = st.text_input(
        "LinkedIn",
        value=saved_profile.get("linkedin", ""),
        key="profile_linkedin"
    )

    github = st.text_input(
        "GitHub",
        value=saved_profile.get("github", ""),
        key="profile_github"
    )

    education = st.text_input(
        "Education",
        value=saved_profile.get("education", ""),
        key="profile_education"
    )

    work_authorization = st.text_area(
        "Work Authorization / Sponsorship Answer",
        value=saved_profile.get("work_authorization", ""),
        height=100,
        key="profile_work_auth"
    )

    common_answer = st.text_area(
        "Common Application Answer",
        value=saved_profile.get("common_answer", ""),
        height=120,
        key="profile_common_answer"
    )

    if st.button("Save Profile", key="save_profile_button"):
        profile_data = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "linkedin": linkedin,
            "github": github,
            "education": education,
            "work_authorization": work_authorization,
            "common_answer": common_answer
        }

        status = save_user_profile(profile_data)
        st.success(status)

    st.divider()

    st.markdown("### Generate Application Packet")

    if st.session_state.latest_jobs:
        selected_job_index = st.selectbox(
            "Select Job",
            range(len(st.session_state.latest_jobs)),
            format_func=lambda i: (
                f"{st.session_state.latest_jobs[i]['title']} - "
                f"{st.session_state.latest_jobs[i]['company']}"
            ),
            key="selected_application_job"
        )

        selected_job = st.session_state.latest_jobs[selected_job_index]

        if st.button("Generate Application Packet", key="generate_packet_button"):
            profile = load_user_profile()

            packet = generate_application_packet(
                profile,
                selected_job
            )

            st.text_area(
                "Application Packet",
                packet,
                height=500,
                key="application_packet_output"
            )

            st.link_button(
                "Open Apply Link",
                selected_job["apply_link"]
            )

        if st.button("Open with Autofill Assistant", key="open_autofill_button"):
            status = open_application_page(selected_job["apply_link"])
            st.info(status)

    else:
        st.info("Search jobs first in the Live IT Jobs tab.")