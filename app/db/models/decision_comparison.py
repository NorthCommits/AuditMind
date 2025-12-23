import uuid
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.database import Base


class DecisionComparison(Base):
    __tablename__ = "decision_comparisons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    decision_key = Column(String, nullable=False, index=True)

    version_a = Column(Integer, nullable=False)
    version_b = Column(Integer, nullable=False)

    comparison_text = Column(String, nullable=False)

    model_name = Column(String, nullable=False)
    prompt_hash = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
