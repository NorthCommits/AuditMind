import hashlib
from sqlalchemy.orm import Session

from app.db.models.decision import Decision
from app.db.models.decision_comparison import DecisionComparison
from app.core.llm_client import generate_decision_explanation, MODEL_NAME


def build_comparison_prompt(
    decision_a: Decision,
    decision_b: Decision
) -> str:
    return f"""
Decision Version {decision_a.version}:
Input: {decision_a.input_payload}
Output: {decision_a.output_payload}

Decision Version {decision_b.version}:
Input: {decision_b.input_payload}
Output: {decision_b.output_payload}

Task:
Compare these two decisions.
Explain:
- What changed between versions
- Whether the outcome consistency is justified
- Any potential risk or policy drift
Do not invent facts.
"""


def compare_decisions(
    db: Session,
    decision_key: str,
    version_a: int,
    version_b: int,
):
    decision_a = (
        db.query(Decision)
        .filter(
            Decision.decision_key == decision_key,
            Decision.version == version_a,
        )
        .first()
    )

    decision_b = (
        db.query(Decision)
        .filter(
            Decision.decision_key == decision_key,
            Decision.version == version_b,
        )
        .first()
    )

    if not decision_a or not decision_b:
        raise ValueError("One or both decision versions not found")

    prompt = build_comparison_prompt(decision_a, decision_b)

    comparison_text = generate_decision_explanation(prompt)

    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()

    comparison = DecisionComparison(
        decision_key=decision_key,
        version_a=version_a,
        version_b=version_b,
        comparison_text=comparison_text,
        model_name=MODEL_NAME,
        prompt_hash=prompt_hash,
    )

    db.add(comparison)
    db.commit()

    return comparison
