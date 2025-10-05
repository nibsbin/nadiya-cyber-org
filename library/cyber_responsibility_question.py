from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field
from robora import QuestionSet
from datetime import date


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
    """Assessment of when and how the primary ministry/department became responsible for the country's cybersecurity governance, prevention, planning, response, or enforcement."""

    incarnation_name: Optional[str] = Field(
        default=None,
        description=(
            "Name of the specific incarnation of the ministry/department "
            "that became responsible for cybersecurity. "
            "If not applicable, return the current "
            "incarnation with ResponsibilityLevel.None."
        ),
    )

    responsible_date: Optional[date] = Field(
        default=None,
        description=(
            "Date when the organ incarnation became responsible for "
            "cybersecurity. If not applicable, return null."
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
    "Assess the PRIMARY (i.e., most important) {domain} ministry/department of {country}. "
    "Do not consider small regulators or third parties. "
    "Regarding this organization's responsibility over {country}'s "
    "cybersecurity governance, prevention, planning, response, or enforcement: "
    "(1) What is the name of the specific organization?, "
    "(2) When it became responsible (if applicable)?, "
    "(3) What is the level of responsibility (none, low, medium, high)?, "
    "(4) Provide explanation/evidence."
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
