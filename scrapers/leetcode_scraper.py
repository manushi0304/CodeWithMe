import requests

def fetch_leetcode_data(username):
    url = "https://leetcode.com/graphql"
    
    # Combined Query: Fetches General Stats + Topic Stats in one go
    query = """
    query userProfile($username: String!) {
      matchedUser(username: $username) {
        username
        profile {
          ranking
          reputation
        }
        submitStats: submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
        tagProblemCounts {
          advanced {
            tagName
            problemsSolved
          }
          intermediate {
            tagName
            problemsSolved
          }
          fundamental {
            tagName
            problemsSolved
          }
        }
      }
    }
    """
    
    variables = {"username": username}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://leetcode.com"
    }

    try:
        response = requests.post(url, json={"query": query, "variables": variables}, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Validation: Check if user exists
        if "errors" in data or data.get("data", {}).get("matchedUser") is None:
            return {"status": "error", "message": "User not found"}

        user_data = data["data"]["matchedUser"]
        
        # --- PROCESS 1: General Stats ---
        # The API returns a list like [{'difficulty': 'All', 'count': 50}, ...]
        # We convert this into a clean dictionary
        stats_list = user_data["submitStats"]["acSubmissionNum"]
        general_stats = {item["difficulty"]: item["count"] for item in stats_list}
        
        # --- PROCESS 2: Topic Stats ---
        # Flatten the nested categories (Fundamental/Intermediate/Advanced)
        tag_counts = user_data["tagProblemCounts"]
        topics_map = {}
        
        for category in ["fundamental", "intermediate", "advanced"]:
            for item in tag_counts[category]:
                topics_map[item["tagName"]] = item["problemsSolved"]
        
        # Sort topics by count (highest first)
        sorted_topics = dict(sorted(topics_map.items(), key=lambda item: item[1], reverse=True))

        # --- MERGED OUTPUT ---
        return {
            "status": "success",
            "username": user_data["username"],
            "general": {
                "totalSolved": general_stats.get("All", 0),
                "easy": general_stats.get("Easy", 0),
                "medium": general_stats.get("Medium", 0),
                "hard": general_stats.get("Hard", 0),
                "ranking": user_data["profile"]["ranking"],
                "reputation": user_data["profile"]["reputation"]
            },
            "topics": sorted_topics
        }

    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Connection failed: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Data parsing error: {e}"}

# --- Usage Example ---
target_user = "shivamsouravjha" 
profile = fetch_leetcode_data(target_user)

if profile["status"] == "success":
    print(f"=== Profile: {profile['username']} ===")
    print(f"Total Solved: {profile['general']['totalSolved']} (Rank: {profile['general']['ranking']})")
    print(f"Breakdown: Easy {profile['general']['easy']} | Med {profile['general']['medium']} | Hard {profile['general']['hard']}")
    
    print("\n=== Top 5 Strongest Topics ===")
    # Get first 5 items from the dictionary
    top_topics = list(profile['topics'].items())[:5]
    for topic, count in top_topics:
        print(f"- {topic}: {count}")
else:
    print(f"Error: {profile['message']}")