from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field
from robora import QuestionSet
from datetime import date

class ConfidenceLevel(Enum):
    """Confidence in the assessment"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"


class OriginalCyberModel(BaseModel):
    involved: bool = Field(
        description="Whether the Organ is directly responsible for or involved in cybersecurity at all."
    )     
    earliest_date: Optional[date] = Field(
        default=None,
        description=(
            "Earliest date when the Organ first became"
            "a direct stakeholder in cybersecurity. "
            "If not involved, return null."
        ),
    )
    incarnation: Optional[str] = Field(
        default=None,
        description=(
            "The incarnation of the Organ associated with earliest_date. "
            "If not involved, return null."
        ),
    )
    confidence: ConfidenceLevel = Field(
        description="Confidence level of your assessment."
    )
    explanation: Optional[str] = Field(
        default=None,
        description="Evidence for the incarnation/date with citation references after each claim."
    )


if __name__ == "__main__":
    print(OriginalCyberModel.model_json_schema())


_template = (
    "Regarding the top-level state Organ (i.e., ministry/department/agency) of {domain} in {country}: "
    "when did the Organ become responsible for cybersecurity? If applicable, answer in the following schema: "
)


def get_question_set(domains: List[str], countries: List[str]) -> QuestionSet:
    domains = [domain.upper() for domain in domains]
    countries = [country.upper() for country in countries]
    word_sets: Dict[str, List[str]] = {
        "domain": domains,
        "country": countries,
    }
    return QuestionSet(
        word_sets=word_sets,
        template=_template,
        response_model=OriginalCyberModel,
    )
