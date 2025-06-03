"""
Feedback Generator Module
From Hasif's Workspace

AI-powered feedback generation for comprehensive essay evaluation.
Author: Hasif50
"""

from typing import Dict, List, Optional, Any
from langchain_core.messages import HumanMessage, SystemMessage
import json


class FeedbackGenerator:
    """
    Generates detailed, constructive feedback for essays using AI.
    From Hasif's Workspace - Built for educational excellence.
    """

    def __init__(self, analyzer=None):
        """
        Initialize the feedback generator.

        Args:
            analyzer: EssayAnalyzer instance for AI capabilities
        """
        self.analyzer = analyzer

    def generate_feedback(
        self,
        essay_text: str,
        analysis_results: Dict[str, Any],
        grade_results: Dict[str, Any],
        prompt: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Generate comprehensive feedback for an essay.

        Args:
            essay_text: The essay content
            analysis_results: Results from essay analysis
            grade_results: Results from grading
            prompt: Optional essay prompt

        Returns:
            Dictionary containing different types of feedback
        """
        feedback = {}

        # Generate AI-powered feedback
        if self.analyzer:
            feedback.update(
                self._generate_ai_feedback(
                    essay_text, analysis_results, grade_results, prompt
                )
            )

        # Generate specific feedback sections
        feedback["strengths"] = self._identify_strengths(
            analysis_results, grade_results
        )
        feedback["improvements"] = self._identify_improvements(
            analysis_results, grade_results
        )
        feedback["suggestions"] = self._generate_suggestions(
            analysis_results, grade_results
        )
        feedback["grammar_feedback"] = self._generate_grammar_feedback(analysis_results)
        feedback["style_feedback"] = self._generate_style_feedback(analysis_results)
        feedback["structure_feedback"] = self._generate_structure_feedback(
            analysis_results
        )

        # Add workspace attribution
        feedback["workspace_attribution"] = "From Hasif's Workspace"

        return feedback

    def _generate_ai_feedback(
        self,
        essay_text: str,
        analysis_results: Dict[str, Any],
        grade_results: Dict[str, Any],
        prompt: Optional[str] = None,
    ) -> Dict[str, str]:
        """Generate AI-powered comprehensive feedback."""
        try:
            # Prepare context for AI
            overall_score = grade_results.get("overall_score", 0)
            letter_grade = grade_results.get("letter_grade", "N/A")
            word_count = analysis_results.get("basic_stats", {}).get("word_count", 0)

            # Create detailed prompt for feedback generation
            system_message = f"""You are an expert writing instructor providing detailed, constructive feedback on student essays. 

The essay received an overall score of {overall_score}/100 (Grade: {letter_grade}) and contains {word_count} words.

Your feedback should be:
1. Constructive and encouraging
2. Specific with concrete examples
3. Actionable with clear improvement steps
4. Balanced between strengths and areas for growth
5. Appropriate for the student's level

Provide feedback in these categories:
- Overall Assessment
- Content Strengths
- Areas for Improvement
- Specific Recommendations

From Hasif's Workspace - Educational Excellence Through AI."""

            user_message = f"Essay to provide feedback on:\n\n{essay_text}"

            if prompt:
                user_message = f"Essay prompt: {prompt}\n\n{user_message}"

            messages = [
                SystemMessage(content=system_message),
                HumanMessage(content=user_message),
            ]

            response = self.analyzer.llm(messages)

            # Parse the response into sections
            feedback_text = response.content

            return {
                "ai_comprehensive_feedback": feedback_text,
                "ai_provider": f"{self.analyzer.model_provider}_{self.analyzer.model_name}",
            }

        except Exception as e:
            return {
                "ai_comprehensive_feedback": f"Error generating AI feedback: {str(e)}",
                "ai_provider": "error",
            }

    def _identify_strengths(
        self, analysis_results: Dict[str, Any], grade_results: Dict[str, Any]
    ) -> str:
        """Identify and describe essay strengths."""
        strengths = []

        # Check basic statistics
        basic_stats = analysis_results.get("basic_stats", {})
        word_count = basic_stats.get("word_count", 0)

        if word_count >= 500:
            strengths.append(
                "**Adequate Length**: Your essay meets the expected word count, demonstrating thorough development of ideas."
            )
        elif word_count >= 300:
            strengths.append(
                "**Good Length**: Your essay has a solid word count that allows for meaningful discussion of the topic."
            )

        # Check vocabulary
        vocab_data = analysis_results.get("vocabulary", {})
        lexical_diversity = vocab_data.get("lexical_diversity", 0)
        complex_word_ratio = vocab_data.get("complex_word_ratio", 0)

        if lexical_diversity > 0.6:
            strengths.append(
                "**Rich Vocabulary**: You demonstrate excellent vocabulary diversity, using varied and sophisticated word choices."
            )
        elif lexical_diversity > 0.4:
            strengths.append(
                "**Good Vocabulary**: Your vocabulary shows good variety and appropriate word selection."
            )

        if complex_word_ratio > 0.15:
            strengths.append(
                "**Academic Language**: You effectively use complex vocabulary that enhances the sophistication of your writing."
            )

        # Check structure
        structure_data = analysis_results.get("structure", {})

        if structure_data.get("has_clear_introduction", False):
            strengths.append(
                "**Strong Introduction**: Your essay begins with a clear introduction that sets up your topic effectively."
            )

        if structure_data.get("has_clear_conclusion", False):
            strengths.append(
                "**Effective Conclusion**: Your essay ends with a conclusion that brings closure to your discussion."
            )

        transition_count = structure_data.get("transition_word_count", 0)
        if transition_count >= 5:
            strengths.append(
                "**Good Flow**: You use transition words effectively to connect ideas and create smooth flow between paragraphs."
            )

        # Check readability
        readability_data = analysis_results.get("readability", {})
        flesch_score = readability_data.get("flesch_reading_ease", 0)

        if flesch_score > 60:
            strengths.append(
                "**Clear Writing**: Your writing is clear and accessible, making it easy for readers to follow your ideas."
            )

        # Check grammar
        grammar_data = analysis_results.get("grammar", {})
        issue_count = grammar_data.get("issue_count", 0)

        if issue_count <= 2:
            strengths.append(
                "**Strong Mechanics**: Your essay demonstrates excellent grammar and mechanical accuracy."
            )
        elif issue_count <= 5:
            strengths.append(
                "**Good Mechanics**: Your essay shows solid command of grammar and writing conventions."
            )

        # Check style
        style_data = analysis_results.get("style", {})
        variety_score = style_data.get("sentence_variety_score", 0)

        if variety_score > 10:
            strengths.append(
                "**Sentence Variety**: You demonstrate good sentence variety, creating engaging and dynamic prose."
            )

        # Check sentiment for appropriate tone
        sentiment_data = analysis_results.get("sentiment", {})
        if sentiment_data:
            tone = sentiment_data.get("overall_tone", "neutral")
            if tone == "positive":
                strengths.append(
                    "**Positive Tone**: Your writing maintains an engaging and optimistic tone throughout."
                )
            elif tone == "neutral":
                strengths.append(
                    "**Balanced Tone**: Your writing maintains an appropriate and balanced tone for academic discourse."
                )

        if not strengths:
            strengths.append(
                "**Effort and Completion**: You have completed the assignment and demonstrated effort in your writing."
            )

        return "\n\n".join(strengths)

    def _identify_improvements(
        self, analysis_results: Dict[str, Any], grade_results: Dict[str, Any]
    ) -> str:
        """Identify areas for improvement."""
        improvements = []

        # Check word count
        basic_stats = analysis_results.get("basic_stats", {})
        word_count = basic_stats.get("word_count", 0)

        if word_count < 250:
            improvements.append(
                "**Essay Length**: Consider expanding your essay to develop your ideas more fully. Aim for at least 300-500 words to provide adequate depth and detail."
            )

        # Check structure issues
        structure_data = analysis_results.get("structure", {})

        if not structure_data.get("has_clear_introduction", False):
            improvements.append(
                "**Introduction**: Strengthen your introduction by clearly stating your main topic or thesis. A strong opening paragraph should engage the reader and preview your main points."
            )

        if not structure_data.get("has_clear_conclusion", False):
            improvements.append(
                "**Conclusion**: Add a more definitive conclusion that summarizes your main points and provides closure. Avoid simply restating your introduction."
            )

        paragraph_count = structure_data.get("paragraph_count", 0)
        if paragraph_count < 3:
            improvements.append(
                "**Paragraph Structure**: Organize your essay into more distinct paragraphs. Each paragraph should focus on one main idea and include supporting details."
            )

        transition_count = structure_data.get("transition_word_count", 0)
        if transition_count < 2:
            improvements.append(
                "**Transitions**: Use more transition words and phrases to connect your ideas and improve the flow between paragraphs (e.g., 'furthermore,' 'however,' 'in addition')."
            )

        # Check vocabulary
        vocab_data = analysis_results.get("vocabulary", {})
        lexical_diversity = vocab_data.get("lexical_diversity", 0)

        if lexical_diversity < 0.4:
            improvements.append(
                "**Vocabulary Variety**: Expand your vocabulary by using more varied word choices. Avoid repeating the same words frequently and consider using synonyms."
            )

        # Check grammar issues
        grammar_data = analysis_results.get("grammar", {})
        issue_count = grammar_data.get("issue_count", 0)

        if issue_count > 10:
            improvements.append(
                "**Grammar and Mechanics**: Focus on improving grammar, spelling, and punctuation. Consider proofreading more carefully or using grammar-checking tools."
            )
        elif issue_count > 5:
            improvements.append(
                "**Proofreading**: Review your essay for minor grammar and mechanical errors. A final proofread can help catch small mistakes."
            )

        # Check readability
        readability_data = analysis_results.get("readability", {})
        flesch_score = readability_data.get("flesch_reading_ease", 0)

        if flesch_score < 30:
            improvements.append(
                "**Sentence Clarity**: Some sentences may be too complex. Consider breaking down long, complicated sentences into shorter, clearer ones."
            )

        # Check style issues
        style_data = analysis_results.get("style", {})
        starter_variety = style_data.get("sentence_starter_variety", 0)

        if starter_variety < 0.5:
            improvements.append(
                "**Sentence Variety**: Vary how you begin your sentences. Starting too many sentences the same way can make your writing feel repetitive."
            )

        style_issues = style_data.get("style_issues", [])
        if style_issues:
            issue_types = set(issue["type"] for issue in style_issues)
            if "Overused Word" in issue_types:
                improvements.append(
                    "**Word Choice**: Avoid overusing certain words. Look for opportunities to use synonyms and vary your language."
                )
            if "Cliché" in issue_types:
                improvements.append(
                    "**Original Language**: Replace clichéd phrases with more original and specific language that better expresses your ideas."
                )

        # Check overall score for general improvements
        overall_score = grade_results.get("overall_score", 0)

        if overall_score < 70:
            improvements.append(
                "**Overall Development**: Focus on developing your ideas more thoroughly with specific examples, details, and explanations to support your main points."
            )

        if not improvements:
            improvements.append(
                "**Continue Refining**: While your essay shows good effort, continue to refine your writing by focusing on clarity, detail, and precision in your expression."
            )

        return "\n\n".join(improvements)

    def _generate_suggestions(
        self, analysis_results: Dict[str, Any], grade_results: Dict[str, Any]
    ) -> str:
        """Generate specific actionable suggestions."""
        suggestions = []

        # Content development suggestions
        word_count = analysis_results.get("basic_stats", {}).get("word_count", 0)
        if word_count < 400:
            suggestions.append(
                "**Expand with Examples**: Add specific examples, anecdotes, or evidence to support your main points and reach a more substantial word count."
            )

        # Structure suggestions
        structure_data = analysis_results.get("structure", {})
        paragraph_count = structure_data.get("paragraph_count", 0)

        if paragraph_count < 4:
            suggestions.append(
                "**Paragraph Development**: Consider organizing your essay into 4-5 paragraphs: introduction, 2-3 body paragraphs (each with one main idea), and conclusion."
            )

        # Grammar and style suggestions
        grammar_data = analysis_results.get("grammar", {})
        grammar_issues = grammar_data.get("grammar_issues", [])

        if grammar_issues:
            passive_voice_count = sum(
                1 for issue in grammar_issues if issue.get("type") == "Passive Voice"
            )
            if passive_voice_count > 2:
                suggestions.append(
                    "**Active Voice**: Try converting passive voice sentences to active voice for stronger, more direct writing. For example, change 'The ball was thrown by John' to 'John threw the ball.'"
                )

            long_sentence_count = sum(
                1 for issue in grammar_issues if issue.get("type") == "Long Sentence"
            )
            if long_sentence_count > 1:
                suggestions.append(
                    "**Sentence Length**: Break down overly long sentences into shorter, more manageable ones. Aim for an average of 15-20 words per sentence."
                )

        # Vocabulary suggestions
        vocab_data = analysis_results.get("vocabulary", {})
        complex_word_ratio = vocab_data.get("complex_word_ratio", 0)

        if complex_word_ratio < 0.1:
            suggestions.append(
                "**Academic Vocabulary**: Incorporate more sophisticated vocabulary appropriate to your topic. Use a thesaurus to find more precise or academic alternatives to common words."
            )

        # Readability suggestions
        readability_data = analysis_results.get("readability", {})
        flesch_kincaid_grade = readability_data.get("flesch_kincaid_grade", 0)

        if flesch_kincaid_grade > 12:
            suggestions.append(
                "**Simplify Complex Ideas**: While sophisticated vocabulary is good, ensure your ideas are clearly expressed. Consider breaking complex concepts into simpler, more digestible parts."
            )

        # Transition suggestions
        transition_count = structure_data.get("transition_word_count", 0)
        if transition_count < 3:
            suggestions.append(
                "**Add Transitions**: Use transitional phrases to connect your ideas: 'First,' 'Additionally,' 'However,' 'In contrast,' 'Furthermore,' 'Finally,' etc."
            )

        # Evidence and support suggestions
        suggestions.append(
            "**Support with Evidence**: Strengthen your arguments with specific examples, statistics, quotes, or personal experiences that directly relate to your main points."
        )

        # Revision suggestions
        suggestions.append(
            "**Read Aloud**: Read your essay aloud to catch awkward phrasing, run-on sentences, and areas where the flow could be improved."
        )

        suggestions.append(
            "**Peer Review**: Have someone else read your essay and provide feedback on clarity and persuasiveness of your arguments."
        )

        # Final polish suggestions
        suggestions.append(
            "**Final Proofread**: After making content revisions, do a final proofread focusing specifically on grammar, spelling, and punctuation errors."
        )

        return "\n\n".join(suggestions)

    def _generate_grammar_feedback(self, analysis_results: Dict[str, Any]) -> str:
        """Generate specific grammar feedback."""
        grammar_data = analysis_results.get("grammar", {})
        grammar_issues = grammar_data.get("grammar_issues", [])

        if not grammar_issues:
            return "**Excellent Grammar**: Your essay demonstrates strong command of grammar and mechanics with minimal errors."

        feedback_parts = []

        # Group issues by type
        issue_types = {}
        for issue in grammar_issues:
            issue_type = issue.get("type", "General")
            if issue_type not in issue_types:
                issue_types[issue_type] = []
            issue_types[issue_type].append(issue)

        # Provide feedback for each type
        for issue_type, issues in issue_types.items():
            count = len(issues)

            if issue_type == "Long Sentence":
                feedback_parts.append(
                    f"**Long Sentences** ({count} instances): Consider breaking down lengthy sentences for better readability. Aim for 15-25 words per sentence on average."
                )

            elif issue_type == "Short Sentence":
                feedback_parts.append(
                    f"**Short Sentences** ({count} instances): Some sentences are very brief. Consider combining related short sentences or adding more detail."
                )

            elif issue_type == "Passive Voice":
                feedback_parts.append(
                    f"**Passive Voice** ({count} instances): Try using active voice for more direct and engaging writing. Active voice typically makes your writing stronger and clearer."
                )

            elif issue_type == "Sentence Fragment":
                feedback_parts.append(
                    f"**Sentence Fragments** ({count} instances): Ensure all sentences are complete with a subject and predicate. Fragments can confuse readers."
                )

            else:
                feedback_parts.append(
                    f"**{issue_type}** ({count} instances): Review these areas for improvement."
                )

        return "\n\n".join(feedback_parts)

    def _generate_style_feedback(self, analysis_results: Dict[str, Any]) -> str:
        """Generate specific style feedback."""
        style_data = analysis_results.get("style", {})

        feedback_parts = []

        # Sentence variety
        variety_score = style_data.get("sentence_variety_score", 0)
        if variety_score < 5:
            feedback_parts.append(
                "**Sentence Variety**: Your sentences tend to be similar in length. Try varying sentence length and structure to create more engaging prose."
            )
        elif variety_score > 15:
            feedback_parts.append(
                "**Sentence Consistency**: While variety is good, ensure your sentences maintain a consistent style appropriate for your audience."
            )
        else:
            feedback_parts.append(
                "**Good Sentence Variety**: You demonstrate effective variation in sentence length and structure."
            )

        # Sentence starters
        starter_variety = style_data.get("sentence_starter_variety", 0)
        if starter_variety < 0.6:
            feedback_parts.append(
                "**Sentence Beginnings**: Vary how you start your sentences. Avoid beginning too many sentences with the same words or patterns."
            )

        # Style issues
        style_issues = style_data.get("style_issues", [])
        if style_issues:
            issue_summary = {}
            for issue in style_issues:
                issue_type = issue.get("type", "General")
                if issue_type not in issue_summary:
                    issue_summary[issue_type] = 0
                issue_summary[issue_type] += 1

            for issue_type, count in issue_summary.items():
                if issue_type == "Overused Word":
                    feedback_parts.append(
                        f"**Word Repetition**: You repeat certain words frequently. Use synonyms and varied vocabulary to avoid monotony."
                    )
                elif issue_type == "Cliché":
                    feedback_parts.append(
                        f"**Clichéd Language**: Replace overused phrases with more original and specific language."
                    )

        if not feedback_parts:
            feedback_parts.append(
                "**Strong Style**: Your writing demonstrates good stylistic choices with appropriate variety and voice."
            )

        return "\n\n".join(feedback_parts)

    def _generate_structure_feedback(self, analysis_results: Dict[str, Any]) -> str:
        """Generate specific structure feedback."""
        structure_data = analysis_results.get("structure", {})

        feedback_parts = []

        # Paragraph organization
        paragraph_count = structure_data.get("paragraph_count", 0)
        if paragraph_count < 3:
            feedback_parts.append(
                "**Paragraph Organization**: Organize your essay into more distinct paragraphs. A typical essay should have an introduction, body paragraphs (2-3), and a conclusion."
            )
        elif paragraph_count > 7:
            feedback_parts.append(
                "**Paragraph Consolidation**: Consider combining some paragraphs. Too many short paragraphs can make your essay feel choppy."
            )

        # Paragraph balance
        paragraph_lengths = structure_data.get("paragraph_lengths", [])
        if paragraph_lengths:
            avg_length = sum(paragraph_lengths) / len(paragraph_lengths)
            if avg_length < 30:
                feedback_parts.append(
                    "**Paragraph Development**: Develop your paragraphs more fully. Each paragraph should contain 50-100 words and focus on one main idea with supporting details."
                )
            elif avg_length > 150:
                feedback_parts.append(
                    "**Paragraph Length**: Some paragraphs may be too long. Consider breaking lengthy paragraphs into smaller, more focused ones."
                )

        # Introduction and conclusion
        if not structure_data.get("has_clear_introduction", False):
            feedback_parts.append(
                "**Introduction**: Strengthen your opening paragraph. A good introduction should engage the reader, introduce your topic, and preview your main points."
            )

        if not structure_data.get("has_clear_conclusion", False):
            feedback_parts.append(
                "**Conclusion**: Add a stronger conclusion that summarizes your main points and provides a sense of closure. Avoid simply repeating your introduction."
            )

        # Transitions
        transition_count = structure_data.get("transition_word_count", 0)
        if transition_count < 2:
            feedback_parts.append(
                "**Transitions**: Use more transitional words and phrases to connect your ideas and improve flow between paragraphs."
            )
        elif transition_count > 10:
            feedback_parts.append(
                "**Transition Balance**: While transitions are important, ensure they feel natural and don't overwhelm your writing."
            )

        if not feedback_parts:
            feedback_parts.append(
                "**Well-Structured**: Your essay demonstrates good organizational structure with clear paragraphs and logical flow."
            )

        return "\n\n".join(feedback_parts)
