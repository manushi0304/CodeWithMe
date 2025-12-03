from fpdf import FPDF

def generate_pdf(user_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="CodeMate AI - Weekly Coding Report", ln=True, align="C")
    
    for platform, stats in user_data.items():
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=platform.capitalize(), ln=True)
        pdf.set_font("Arial", size=12)
        for key, value in stats.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    pdf.output("report.pdf")