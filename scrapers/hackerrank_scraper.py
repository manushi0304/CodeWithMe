import requests
from bs4 import BeautifulSoup

def fetch_hackerrank_data(username):
    headers = {"User-Agent": "CodeMateAI/1.0"}
    try:
        url = f"https://www.hackerrank.com/{username}"
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        badges = soup.find_all("div", class_="hacker-badge")
        if not badges:
            return {}
        
        domains = [badge.text.strip() for badge in badges]
        # Estimate solved count based on badges (rough approximation)
        solved_count = len(domains) * 10  
            
        return {
            "badges": domains,
            "solved": solved_count  
        }
    except requests.exceptions.Timeout:
        print("HackerRank request timed out")
        return {}  
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Error fetching Hackerrank data: {e}")
        return {}