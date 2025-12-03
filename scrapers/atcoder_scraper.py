import requests
from bs4 import BeautifulSoup

def fetch_atcoder_data(username):
    headers = {"User-Agent": "CodeMateAI/1.0"}
    try:
        url = f"https://atcoder.jp/users/{username}"
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        tables = soup.find_all("table")
        if len(tables) < 2:
            return {}
            
        stats_table = tables[1]
        tds = stats_table.find_all("td")
        if len(tds) < 3:
            return {}
        
        # Extract rating and convert to solved count (approximation)
        rating = tds[1].text.strip()
        rating_num = int(rating) if rating.isdigit() else 0
        solved_count = max(0, rating_num // 100)  # Rough estimate: rating/100 = problems solved
            
        return {
            "rating": rating,
            "highest_rating": tds[2].text.strip(),
            "solved": solved_count  
        }
    except requests.exceptions.Timeout:
        print("AtCoder request timed out")
        return {}  
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Error fetching AtCoder data: {e}")
        return {}