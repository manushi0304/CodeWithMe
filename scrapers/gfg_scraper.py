import requests
from bs4 import BeautifulSoup

def fetch_gfg_data(username):
    try:
        soup = BeautifulSoup(
            requests.get(
                f"https://auth.geeksforgeeks.org/user/{username}/practice",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            ).text,
            "html.parser"
        )

        solved_div = soup.find("div", class_="score_card_value")
        total = int(solved_div.text.strip()) if solved_div else 0

        return {
            "status": "success",
            "platform": "geeksforgeeks",
            "username": username,
            "general": {
                "totalSolved": total,
                "easy": None,
                "medium": None,
                "hard": None,
                "rating": None,
                "rank": None,
                "stars": None,
                "reputation": None
            },
            "topics": {},
            "metadata": {"source": "scraper", "confidence": "low"}
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
