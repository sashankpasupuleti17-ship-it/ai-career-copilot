import json
import os

PROFILE_FILE = "user_profile.json"


def save_user_profile(profile_data):
    with open(PROFILE_FILE, "w", encoding="utf-8") as file:
        json.dump(profile_data, file, indent=4)

    return "Profile saved successfully."


def load_user_profile():
    if not os.path.exists(PROFILE_FILE):
        return {}

    with open(PROFILE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_application_packet(profile, job):
    packet = f"""
APPLICATION PACKET

Role: {job.get("title", "N/A")}
Company: {job.get("company", "N/A")}
Location: {job.get("location", "N/A")}

Candidate Details:
Name: {profile.get("full_name", "N/A")}
Email: {profile.get("email", "N/A")}
Phone: {profile.get("phone", "N/A")}
LinkedIn: {profile.get("linkedin", "N/A")}
GitHub: {profile.get("github", "N/A")}
Education: {profile.get("education", "N/A")}
Work Authorization: {profile.get("work_authorization", "N/A")}

Suggested Application Answer:
I am interested in this role because it aligns with my background in Python, AI, machine learning, and LLM-based application development. I have hands-on experience building AI-powered systems, including resume analysis, RAG-based retrieval, semantic search, and job tracking tools.

Skills to Highlight:
- Python
- LLM APIs
- RAG
- ChromaDB
- Streamlit
- Resume analysis
- Semantic search
- API integration
- GitHub

Short Cover Letter:
Dear Hiring Team,

I am excited to apply for the {job.get("title", "role")} position at {job.get("company", "your company")}. I am currently building AI-powered applications focused on resume intelligence, Retrieval-Augmented Generation, semantic search, and job automation. My experience with Python, LLM APIs, vector databases, and Streamlit aligns well with this opportunity.

I would welcome the opportunity to contribute my technical skills, problem-solving ability, and strong interest in AI engineering to your team.

Sincerely,
{profile.get("full_name", "Candidate")}
"""

    return packet