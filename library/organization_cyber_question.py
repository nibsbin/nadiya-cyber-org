from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field
from robora import QuestionSet
from datetime import date


class ResponsibilityLevel(Enum):
    """Organization's level of cybersecurity responsibility"""
    HIGH = "HIGH"
    LOW = "LOW"
    NONE = "NONE"


class ConfidenceLevel(Enum):
    """Confidence in the assessment"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NONE = "NONE"


class OrganizationCyberModel(BaseModel):
    """Assessment of when and how the organization became responsible for the country's cybersecurity governance, prevention, planning, response, or enforcement."""
    organization: str = Field(
        description="Name of the given top-level state Organ (i.e., ministry/department/agency)."
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
    print(OrganizationCyberModel.model_json_schema())


_template = (
    "Assess the cybersecurity responsibility of {organization_country}. "
)


def get_question_set(organizations: List[str], countries: List[str]) -> QuestionSet:
    org_countries = [f"{org} in {country}" for (org, country) in zip(organizations, countries)]
    word_sets: Dict[str, List[str]] = {
        "organization_country": org_countries
    }
    return QuestionSet(
        word_sets=word_sets,
        template=_template,
        response_model=OrganizationCyberModel,
    )
