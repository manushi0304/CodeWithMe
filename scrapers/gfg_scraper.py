import requests
import json
import re
import time
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- HELPER: CREATE A ROBUST SESSION ---
def get_retry_session():
    """
    Creates a requests session that automatically retries 3 times 
    if the connection fails or times out.
    """
    session = requests.Session()
    retry = Retry(
        total=3, 
        read=3, 
        connect=3, 
        backoff_factor=1, # Wait 1s, 2s, 4s between retries
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# ==========================================
# 1. LEETCODE SCRAPER (Fixed Timeouts)
# ==========================================
def fetch_leetcode_data(username):
    url = "https://leetcode.com/graphql"
    query = """
    query userProblems($username: String!) {
      matchedUser(username: $username) {
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """
    variables = {"username": username}
    
    try:
        session = get_retry_session()
        # Increased timeout to 30 seconds
        response = session.post(url, json={"query": query, "variables": variables}, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                return {"status": "error", "message": "User not found"}
            
            if "data" not in data or not data["data"]["matchedUser"]:
                return {"status": "error", "message": "User does not exist"}

            stats = data["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
            return {
                "status": "success",
                "totalSolved": stats[0]["count"],
                "easy": stats[1]["count"],
                "medium": stats[2]["count"],
                "hard": stats[3]["count"],
                "topics": {} 
            }
        else:
            return {"status": "error", "message": f"LeetCode Error: {response.status_code}"}
    except Exception as e:
        print(f"LeetCode Exception: {e}")
        return {"status": "error", "message": "Connection timed out. Try again."}

# ==========================================
# 2. CODEFORCES SCRAPER
# ==========================================
def fetch_codeforces_data(username):
    try:
        url = f"https://codeforces.com/api/user.info?handles={username}"
        session = get_retry_session()
        response = session.get(url, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK":
                info = data["result"][0]
                return {
                    "status": "success",
                    "rating": info.get("rating", 0),
                    "rank": info.get("rank", "unrated"),
                    "totalSolved": 0 
                }
        return {"status": "error", "message": "User not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ==========================================
# 3. GEEKSFORGEEKS SCRAPER (Robust)
# ==========================================
def fetch_gfg_data(username):
    """
    Tries 3 methods to get GFG Data:
    1. Direct JSON extraction (Fastest)
    2. Text Scraping (Backup)
    3. Public Proxy API (Failsafe)
    """
    url = f"https://www.geeksforgeeks.org/user/{username}/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/'
    }
    
    try:
        print(f"Fetching GFG data for: {username}...")
        session = get_retry_session()
        response = session.get(url, headers=headers, timeout=20)
        
        # Check for Security Block
        if response.status_code == 403 or "captcha" in response.text.lower():
            print("GFG blocked local request. Switching to Proxy API...")
            return fetch_gfg_proxy(username)

        if response.status_code != 200:
            return {"status": "error", "message": "Profile not found"}

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # METHOD 1: Hidden JSON Data
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if script_tag:
            try:
                data = json.loads(script_tag.string)
                page_props = data.get("props", {}).get("pageProps", {})
                user_info = page_props.get("userInfo", {})
                user_stats = page_props.get("userSolvedStats", {})
                
                total = user_info.get("total_problems_solved", 0)
                
                if total > 0:
                    return {
                        "status": "success",
                        "totalSolved": total,
                        "codingScore": user_info.get("score", 0),
                        "easy": user_stats.get("Easy", {}).get("count", 0),
                        "medium": user_stats.get("Medium", {}).get("count", 0),
                        "hard": user_stats.get("Hard", {}).get("count", 0),
                        "topics": {
                            "School": user_stats.get("School", {}).get("count", 0),
                            "Basic": user_stats.get("Basic", {}).get("count", 0),
                            "Easy": user_stats.get("Easy", {}).get("count", 0),
                            "Medium": user_stats.get("Medium", {}).get("count", 0),
                            "Hard": user_stats.get("Hard", {}).get("count", 0)
                        }
                    }
            except:
                pass 

        # METHOD 2: Regex Text Search
        return fetch_gfg_fallback(response.text)

    except Exception as e:
        print(f"GFG Local Failed: {e}")
        return fetch_gfg_proxy(username)

def fetch_gfg_fallback(html_content):
    try:
        match = re.search(r'Problems\s*Solved\s*[:\s-]*(\d+)', html_content, re.IGNORECASE)
        if not match:
            match = re.search(r'(\d+)\s*Problems\s*Solved', html_content, re.IGNORECASE)
        
        total = int(match.group(1)) if match else 0
        
        if total > 0:
            return {
                "status": "success",
                "totalSolved": total,
                "easy": 0, "medium": 0, "hard": 0,
                "topics": {}
            }
        return {"status": "error", "message": "Could not scrape data"}
    except:
        return {"status": "error", "message": "Fallback error"}

def fetch_gfg_proxy(username):
    """
    Failsafe: Uses a free public API if local scraping is blocked.
    """
    try:
        # Increase timeout for the proxy as well
        proxy_url = f"https://geeks-for-geeks-stats-api.vercel.app/?userName={username}"
        r = requests.get(proxy_url, timeout=15)
        if r.status_code == 200:
            d = r.json()
            if "totalProblemsSolved" in d:
                return {
                    "status": "success",
                    "totalSolved": d.get("totalProblemsSolved", 0),
                    "easy": d.get("easySolved", 0),
                    "medium": d.get("mediumSolved", 0),
                    "hard": d.get("hardSolved", 0),
                    "topics": {} 
                }
    except:
        pass
    
    return {"status": "error", "message": "All methods failed. Profile might be private."}

# ==========================================
# 4. OTHER SCRAPERS
# ==========================================
def fetch_codechef_data(username):
    return {} 

def fetch_atcoder_data(username):
    return {} 

def fetch_hackerrank_data(username):
    return {}