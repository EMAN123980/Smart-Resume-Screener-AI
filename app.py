import streamlit as st
import pdfplumber
import pytesseract
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from pdf2image import convert_from_bytes
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
# =====================================
# Tesseract OCR Path (Windows)
# =====================================
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =====================================
# Page Configuration
# =====================================
st.set_page_config(
    page_title="Smart Resume Screener AI",
    page_icon="📄",
    layout="wide"
)

# =====================================
# Custom CSS
# =====================================
st.markdown("""
<style>

.main-title{
text-align:center;
font-size:42px;
font-weight:bold;
color:#2563EB;
}

.subtitle{
text-align:center;
font-size:18px;
color:gray;
margin-bottom:25px;
}

.card{
background:#F8FAFC;
padding:20px;
border-radius:15px;
box-shadow:2px 2px 12px rgba(0,0,0,.15);
margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# OCR Functions
# =====================================

def extract_text_ocr(uploaded_file):

    uploaded_file.seek(0)

    pdf_bytes = uploaded_file.read()

    images = convert_from_bytes(
        pdf_bytes,
        poppler_path=r"C:\Srf poppler\Library\bin"
    )

    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    return text


def extract_resume_text(uploaded_file):

    text = ""

    uploaded_file.seek(0)

    try:

        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text + "\n"

    except:

        pass

    if len(text.strip()) < 20:

        uploaded_file.seek(0)

        text = extract_text_ocr(uploaded_file)

    return text

# =====================================
# Header
# =====================================

st.markdown(
"""
<div class='main-title'>
📄 Smart Resume Screener AI
</div>

<div class='subtitle'>
AI Powered Resume Screening & ATS Analyzer
</div>
""",
unsafe_allow_html=True
)

# =====================================
# Sidebar
# =====================================

with st.sidebar:

    st.title("📌 Navigation")

    st.success("Industry Edition")

    st.markdown("---")

    st.write("🏠 Dashboard")

    st.write("📄 Resume Analysis")

    st.write("📊 ATS Report")

    st.write("🤖 AI Recommendation")

    st.write("📥 Download Report")

    st.markdown("---")

    st.info("Developed using Python + Streamlit")
    # =====================================
# Resume Upload
# =====================================

st.markdown("## 📤 Upload Resume")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

# =====================================
# Resume Processing
# =====================================

if uploaded_file is not None:

    st.success("✅ Resume Uploaded Successfully!")

    with st.spinner("🤖 AI is analyzing your resume..."):

        text = extract_resume_text(uploaded_file)

    # =====================================
    # Show Extracted Text
    # =====================================

    with st.expander("📄 View Extracted Resume"):

        st.text_area(
            "Resume Text",
            text,
            height=300
        )

    # =====================================
    # Candidate Name
    # =====================================

    candidate_name = "Not Found"

    for line in text.split("\n"):

        line = line.strip()

        if (
            len(line) > 3
            and len(line.split()) <= 4
            and "@" not in line
            and not any(ch.isdigit() for ch in line)
        ):
            candidate_name = line
            break

    # =====================================
    # Email Detection
    # =====================================

    emails = re.findall(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    email = emails[0] if emails else "Not Found"

    # =====================================
    # Phone Detection
    # =====================================

    phones = re.findall(
        r'(\+?\d[\d\s\-]{8,15}\d)',
        text
    )

    phone = phones[0] if phones else "Not Found"

    # =====================================
    # Education Detection
    # =====================================

    education_keywords = [

        "BS","BSc","Bachelor",

        "MS","MSc","Master",

        "Computer Science",

        "Software Engineering",

        "Intermediate",

        "Matric",

        "PhD"

    ]

    found_education = []

    for edu in education_keywords:

        if edu.lower() in text.lower():

            found_education.append(edu)

    # =====================================
    # Candidate Information
    # =====================================

    st.markdown("## 👤 Candidate Information")

    col1, col2 = st.columns(2)

    with col1:

        st.info(f"👤 Name : {candidate_name}")

        st.info(f"📧 Email : {email}")

    with col2:

        st.info(f"📞 Phone : {phone}")

        if found_education:

            st.success(
                "🎓 " + ", ".join(found_education)
            )

        else:

            st.warning("Education Not Found")
            # =====================================
    # Experience Detection
    # =====================================

    experience = re.findall(
        r'(\d+\+?\s*(?:years?|yrs?|months?))',
        text,
        re.IGNORECASE
    )

    # =====================================
    # Skills Detection
    # =====================================

    skills = [

        "Python",
        "Java",
        "C++",
        "C",
        "SQL",
        "MySQL",
        "HTML",
        "CSS",
        "JavaScript",
        "PHP",
        "React",
        "Node.js",
        "Flask",
        "Django",
        "Streamlit",
        "Git",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Data Science",
        "Data Analysis",
        "Power BI",
        "Excel"

    ]

    found_skills = []

    for skill in skills:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    # =====================================
    # ATS Score
    # =====================================

    score = min(len(found_skills) * 5, 100)

    # =====================================
    # Job Role Prediction
    # =====================================

    text_lower = text.lower()

    job_role = "General Candidate"

    if "machine learning" in text_lower or "artificial intelligence" in text_lower:

        job_role = "Machine Learning Engineer"

    elif "python" in text_lower and ("django" in text_lower or "flask" in text_lower):

        job_role = "Python Backend Developer"

    elif "python" in text_lower:

        job_role = "Python Developer"

    elif "react" in text_lower:

        job_role = "React Developer"

    elif "html" in text_lower and "css" in text_lower and "javascript" in text_lower:

        job_role = "Frontend Web Developer"

    elif "sql" in text_lower:

        job_role = "Database Developer"

    # =====================================
    # Dashboard
    # =====================================

    st.markdown("## 📊 AI Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👤 Candidate", candidate_name)

    col2.metric("📊 ATS Score", f"{score}/100")

    col3.metric("💡 Skills", len(found_skills))

    col4.metric("💼 Job Role", job_role)

    # =====================================
    # Skills
    # =====================================

    st.markdown("## 💡 Skills Detected")

    if found_skills:

        st.success(", ".join(found_skills))

    else:

        st.error("No Skills Found")

    # =====================================
    # Experience
    # =====================================

    st.markdown("## 💼 Experience")

    if experience:

        st.success(", ".join(experience))

    else:

        st.warning("Experience Not Found")

    # =====================================
    # ATS Score Progress
    # =====================================

    st.markdown("## 📈 ATS Score")

    st.progress(score)

    st.write(f"### Overall ATS Score: {score}/100")

    # =====================================
    # AI Recommendation
    # =====================================

    st.markdown("## 🤖 AI Recommendation")

    if score >= 80:

        rating = "⭐⭐⭐⭐⭐"

        recommendation = "Excellent Resume"

        st.success("🟢 Highly Recommended for Interview")

    elif score >= 60:

        rating = "⭐⭐⭐⭐"

        recommendation = "Good Resume"

        st.warning("🟡 Good Resume - Add more relevant skills")

    else:

        rating = "⭐⭐"

        recommendation = "Needs Improvement"

        st.error("🔴 Improve your resume before applying")

    st.write(f"### ⭐ Rating : {rating}")
    # =====================================
    # Resume vs Job Description Matching
    # =====================================

    st.markdown("## 💼 Resume vs Job Description Matching")

    job_description = st.text_area(
        "Paste Job Description Here",
        height=200,
        placeholder="Paste the complete Job Description..."
    )

    matched_skills = []
    missing_skills = []
    ats_match = 0

    if job_description.strip():

        jd_lower = job_description.lower()

        for skill in skills:

            if skill.lower() in jd_lower:

                if skill.lower() in text.lower():

                    matched_skills.append(skill)

                else:

                    missing_skills.append(skill)

        total = len(matched_skills) + len(missing_skills)

        if total > 0:

            ats_match = int(
                (len(matched_skills) / total) * 100
            )

        st.markdown("### 🎯 ATS Match Score")

        st.progress(ats_match)

        st.write(f"### {ats_match}% Match")

        left, right = st.columns(2)

        with left:

            st.success("✅ Matched Skills")

            if matched_skills:

                for skill in matched_skills:

                    st.write("✔", skill)

            else:

                st.write("No Skills Matched")

        with right:

            st.error("❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:

                    st.write("✖", skill)

            else:

                st.write("No Missing Skills")

    # =====================================
    # Skills Chart
    # =====================================

    st.markdown("## 📊 Skills Analysis")

    chart = pd.DataFrame({

        "Category":[
            "Detected Skills",
            "Missing Skills"
        ],

        "Count":[
            len(found_skills),
            len(skills)-len(found_skills)
        ]

    })

    st.bar_chart(chart.set_index("Category"))

    # =====================================
    # Resume Summary
    # =====================================

    st.markdown("## 📝 Resume Summary")

    st.info(f"""

👤 Candidate : {candidate_name}

📧 Email : {email}

📞 Phone : {phone}

🎓 Education :
{", ".join(found_education) if found_education else "Not Found"}

💼 Suggested Role :
{job_role}

⭐ Rating :
{rating}

📊 ATS Score :
{score}/100

💡 Skills Found :
{len(found_skills)}

🤖 Recommendation :
{recommendation}

""")

    # =====================================
    # Download Report
    # =====================================

    report = f"""
SMART RESUME SCREENER AI REPORT

Candidate Name:
{candidate_name}

Email:
{email}

Phone:
{phone}

Education:
{", ".join(found_education) if found_education else "Not Found"}

Experience:
{", ".join(experience) if experience else "Not Found"}

Skills:
{", ".join(found_skills) if found_skills else "Not Found"}

Suggested Job Role:
{job_role}

ATS Score:
{score}/100

Rating:
{rating}

Recommendation:
{recommendation}
"""

    st.download_button(

        "📄 Download Resume Report",

        report,

        file_name="Resume_Report.txt",

        mime="text/plain"

    )

    # =====================================
    # Footer
    # =====================================

    st.markdown("---")

    st.markdown(
        """
<div style='text-align:center;
padding:20px;
color:gray;'>

❤️ Smart Resume Screener AI

Industry Edition Version 4.0

Built with Python • Streamlit • OCR

</div>
""",
        unsafe_allow_html=True
    )

else:

    st.info("👆 Upload a Resume PDF to start analysis.")
    # =====================================
# Resume Improvement Suggestions
# =====================================

st.markdown("## 🚀 Resume Improvement Suggestions")

suggestions = []

if score < 80:
    suggestions.append("Add more relevant technical skills.")

if not experience:
    suggestions.append("Mention your work experience or internships.")

if not found_education:
    suggestions.append("Add your educational qualifications.")

if len(found_skills) < 8:
    suggestions.append("Include more tools and technologies related to your field.")

if email == "Not Found":
    suggestions.append("Add a professional email address.")

if phone == "Not Found":
    suggestions.append("Add your contact number.")

if suggestions:

    for tip in suggestions:

        st.warning("💡 " + tip)

else:

    st.success("🎉 Excellent! Your resume looks professional.")

# =====================================
# Candidate Performance
# =====================================

st.markdown("## 🏆 Candidate Performance")

if score >= 80:

    st.success("🌟 Excellent Candidate")

elif score >= 60:

    st.info("👍 Good Candidate")

elif score >= 40:

    st.warning("⚠ Average Candidate")

else:

    st.error("❌ Needs Major Improvements")

# =====================================
# AI Decision
# =====================================

st.markdown("## 🤖 Final AI Decision")

if score >= 80:

    st.success("✅ Recommended for Interview")

elif score >= 60:

    st.info("🟡 Can be shortlisted after improvements")

else:

    st.error("❌ Not Recommended")

# =====================================
# Analysis Completion
# =====================================

st.balloons()

st.success("🎉 Resume Analysis Completed Successfully!")
# =====================================
# Resume Improvement Suggestions
# =====================================

st.markdown("## 🚀 Resume Improvement Suggestions")

suggestions = []

if score < 80:
    suggestions.append("Add more relevant technical skills.")

if not experience:
    suggestions.append("Mention your work experience or internships.")

if not found_education:
    suggestions.append("Add your educational qualifications.")

if len(found_skills) < 8:
    suggestions.append("Include more tools and technologies related to your field.")

if email == "Not Found":
    suggestions.append("Add a professional email address.")

if phone == "Not Found":
    suggestions.append("Add your contact number.")

if suggestions:

    for tip in suggestions:

        st.warning("💡 " + tip)

else:

    st.success("🎉 Excellent! Your resume looks professional.")

# =====================================
# Candidate Performance
# =====================================

st.markdown("## 🏆 Candidate Performance")

if score >= 80:

    st.success("🌟 Excellent Candidate")

elif score >= 60:

    st.info("👍 Good Candidate")

elif score >= 40:

    st.warning("⚠ Average Candidate")

else:

    st.error("❌ Needs Major Improvements")

# =====================================
# AI Decision
# =====================================

st.markdown("## 🤖 Final AI Decision")

if score >= 80:

    st.success("✅ Recommended for Interview")

elif score >= 60:

    st.info("🟡 Can be shortlisted after improvements")

else:

    st.error("❌ Not Recommended")

# =====================================
# Analysis Completion
# =====================================

st.balloons()

st.success("🎉 Resume Analysis Completed Successfully!")
# =====================================
# Professional PDF Report
# =====================================

st.markdown("## 📄 Professional PDF Report")

def generate_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>SMART RESUME SCREENER AI REPORT</b>", styles["Title"])
    )

    story.append(
        Paragraph(f"<b>Candidate Name:</b> {candidate_name}", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Email:</b> {email}", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Phone:</b> {phone}", styles["Normal"])
    )

    story.append(
        Paragraph(
            f"<b>Education:</b> {', '.join(found_education) if found_education else 'Not Found'}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Experience:</b> {', '.join(experience) if experience else 'Not Found'}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Skills:</b> {', '.join(found_skills)}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Suggested Job Role:</b> {job_role}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>ATS Score:</b> {score}/100",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Rating:</b> {rating}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Recommendation:</b> {recommendation}",
            styles["Normal"]
        )
    )

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf


pdf_report = generate_pdf()

st.download_button(

    label="📥 Download Professional PDF Report",

    data=pdf_report,

    file_name="Smart_Resume_Report.pdf",

    mime="application/pdf"

)

st.success("✅ Professional PDF Report Ready")
# =====================================
# FINAL DASHBOARD
# =====================================

st.markdown("---")
st.markdown("## 🎯 Resume Health Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.success(f"""
### 📊 ATS

# {score}/100
""")

col2.info(f"""
### 💡 Skills

# {len(found_skills)}
""")

col3.warning(f"""
### 🎓 Education

# {len(found_education)}
""")

col4.error(f"""
### 💼 Experience

# {len(experience)}
""")

# =====================================
# PROJECT STATISTICS
# =====================================

st.markdown("## 📈 Analysis Statistics")

stat1, stat2 = st.columns(2)

with stat1:

    st.metric(
        "Resume Completion",
        f"{score}%"
    )

    st.metric(
        "Matched Skills",
        len(found_skills)
    )

with stat2:

    st.metric(
        "Education Entries",
        len(found_education)
    )

    st.metric(
        "Experience Entries",
        len(experience)
    )

# =====================================
# ABOUT PROJECT
# =====================================

st.markdown("---")

with st.expander("ℹ️ About Smart Resume Screener AI"):

    st.markdown("""

### 📄 Smart Resume Screener AI

This application analyzes resumes using Artificial Intelligence techniques.

### Features

✅ OCR Support

✅ ATS Score

✅ Skills Detection

✅ Email Detection

✅ Phone Detection

✅ Education Detection

✅ Experience Detection

✅ Job Role Prediction

✅ Resume vs Job Description Matching

✅ Interactive Charts

✅ Professional PDF Report

### Technologies Used

- Python

- Streamlit

- PDFPlumber

- Pytesseract OCR

- Plotly

- Pandas

- ReportLab

""")

# =====================================
# FINAL SUCCESS MESSAGE
# =====================================

st.markdown("---")

st.success("🎉 Resume Analysis Completed Successfully!")

st.balloons()

# =====================================
# FOOTER
# =====================================

st.markdown(
"""
<hr>

<div style="text-align:center">

<h3>📄 Smart Resume Screener AI</h3>

<p>
Industry Edition Version 4.0
</p>

<p>
Developed using ❤️ Python, Streamlit, OCR & AI
</p>

<p>
© 2026 All Rights Reserved
</p>

</div>
""",
unsafe_allow_html=True
)
