import requests
from bs4 import BeautifulSoup

def fetch_codechef_data(username):
    headers = {"User-Agent": "CodeMateAI/1.0"}
    try:
        url = f"https://www.codechef.com/users/{username}"
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        rating_tag = soup.find("div", class_="rating-number")
        stars_tag = soup.find("span", class_="rating-star")
        solved_section = soup.find("section", class_="rating-data-section problems-solved")
        
        if not all([rating_tag, stars_tag, solved_section]):
            return {"error": "Profile data not found"}
        
        solved = solved_section.find("h5").text if solved_section else "0"
        return {
            "rating": rating_tag.text.strip(),
            "stars": stars_tag.text.strip(),
            "problems_solved": solved.replace("Fully Solved (", "").replace(")", ""),
            "solved": int(solved_count) if solved_count.isdigit() else 0
        }
    except requests.exceptions.Timeout:
        print("Request timed out, retrying...")
        return fetch_codechef_data(username)
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Error fetching Codechef data: {e}")
        return {}