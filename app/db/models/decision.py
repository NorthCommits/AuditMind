import uuid
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.database import Base


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_key = Column(String, nullable=False, index=True)

    version = Column(Integer, nullable=False)

    input_payload = Column(JSON, nullable=False)
    output_payload = Column(JSON, nullable=False)

    decision_made_by = Column(String, nullable=False)  # human | system | ai-assisted

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    explanation = Column(String, nullable=True)
    confidence_score = Column(String, nullable=True)
