from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.db.models.decision import Decision
from app.schemas.decision import DecisionCreate, DecisionResponse

router = APIRouter(prefix="/decisions", tags=["Decisions"])


@router.post("/", response_model=DecisionResponse)
def create_decision(
    payload: DecisionCreate,
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
