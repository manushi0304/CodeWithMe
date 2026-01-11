import requests
from bs4 import BeautifulSoup
from collections import defaultdict

def fetch_hackerrank_data(username):
    url = f"https://www.hackerrank.com/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        soup = BeautifulSoup(
            requests.get(url, headers=headers, timeout=15).text,
            "html.parser"
        )

        solved_tag = soup.find("div", {"data-attr": "completed_challenges_count"})
        total = int(solved_tag.text.strip()) if solved_tag else 0

        stars = soup.text.count("★")

        skills = defaultdict(int)
        for s in soup.find_all("span", class_="skills-category-title"):
            skills[s.text.strip()] += 1

        return {
            "status": "success",
            "platform": "hackerrank",
            "username": username,
            "general": {
                "totalSolved": total,
                "easy": None,
                "medium": None,
                "hard": None,
                "rating": None,
                "rank": None,
                "stars": stars,
                "reputation": None
            },
            "topics": dict(skills),
            "metadata": {"source": "scraper", "confidence": "medium"}
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
