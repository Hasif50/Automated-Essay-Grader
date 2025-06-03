# Automated Essay Grader

## Overview

The Automated Essay Grader is a Python-based application designed to automate the process of analyzing and grading essays using advanced AI technologies. It leverages cutting-edge technologies such as OpenAI's GPT models, LangChain, and Azure's AI services to process and evaluate essays efficiently.

## Features

- **AI-Powered Essay Analysis** - Comprehensive evaluation of essay content, structure, and quality
- **Multi-Criteria Grading** - Assessment across multiple dimensions including grammar, coherence, argument strength, and creativity
- **Real-time Feedback** - Instant detailed feedback with suggestions for improvement
- **Rubric-Based Scoring** - Customizable grading rubrics for different essay types
- **Plagiarism Detection** - Basic similarity checking against common sources
- **Export Capabilities** - Generate detailed reports in PDF and CSV formats

## Future Features

- Integration with Learning Management Systems (LMS)
- Advanced plagiarism detection with external databases
- Multi-language support for essay grading
- Batch processing for multiple essays
- Teacher dashboard for class-wide analytics
- Student progress tracking over time

## Setup Instructions

**Clone the Repository**:
```bash
git clone https://github.com/Hasif50/Automated-Essay-Grader.git
cd Automated-Essay-Grader
```

**Install Dependencies**:
```bash
pip install -r requirements.txt
```

**Set Up Environment Variables**:
Copy `.env.sample` to `.env` and fill in your API keys:
```bash
cp .env.sample .env
```

Edit the `.env` file with your API credentials:
```
OPENAI_API_KEY=your_openai_api_key_here
AZURE_API_KEY=your_azure_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
```

**Run the Application**:
```bash
streamlit run app.py
```

## How to Contribute

We welcome contributions from the community! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## Project Structure

```
automated-essay-grader/
│
├── .env.sample
├── .gitignore
├── .env
├── app.py
├── requirements.txt
├── README.md
├── CONTRIBUTING.md
├── LICENSE
│
├── src/
│   ├── __init__.py
│   ├── essay_analyzer.py
│   ├── grading_engine.py
│   ├── feedback_generator.py
│   └── utils.py
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── prompts.py
│
├── data/
│   ├── sample_essays/
│   ├── rubrics/
│   └── outputs/
│
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_grading.py
│   └── test_utils.py
│
└── docs/
    ├── user_guide.md
    ├── api_reference.md
    └── deployment_guide.md
```

## Code Flow

**Environment and Configuration Files**:
- `.env` - Contains API keys and configuration settings
- `.env.sample` - Template for environment variables
- `.gitignore` - Specifies files to ignore in version control

**Python Scripts**:
- `app.py` - Main Streamlit application entry point
- `src/essay_analyzer.py` - Core essay analysis functionality
- `src/grading_engine.py` - Grading logic and scoring algorithms
- `src/feedback_generator.py` - AI-powered feedback generation
- `config/prompts.py` - LLM prompt templates for different grading criteria

**Data Handling**:
- `data/` - Contains sample essays, grading rubrics, and output files
- Essay parsing and text extraction from various formats (PDF, DOCX, TXT)

**Essay Grading Process**:
- Upload essay through Streamlit interface
- Text extraction and preprocessing
- Multi-criteria analysis using AI models
- Score calculation based on rubric
- Detailed feedback generation
- Report generation and export

**Dependencies**:
- `requirements.txt` - All required Python packages

**Documentation**:
- `README.md` - Project overview and setup instructions
- `docs/` - Comprehensive documentation for users and developers

## Key Components

### **`app.py`**:
Main Streamlit application that provides the user interface for uploading essays and displaying results.

### **`src/essay_analyzer.py`**:
Core analysis engine that processes essays and extracts key features for grading.

### **`src/grading_engine.py`**:
Implements the grading logic using AI models to evaluate essays across multiple criteria.

### **`src/feedback_generator.py`**:
Generates detailed, constructive feedback to help students improve their writing.

### **`config/prompts.py`**:
Contains all prompt templates used for different aspects of essay evaluation.

## Technology Stack

- **Language**: Python 3.10+
- **Framework**: Streamlit for web interface
- **AI Models**: OpenAI GPT-4, Azure AI services
- **Libraries**: LangChain, pandas, numpy, nltk
- **Cloud**: Azure for deployment and scaling

## About

Real-world Problem Solved: Assists educators in providing consistent, unbiased grading with actionable feedback for students.
The Automated Essay Grader project is designed to assist educators and students by providing consistent, detailed, and constructive feedback on written work. This tool aims to enhance the learning experience through AI-powered analysis.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 

## Acknowledgments

- Built with modern AI technologies for educational enhancement
- Designed to support both educators and students
