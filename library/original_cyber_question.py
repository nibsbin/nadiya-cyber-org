from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field
from robora import QuestionSet


class ConfidenceLevel(Enum):
    """Confidence in the assessment"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"


class OriginalCyberModel(BaseModel):
    """When a ministry/department first became a direct stakeholder in cybersecurity."""
    earliest_date: Optional[str] = Field(
        default=None,
        description=(
            "Earliest date (year or full date) when the ministry/department is known to have been "
            "a direct stakeholder in cybersecurity. If not applicable≈, return null."
        ),
    )
    earliest_date_entity: Optional[str] = Field(
        default=None,
        description=(
            "The named entity (organization, person, event) associated with the earliest date "
            "when the ministry/department became direct stakeholder in cybersecurity. "
            "If not applicable, return null."
        ),
    )
    confidence: ConfidenceLevel = Field(
        description="Confidence level of the date provided"
    )
    explanation: Optional[str] = Field(
        default=None,
        description="Explanation for the date with citation references after each claim."
    )


if __name__ == "__main__":
    print(OriginalCyberModel.model_json_schema())


_template = (
    "If the {domain} ministry/department of {country} is a direct stakeholder in cybersecurity, "
    "when did {domain} ministry/department of {country} "
    "become responsible for or involved in cybersecurity? "
    "Provide the earliest known date and name of the entity at this time."
)


def get_question_set(domains: List[str], countries: List[str]) -> QuestionSet:
    word_sets: Dict[str, List[str]] = {
        "domain": domains,
        "country": countries,
    }
    return QuestionSet(
        word_sets=word_sets,
        template=_template,
        response_model=OriginalCyberModel,
    )
