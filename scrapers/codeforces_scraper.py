import requests
from collections import defaultdict

def fetch_codeforces_data(handle):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        # --- USER INFO ---
        info = requests.get(
            f"https://codeforces.com/api/user.info?handles={handle}",
            headers=headers,
            timeout=10
        ).json()

        if info.get("status") != "OK":
            return {"status": "error", "message": "User not found"}

        user = info["result"][0]

        # --- SUBMISSIONS ---
        subs = requests.get(
            f"https://codeforces.com/api/user.status?handle={handle}",
            headers=headers,
            timeout=10
        ).json().get("result", [])

        solved = {}
        difficulty = {"easy": 0, "medium": 0, "hard": 0}
        topics = defaultdict(int)

        for s in subs:
            if s.get("verdict") == "OK":
                p = s["problem"]
                key = (p["contestId"], p["index"])
                if key in solved:
                    continue
                solved[key] = True

                rating = p.get("rating", 0)
                if rating <= 1200:
                    difficulty["easy"] += 1
                elif rating <= 1800:
                    difficulty["medium"] += 1
                else:
                    difficulty["hard"] += 1

                for tag in p.get("tags", []):
                    topics[tag] += 1

        return {
            "status": "success",
            "platform": "codeforces",
            "username": handle,
            "general": {
                "totalSolved": len(solved),
                "easy": difficulty["easy"],
                "medium": difficulty["medium"],
                "hard": difficulty["hard"],
                "rating": user.get("rating"),
                "rank": user.get("rank"),
                "stars": None,
                "reputation": None
            },
            "topics": dict(sorted(topics.items(), key=lambda x: x[1], reverse=True)),
            "metadata": {"source": "api", "confidence": "high"}
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
