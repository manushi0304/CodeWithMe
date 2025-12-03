def simulate_interview(problem_statement, time_limit=30):
    return "\n".join([
        f"Coding Interview Starts Now!",
        f"Question: {problem_statement}",
        f"Time Limit: {time_limit} minutes",
        "",
        "Think out loud... explaining your thought process...",
        "",
        "Now attempt your solution in the editor below..."
    ])