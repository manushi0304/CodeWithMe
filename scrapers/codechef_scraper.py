import requests
from bs4 import BeautifulSoup
import re

def fetch_codechef_data(username):
    try:
        soup = BeautifulSoup(
            requests.get(
                f"https://www.codechef.com/users/{username}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            ).text,
            "html.parser"
        )

        rating = soup.find("div", class_="rating-number")
        stars = soup.find("span", class_="rating-star")

        solved_match = re.search(r"\d+", soup.text)
        solved = int(solved_match.group()) if solved_match else 0

        return {
            "status": "success",
            "platform": "codechef",
            "username": username,
            "general": {
                "totalSolved": solved,
                "easy": None,
                "medium": None,
                "hard": None,
                "rating": int(rating.text.strip()) if rating else None,
                "rank": None,
                "stars": stars.text.strip() if stars else None,
                "reputation": None
            },
            "topics": {},
            "metadata": {"source": "scraper", "confidence": "low"}
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
