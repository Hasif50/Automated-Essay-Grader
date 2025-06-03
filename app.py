"""
Automated Essay Grader - Main Application
From Hasif's Workspace

A comprehensive AI-powered essay grading system built with Streamlit and LangChain.
Author: Hasif50
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# Import custom modules
from essay_analyzer import EssayAnalyzer
from grading_engine import GradingEngine
from feedback_generator import FeedbackGenerator
from utils import load_document, validate_file, generate_report, save_results

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Automated Essay Grader",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    .score-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .feedback-section {
        background-color: #fff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .attribution {
        text-align: center;
        color: #888;
        font-style: italic;
        margin-top: 2rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


def main():
    """Main application function"""

    # Header
    st.markdown(
        '<h1 class="main-header">📝 Automated Essay Grader</h1>', unsafe_allow_html=True
    )
    st.markdown(
        '<p class="sub-header">AI-Powered Essay Analysis and Grading System</p>',
        unsafe_allow_html=True,
    )

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Model selection
        model_provider = st.selectbox(
            "AI Model Provider",
            ["OpenAI", "Azure OpenAI"],
            help="Select the AI model provider for essay analysis",
        )

        if model_provider == "OpenAI":
            model_name = st.selectbox(
                "Model",
                ["gpt-4", "gpt-3.5-turbo"],
                help="Select the specific model to use",
            )
        else:
            model_name = st.selectbox(
                "Azure Model",
                ["gpt-4", "gpt-35-turbo"],
                help="Select the Azure OpenAI model",
            )

        # Grading parameters
        st.subheader("Grading Parameters")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
        max_tokens = st.slider("Max Tokens", 500, 4000, 2000, 100)

        # Rubric selection
        rubric_type = st.selectbox(
            "Grading Rubric",
            ["Standard", "Academic", "Creative Writing", "Argumentative", "Custom"],
            help="Select the grading rubric to use",
        )

        # Analysis options
        st.subheader("Analysis Options")
        enable_grammar = st.checkbox("Grammar Analysis", value=True)
        enable_style = st.checkbox("Style Analysis", value=True)
        enable_plagiarism = st.checkbox("Basic Plagiarism Check", value=False)
        enable_sentiment = st.checkbox("Sentiment Analysis", value=True)

        st.markdown("---")
        st.markdown(
            '<p class="attribution">From Hasif\'s Workspace</p>', unsafe_allow_html=True
        )

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("📄 Upload Essay")

        # File upload
        uploaded_file = st.file_uploader(
            "Choose an essay file",
            type=["txt", "pdf", "docx"],
            help="Upload your essay in TXT, PDF, or DOCX format",
        )

        # Text input as alternative
        st.subheader("Or paste your essay here:")
        essay_text = st.text_area(
            "Essay Content", height=300, placeholder="Paste your essay content here..."
        )

        # Essay prompt/topic (optional)
        essay_prompt = st.text_area(
            "Essay Prompt/Topic (Optional)",
            height=100,
            placeholder="Enter the essay prompt or topic if available...",
        )

    with col2:
        st.header("📊 Quick Stats")

        if uploaded_file or essay_text:
            # Get essay content
            if uploaded_file:
                try:
                    content = load_document(uploaded_file)
                    if validate_file(uploaded_file):
                        st.success("✅ File uploaded successfully!")
                    else:
                        st.error("❌ Invalid file format or size")
                        return
                except Exception as e:
                    st.error(f"❌ Error loading file: {str(e)}")
                    return
            else:
                content = essay_text

            if content:
                # Basic statistics
                word_count = len(content.split())
                char_count = len(content)
                paragraph_count = len([p for p in content.split("\n\n") if p.strip()])

                st.metric("Word Count", word_count)
                st.metric("Character Count", char_count)
                st.metric("Paragraphs", paragraph_count)

                # Estimated reading time
                reading_time = max(1, word_count // 200)
                st.metric("Est. Reading Time", f"{reading_time} min")

    # Analysis button
    if st.button("🔍 Analyze Essay", type="primary", use_container_width=True):
        if not (uploaded_file or essay_text.strip()):
            st.error("Please upload a file or paste essay content to analyze.")
            return

        # Get essay content
        if uploaded_file:
            content = load_document(uploaded_file)
        else:
            content = essay_text

        if not content.strip():
            st.error("The essay content appears to be empty.")
            return

        # Initialize components
        with st.spinner("Initializing AI models..."):
            try:
                analyzer = EssayAnalyzer(
                    model_provider=model_provider.lower().replace(" ", "_"),
                    model_name=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                grading_engine = GradingEngine(
                    rubric_type=rubric_type.lower(), analyzer=analyzer
                )

                feedback_generator = FeedbackGenerator(analyzer=analyzer)

            except Exception as e:
                st.error(f"Error initializing AI models: {str(e)}")
                return

        # Perform analysis
        with st.spinner("Analyzing essay..."):
            try:
                # Basic analysis
                analysis_results = analyzer.analyze_essay(
                    content,
                    prompt=essay_prompt,
                    enable_grammar=enable_grammar,
                    enable_style=enable_style,
                    enable_plagiarism=enable_plagiarism,
                    enable_sentiment=enable_sentiment,
                )

                # Grading
                grade_results = grading_engine.grade_essay(
                    content, analysis_results, prompt=essay_prompt
                )

                # Feedback generation
                feedback = feedback_generator.generate_feedback(
                    content, analysis_results, grade_results, prompt=essay_prompt
                )

            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                return

        # Display results
        st.header("📊 Analysis Results")

        # Overall score
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
            <div class="score-card">
                <h3>Overall Score</h3>
                <h2 style="color: #1f77b4;">{grade_results.get("overall_score", 0)}/100</h2>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
            <div class="score-card">
                <h3>Grade</h3>
                <h2 style="color: #1f77b4;">{grade_results.get("letter_grade", "N/A")}</h2>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
            <div class="score-card">
                <h3>Content Quality</h3>
                <h2 style="color: #1f77b4;">{grade_results.get("content_score", 0)}/25</h2>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                f"""
            <div class="score-card">
                <h3>Grammar</h3>
                <h2 style="color: #1f77b4;">{grade_results.get("grammar_score", 0)}/25</h2>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Detailed scores
        st.subheader("📈 Detailed Breakdown")

        score_data = {
            "Criteria": [
                "Content & Ideas",
                "Organization",
                "Grammar & Mechanics",
                "Style & Voice",
            ],
            "Score": [
                grade_results.get("content_score", 0),
                grade_results.get("organization_score", 0),
                grade_results.get("grammar_score", 0),
                grade_results.get("style_score", 0),
            ],
            "Max Score": [25, 25, 25, 25],
        }

        df_scores = pd.DataFrame(score_data)
        st.dataframe(df_scores, use_container_width=True)

        # Feedback sections
        st.subheader("💬 Detailed Feedback")

        # Strengths
        with st.expander("✅ Strengths", expanded=True):
            st.markdown(
                f"""
            <div class="feedback-section">
                {feedback.get("strengths", "No specific strengths identified.")}
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Areas for improvement
        with st.expander("🔧 Areas for Improvement", expanded=True):
            st.markdown(
                f"""
            <div class="feedback-section">
                {feedback.get("improvements", "No specific improvements suggested.")}
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Specific suggestions
        with st.expander("💡 Specific Suggestions", expanded=True):
            st.markdown(
                f"""
            <div class="feedback-section">
                {feedback.get("suggestions", "No specific suggestions available.")}
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Grammar and style issues
        if enable_grammar and analysis_results.get("grammar_issues"):
            with st.expander("📝 Grammar & Style Issues"):
                for issue in analysis_results["grammar_issues"]:
                    st.warning(
                        f"**{issue.get('type', 'Issue')}**: {issue.get('description', 'No description')}"
                    )

        # Save results
        st.subheader("💾 Save Results")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📄 Generate PDF Report"):
                try:
                    pdf_path = generate_report(
                        content, analysis_results, grade_results, feedback, format="pdf"
                    )
                    st.success(f"PDF report generated: {pdf_path}")
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")

        with col2:
            if st.button("📊 Export to CSV"):
                try:
                    csv_path = save_results(
                        analysis_results, grade_results, feedback, format="csv"
                    )
                    st.success(f"Results exported: {csv_path}")
                except Exception as e:
                    st.error(f"Error exporting CSV: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        '<p class="attribution">Built with ❤️ from Hasif\'s Workspace | '
        "Powered by AI for Educational Excellence</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
