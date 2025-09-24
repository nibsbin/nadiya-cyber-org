from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from robora import Question, QuestionSet
from typing import Dict

class CyberRelevanceLevel(Enum):
    """Level of cybersecurity involvement"""
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

class CyberRelevanceModel(BaseModel):
    """Assessment of whether a ministry/department is a cybersecurity stakeholder"""    
    relevance_level: CyberRelevanceLevel = Field(
        description="Level of cybersecurity involvement"
    )
    confidence: ConfidenceLevel = Field(
        description="Confidence level of this assessment"
    )
    explanation: Optional[str] = Field(
        default=None,
        description="Explanation for the assessment with citation reference after each claim."
    )

if __name__ == "__main__":
    # Output schema
    print(CyberRelevanceModel.model_json_schema())

_template = "Is the department/ministry of {domain} in {country} a direct stakeholder (i.e., responsible for or involved) in the country's cybersecurity?"
def get_question_set(domains:List[str],countries:List[str]) -> QuestionSet:
    word_sets:Dict[str,List[str]] = {
        "domain": domains,
        "country": countries,
    }
    return QuestionSet(
        word_sets=word_sets,
        template = _template,
        response_model=CyberRelevanceModel,
    )
