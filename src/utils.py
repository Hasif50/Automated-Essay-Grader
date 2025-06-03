"""
Utilities Module
From Hasif's Workspace

Utility functions for document processing, file handling, and report generation.
Author: Hasif50
"""

import os
import io
import json
import csv
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import streamlit as st

# Document processing imports
try:
    import PyPDF2
    import pdfplumber
    from docx import Document

    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    st.warning(
        "PDF processing libraries not available. Install PyPDF2 and pdfplumber for full functionality."
    )

# Report generation imports
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def load_document(uploaded_file) -> str:
    """
    Load and extract text from uploaded document.

    Args:
        uploaded_file: Streamlit uploaded file object

    Returns:
        Extracted text content

    Raises:
        Exception: If file cannot be processed
    """
    try:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension == "txt":
            return _load_text_file(uploaded_file)
        elif file_extension == "pdf":
            return _load_pdf_file(uploaded_file)
        elif file_extension in ["docx", "doc"]:
            return _load_docx_file(uploaded_file)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    except Exception as e:
        raise Exception(f"Error loading document: {str(e)}")


def _load_text_file(uploaded_file) -> str:
    """Load text from TXT file."""
    try:
        # Try UTF-8 first
        content = uploaded_file.read().decode("utf-8")
        return content
    except UnicodeDecodeError:
        # Fallback to other encodings
        uploaded_file.seek(0)
        try:
            content = uploaded_file.read().decode("latin-1")
            return content
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            content = uploaded_file.read().decode("cp1252")
            return content


def _load_pdf_file(uploaded_file) -> str:
    """Load text from PDF file."""
    if not PDF_AVAILABLE:
        raise Exception(
            "PDF processing libraries not installed. Please install PyPDF2 and pdfplumber."
        )

    text_content = ""

    try:
        # Try with pdfplumber first (better text extraction)
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
    except Exception:
        # Fallback to PyPDF2
        try:
            uploaded_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Could not extract text from PDF: {str(e)}")

    if not text_content.strip():
        raise Exception("No text could be extracted from the PDF file.")

    return text_content


def _load_docx_file(uploaded_file) -> str:
    """Load text from DOCX file."""
    if not PDF_AVAILABLE:
        raise Exception(
            "Document processing libraries not installed. Please install python-docx."
        )

    try:
        doc = Document(uploaded_file)
        text_content = ""

        for paragraph in doc.paragraphs:
            text_content += paragraph.text + "\n"

        if not text_content.strip():
            raise Exception("No text could be extracted from the document.")

        return text_content

    except Exception as e:
        raise Exception(f"Could not extract text from DOCX file: {str(e)}")


def validate_file(uploaded_file) -> bool:
    """
    Validate uploaded file for size and format.

    Args:
        uploaded_file: Streamlit uploaded file object

    Returns:
        True if file is valid, False otherwise
    """
    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB in bytes
    if uploaded_file.size > max_size:
        st.error(
            f"File size ({uploaded_file.size / 1024 / 1024:.1f}MB) exceeds maximum allowed size (10MB)."
        )
        return False

    # Check file extension
    allowed_extensions = ["txt", "pdf", "docx", "doc"]
    file_extension = uploaded_file.name.split(".")[-1].lower()

    if file_extension not in allowed_extensions:
        st.error(
            f"File format '{file_extension}' is not supported. Allowed formats: {', '.join(allowed_extensions)}"
        )
        return False

    return True


def save_results(
    analysis_results: Dict[str, Any],
    grade_results: Dict[str, Any],
    feedback: Dict[str, str],
    format: str = "json",
    filename: Optional[str] = None,
) -> str:
    """
    Save analysis results to file.

    Args:
        analysis_results: Essay analysis results
        grade_results: Grading results
        feedback: Generated feedback
        format: Output format ('json', 'csv')
        filename: Optional custom filename

    Returns:
        Path to saved file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not filename:
        filename = f"essay_analysis_{timestamp}"

    # Ensure output directory exists
    output_dir = Path("data/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    if format.lower() == "json":
        return _save_json_results(
            analysis_results, grade_results, feedback, output_dir, filename
        )
    elif format.lower() == "csv":
        return _save_csv_results(
            analysis_results, grade_results, feedback, output_dir, filename
        )
    else:
        raise ValueError(f"Unsupported format: {format}")


def _save_json_results(
    analysis_results: Dict[str, Any],
    grade_results: Dict[str, Any],
    feedback: Dict[str, str],
    output_dir: Path,
    filename: str,
) -> str:
    """Save results as JSON file."""
    filepath = output_dir / f"{filename}.json"

    combined_results = {
        "timestamp": datetime.now().isoformat(),
        "analysis_results": analysis_results,
        "grade_results": grade_results,
        "feedback": feedback,
        "workspace_attribution": "From Hasif's Workspace",
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(combined_results, f, indent=2, ensure_ascii=False)

    return str(filepath)


def _save_csv_results(
    analysis_results: Dict[str, Any],
    grade_results: Dict[str, Any],
    feedback: Dict[str, str],
    output_dir: Path,
    filename: str,
) -> str:
    """Save results as CSV file."""
    filepath = output_dir / f"{filename}.csv"

    # Flatten the results for CSV format
    flattened_data = []

    # Basic statistics
    basic_stats = analysis_results.get("basic_stats", {})
    for key, value in basic_stats.items():
        flattened_data.append(
            {"Category": "Basic Statistics", "Metric": key, "Value": value}
        )

    # Readability scores
    readability = analysis_results.get("readability", {})
    for key, value in readability.items():
        flattened_data.append(
            {"Category": "Readability", "Metric": key, "Value": value}
        )

    # Grade results
    for key, value in grade_results.items():
        if key not in ["detailed_feedback", "grading_breakdown"]:
            flattened_data.append({"Category": "Grades", "Metric": key, "Value": value})

    # Create DataFrame and save
    df = pd.DataFrame(flattened_data)
    df.to_csv(filepath, index=False, encoding="utf-8")

    return str(filepath)


def generate_report(
    essay_text: str,
    analysis_results: Dict[str, Any],
    grade_results: Dict[str, Any],
    feedback: Dict[str, str],
    format: str = "pdf",
    filename: Optional[str] = None,
) -> str:
    """
    Generate a comprehensive report.

    Args:
        essay_text: Original essay text
        analysis_results: Analysis results
        grade_results: Grading results
        feedback: Generated feedback
        format: Report format ('pdf', 'html')
        filename: Optional custom filename

    Returns:
        Path to generated report
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if not filename:
        filename = f"essay_report_{timestamp}"

    # Ensure output directory exists
    output_dir = Path("data/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    if format.lower() == "pdf":
        return _generate_pdf_report(
            essay_text, analysis_results, grade_results, feedback, output_dir, filename
        )
    elif format.lower() == "html":
        return _generate_html_report(
            essay_text, analysis_results, grade_results, feedback, output_dir, filename
        )
    else:
        raise ValueError(f"Unsupported report format: {format}")


def _generate_pdf_report(
    essay_text: str,
    analysis_results: Dict[str, Any],
    grade_results: Dict[str, Any],
    feedback: Dict[str, str],
    output_dir: Path,
    filename: str,
) -> str:
    """Generate PDF report."""
    if not REPORTLAB_AVAILABLE:
        raise Exception("ReportLab not installed. Cannot generate PDF reports.")

    filepath = output_dir / f"{filename}.pdf"

    # Create PDF document
    doc = SimpleDocTemplate(str(filepath), pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center alignment
    )
    story.append(Paragraph("Essay Analysis Report", title_style))
    story.append(Paragraph("From Hasif's Workspace", styles["Normal"]))
    story.append(Spacer(1, 20))

    # Timestamp
    story.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"],
        )
    )
    story.append(Spacer(1, 20))

    # Overall Grade
    story.append(Paragraph("Overall Assessment", styles["Heading2"]))
    overall_score = grade_results.get("overall_score", 0)
    letter_grade = grade_results.get("letter_grade", "N/A")
    story.append(
        Paragraph(
            f"Score: {overall_score}/100 (Grade: {letter_grade})", styles["Normal"]
        )
    )
    story.append(Spacer(1, 15))

    # Detailed Scores
    story.append(Paragraph("Detailed Scores", styles["Heading2"]))

    # Create scores table
    score_data = [["Criterion", "Score", "Max Score", "Percentage"]]
    criteria_scores = grade_results.get("criteria_scores", {})
    grading_breakdown = grade_results.get("grading_breakdown", {})

    for criterion_key, score in criteria_scores.items():
        breakdown = grading_breakdown.get(criterion_key, {})
        criterion_name = breakdown.get("name", criterion_key.title())
        max_score = breakdown.get("max_score", 25)
        percentage = breakdown.get("percentage", 0)

        score_data.append(
            [criterion_name, f"{score:.1f}", str(max_score), f"{percentage:.1f}%"]
        )

    score_table = Table(score_data)
    score_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    story.append(score_table)
    story.append(Spacer(1, 20))

    # Basic Statistics
    story.append(Paragraph("Essay Statistics", styles["Heading2"]))
    basic_stats = analysis_results.get("basic_stats", {})

    stats_data = [["Metric", "Value"]]
    stats_data.append(["Word Count", str(basic_stats.get("word_count", 0))])
    stats_data.append(["Sentence Count", str(basic_stats.get("sentence_count", 0))])
    stats_data.append(["Paragraph Count", str(basic_stats.get("paragraph_count", 0))])
    stats_data.append(
        [
            "Avg Words per Sentence",
            f"{basic_stats.get('avg_words_per_sentence', 0):.1f}",
        ]
    )

    stats_table = Table(stats_data)
    stats_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    story.append(stats_table)
    story.append(Spacer(1, 20))

    # Feedback sections
    story.append(Paragraph("Feedback", styles["Heading2"]))

    # Strengths
    story.append(Paragraph("Strengths", styles["Heading3"]))
    strengths = feedback.get("strengths", "No specific strengths identified.")
    story.append(Paragraph(strengths, styles["Normal"]))
    story.append(Spacer(1, 15))

    # Areas for Improvement
    story.append(Paragraph("Areas for Improvement", styles["Heading3"]))
    improvements = feedback.get("improvements", "No specific improvements suggested.")
    story.append(Paragraph(improvements, styles["Normal"]))
    story.append(Spacer(1, 15))

    # Suggestions
    story.append(Paragraph("Specific Suggestions", styles["Heading3"]))
    suggestions = feedback.get("suggestions", "No specific suggestions available.")
    story.append(Paragraph(suggestions, styles["Normal"]))
    story.append(Spacer(1, 20))

    # Footer
    story.append(
        Paragraph(
            "Generated by Automated Essay Grader - From Hasif's Workspace",
            styles["Normal"],
        )
    )

    # Build PDF
    doc.build(story)

    return str(filepath)


def _generate_html_report(
    essay_text: str,
    analysis_results: Dict[str, Any],
    grade_results: Dict[str, Any],
    feedback: Dict[str, str],
    output_dir: Path,
    filename: str,
) -> str:
    """Generate HTML report."""
    filepath = output_dir / f"{filename}.html"

    # HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Essay Analysis Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
            }}
            .header {{
                text-align: center;
                border-bottom: 2px solid #333;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .score-card {{
                background-color: #f0f2f6;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                border-left: 5px solid #1f77b4;
            }}
            .feedback-section {{
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin: 20px 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .attribution {{
                text-align: center;
                color: #888;
                font-style: italic;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Essay Analysis Report</h1>
            <p>From Hasif's Workspace</p>
            <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="score-card">
            <h2>Overall Assessment</h2>
            <p><strong>Score:</strong> {grade_results.get("overall_score", 0)}/100</p>
            <p><strong>Grade:</strong> {grade_results.get("letter_grade", "N/A")}</p>
        </div>
        
        <h2>Detailed Scores</h2>
        <table>
            <tr>
                <th>Criterion</th>
                <th>Score</th>
                <th>Max Score</th>
                <th>Percentage</th>
            </tr>
    """

    # Add score rows
    criteria_scores = grade_results.get("criteria_scores", {})
    grading_breakdown = grade_results.get("grading_breakdown", {})

    for criterion_key, score in criteria_scores.items():
        breakdown = grading_breakdown.get(criterion_key, {})
        criterion_name = breakdown.get("name", criterion_key.title())
        max_score = breakdown.get("max_score", 25)
        percentage = breakdown.get("percentage", 0)

        html_content += f"""
            <tr>
                <td>{criterion_name}</td>
                <td>{score:.1f}</td>
                <td>{max_score}</td>
                <td>{percentage:.1f}%</td>
            </tr>
        """

    html_content += """
        </table>
        
        <h2>Essay Statistics</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
            </tr>
    """

    # Add statistics rows
    basic_stats = analysis_results.get("basic_stats", {})
    stats_items = [
        ("Word Count", basic_stats.get("word_count", 0)),
        ("Sentence Count", basic_stats.get("sentence_count", 0)),
        ("Paragraph Count", basic_stats.get("paragraph_count", 0)),
        (
            "Avg Words per Sentence",
            f"{basic_stats.get('avg_words_per_sentence', 0):.1f}",
        ),
    ]

    for metric, value in stats_items:
        html_content += f"""
            <tr>
                <td>{metric}</td>
                <td>{value}</td>
            </tr>
        """

    html_content += f"""
        </table>
        
        <h2>Feedback</h2>
        
        <div class="feedback-section">
            <h3>Strengths</h3>
            <p>{feedback.get("strengths", "No specific strengths identified.")}</p>
        </div>
        
        <div class="feedback-section">
            <h3>Areas for Improvement</h3>
            <p>{feedback.get("improvements", "No specific improvements suggested.")}</p>
        </div>
        
        <div class="feedback-section">
            <h3>Specific Suggestions</h3>
            <p>{feedback.get("suggestions", "No specific suggestions available.")}</p>
        </div>
        
        <div class="attribution">
            <p>Generated by Automated Essay Grader - From Hasif's Workspace</p>
        </div>
    </body>
    </html>
    """

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    return str(filepath)


def format_score_display(score: float, max_score: float = 100) -> str:
    """
    Format score for display.

    Args:
        score: The score value
        max_score: Maximum possible score

    Returns:
        Formatted score string
    """
    percentage = (score / max_score) * 100 if max_score > 0 else 0
    return f"{score:.1f}/{max_score} ({percentage:.1f}%)"


def get_performance_color(percentage: float) -> str:
    """
    Get color code based on performance percentage.

    Args:
        percentage: Performance percentage (0-100)

    Returns:
        Color code for display
    """
    if percentage >= 90:
        return "#28a745"  # Green
    elif percentage >= 80:
        return "#17a2b8"  # Blue
    elif percentage >= 70:
        return "#ffc107"  # Yellow
    elif percentage >= 60:
        return "#fd7e14"  # Orange
    else:
        return "#dc3545"  # Red


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def clean_text_for_analysis(text: str) -> str:
    """
    Clean text for analysis by removing extra whitespace and formatting.

    Args:
        text: Raw text input

    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = " ".join(text.split())

    # Remove multiple newlines
    text = "\n".join(line.strip() for line in text.split("\n") if line.strip())

    return text


def get_workspace_info() -> Dict[str, str]:
    """
    Get workspace attribution information.

    Returns:
        Dictionary with workspace information
    """
    return {
        "workspace": "Hasif's Workspace",
        "author": "Hasif50",
        "version": "1.0.0",
        "description": "AI-Powered Essay Grading System",
    }
