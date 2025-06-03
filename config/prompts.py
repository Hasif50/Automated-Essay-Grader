"""
Prompts Configuration
From Hasif's Workspace

AI prompt templates for essay analysis and grading.
Author: Hasif50
"""

from typing import Dict, Any


class PromptTemplates:
    """
    Collection of prompt templates for different analysis tasks.
    From Hasif's Workspace - Optimized for educational excellence.
    """

    # Base system prompts
    BASE_SYSTEM_PROMPT = """You are an expert writing instructor and essay evaluator with extensive experience in academic assessment. You provide constructive, detailed, and educational feedback that helps students improve their writing skills.

Your analysis should be:
- Objective and fair
- Constructive and encouraging
- Specific with concrete examples
- Educational and actionable
- Appropriate for the student's level

From Hasif's Workspace - Educational Excellence Through AI."""

    # Content analysis prompts
    CONTENT_ANALYSIS_PROMPT = """Analyze the following essay for content quality, depth of ideas, and relevance to the topic.

Evaluate:
1. Clarity and strength of main ideas
2. Depth of analysis and critical thinking
3. Relevance to the topic/prompt
4. Use of evidence and examples
5. Logical development of arguments

Essay to analyze:
{essay_text}

{prompt_context}

Provide detailed feedback on content quality and suggest specific improvements."""

    THESIS_ANALYSIS_PROMPT = """Evaluate the thesis statement and argument development in this essay.

Look for:
1. Clear, specific thesis statement
2. Argument structure and logic
3. Supporting evidence quality
4. Counterargument acknowledgment
5. Conclusion effectiveness

Essay:
{essay_text}

{prompt_context}

Assess the strength of the thesis and overall argument structure."""

    # Organization analysis prompts
    ORGANIZATION_ANALYSIS_PROMPT = """Analyze the organizational structure and flow of this essay.

Examine:
1. Introduction effectiveness
2. Paragraph structure and unity
3. Transition usage and flow
4. Logical sequence of ideas
5. Conclusion strength

Essay:
{essay_text}

Evaluate the organizational structure and suggest improvements for better flow and coherence."""

    # Style and voice analysis prompts
    STYLE_ANALYSIS_PROMPT = """Evaluate the writing style, voice, and language use in this essay.

Consider:
1. Clarity and conciseness
2. Sentence variety and structure
3. Word choice and vocabulary
4. Tone appropriateness
5. Voice consistency

Essay:
{essay_text}

{prompt_context}

Analyze the writing style and provide suggestions for enhancement."""

    # Grammar and mechanics prompts
    GRAMMAR_ANALYSIS_PROMPT = """Review this essay for grammar, mechanics, and technical writing issues.

Check for:
1. Grammar accuracy
2. Punctuation and capitalization
3. Sentence structure problems
4. Spelling errors
5. Usage issues

Essay:
{essay_text}

Identify specific grammar and mechanical issues with suggestions for correction."""

    # Comprehensive feedback prompts
    COMPREHENSIVE_FEEDBACK_PROMPT = """Provide comprehensive feedback on this essay covering all major aspects of writing quality.

The essay received the following scores:
{score_summary}

Analyze:
1. Overall strengths and accomplishments
2. Specific areas needing improvement
3. Concrete suggestions for enhancement
4. Next steps for the writer

Essay:
{essay_text}

{prompt_context}

Provide balanced, constructive feedback that acknowledges strengths while offering specific guidance for improvement."""

    # Rubric-specific prompts
    STANDARD_RUBRIC_PROMPT = """Evaluate this essay using a standard academic writing rubric focusing on:

1. Content & Ideas (35%): Quality of ideas, depth of analysis, relevance
2. Organization & Structure (25%): Logical flow, paragraph structure, transitions
3. Grammar & Mechanics (20%): Grammar, spelling, punctuation, sentence structure
4. Style & Voice (20%): Word choice, sentence variety, clarity, tone

Essay:
{essay_text}

{prompt_context}

Provide scores and detailed feedback for each criterion."""

    ACADEMIC_RUBRIC_PROMPT = """Assess this academic essay focusing on scholarly writing criteria:

1. Thesis & Argument (30%): Clear thesis, argument development, logical reasoning
2. Evidence & Support (25%): Quality of evidence, source integration, examples
3. Critical Analysis (25%): Depth of analysis, critical thinking, interpretation
4. Writing Mechanics (20%): Grammar, style, academic conventions

Essay:
{essay_text}

{prompt_context}

Evaluate using academic writing standards and provide scholarly feedback."""

    CREATIVE_WRITING_PROMPT = """Evaluate this creative writing piece focusing on artistic and narrative elements:

1. Creativity & Originality (30%): Original ideas, creative expression, imagination
2. Narrative Structure (25%): Plot development, character development, pacing
3. Language & Style (25%): Descriptive language, literary devices, voice
4. Technical Skills (20%): Grammar, spelling, writing conventions

Creative piece:
{essay_text}

{prompt_context}

Assess the creative and artistic merits while providing constructive feedback."""

    ARGUMENTATIVE_RUBRIC_PROMPT = """Analyze this argumentative essay for persuasive writing effectiveness:

1. Claim & Position (25%): Clear claim, position strength, stance clarity
2. Reasoning & Logic (30%): Logical reasoning, argument development, coherence
3. Evidence & Sources (25%): Quality of evidence, source credibility, integration
4. Counterargument (20%): Acknowledgment of opposing views, refutation strength

Argumentative essay:
{essay_text}

{prompt_context}

Evaluate the persuasive effectiveness and logical strength of the argument."""

    @classmethod
    def get_prompt(cls, prompt_type: str, **kwargs) -> str:
        """Get a formatted prompt template."""
        prompt_map = {
            "content_analysis": cls.CONTENT_ANALYSIS_PROMPT,
            "thesis_analysis": cls.THESIS_ANALYSIS_PROMPT,
            "organization_analysis": cls.ORGANIZATION_ANALYSIS_PROMPT,
            "style_analysis": cls.STYLE_ANALYSIS_PROMPT,
            "grammar_analysis": cls.GRAMMAR_ANALYSIS_PROMPT,
            "comprehensive_feedback": cls.COMPREHENSIVE_FEEDBACK_PROMPT,
            "standard_rubric": cls.STANDARD_RUBRIC_PROMPT,
            "academic_rubric": cls.ACADEMIC_RUBRIC_PROMPT,
            "creative_writing": cls.CREATIVE_WRITING_PROMPT,
            "argumentative_rubric": cls.ARGUMENTATIVE_RUBRIC_PROMPT,
        }

        template = prompt_map.get(prompt_type, cls.COMPREHENSIVE_FEEDBACK_PROMPT)
        return template.format(**kwargs)

    @classmethod
    def format_prompt_context(cls, prompt: str = None) -> str:
        """Format the prompt context section."""
        if prompt:
            return f"Essay prompt/topic: {prompt}"
        return "No specific prompt provided."

    @classmethod
    def format_score_summary(cls, scores: Dict[str, Any]) -> str:
        """Format score summary for feedback prompts."""
        summary_parts = []

        overall_score = scores.get("overall_score", 0)
        letter_grade = scores.get("letter_grade", "N/A")
        summary_parts.append(
            f"Overall Score: {overall_score}/100 (Grade: {letter_grade})"
        )

        criteria_scores = scores.get("criteria_scores", {})
        if criteria_scores:
            summary_parts.append("Criterion Scores:")
            for criterion, score in criteria_scores.items():
                summary_parts.append(f"- {criterion.title()}: {score}/25")

        return "\n".join(summary_parts)


# Create global instance
prompt_templates = PromptTemplates()
