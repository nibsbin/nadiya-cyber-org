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

class OrganizationModel(BaseModel):
    organization_name: str = Field(
        description="Name of the top-level state Organ (i.e., ministry/department/agency). If no such Organ exists, return 'NONE'."
    )
    confidence: ConfidenceLevel = Field(
        description="Confidence level of your assessment."
    )

if __name__ == "__main__":
    print(OrganizationModel.model_json_schema())


_template = (
   "What is the top-level state Organ (i.e., ministry/department/agency) responsible for {domain} in {country}?"
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
        response_model=OrganizationModel,
    )
