from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import GUID, TimestampMixin, generate_uuid, AssessmentStatus
from typing import List

class Patient(Base, TimestampMixin):
    """患者モデル"""
    __tablename__ = "patients"

    id = Column(GUID, primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    
    # リレーションシップ
    assessment_results = relationship("AssessmentResult", back_populates="patient")

    def __repr__(self) -> str:
        return f"<Patient(id={self.id}, name={self.name})>"

class Assessment(Base, TimestampMixin):
    """検査マスターモデル"""
    __tablename__ = "assessments"

    id = Column(GUID, primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    cutoff = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)
    
    # リレーションシップ
    questions = relationship("Question", back_populates="assessment", cascade="all, delete-orphan")
    options = relationship("Option", back_populates="assessment", cascade="all, delete-orphan")
    results = relationship("AssessmentResult", back_populates="assessment")

    def __repr__(self) -> str:
        return f"<Assessment(id={self.id}, name={self.name}, type={self.type})>"

class Question(Base):
    """質問モデル"""
    __tablename__ = "questions"

    id = Column(GUID, primary_key=True, default=generate_uuid)
    assessment_id = Column(GUID, ForeignKey("assessments.id"), nullable=False)
    text = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)
    
    # リレーションシップ
    assessment = relationship("Assessment", back_populates="questions")
    answers = relationship("AnswerDetail", back_populates="question")

    def __repr__(self) -> str:
        return f"<Question(id={self.id}, assessment_id={self.assessment_id}, order={self.order})>"

class Option(Base):
    """選択肢モデル"""
    __tablename__ = "options"

    id = Column(GUID, primary_key=True, default=generate_uuid)
    assessment_id = Column(GUID, ForeignKey("assessments.id"), nullable=False)
    text = Column(Text, nullable=False)
    value = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    
    # リレーションシップ
    assessment = relationship("Assessment", back_populates="options")
    answers = relationship("AnswerDetail", back_populates="selected_option")

    def __repr__(self) -> str:
        return f"<Option(id={self.id}, assessment_id={self.assessment_id}, value={self.value})>"