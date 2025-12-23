import hashlib
from sqlalchemy.orm import Session

from app.db.models.decision_explanation import DecisionExplanation
from app.db.models.decision import Decision
from app.core.llm_client import generate_decision_explanation, MODEL_NAME


def build_prompt(decision: Decision) -> str:
    return f"""
Decision Version: {decision.version}

Input Data:
{decision.input_payload}

Output Data:
{decision.output_payload}

Task:
Explain why this decision outcome occurred.
Highlight key factors and any uncertainty.
Do not add information not present in the input or output.
"""


def explain_decision_async(
    db: Session,
    decision: Decision,
):
    prompt = build_prompt(decision)

    explanation_text = generate_decision_explanation(prompt)

    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()

    explanation = DecisionExplanation(
        decision_id=decision.id,
        decision_key=decision.decision_key,
        decision_version=str(decision.version),
        explanation_text=explanation_text,
        confidence_score=0.85,
        model_name=MODEL_NAME,
        prompt_hash=prompt_hash,
    )

    db.add(explanation)
    db.commit()
