import os
import streamlit as st
from PyPDF2 import PdfReader
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from dotenv import load_dotenv
from octoai.client import OctoAI
from octoai.text_gen import ChatMessage
from Lama import *
import time


st.set_page_config(page_title='Task Management and Evaluator', layout='wide')
col1, col2 = st.columns([5,1])  
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom, #fffefb, #fffefb);
        color: black;
    }
    .stApp {
        background: linear-gradient(to bottom, #fffefb, #fffefb);
        color: black;
    }
    .stButton button {
        border-color: black !important;
        border-width: 2px !important;
        background : #d4eaf7;
        color: black !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background: #cccbc8 !important;
        color: black !important;
        border-radius: 10px !important;
        border: 2px solid black !important;
    }
    .stTextArea div[role="textbox"] {
        background: #cccbc8 !important;
        color: black !important;
        border-radius: 10px !important;
        border: 2px solid black !important;
    }
    .stExpanderHeader {
        background-color: #cccbc8;
        color: black;
    }
    .stExpanderContent {
        background-color: #cccbc8;
        color: black;
    }
    .stExpanderHeader:hover {
        background-color: #cccbc8;
    }
    .stDownloadButton > button {
        background-color: #d4eaf7 !important;
        color: black !important;
    }
    .css-18e3th9, .css-1d391kg {
        padding: 2rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

with col1:
    st.title("Internee Task Manager and Evaluator ")

# # Load .env file
# dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
# load_success = load_dotenv(dotenv_path)

# # Replace with your actual API key
# llama_api_key = os.getenv('LLAMA_API_KEY')
llama_api_key = st.secrets["LLAMA_API_KEY"]
client = OctoAI(api_key=llama_api_key)


def pdf_generator(final_report):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=26,
        spaceAfter=12,
        alignment=1  # Center align
    )

    heading_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceAfter=6,
        alignment=0  # Left align
    )

    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=11,
        leading=14,
        spaceAfter=6,
        alignment=4  # Justified
    )

    # Build the document
    content = []

    # Title
    title = Paragraph("Evaluation Report", title_style)
    content.append(title)
    content.append(Spacer(1, 0.2 * inch))

    # Split the final_report into sections
    sections = final_report.split('Analysis\n')
    recomend_sections = final_report.split('Recommendations\n')

    if len(sections) > 1:
        remarks_section = sections[0].strip()
        analysis_section = sections[1].split('Recommendations\n')[0].strip()
        recomend_sections = sections[1].split('Recommendations\n')[1].strip() if len(recomend_sections) > 1 else ""
    else:
        remarks_section = final_report
        analysis_section = ""
        recomend_sections = ""

    # Process the remarks section for the table
    remarks_lines = remarks_section.split('\n')
    table_data = []
    headers_added = False
    for line in remarks_lines:
        if 'Task' in line and 'Remarks' in line:
            # Add headers
            headers_added = True
            table_data.append([cell.strip() for cell in line.split('|') if cell.strip()])
            continue

        if headers_added and 'Task' in line or 'Remarks' in line or "----------" in line or "----------------" in line:
            continue  # Skip header lines

        cells = [cell.strip() for cell in line.split('|') if cell.strip()]
        if len(cells) == 2:
            table_data.append(cells)

    # Define table style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ])

    if table_data:
        table = Table(table_data, colWidths=[doc.width/len(table_data[0])] * len(table_data[0]))
        table.setStyle(table_style)
        content.append(table)
        content.append(Spacer(1, 0.2 * inch))

    # Add Analysis section
    if analysis_section:
        analysis_title = Paragraph("Analysis", heading_style)
        content.append(analysis_title)
        content.append(Spacer(1, 0.1 * inch))

        overall_analysis = Paragraph(analysis_section.replace('\n', '<br/>'), body_style)
        content.append(overall_analysis)

    # Add Recommendations section
    if recomend_sections:
        recommendations_title = Paragraph("Recommendations", heading_style)
        content.append(recommendations_title)
        content.append(Spacer(1, 0.1 * inch))

        recommendations = Paragraph(recomend_sections.replace('\n', '<br/>'), body_style)
        content.append(recommendations)

    # Build PDF
    doc.build(content)

    # Return PDF buffer
    buffer.seek(0)
    return buffer.read()

def main():


    # Select semester
    semester = st.selectbox("Select Semester", ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"])

    task =" "
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("AI Developer"):
            with st.spinner('Generating Task...'):
                task = task_manager(semester, "AI")
            st.session_state.task = task
            st.session_state.subject = "AI"
    with col2:
        if st.button("Backend Developer"):
            with st.spinner('Generating Task...'):
                task = task_manager(semester, "Backend")
            st.session_state.task = task
            st.session_state.subject = "Backend"
    with col3:
        if st.button("Frontend Developer"):
            with st.spinner('Generating Task...'):
                task = task_manager(semester, "Frontend")
            st.session_state.task = task
            st.session_state.subject = "Frontend"

    # Task and code input
    if "task" in st.session_state:
        task_title = f"{st.session_state.subject} Task"
        col1, col2 = st.columns([1, 1])
        with col1:
            # st.subheader(task_title)
            task=st.text_area(task_title, value=st.session_state.task, height=300)
        with col2:
            code_input = st.text_area("Enter your code here", height=300)
            if st.button("Evaluate", key="evaluate"):
                with st.spinner('Evaluating...'):
                    evaluation = task_evaluator(semester,task,st.session_state.subject, code_input)
                st.session_state.evaluation = evaluation

    # Evaluation report
    if "evaluation" in st.session_state:
        with st.expander("Evaluation Report", expanded=True):
            st.markdown(st.session_state.evaluation)
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = [Paragraph(st.session_state.evaluation, styles["Normal"])]
            doc.build(story)
            buffer.seek(0)
            # pdf_buffer = pdf_generator(buffer)
            pdf_buffer = pdf_generator(st.session_state.evaluation)
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="evaluation_report.pdf",
                mime="application/pdf"
                )
if __name__ == "__main__":
    main()