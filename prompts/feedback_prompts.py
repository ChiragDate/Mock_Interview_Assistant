from langchain.prompts import PromptTemplate

# Define PromptTemplate for JSON output
feedback_prompt_template = PromptTemplate(
    input_variables=["resume_text", "round_name", "formatted_qa", "scoring_criteria"],
    template="""
You are an expert interviewer providing feedback on a mock interview.
The interview was for the '{round_name}' round.
The candidate's resume is provided below for context.
Analyze the following question and answer pairs from the interview.

Resume Context:
---
{resume_text}
---

Interview Questions and Answers:
---
{formatted_qa}
---

Scoring Criteria (per question, max 10 points):
{scoring_criteria}

Instructions:
1. Provide constructive overall feedback for the candidate's performance in this round.
2. Give specific suggestions for improvement based on their answers.
3. Score each answer individually based on the criteria provided.
4. Calculate a total score (sum of all individual question scores).
5. Return the entire output strictly in valid JSON format, like this:

```json
{{
  "overall_feedback": "Your overall comments here...",
  "suggestions": "Specific suggestions here...",
  "scores_per_question": [8, 7, 9, 6],
  "total_score": 30
}}
"""
)


def format_qa_pairs(qa_pairs: list[dict]) -> str:
    return "\n".join([f"Q: {item['question']}\nA: {item['answer']}" for item in qa_pairs])

def get_feedback_prompt(resume_text: str, round_name: str, qa_pairs: list[dict], scoring_criteria: str = None) -> str:
    """Generates feedback prompt using LangChain PromptTemplate."""

    if not scoring_criteria:
        scoring_criteria = """
Score each answer out of 10 based on the following criteria:
1. Relevance: How well does the answer address the question? (0-3 points)
2. Clarity: How clear and concise is the answer? (0-2 points)
3. Detail/Examples: Does the answer provide sufficient detail or examples (like STAR method where applicable)? (0-3 points)
4. Resume Alignment: How well does the answer align with the candidate's resume? (0-2 points)
"""

    formatted_qa = format_qa_pairs(qa_pairs)

    return feedback_prompt_template.format(
        resume_text=resume_text,
        round_name=round_name,
        formatted_qa=formatted_qa,
        scoring_criteria=scoring_criteria
    )
