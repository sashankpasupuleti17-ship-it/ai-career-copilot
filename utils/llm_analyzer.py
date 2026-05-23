import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_resume(resume_text, job_description):

    try:
        prompt = f"""
You are an expert AI career coach and ATS resume reviewer.

Analyze this resume against the job description.

Return:
1. ATS Match Score /100
2. Matched Skills
3. Missing Skills
4. Resume Weaknesses
5. Improvement Suggestions
6. Career Suggestions
7. Projects to Build

Resume:
{resume_text}

Job Description:
{job_description}
"""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI resume reviewer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Error: {e}"