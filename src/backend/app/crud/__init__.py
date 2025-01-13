from app.crud.base import CRUDBase
from app.crud.patient import CRUDPatient, patient
from app.crud.assessment import CRUDAssessment, assessment
from app.crud.result import CRUDAssessmentResult, assessment_result

__all__ = [
    "CRUDBase",
    "CRUDPatient",
    "patient",
    "CRUDAssessment",
    "assessment",
    "CRUDAssessmentResult",
    "assessment_result"
]