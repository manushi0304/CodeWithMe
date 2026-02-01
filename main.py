import streamlit as st
import random
import json
# Ensure you have these modules created or empty placeholders if not using them yet
from scrapers import *
from roadmap_generator import generate_roadmap
from pdf_report_generator import generate_pdf
from weekly_emailer import send_weekly_email
from utils import load_user_data, save_user_data
from code_evaluator import evaluate_code
from senior_dev_feedback import review_code_as_senior
from prompt_to_sql import prompt_to_sql
from code_translator import translate_code
from prompt_to_code import prompt_to_code as generate_code_from_prompt
from security_scanner import scan_security_issues
from coding_interview_simulator import simulate_interview
from code_performance_benchmark import benchmark_code
from codebase_analyzer import analyze_codebase

st.set_page_config(page_title="Eduvision", layout="wide")
st.title("EduVision")

tab1, tab2, tab3, tab4 = st.tabs(["Connect Handles", "Analyze & Roadmap", "AI Tools", "PDF & Email"])

# ---------------------------------------------------------
# TAB 1: CONNECT HANDLES
# ---------------------------------------------------------
with tab1:
    st.header("Enter Your Coding Handles")
    
    def sanitize_username(input_str):
        return input_str.split("/")[-1] if "/" in input_str else input_str

    # Inputs
    lc = sanitize_username(st.text_input("LeetCode Username"))
    #cf = sanitize_username(st.text_input("Codeforces Handle"))
    #gfg = sanitize_username(st.text_input("GeeksforGeeks Username"))
    #cc = sanitize_username(st.text_input("CodeChef Username"))
    #at = sanitize_username(st.text_input("AtCoder Username"))
    #hr = sanitize_username(st.text_input("HackerRank Username"))
    
    st.markdown("**Note:** If you have a URL, paste it directly. Otherwise, just enter the username.")

    if st.button("Fetch Stats & Save", key="fetch_stats_btn"):
        with st.spinner("Fetching data..."):
            # 1. Fetch Data
            user_stats = {
                "leetcode": fetch_leetcode_data(lc) if lc else {},
                "codeforces": fetch_codeforces_data(cf) if cf else {},
                "gfg": fetch_gfg_data(gfg) if gfg else {},
                "codechef": fetch_codechef_data(cc) if cc else {},
                "atcoder": fetch_atcoder_data(at) if at else {},
                "hackerrank": fetch_hackerrank_data(hr) if hr else {}
            }
            save_user_data(user_stats)
            
            # 2. Calculate Totals (Robust Logic)
            total_solved = 0
            platform_data = []
            
            for platform, stats in user_stats.items():
                if not stats: continue
                
                # Check if data is nested in 'general' (New Scraper Structure)
                if "general" in stats:
                    count = stats["general"].get("totalSolved", 0)
                # Check if data is flat (Old Scraper Structure)
                else:
                    count = stats.get("totalSolved", stats.get("solved", 0))
                
                # Safe integer conversion
                try:
                    count = int(count)
                except:
                    count = 0
                    
                total_solved += count
                platform_data.append((platform.capitalize(), count))

            st.success("Stats fetched and saved!")
            st.divider()
            
            # 3. Summary Cards
            st.subheader("📊 Coding Profile Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Solved", total_solved)
            col2.metric("Platforms Connected", len(platform_data))
            col3.metric("Active Profiles", sum(1 for _, count in platform_data if count > 0))
            
            # 4. Platform Breakdown
            st.subheader("Platform Breakdown")
            for platform, count in platform_data:
                progress = count / total_solved if total_solved > 0 else 0
                st.progress(progress, text=f"{platform}: {count} problems")
            
            # 5. Topics Section (Robust Extraction)
            st.subheader("Topics Covered")
            
            # Try to find topics in LeetCode data (either root or general)
            lc_data = user_stats.get("leetcode", {})
            lc_topics = lc_data.get("topics", {})
            if not lc_topics and "general" in lc_data:
                lc_topics = lc_data["general"].get("topics", {})

            if lc_topics:
                # Get top 5 topics
                top_topics = list(lc_topics.items())[:5]
                topic_cols = st.columns(len(top_topics))
                for idx, (t_name, t_count) in enumerate(top_topics):
                    with topic_cols[idx]:
                        st.info(f"**{t_name}**\n\n{t_count}")
            elif total_solved > 0:
                st.warning("Detailed topic data not available from LeetCode.")

# ---------------------------------------------------------
# TAB 2: ANALYZE & ROADMAP (UPDATED)
# ---------------------------------------------------------
with tab2:
    st.header("Personalized Coding Roadmap")
    
    # 1. Initialize Session State (Fixes Reload Issue)
    if "generated_roadmap" not in st.session_state:
        st.session_state.generated_roadmap = None

    # 2. Button: Only Updates State
    if st.button("Generate Roadmap", key="gen_roadmap_btn"):
        data = load_user_data()
        if data:
            with st.spinner("Summoning the AI Guild Master..."):
                # Call the new function which returns {'topics': [], 'detailed_plan': '...'}
                st.session_state.generated_roadmap = generate_roadmap(data)
        else:
            st.warning("No user data found. Connect handles first!")

    # 3. Display Logic (Persists after interactions)
    if st.session_state.generated_roadmap:
        roadmap = st.session_state.generated_roadmap
        
        # A. Horizontal Topic Cards
        st.subheader("⚔️ Your Current Battlefronts (Weaknesses)")
        
        # Safely get topics list
        topics_list = roadmap.get("topics", [])
        
        if topics_list:
            cols = st.columns(len(topics_list))
            for i, topic in enumerate(topics_list):
                with cols[i]:
                    st.markdown(f"""
                    <div style='
                        border: 2px solid #ff4b4b;
                        border-radius: 10px;
                        padding: 15px;
                        text-align: center;
                        background: #1E1E1E;
                        color: #FFFFFF;
                        height: 100px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                    '>
                    <h4 style='margin:0; padding:0;'>{topic}</h4>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No specific weak topics detected. General training recommended.")
        
        # B. Detailed Plan
        st.subheader("📝 Your 1-Week Action Plan")
        
        # Safely get the markdown plan (Fixes KeyError)
        plan_content = roadmap.get("detailed_plan", "⚠️ Plan generation failed.")
        
        with st.expander("View Full Adventure Log", expanded=True):
            st.markdown(plan_content)
        
        # C. Download Button
        st.download_button(
            label="📥 Download Adventure Log",
            data=plan_content,
            file_name="my_coding_adventure.md",
            mime="text/markdown"
        )

        # D. Progress Tracker (Updated for 14 days)
        st.subheader("🛡️ 7-Day Campaign Tracker")
        col_a, col_b = st.columns(2)
        
        completed_count = 0
        for day in range(1, 8):
            col = col_a if day <= 4 else col_b
            if col.checkbox(f"Day {day} Complete", key=f"quest_day_{day}"):
                completed_count += 1
        
        st.progress(completed_count / 7, text=f"Progress: {int((completed_count/7)*100)}%")
# ...
    else:
        # Default state before generation
        st.info("👈 Click 'Generate Roadmap' to receive your personalized adventure!")

    st.markdown("---")
    
    # Codebase Analyzer
    st.subheader("Analyze Codebase")
    uploaded_folder = st.text_input("Enter path to your local codebase folder")
    if st.button("Analyze Codebase", key="analyze_codebase_btn"):
        if uploaded_folder:
            summary = analyze_codebase(uploaded_folder)
            st.json(summary)

# ---------------------------------------------------------
# TAB 3: AI TOOLS
# ---------------------------------------------------------
with tab3:
    st.header("Intelligent AI Assistants")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Prompt to Code")
        prompt = st.text_area("Describe what you want to build:")
        if st.button("Generate Code", key="gen_code_btn"):
            with st.spinner('Generating...'):
                st.code(generate_code_from_prompt(prompt), language="python")
        
        st.subheader("Code Review")
        code = st.text_area("Paste your code for review:")
        context = st.text_input("Context (optional):")
        if st.button("Review as Senior Developer", key="review_code_btn"):
            with st.spinner('Analyzing...'):
                st.markdown(review_code_as_senior(code, context))
        
        st.subheader("Security Scan")
        if st.button("Scan Code for Vulnerabilities", key="scan_sec_btn"):
            issues = scan_security_issues(code)
            st.markdown("\n".join(issues) if isinstance(issues, list) else issues)
    
    with col2:
        st.subheader("Code Evaluator")
        if st.button("Run Code Evaluation", key="eval_code_btn"):
            st.write(evaluate_code(code))
        
        st.subheader("Prompt to SQL")
        nl = st.text_input("Ask a data question:")
        if st.button("Convert to SQL", key="gen_sql_btn"):
            st.code(prompt_to_sql(nl), language="sql")
        
        st.subheader("Code Translator")
        from_lang = st.selectbox("From", ["python", "java", "cpp", "javascript"])
        to_lang = st.selectbox("To", ["java", "python", "cpp", "javascript"])
        if st.button("Translate", key="trans_code_btn"):
            st.code(translate_code(code, from_lang, to_lang), language=to_lang)
        
        st.subheader("Performance Benchmark")
        if st.button("Benchmark Code", key="bench_code_btn"):
            result = benchmark_code(code)
            st.write(result)
    
    st.markdown("---")
    st.subheader("Coding Interview Simulator")
    
    # Initialize session state for interview
    if 'interview_active' not in st.session_state:
        st.session_state.interview_active = False
    if 'interview_question' not in st.session_state:
        st.session_state.interview_question = ""
    if 'interview_solution' not in st.session_state:
        st.session_state.interview_solution = ""
    
    interview_questions = [
        "Reverse a linked list",
        "Find the middle element of a linked list",
        "Implement a stack using queues",
        "Check if a binary tree is balanced",
        "Implement an LRU cache",
        "Find the longest substring without repeating characters",
        "Rotate an array to the right by k steps",
        "Design a parking lot system"
    ]
    
    if st.button("Simulate Interview", key="simulate_interview_main"):
        selected_question = random.choice(interview_questions)
        st.session_state.interview_question = selected_question
        result = simulate_interview(selected_question, 30)
        st.session_state.interview_active = True
        st.write(result)
    
    if st.session_state.interview_active:
        st.markdown(f"**Current Question:** {st.session_state.interview_question}")
        solution = st.text_area("Write your solution here:", height=300, key="solution_editor")
        st.session_state.interview_solution = solution
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Submit Solution", key="submit_solution_btn"):
                evaluation = evaluate_code(solution)
                st.session_state.evaluation_result = "\n".join(evaluation)
                st.success("Solution submitted for evaluation!")
        with col2:
            if st.button("End Interview", key="end_interview_btn"):
                st.session_state.interview_active = False
        with col3:
            if st.button("Clear Solution", key="clear_solution_btn"):
                st.session_state.interview_solution = ""
                st.experimental_rerun()
        
        if hasattr(st.session_state, 'evaluation_result'):
            st.subheader("Evaluation Feedback")
            st.write(st.session_state.evaluation_result)
            
            if st.button("Benchmark Solution Performance", key="benchmark_solution_btn"):
                benchmark_result = benchmark_code(st.session_state.interview_solution)
                st.write("Performance Metrics:")
                st.json(benchmark_result)

# ---------------------------------------------------------
# TAB 4: PDF & EMAIL
# ---------------------------------------------------------
with tab4:
    st.header("Weekly Reminder + Progress Report")
    email = st.text_input("Enter your email:")
    
    if st.button("Send Weekly Email", key="send_email_btn"):
        data = load_user_data()
        # Logic to get roadmap for email
        if data:
            # If roadmap exists in state, use it; otherwise generate fresh
            if st.session_state.get("generated_roadmap"):
                roadmap = st.session_state.generated_roadmap
            else:
                roadmap = generate_roadmap(data)
                
            result = send_weekly_email(email, roadmap)
            if result is True:
                st.success("Email sent!")
            else:
                st.error(f"Failed to send email: {result}")
        else:
             st.error("No user data found.")
    
    if st.button("Generate PDF Report", key="gen_pdf_btn"):
        data = load_user_data()
        if data:
            generate_pdf(data)
            st.success("PDF report saved!")
        else:
            st.error("No user data found.")
    
    st.markdown("---")
    #st.caption("© 2025 CodeWithME| Manushi Bombaywala")