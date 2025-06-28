from langchain.prompts import PromptTemplate

question_generation_template = PromptTemplate(
    input_variables=["resume_text", "round_name", "num_questions", "instructions"],
    template="""
Based on the following resume text, generate {num_questions} relevant interview questions for a '{round_name}' round.
{instructions}
Ensure the questions are open-ended and encourage detailed answers. Do not ask questions that can be answered with a simple 'yes' or 'no'.

Format the output strictly as a Python list of strings, like this:
["Question 1?", "Question 2?", "Question 3?"] 
Do not add any other extra text apart from the Python list.
Eg: Do not add introduction like, " Here are the 5 questions for HR round "

Resume Text:
---
{resume_text}
---

Generate the list of questions now:
"""
)


def get_question_generation_prompt(resume_text: str, round_name: str, num_questions: int = 5) -> str:
    """Generates question generation prompt using LangChain PromptTemplate."""
    
    round_instructions = {
        "HR": "Focus on behavioral questions, cultural fit, salary expectations (ask indirectly), and general background.",
        "Technical": "Focus on specific technical skills, technologies, and project experiences mentioned in the resume. Ask problem-solving or coding concept questions relevant to the skills.",
        "Managerial": "Focus on leadership potential, team collaboration, conflict resolution, project management approaches, and career goals.",
        "General": "Ask a mix of behavioral, situational, and resume-based questions."
    }

    instructions = round_instructions.get(round_name, round_instructions["General"])

    return question_generation_template.format(
        resume_text=resume_text,
        round_name=round_name,
        num_questions=num_questions,
        instructions=instructions
    )




# Prompt was generating extra here are the 4 questions for hr round as in the input where i only wanted the list 