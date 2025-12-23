from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import BackgroundTasks
from app.core.ai_explainer import explain_decision_async
from app.core.decision_comparator import compare_decisions


from app.db.database import get_db
from app.db.models.decision import Decision
from app.schemas.decision import DecisionCreate, DecisionResponse

router = APIRouter(prefix="/decisions", tags=["Decisions"])


@router.post("/", response_model=DecisionResponse)
def create_decision(
    payload: DecisionCreate,
    background_tasks:BackgroundTasks,
    db: Session = Depends(get_db)
):
    latest_version = (
        db.query(func.max(Decision.version))
        .filter(Decision.decision_key == payload.decision_key)
        .scalar()
    )

    next_version = 1 if latest_version is None else latest_version + 1

    decision = Decision(
        decision_key=payload.decision_key,
        version=next_version,
        input_payload=payload.input_payload,
        output_payload=payload.output_payload,
        decision_made_by=payload.decision_made_by,
    )

    db.add(decision)
    db.commit()
    db.refresh(decision)

    background_tasks.add_task(
    explain_decision_async,
    db,
    decision
)


    return DecisionResponse(
        id=str(decision.id),
        decision_key=decision.decision_key,
        version=decision.version,
    )


@router.get("/{decision_key}")
def get_decision_history(
    decision_key: str,
    db: Session = Depends(get_db)
):
    decisions = (
        db.query(Decision)
        .filter(Decision.decision_key == decision_key)
        .order_by(Decision.version.asc())
        .all()
    )

    return [
        {
            "id": str(d.id),
            "decision_key": d.decision_key,
            "version": d.version,
            "input_payload": d.input_payload,
            "output_payload": d.output_payload,
            "decision_made_by": d.decision_made_by,
            "created_at": d.created_at,
        }
        for d in decisions
    ]

@router.post("/{decision_key}/compare")
def compare_decision_versions(
    decision_key: str,
    version_a: int,
    version_b: int,
    db: Session = Depends(get_db),
):
    comparison = compare_decisions(
        db=db,
        decision_key=decision_key,
        version_a=version_a,
        version_b=version_b,
    )

    return {
        "decision_key": comparison.decision_key,
        "version_a": comparison.version_a,
        "version_b": comparison.version_b,
        "comparison_text": comparison.comparison_text,
        "model_name": comparison.model_name,
        "created_at": comparison.created_at,
    }
