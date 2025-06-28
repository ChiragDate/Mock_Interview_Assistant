import json
import re
from core.llm_Service import generate_completion
from prompts.feedback_prompts import get_feedback_prompt

def generate_feedback_and_scores(resume_text: str, round_name: str, qa_pairs: list[dict]) -> dict:
    """Parses LLM feedback (in JSON format embedded inside markdown/code block) into a structured result."""

    print("\nGenerating feedback based on your interview...")
    prompt = get_feedback_prompt(resume_text, round_name, qa_pairs)
    raw_feedback = generate_completion(prompt, max_tokens=1500, temperature=0.5)

    feedback_data = {
        "overall_feedback": "Could not parse feedback.",
        "suggestions": "Could not parse suggestions.",
        "scores_per_question": [],
        "total_score": 0,
        "raw_output": raw_feedback
    }

    try:
        # Extract the JSON block from markdown-style backticks if present
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", raw_feedback, re.DOTALL)
        if json_match:
            feedback_json = json.loads(json_match.group(1))
        else:
            # Try to find a raw JSON-like object if not inside markdown
            feedback_json = json.loads(raw_feedback)

        # Basic fields
        feedback_data["overall_feedback"] = feedback_json.get("overall_feedback", feedback_data["overall_feedback"])
        feedback_data["suggestions"] = feedback_json.get("suggestions", feedback_data["suggestions"])
        feedback_data["total_score"] = feedback_json.get("total_score", feedback_data["total_score"])

        # Parse detailed score breakdown per question (from raw_output, outside JSON block)
        scores = []
        breakdown_blocks = raw_feedback.split("Q1:")[-1].split("\n\nQ")[0].strip().split("\n\n")

        for i, qa in enumerate(qa_pairs):
            try:
                block_start = f"Q{i+1}:"
                block_text = next((b for b in breakdown_blocks if b.strip().startswith(block_start)), "")
                relevance = int(re.search(r"Relevance:\s*(\d+)", block_text).group(1))
                clarity = int(re.search(r"Clarity:\s*(\d+)", block_text).group(1))
                detail = int(re.search(r"Detail/Examples:\s*(\d+)", block_text).group(1))
                alignment = int(re.search(r"Resume Alignment:\s*(\d+)", block_text).group(1))
                total = int(re.search(r"Score:\s*(\d+)", block_text).group(1))

                scores.append({
                    "question": qa["question"],
                    "criteria": {
                        "relevance": relevance,
                        "clarity": clarity,
                        "detail_examples": detail,
                        "resume_alignment": alignment
                    },
                    "total_score": total
                })
            except Exception as e:
                print(f"Warning: Failed to parse detailed scores for Q{i+1}: {e}")

        # If we got as many detailed scores as questions, use them
        if len(scores) == len(qa_pairs):
            feedback_data["scores_per_question"] = scores
        else:
            # fallback: try from JSON array if provided
            json_scores = feedback_json.get("scores_per_question", [])
            if len(json_scores) == len(qa_pairs):
                feedback_data["scores_per_question"] = [
                    {
                        "question": qa["question"],
                        "criteria": {},
                        "total_score": int(s)
                    }
                    for qa, s in zip(qa_pairs, json_scores)
                ]

        # Fallback to computing total
        if not feedback_data["total_score"] and feedback_data["scores_per_question"]:
            feedback_data["total_score"] = sum(s["total_score"] for s in feedback_data["scores_per_question"])

    except Exception as e:
        print(f"Error parsing feedback: {e}")
        print("Returning raw feedback in 'raw_output' field.")

    print("Feedback generated.")
    return feedback_data
