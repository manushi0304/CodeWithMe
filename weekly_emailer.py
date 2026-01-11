import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")


def format_roadmap_email(roadmap):
    """
    Converts roadmap dict into clean, well-formatted email
    """
    topics = roadmap.get("topics", [])
    detailed_plan = roadmap.get("detailed_plan", "")

    topic_line = ", ".join(topics) if topics else "General Practice"

    # Plain text version
    text_body = f"""Hello 👋,

Here's your personalized weekly coding roadmap from CodeMate AI.

📌 Focus Topics:
{topic_line}

----------------------------------------

{detailed_plan}

----------------------------------------

🚀 Stay consistent. Solve daily. Reflect weekly.

– CodeMate AI
"""

    # HTML version for better formatting
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .topics {{
            background-color: #e3f2fd;
            padding: 15px;
            border-left: 4px solid #2196F3;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .topics strong {{
            color: #1976D2;
        }}
        .roadmap {{
            background-color: #fafafa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.8;
        }}
        .roadmap h1 {{
            color: #2c3e50;
            font-size: 24px;
            margin-top: 0;
        }}
        .roadmap h2 {{
            color: #34495e;
            font-size: 18px;
            margin-top: 20px;
        }}
        .roadmap h3 {{
            color: #3498db;
            font-size: 16px;
            margin-top: 15px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            color: #7f8c8d;
            font-style: italic;
        }}
        .motivational {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin: 20px 0;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">Hello 👋</h1>
        
        <p>Here's your personalized weekly coding roadmap from <strong>CodeMate AI</strong>.</p>
        
        <div class="topics">
            <strong>📌 Focus Topics:</strong><br>
            {topic_line}
        </div>
        
        <div class="roadmap">
{detailed_plan}
        </div>
        
        <div class="motivational">
            🚀 Stay consistent. Solve daily. Reflect weekly.
        </div>
        
        <div class="footer">
            – CodeMate AI
        </div>
    </div>
</body>
</html>
"""

    return text_body.strip(), html_body.strip()


def send_weekly_email(to_email, roadmap_data):
    """
    Sends formatted email with both plain text and HTML versions
    """
    # Create message with both plain text and HTML
    msg = MIMEMultipart('alternative')
    
    # Format roadmap properly
    if isinstance(roadmap_data, dict):
        text_content, html_content = format_roadmap_email(roadmap_data)
    else:
        text_content = str(roadmap_data)
        html_content = f"<html><body><pre>{text_content}</pre></body></html>"

    # Attach both versions
    part1 = MIMEText(text_content, 'plain', 'utf-8')
    part2 = MIMEText(html_content, 'html', 'utf-8')
    
    msg.attach(part1)
    msg.attach(part2)
    
    # Set headers
    msg["Subject"] = "📅 Your CodeMate AI Weekly Coding Plan"
    msg["From"] = EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)
        print(f"✅ Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return str(e)
