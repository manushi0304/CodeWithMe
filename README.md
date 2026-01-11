# 🚀 CodeWithMe - AI-Powered Coding Assistant Platform

> Your intelligent companion for mastering data structures, algorithms, and coding interview preparation powered by AI.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Modules](#modules)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

**CodeWithMe** is a comprehensive AI-powered platform designed to help developers prepare for coding interviews, improve their algorithmic skills, and build better software. The platform leverages advanced AI capabilities to provide personalized learning paths, code analysis, security scanning, and interactive interview simulations.

### Why CodeWithMe?

- **Personalized Learning**: AI-generated weekly roadmaps tailored to your skill level
- **Real-time Feedback**: Get senior developer-level code reviews instantly
- **Interview Ready**: Simulate real coding interviews with AI
- **Security First**: Automated security vulnerability scanning
- **Multi-language Support**: Translate code between different programming languages
- **Performance Analysis**: Benchmark your code against optimal solutions

## ✨ Features

### 🧠 Core Features

| Feature | Description |
|---------|-------------|
| **AI Code Evaluation** | Get intelligent feedback on your code quality, efficiency, and best practices |
| **Personalized Roadmaps** | Weekly learning plans focused on specific DSA topics |
| **Interview Simulator** | Practice coding interviews with an AI interviewer |
| **Code Translation** | Convert code between Python, JavaScript, Java, C++, and more |
| **Security Scanner** | Identify vulnerabilities and security issues in your codebase |
| **Performance Benchmarking** | Compare your solution's time and space complexity |
| **Codebase Analysis** | Get insights into code structure, complexity, and maintainability |
| **Weekly Email Reports** | Receive beautiful HTML email reports with your progress |
| **SQL Query Generation** | Convert natural language to SQL queries |
| **Prompt-to-Code** | Generate working code from natural language descriptions |

### 🌟 Additional Features

- **PDF Report Generation**: Export your progress and analysis as professional PDF reports
- **LeetCode Integration**: Scrape and analyze problems from LeetCode
- **Senior Developer Feedback**: Get code reviews as if from a senior engineer
- **Custom Utilities**: Helper functions for common coding tasks

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Gmail account (for email features)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/manushi0304/CodeWithMe.git
   cd CodeWithMe
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Email Configuration
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-app-specific-password
   
   # API Keys (if needed)
   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
CodeWithMe/
│
├── scrapers/                      # Web scraping modules
│   └── leetcode_scraper.py       # LeetCode problem scraper
│
├── code_evaluator.py             # AI-powered code evaluation
├── code_performance_benchmark.py  # Performance analysis tool
├── code_translator.py            # Multi-language code translation
├── codebase_analyzer.py          # Codebase complexity analysis
├── coding_interview_simulator.py  # Interactive interview practice
├── main.py                       # Main application entry point
├── pdf_report_generator.py       # PDF report generation
├── prompt_to_code.py             # Natural language to code
├── prompt_to_sql.py              # Natural language to SQL
├── roadmap_generator.py          # Personalized learning paths
├── security_scanner.py           # Security vulnerability scanner
├── senior_dev_feedback.py        # Code review system
├── utils.py                      # Utility functions
├── weekly_emailer.py             # Email notification system
│
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🎮 Usage

### Main Menu

Run the main application to access all features:

```bash
python main.py
```

You'll see an interactive menu with options like:

```
╔══════════════════════════════════════╗
║      CodeWithMe - AI Assistant       ║
╚══════════════════════════════════════╝

1. 📝 Evaluate Code
2. 🗺️  Generate Learning Roadmap
3. 🎤 Interview Simulator
4. 🔄 Translate Code
5. 🔒 Security Scan
6. ⚡ Performance Benchmark
7. 📊 Analyze Codebase
8. 📧 Send Weekly Email
9. 🔍 Prompt to Code
10. 💾 Prompt to SQL
11. 📄 Generate PDF Report
0. ❌ Exit

Select an option:
```

### Example Workflows

#### 1. Get Code Feedback

```python
from code_evaluator import evaluate_code

code = """
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
"""

feedback = evaluate_code(code, language="python")
print(feedback)
```

#### 2. Generate Weekly Roadmap

```python
from roadmap_generator import generate_roadmap
from weekly_emailer import send_weekly_email

# Generate personalized roadmap
roadmap = generate_roadmap(
    topics=["Heap", "Backtracking", "Recursion"],
    skill_level="intermediate"
)

# Send via email
send_weekly_email("user@example.com", roadmap)
```

#### 3. Simulate Coding Interview

```python
from coding_interview_simulator import start_interview

# Start interactive interview session
start_interview(
    difficulty="medium",
    topic="arrays",
    time_limit=45  # minutes
)
```

#### 4. Scan for Security Issues

```python
from security_scanner import scan_code

code = """
import os
password = "hardcoded_password"
eval(user_input)
"""

vulnerabilities = scan_code(code)
for issue in vulnerabilities:
    print(f"⚠️ {issue['severity']}: {issue['description']}")
```

## 📦 Modules

### Code Evaluator
Analyzes code quality, suggests improvements, and provides best practice recommendations.

**Features:**
- Time and space complexity analysis
- Code style and formatting suggestions
- Best practices validation
- Bug detection

### Roadmap Generator
Creates personalized weekly learning plans based on your goals and skill level.

**Customization Options:**
- Topic selection (Arrays, Trees, Graphs, DP, etc.)
- Difficulty level (Beginner, Intermediate, Advanced)
- Time commitment (hours per week)
- Learning style preferences

### Interview Simulator
Simulates real coding interviews with an AI interviewer.

**Capabilities:**
- Multiple difficulty levels
- Real-time hints and guidance
- Performance evaluation
- Follow-up questions
- Time tracking

### Code Translator
Translates code between different programming languages while preserving logic.

**Supported Languages:**
- Python
- JavaScript
- Java
- C++
- And more...

### Security Scanner
Identifies security vulnerabilities and suggests fixes.

**Detection Areas:**
- SQL Injection
- XSS vulnerabilities
- Hardcoded credentials
- Unsafe eval() usage
- Directory traversal
- Insecure randomness

### Performance Benchmark
Measures and compares code performance.

**Metrics:**
- Execution time
- Memory usage
- Time complexity
- Space complexity
- Comparison with optimal solutions
- 
## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Add docstrings to all functions and classes
- Include unit tests for new features
- Update documentation as needed
- Keep commits atomic and well-described


## 🙏 Acknowledgments

- Hugging Face
- The open-source community

## 🗺️ Roadmap

- [ ] Add support for more programming languages
- [ ] Integrate with GitHub for automatic code reviews
- [ ] Mobile app development
- [ ] Community features (leaderboards, challenges)
- [ ] Advanced analytics dashboard
- [ ] Chrome extension for LeetCode
- [ ] VS Code plugin

## ⭐ Star History

If you find this project helpful, please consider giving it a star! ⭐

---

<div align="center">

**Built with ❤️ by developers, for developers**

[Report Bug](https://github.com/manushi0304/CodeWithMe/issues) · [Request Feature](https://github.com/manushi0304/CodeWithMe/issues)

</div>
