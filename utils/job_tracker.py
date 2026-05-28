import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")


def is_recent_job(created_date, hours=48):
    try:
        posted_time = datetime.fromisoformat(
            created_date.replace("Z", "+00:00")
        )

        now = datetime.now(timezone.utc)

        return now - posted_time <= timedelta(hours=hours)

    except Exception:
        return False


def search_it_jobs(
    keyword="AI Engineer Intern",
    location="United States",
    results_per_page=50
):

    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "what": keyword,
        "where": location,
        "results_per_page": results_per_page,
        "sort_by": "date",
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return {
            "error": f"API Error {response.status_code}: {response.text}"
        }

    data = response.json()

    jobs = []

    for job in data.get("results", []):

        created_date = job.get("created", "N/A")

        recent = is_recent_job(
            created_date,
            hours=48
        )

        if recent:

            jobs.append({

                "title":
                job.get("title", "N/A"),

                "company":
                job.get(
                    "company",
                    {}
                ).get(
                    "display_name",
                    "N/A"
                ),

                "location":
                job.get(
                    "location",
                    {}
                ).get(
                    "display_name",
                    "N/A"
                ),

                "created":
                created_date,

                "description":
                job.get(
                    "description",
                    "N/A"
                ),

                "apply_link":
                job.get(
                    "redirect_url",
                    "N/A"
                ),

                "is_recent":
                True
            })

    return jobs