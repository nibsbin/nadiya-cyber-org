from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field
from robora import QuestionSet


class ResponsibilityLevel(Enum):
    """Level of cybersecurity responsibility"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"


class ConfidenceLevel(Enum):
    """Confidence in the assessment"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"


class CyberResponsibilityModel(BaseModel):
    """Assessment of when and how a ministry/department became responsible for cybersecurity."""

    organ_incarnation_name: Optional[str] = Field(
        default=None,
        description=(
            "Name of the specific organization/entity/incarnation of the ministry/department "
            "that became responsible for cybersecurity. If not applicable, return the current "
            "incarnation with ResponsibilityLevel.None."
        ),
    )

    responsible_date: Optional[str] = Field(
        default=None,
        description=(
            "Date (year or full date) when the organ incarnation became responsible for "
            "or involved in cybersecurity. If not applicable, return null."
        ),
    )

    responsibility_level: ResponsibilityLevel = Field(
        description="Level of cybersecurity responsibility"
    )

    explanation: Optional[str] = Field(
        default=None,
        description=(
            "Explanation for the assessment including evidence and citation references "
            "after each claim."
        )
    )

    confidence: ConfidenceLevel = Field(
        description="Confidence level of this assessment"
    )


if __name__ == "__main__":
    print(CyberResponsibilityModel.model_json_schema())


_template = (
    "Assess the {domain} ministry/department of {country} as a cybersecurity stakeholder. "
    "If it is responsible for or involved in cybersecurity, provide: "
    "(1) the name of the specific organ/entity incarnation that became responsible, "
    "(2) when it became responsible, "
    "(3) the level of responsibility (none, low, medium, high), "
    "(4) explanation with evidence."
)


def get_question_set(domains: List[str], countries: List[str]) -> QuestionSet:
    word_sets: Dict[str, List[str]] = {
        "domain": domains,
        "country": countries,
    }
    return QuestionSet(
        word_sets=word_sets,
        template=_template,
        response_model=CyberResponsibilityModel,
    )
