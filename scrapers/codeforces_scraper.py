import requests

def fetch_codeforces_data(handle):
    headers = {"User-Agent": "CodeMateAI/1.0"}
    try:
        url = f"https://codeforces.com/api/user.info?handles={handle}"
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        data = res.json()
        
        if not data.get("result"):
            return {}
            
        user_info = data["result"][0]
        
        # Get additional stats for solved problems
        try:
            stats_url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1000"
            stats_res = requests.get(stats_url, headers=headers, timeout=10)
            if stats_res.status_code == 200:
                stats_data = stats_res.json()
                solved_count = len(set(sub["problem"]["name"] for sub in stats_data.get("result", []) 
                                    if sub.get("verdict") == "OK"))
            else:
                solved_count = 0
        except:
            solved_count = 0
            
        return {
            "rating": user_info.get("rating", "N/A"),
            "maxRating": user_info.get("maxRating", "N/A"),
            "rank": user_info.get("rank", "N/A"),
            "solved": solved_count  
        }
    except requests.exceptions.Timeout:
        print("Codeforces request timed out")
        return {}  
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Error fetching Codeforces data: {e}")
        return {}