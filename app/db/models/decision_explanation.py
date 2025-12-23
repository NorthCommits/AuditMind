import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.database import Base


class DecisionExplanation(Base):
    __tablename__ = "decision_explanations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    decision_id = Column(
        UUID(as_uuid=True),
        ForeignKey("decisions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    decision_key = Column(String, nullable=False, index=True)
    decision_version = Column(String, nullable=False)

    explanation_text = Column(String, nullable=False)

    confidence_score = Column(Float, nullable=True)
    risk_summary = Column(String, nullable=True)

    model_name = Column(String, nullable=False)
    model_version = Column(String, nullable=True)
    prompt_hash = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
