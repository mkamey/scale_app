from sqlalchemy import Column, ForeignKey, Integer, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.base import GUID, TimestampMixin, generate_uuid, AssessmentStatus
from datetime import datetime

class AssessmentResult(Base, TimestampMixin):
    """検査結果モデル"""
    __tablename__ = "assessment_results"

    id = Column(GUID, primary_key=True, default=generate_uuid)
    patient_id = Column(GUID, ForeignKey("patients.id"), nullable=False)
    assessment_id = Column(GUID, ForeignKey("assessments.id"), nullable=False)
    total_score = Column(Integer, nullable=True)  # 完了時に計算
    status = Column(
        Enum(AssessmentStatus),
        nullable=False,
        default=AssessmentStatus.NOT_STARTED
    )
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # リレーションシップ
    patient = relationship("Patient", back_populates="assessment_results")
    assessment = relationship("Assessment", back_populates="results")
    answer_details = relationship(
        "AnswerDetail",
        back_populates="result",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<AssessmentResult("
            f"id={self.id}, "
            f"patient_id={self.patient_id}, "
            f"assessment_id={self.assessment_id}, "
            f"status={self.status}"
            f")>"
        )

    def start(self) -> None:
        """検査を開始する"""
        if self.status == AssessmentStatus.NOT_STARTED:
            self.status = AssessmentStatus.IN_PROGRESS
            self.started_at = datetime.now()

    def complete(self) -> None:
        """検査を完了する"""
        if self.status == AssessmentStatus.IN_PROGRESS:
            self.status = AssessmentStatus.COMPLETED
            self.completed_at = datetime.now()
            self.calculate_total_score()

    def calculate_total_score(self) -> None:
        """合計スコアを計算する"""
        self.total_score = sum(
            answer.value for answer in self.answer_details
        )

class AnswerDetail(Base, TimestampMixin):
    """回答詳細モデル"""
    __tablename__ = "answer_details"

    id = Column(GUID, primary_key=True, default=generate_uuid)
    result_id = Column(GUID, ForeignKey("assessment_results.id"), nullable=False)
    question_id = Column(GUID, ForeignKey("questions.id"), nullable=False)
    selected_option_id = Column(GUID, ForeignKey("options.id"), nullable=False)
    value = Column(Integer, nullable=False)
    answered_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now
    )

    # リレーションシップ
    result = relationship("AssessmentResult", back_populates="answer_details")
    question = relationship("Question", back_populates="answers")
    selected_option = relationship("Option", back_populates="answers")

    def __repr__(self) -> str:
        return (
            f"<AnswerDetail("
            f"id={self.id}, "
            f"result_id={self.result_id}, "
            f"question_id={self.question_id}, "
            f"value={self.value}"
            f")>"
        )