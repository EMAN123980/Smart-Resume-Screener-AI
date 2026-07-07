# ==========================================
# Smart Resume Screener AI
# Industry Edition v5.0
# Part 1
# ==========================================

import streamlit as st
import pandas as pd
import pdfplumber
import pytesseract
import re

from pdf2image import convert_from_bytes
from PIL import Image

import plotly.express as px
import plotly.graph_objects as go

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import getSampleStyleSheet

from io import BytesIO

from styles import load_css

# ==========================================
# OCR Configuration
# ==========================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

POPPLER_PATH = r"C:\Srf poppler\Library\bin"

# ==========================================
# Streamlit Page Config
# ==========================================

st.set_page_config(
    page_title="Smart Resume Screener AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# Load CSS
# ==========================================

load_css()

# ==========================================
# Sidebar
# ==========================================

with st.sidebar:

    st.title("📄 Smart Resume Screener AI")

    st.markdown("---")

    st.success("Industry Edition v5.0")

    st.write("### Features")

    st.write("✅ OCR Support")
    st.write("✅ ATS Score")
    st.write("✅ Skills Detection")
    st.write("✅ Resume Ranking")
    st.write("✅ AI Recommendation")
    st.write("✅ Job Role Prediction")
    st.write("✅ PDF Report")
    st.write("✅ Charts")
    st.write("✅ JD Matching")

    st.markdown("---")

    st.info(
        "Upload a Resume PDF to start analysis."
    )

# ==========================================
# Main Header
# ==========================================

st.title("📄 Smart Resume Screener AI")

st.caption(
    "AI Powered Resume Screening System"
)

st.markdown("---")

# ==========================================
# Resume Upload
# ==========================================

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)
# ==========================================
# PART 2
# OCR + PDF Text Extraction
# ==========================================

def extract_text_pdf(uploaded_file):
    """
    Extract text from a normal (text-based) PDF.
    """
    uploaded_file.seek(0)

    text = ""

    try:
        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception:

        text = ""

    return text


def extract_text_ocr(uploaded_file):
    try:
        uploaded_file.seek(0)
        pdf_bytes = uploaded_file.read()

        images = convert_from_bytes(pdf_bytes)

        text = ""

        for image in images:
            text += pytesseract.image_to_string(image)

        return text

    except Exception:
        return ""


def extract_resume_text(uploaded_file):
    """
    Automatically choose PDF text extraction
    or OCR depending on the resume.
    """

    text = extract_text_pdf(uploaded_file)

    # If almost no text is found,
    # automatically use OCR.

    if len(text.strip()) < 20:

        text = extract_text_ocr(uploaded_file)

    return text


# ==========================================
# Start Resume Analysis
# ==========================================

if uploaded_file is not None:

    st.success("✅ Resume Uploaded Successfully!")

    text = extract_resume_text(uploaded_file)

    st.subheader("📄 Extracted Resume Text")

    st.text_area(
        "Resume Content",
        text,
        height=300
    )
    # ==========================================
# PART 3
# Candidate Information Extraction
# ==========================================

    # --------------------------------------
    # Candidate Name
    # --------------------------------------

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    candidate_name = "Not Found"

    for line in lines[:5]:

        if (
            len(line.split()) >= 2
            and len(line.split()) <= 4
            and not any(char.isdigit() for char in line)
            and "resume" not in line.lower()
            and "curriculum" not in line.lower()
            and "vitae" not in line.lower()
            and "email" not in line.lower()
        ):
            candidate_name = line
            break

    st.subheader("👤 Candidate Name")
    st.success(candidate_name)

    # --------------------------------------
    # Email Detection
    # --------------------------------------

    emails = re.findall(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    email = emails[0] if emails else "Not Found"

    st.subheader("📧 Email")

    if emails:
        st.success(email)
    else:
        st.error("No Email Found")

    # --------------------------------------
    # Phone Detection
    # --------------------------------------

    phones = re.findall(
        r'(\+?\d[\d\s\-\(\)]{8,18}\d)',
        text
    )

    phone = phones[0] if phones else "Not Found"

    st.subheader("📞 Phone Number")

    if phones:
        st.success(phone)
    else:
        st.error("No Phone Number Found")

    # --------------------------------------
    # Education Detection
    # --------------------------------------

    education_keywords = [

        "Matric",

        "Intermediate",

        "ICS",

        "FA",

        "FSc",

        "DAE",

        "Bachelor",

        "BS",

        "BSc",

        "BE",

        "BBA",

        "BCS",

        "Master",

        "MS",

        "MSc",

        "MBA",

        "MPhil",

        "PhD",

        "Computer Science",

        "Software Engineering",

        "Information Technology",

        "Artificial Intelligence",

        "Data Science"

    ]

    found_education = []

    for edu in education_keywords:

        if edu.lower() in text.lower():

            found_education.append(edu)

    st.subheader("🎓 Education")

    if found_education:

        st.success(", ".join(sorted(set(found_education))))

    else:

        st.warning("Education Not Found")

    # --------------------------------------
    # Experience Detection
    # --------------------------------------

    experience = re.findall(

        r'(\d+\+?\s*(?:years?|yrs?|months?))',

        text,

        re.IGNORECASE

    )

    st.subheader("💼 Experience")

    if experience:

        st.success(", ".join(experience))

    else:

        st.warning("Experience Not Found")
        # ==========================================
# PART 4
# Skills Detection + ATS + AI Analysis
# ==========================================

    # --------------------------------------
    # Skills Detection
    # --------------------------------------

    skills = [

        "Python",
        "Java",
        "C",
        "C++",
        "C#",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Angular",
        "Node.js",
        "PHP",
        "Laravel",
        "Django",
        "Flask",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Oracle",
        "Git",
        "GitHub",
        "Docker",
        "Kubernetes",
        "Linux",
        "AWS",
        "Azure",
        "Google Cloud",
        "Firebase",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Data Science",
        "Data Analysis",
        "Pandas",
        "NumPy",
        "TensorFlow",
        "PyTorch",
        "OpenCV",
        "Streamlit",
        "Power BI",
        "Tableau",
        "Excel"

    ]

    found_skills = []

    for skill in skills:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    found_skills = sorted(list(set(found_skills)))

    st.subheader("💡 Skills Detected")

    if found_skills:

        st.success(", ".join(found_skills))

    else:

        st.error("No Skills Found")

    # --------------------------------------
    # ATS Score
    # --------------------------------------

    score = 0

    score += min(len(found_skills) * 4, 40)

    if candidate_name != "Not Found":
        score += 10

    if email != "Not Found":
        score += 10

    if phone != "Not Found":
        score += 10

    if found_education:
        score += 15

    if experience:
        score += 15

    if score > 100:
        score = 100

    st.subheader("📊 ATS Score")

    st.progress(score)

    st.success(f"{score}/100")

    # --------------------------------------
    # Resume Rating
    # --------------------------------------

    if score >= 85:

        rating = "⭐⭐⭐⭐⭐ Excellent"

    elif score >= 70:

        rating = "⭐⭐⭐⭐ Very Good"

    elif score >= 55:

        rating = "⭐⭐⭐ Good"

    elif score >= 40:

        rating = "⭐⭐ Average"

    else:

        rating = "⭐ Needs Improvement"

    st.subheader("🏆 Resume Rating")

    st.info(rating)

    # --------------------------------------
    # AI Recommendation
    # --------------------------------------

    if score >= 80:

        recommendation = "✅ Highly Recommended"

    elif score >= 60:

        recommendation = "🟡 Recommended with Minor Improvements"

    else:

        recommendation = "❌ Needs Significant Improvement"

    st.subheader("🤖 AI Recommendation")

    if score >= 80:

        st.success(recommendation)

    elif score >= 60:

        st.warning(recommendation)

    else:

        st.error(recommendation)

    # --------------------------------------
    # Job Role Prediction
    # --------------------------------------

    if "machine learning" in text.lower() or "deep learning" in text.lower():

        job_role = "Machine Learning Engineer"

    elif "data science" in text.lower():

        job_role = "Data Scientist"

    elif "python" in text.lower():

        job_role = "Python Developer"

    elif "java" in text.lower():

        job_role = "Java Developer"

    elif "react" in text.lower():

        job_role = "Frontend Developer"

    elif "node.js" in text.lower():

        job_role = "Backend Developer"

    elif "sql" in text.lower():

        job_role = "Database Developer"

    else:

        job_role = "General Software Engineer"

    st.subheader("🎯 Suggested Job Role")

    st.success(job_role)
    # ==========================================
# PART 5
# Dashboard + Charts + Resume Summary
# ==========================================

    # --------------------------------------
    # Dashboard Metrics
    # --------------------------------------

    st.markdown("---")
    st.subheader("📊 Resume Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("ATS Score", f"{score}/100")
    col2.metric("Skills", len(found_skills))
    col3.metric("Education", len(found_education))
    col4.metric("Experience", len(experience))

    # --------------------------------------
    # Skills Pie Chart
    # --------------------------------------

    st.subheader("📈 Skills Analytics")

    total_skills = len(skills)
    detected = len(found_skills)
    missing = total_skills - detected

    pie = px.pie(
        values=[detected, missing],
        names=["Detected", "Missing"],
        title="Skills Distribution"
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

    # --------------------------------------
    # ATS Gauge
    # --------------------------------------

    gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=score,

            title={"text": "ATS Score"},

            gauge={

                "axis": {"range": [0, 100]},

                "bar": {"color": "green"},

                "steps": [

                    {"range": [0, 40], "color": "#ffcccc"},

                    {"range": [40, 70], "color": "#fff4cc"},

                    {"range": [70, 100], "color": "#d4edda"}

                ]

            }

        )

    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

    # --------------------------------------
    # Resume Summary
    # --------------------------------------

    st.subheader("📝 Resume Summary")

    st.info(f"""

👤 Candidate Name:
{candidate_name}

📧 Email:
{email}

📞 Phone:
{phone}

🎓 Education:
{", ".join(found_education) if found_education else "Not Found"}

💼 Experience:
{", ".join(experience) if experience else "Not Found"}

💡 Skills:
{len(found_skills)}

🎯 Suggested Role:
{job_role}

📊 ATS Score:
{score}/100

🏆 Rating:
{rating}

🤖 Recommendation:
{recommendation}

""")

    # --------------------------------------
    # Resume Improvement Suggestions
    # --------------------------------------

    st.subheader("🚀 Resume Improvement Suggestions")

    suggestions = []

    if len(found_skills) < 8:
        suggestions.append("Add more technical skills related to your field.")

    if not experience:
        suggestions.append("Include internship or job experience.")

    if not found_education:
        suggestions.append("Mention your education details clearly.")

    if email == "Not Found":
        suggestions.append("Add a professional email address.")

    if phone == "Not Found":
        suggestions.append("Add your contact number.")

    if suggestions:

        for item in suggestions:

            st.warning("💡 " + item)

    else:

        st.success("🎉 Excellent! Your resume looks professional.")
        # ==========================================
# PART 6
# Resume vs Job Description Matching
# ==========================================

    st.markdown("---")
    st.subheader("💼 Resume vs Job Description Matching")

    job_description = st.text_area(
        "Paste Job Description Here",
        height=220,
        placeholder="Paste the complete Job Description..."
    )

    if job_description:

        jd_lower = job_description.lower()

        matched_skills = []
        missing_skills = []

        for skill in skills:

            if skill.lower() in jd_lower:

                if skill.lower() in text.lower():

                    matched_skills.append(skill)

                else:

                    missing_skills.append(skill)

        total_required = len(matched_skills) + len(missing_skills)

        if total_required > 0:

            match_score = int(
                (len(matched_skills) / total_required) * 100
            )

        else:

            match_score = 0

        # --------------------------------------
        # Match Score
        # --------------------------------------

        st.subheader("🎯 Resume Match Score")

        st.progress(match_score)

        st.success(f"{match_score}% Match")

        # --------------------------------------
        # Dashboard
        # --------------------------------------

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Matched Skills",
            len(matched_skills)
        )

        col2.metric(
            "Missing Skills",
            len(missing_skills)
        )

        col3.metric(
            "Match %",
            f"{match_score}%"
        )

        # --------------------------------------
        # Matched Skills
        # --------------------------------------

        st.subheader("✅ Matched Skills")

        if matched_skills:

            st.success(", ".join(matched_skills))

        else:

            st.warning("No matching skills found.")

        # --------------------------------------
        # Missing Skills
        # --------------------------------------

        st.subheader("❌ Missing Skills")

        if missing_skills:

            st.error(", ".join(missing_skills))

        else:

            st.success("Excellent! No missing skills.")

        # --------------------------------------
        # AI Feedback
        # --------------------------------------

        st.subheader("🤖 AI Feedback")

        if match_score >= 80:

            st.success(
                "Excellent match! Your resume is highly aligned with the Job Description."
            )

        elif match_score >= 60:

            st.warning(
                "Good match. Add a few more relevant skills to improve your chances."
            )

        elif match_score >= 40:

            st.info(
                "Average match. Consider updating your resume according to the Job Description."
            )

        else:

            st.error(
                "Poor match. Add the missing skills and relevant experience before applying."
            )

    else:

        st.info(
            "Paste a Job Description above to calculate Resume Match Score."
        )
        # ==========================================
# PART 7
# Professional PDF Report + Download
# ==========================================

    st.markdown("---")
    st.subheader("📄 Professional Resume Report")

    def generate_pdf_report():

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>Smart Resume Screener AI Report</b>",
                styles["Title"]
            )
        )

        story.append(
            Paragraph("<br/>", styles["Normal"])
        )

        story.append(
            Paragraph(
                f"<b>Candidate Name:</b> {candidate_name}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Email:</b> {email}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Phone:</b> {phone}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Education:</b> {', '.join(found_education) if found_education else 'Not Found'}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Experience:</b> {', '.join(experience) if experience else 'Not Found'}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Skills:</b> {', '.join(found_skills) if found_skills else 'None'}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Suggested Job Role:</b> {job_role}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>ATS Score:</b> {score}/100",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Resume Rating:</b> {rating}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>AI Recommendation:</b> {recommendation}",
                styles["BodyText"]
            )
        )

        if job_description:

            story.append(
                Paragraph(
                    f"<b>Resume Match Score:</b> {match_score}%",
                    styles["Heading2"]
                )
            )

            story.append(
                Paragraph(
                    f"<b>Matched Skills:</b> {', '.join(matched_skills) if matched_skills else 'None'}",
                    styles["BodyText"]
                )
            )

            story.append(
                Paragraph(
                    f"<b>Missing Skills:</b> {', '.join(missing_skills) if missing_skills else 'None'}",
                    styles["BodyText"]
                )
            )

        story.append(
            Paragraph("<br/>", styles["Normal"])
        )

        story.append(
            Paragraph(
                "<b>Resume Improvement Suggestions</b>",
                styles["Heading2"]
            )
        )

        if suggestions:

            for item in suggestions:

                story.append(
                    Paragraph(
                        "• " + item,
                        styles["BodyText"]
                    )
                )

        else:

            story.append(
                Paragraph(
                    "Excellent! No improvements required.",
                    styles["BodyText"]
                )
            )

        doc.build(story)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf

    pdf_file = generate_pdf_report()

    st.download_button(

        label="📥 Download Professional PDF Report",

        data=pdf_file,

        file_name="Resume_Analysis_Report.pdf",

        mime="application/pdf"

    )
    # ==========================================
# PART 8
# Final Dashboard + About + Footer
# ==========================================

    st.markdown("---")

    st.subheader("📊 Final Analysis Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "ATS Score",
        f"{score}/100"
    )

    c2.metric(
        "Skills",
        len(found_skills)
    )

    c3.metric(
        "Education",
        len(found_education)
    )

    c4.metric(
        "Experience",
        len(experience)
    )

    st.markdown("---")

    st.subheader("📈 Resume Performance")

    if score >= 85:

        st.success(
            "🌟 Outstanding Resume! Highly competitive for professional opportunities."
        )

    elif score >= 70:

        st.success(
            "✅ Strong Resume. Minor improvements can make it even better."
        )

    elif score >= 50:

        st.warning(
            "⚠ Good Resume. Add more skills and experience to increase ATS score."
        )

    else:

        st.error(
            "❌ Resume needs significant improvements before applying."
        )

    st.markdown("---")

    with st.expander("ℹ️ About Smart Resume Screener AI"):

        st.markdown("""

### 📄 Smart Resume Screener AI

This application analyzes resumes using Artificial Intelligence techniques.

### ✨ Features

- OCR Support
- Text PDF Support
- Candidate Name Detection
- Email Detection
- Phone Detection
- Education Detection
- Experience Detection
- Skills Detection
- ATS Score Calculation
- Resume Rating
- AI Recommendation
- Job Role Prediction
- Resume vs Job Description Matching
- Interactive Charts
- Professional PDF Report

### 🛠 Technologies Used

- Python
- Streamlit
- PDFPlumber
- PDF2Image
- PyTesseract
- Plotly
- Pandas
- ReportLab

""")

    st.markdown("---")

    st.success("🎉 Resume Analysis Completed Successfully!")

    st.balloons()

    st.markdown(
        """
        <div style="text-align:center;padding:20px;">

        <h3>📄 Smart Resume Screener AI</h3>

        <p>
        Industry Edition v5.0
        </p>

        <p>
        Developed using Python • Streamlit • OCR • AI
        </p>

        <p>
        © 2026 All Rights Reserved
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info("📂 Upload a Resume PDF to start analysis.")
    # ==========================================
# PART 9
# Final Optimizations & Error Handling
# ==========================================

# --------------------------------------
# Helpful Tips
# --------------------------------------

with st.sidebar:

    st.markdown("---")

    st.subheader("💡 Tips")

    st.info(
        """
• Upload PDF resumes only

• Text PDFs are faster

• Scanned PDFs use OCR

• Add Job Description for better ATS Matching

• Download the final PDF report
"""
    )

# --------------------------------------
# AI Resume Score Explanation
# --------------------------------------

st.markdown("---")

with st.expander("📘 How is ATS Score Calculated?"):

    st.write("""
The ATS Score is calculated using multiple resume factors.

### Score Distribution

- Skills → 40 Marks
- Candidate Name → 10 Marks
- Email → 10 Marks
- Phone Number → 10 Marks
- Education → 15 Marks
- Experience → 15 Marks

Maximum Score = 100
""")

# --------------------------------------
# Disclaimer
# --------------------------------------

st.markdown("---")

st.caption(
    """
⚠️ This application provides an AI-assisted resume analysis.
The ATS score is an estimated evaluation and should not be
considered an official hiring decision.
"""
)

# --------------------------------------
# Final Thank You
# --------------------------------------

st.markdown("---")

st.success("✅ Smart Resume Screener AI is Ready!")

st.info(
    """
Thank you for using Smart Resume Screener AI.

Built for Educational & Professional Learning.
"""
)

# ==========================================
# END OF APPLICATION
# ==========================================
