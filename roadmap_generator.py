import json
import random
import torch
import streamlit as st
from transformers import pipeline

# --- 1. SDE INTERVIEW PRIORITY (Ranked by Importance) ---
# Index 0 is highest priority to learn.
SDE_PRIORITY_MAP = [
    ("Array", "array"), 
    ("String", "string"), 
    ("Hash Table", "hash-table"),
    ("Two Pointers", "two-pointers"), 
    ("Sliding Window", "sliding-window"),
    ("Stack", "stack"), 
    ("Queue", "queue"), 
    ("Linked List", "linked-list"),
    ("Binary Search", "binary-search"), 
    ("Tree", "tree"), 
    ("Heap", "heap-priority-queue"),
    ("Recursion", "recursion"),
    ("Backtracking", "backtracking"), 
    ("Greedy", "greedy"), 
    ("Graph", "graph"), 
    ("BFS", "breadth-first-search"), 
    ("DFS", "depth-first-search"),
    ("Dynamic Programming", "dynamic-programming"), 
    ("Trie", "trie")
]

# STRICT PATTERNS (Prevents Hallucinations)
TOPIC_PATTERNS = {
    "Array": "Prefix Sums or Kadane's Algorithm",
    "String": "Palindrome checks or Anagrams",
    "Hash Table": "Frequency Counting or Two Sum pattern",
    "Two Pointers": "Left/Right pointers or Slow/Fast pointers",
    "Sliding Window": "Fixed vs Variable size windows",
    "Stack": "Monotonic Stack (Next Greater Element)",
    "Queue": "FIFO operations or BFS usage",
    "Linked List": "In-place reversal or Cycle detection",
    "Binary Search": "Search space reduction (Lower/Upper Bound)",
    "Tree": "Recursive Traversal (Pre/In/Post order)",
    "Heap": "Top K Frequent Elements",
    "Recursion": "Base cases and recursive leap of faith",
    "Backtracking": "State space tree pruning",
    "Greedy": "Local optimal choice (Interval scheduling)",
    "Graph": "Adjacency Matrix/List representation",
    "BFS": "Level-order traversal (Shortest Path)",
    "DFS": "Connected Components or Path finding",
    "Dynamic Programming": "Memoization (Top-Down) or Tabulation",
    "Trie": "Prefix tree insertion and search"
}

# --- 2. CACHED MODEL LOADING ---
@st.cache_resource
def load_roadmap_model():
    print("⏳ Loading Qwen for Roadmap...")
    try:
        return pipeline(
            "text-generation",
            model="Qwen/Qwen2.5-1.5B-Instruct",
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto", 
        )
    except Exception as e:
        print(f"⚠️ Model Error: {e}")
        return None

# --- 3. MAIN GENERATOR ---
def generate_roadmap(user_data):
    pipe = load_roadmap_model()
    
    # --- A. PARSE DATA ---
    if isinstance(user_data, str):
        try: data = json.loads(user_data)
        except: data = {"leetcode": {"general": {"topics": {}}}}
    else: data = user_data

    leetcode = data.get("leetcode", {})
    if "general" in leetcode and "topics" in leetcode["general"]:
        topics_stats = leetcode["general"]["topics"]
    else:
        topics_stats = leetcode.get("topics", {})

    username = leetcode.get("username", "Interviewee")
    last_contest = leetcode.get("lastContest", "the most recent Weekly Contest")
    if not last_contest or str(last_contest) == "None":
        last_contest = "the most recent Weekly Contest"

    # --- B. INTELLIGENT TOPIC SELECTION (FIXED) ---
    # 1. Map user stats to priority list
    user_weaknesses = []
    
    for index, (name, slug) in enumerate(SDE_PRIORITY_MAP):
        solved = topics_stats.get(name, 0)
        
        # We define a "Weakness" as solved < 15.
        # We store the 'priority' (index) to prioritize Arrays over Tries.
        if solved < 15:
            user_weaknesses.append({
                "name": name, 
                "slug": slug, 
                "priority": index
            })

    # 2. Selection Strategy
    # If we have many weaknesses, we focus on the high-priority ones first.
    # But to vary the output, we pick 3 randomly from the TOP 6 most important weaknesses.
    
    if len(user_weaknesses) >= 3:
        # Sort by SDE Priority (Index 0 is best) to find critical gaps
        user_weaknesses.sort(key=lambda x: x["priority"])
        
        # Take the top 6 most important missing skills
        top_candidates = user_weaknesses[:6]
        
        # Pick 3 random ones from this "High Value" pool
        selected = random.sample(top_candidates, 3)
        w1, w2, w3 = selected[0]["name"], selected[1]["name"], selected[2]["name"]
        
    elif len(user_weaknesses) > 0:
        # Not enough weaknesses? Fill the rest with defaults
        selected_names = [w["name"] for w in user_weaknesses]
        defaults = ["Dynamic Programming", "Graph", "Heap", "Backtracking"]
        
        for d in defaults:
            if d not in selected_names and len(selected_names) < 3:
                selected_names.append(d)
                
        w1, w2, w3 = selected_names[:3]
        
    else:
        # User is a master? Give them the hardest stuff.
        w1, w2, w3 = "Dynamic Programming", "Graph", "Trie"

    # --- C. GET PATTERNS ---
    p1 = TOPIC_PATTERNS.get(w1, "Core Logic")
    p2 = TOPIC_PATTERNS.get(w2, "Core Logic")
    p3 = TOPIC_PATTERNS.get(w3, "Core Logic")

    # --- D. GENERATE PROMPT ---
    system_msg = "You are 'The Interview Sensei'. Output ONLY valid Markdown. Do not hallucinate. Explain the specific concepts provided."
    
    user_msg = f"""
    Create a **7-Day Interview Plan** for "{username}".
    
    **DATA:**
    1. Topic: {w1} | Pattern: {p1}
    2. Topic: {w2} | Pattern: {p2}
    3. Topic: {w3} | Pattern: {p3}
    4. Contest: {last_contest}
    
    **INSTRUCTIONS:**
    - Explain the specific patterns provided above.
    - **Day 7**: Explicitly mention "{last_contest}".
    - **No Code Blocks**: Explain logic in plain English.
    
    **OUTPUT FORMAT:**
    # 📜 Codex of {w1}, {w2} & {w3}
    
    ## 🛡️ Strategy
    (One sentence on why these topics matter.)
    
    ## 🗺️ The Path
    ### Day 1: {w1} Fundamentals
    - **Concept**: (Define {w1} basics clearly.)
    - **Goal**: Solve 2 Easy problems.
    
    ### Day 2: {w1} Pattern: {p1}
    - **Concept**: (Explain specifically how **{p1}** works.)
    - **Goal**: Solve a Medium problem using **{p1}**.
    
    ### Day 3: {w2} Fundamentals
    - **Concept**: (Define {w2} basics.)
    - **Goal**: Solve 2 Easy problems.
    
    ### Day 4: {w2} Pattern: {p2}
    - **Concept**: (Explain specifically how **{p2}** works.)
    - **Goal**: Solve a Medium problem using **{p2}**.
    
    ### Day 5: {w3} Fundamentals
    - **Concept**: (Define {w3} basics.)
    - **Goal**: Solve 2 Easy problems.
    
    ### Day 6: {w3} Pattern: {p3}
    - **Concept**: (Explain specifically how **{p3}** works.)
    - **Goal**: Solve a Medium problem using **{p3}**.
    
    ### Day 7: The Contest Redemption
    - **Challenge**: Start a Virtual Contest for **{last_contest}**.
    - **Target**: Solve at least 2 problems in 60 minutes.
    - **Reward**: (Text reward like "Speed Coder Badge")
    """

    # --- E. RUN AI ---
    if pipe:
        out = pipe([{"role": "user", "content": user_msg}], max_new_tokens=1200, temperature=0.3)
        plan = out[0]['generated_text'][-1]['content']
    else:
        plan = "⚠️ AI Model not loaded."

    return {
        "topics": [w1, w2, w3],
        "detailed_plan": plan 
    }