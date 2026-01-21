from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

router = APIRouter()

class SyllabusSection(BaseModel):
    id: str
    paper: str  # GS1, GS2, GS3, GS4, Essay, Optional
    topic: str
    sub_topics: List[str]
    weightage: str  # High, Medium, Low
    questions_asked: int  # Last 5 years

class SyllabusResponse(BaseModel):
    paper: str
    total_topics: int
    sections: List[SyllabusSection]

@router.get("/complete", response_model=List[SyllabusResponse])
async def get_complete_syllabus():
    """Get complete UPSC syllabus organized by papers"""
    
    syllabus = [
        {
            "paper": "GS Paper 1 - Indian Heritage and Culture, History and Geography",
            "total_topics": 15,
            "sections": [
                {
                    "id": "gs1_1",
                    "paper": "GS1",
                    "topic": "Indian Culture",
                    "sub_topics": [
                        "Ancient India - Art forms, literature, architecture",
                        "Medieval India - Major dynasties, art and culture",
                        "Modern India - Freedom struggle, cultural movements",
                        "Salient aspects of Indian art, architecture, sculpture"
                    ],
                    "weightage": "High",
                    "questions_asked": 8
                },
                {
                    "id": "gs1_2",
                    "paper": "GS1",
                    "topic": "Modern Indian History",
                    "sub_topics": [
                        "18th Century events - British expansion",
                        "Freedom Struggle - Moderate and extremist phase",
                        "Social reform movements",
                        "Post-independence consolidation and reorganization"
                    ],
                    "weightage": "High",
                    "questions_asked": 12
                },
                {
                    "id": "gs1_3",
                    "paper": "GS1",
                    "topic": "World History",
                    "sub_topics": [
                        "Colonialism and decolonization",
                        "World Wars and their impact",
                        "Redrawal of national boundaries",
                        "Cold War and post-Cold War era"
                    ],
                    "weightage": "Medium",
                    "questions_asked": 5
                },
                {
                    "id": "gs1_4",
                    "paper": "GS1",
                    "topic": "Indian Geography",
                    "sub_topics": [
                        "Physical features of India",
                        "Distribution of key natural resources",
                        "Major crops and cropping patterns",
                        "Industries location factors"
                    ],
                    "weightage": "High",
                    "questions_asked": 10
                },
                {
                    "id": "gs1_5",
                    "paper": "GS1",
                    "topic": "World Geography",
                    "sub_topics": [
                        "Physical geography - climate, soil, vegetation",
                        "Major landforms and their distribution",
                        "Natural disasters and disaster management",
                        "Environmental geography"
                    ],
                    "weightage": "Medium",
                    "questions_asked": 6
                }
            ]
        },
        {
            "paper": "GS Paper 2 - Governance, Constitution, Polity, Social Justice",
            "total_topics": 12,
            "sections": [
                {
                    "id": "gs2_1",
                    "paper": "GS2",
                    "topic": "Indian Constitution",
                    "sub_topics": [
                        "Historical underpinnings and evolution",
                        "Salient features and amendments",
                        "Functions and responsibilities of Union and States",
                        "Federal structure, devolution of powers"
                    ],
                    "weightage": "High",
                    "questions_asked": 15
                },
                {
                    "id": "gs2_2",
                    "paper": "GS2",
                    "topic": "Governance",
                    "sub_topics": [
                        "E-governance applications, models, successes",
                        "Government policies and interventions",
                        "Development processes and development industry",
                        "Role of civil services in democracy"
                    ],
                    "weightage": "High",
                    "questions_asked": 14
                },
                {
                    "id": "gs2_3",
                    "paper": "GS2",
                    "topic": "Social Justice",
                    "sub_topics": [
                        "Welfare schemes for vulnerable sections",
                        "Mechanisms, laws, institutions for protection",
                        "Issues relating to poverty and hunger",
                        "Education, human resources development"
                    ],
                    "weightage": "High",
                    "questions_asked": 11
                }
            ]
        },
        {
            "paper": "GS Paper 3 - Technology, Economy, Environment, Security",
            "total_topics": 14,
            "sections": [
                {
                    "id": "gs3_1",
                    "paper": "GS3",
                    "topic": "Indian Economy",
                    "sub_topics": [
                        "Planning, mobilization of resources, growth",
                        "Inclusive growth and issues arising from it",
                        "Government budgeting, taxation, subsidies",
                        "Major crops, irrigation, agricultural marketing"
                    ],
                    "weightage": "High",
                    "questions_asked": 16
                },
                {
                    "id": "gs3_2",
                    "paper": "GS3",
                    "topic": "Science and Technology",
                    "sub_topics": [
                        "Developments in IT, Space, Computers, robotics",
                        "Biotechnology in health and agriculture",
                        "Awareness in IPR and digital property rights",
                        "Conservation, environmental pollution and degradation"
                    ],
                    "weightage": "High",
                    "questions_asked": 13
                },
                {
                    "id": "gs3_3",
                    "paper": "GS3",
                    "topic": "Internal Security",
                    "sub_topics": [
                        "Challenges to internal security through terrorism",
                        "Linkages of organized crime with terrorism",
                        "Role of external state and non-state actors",
                        "Cyber security, money laundering"
                    ],
                    "weightage": "High",
                    "questions_asked": 9
                }
            ]
        },
        {
            "paper": "GS Paper 4 - Ethics, Integrity and Aptitude",
            "total_topics": 8,
            "sections": [
                {
                    "id": "gs4_1",
                    "paper": "GS4",
                    "topic": "Ethics and Human Interface",
                    "sub_topics": [
                        "Essence, determinants and consequences of ethics",
                        "Dimensions of ethics in private and public relationships",
                        "Human values - role in forming attitudes",
                        "Attitude: content, structure, function"
                    ],
                    "weightage": "High",
                    "questions_asked": 10
                },
                {
                    "id": "gs4_2",
                    "paper": "GS4",
                    "topic": "Aptitude and Foundational Values",
                    "sub_topics": [
                        "Integrity, probity in governance",
                        "Objectivity and dedication in public service",
                        "Empathy, tolerance and compassion",
                        "Emotional intelligence and its utility"
                    ],
                    "weightage": "High",
                    "questions_asked": 12
                }
            ]
        }
    ]
    
    return syllabus


@router.get("/paper/{paper_name}")
async def get_paper_syllabus(paper_name: str):
    """Get syllabus for specific paper (GS1, GS2, GS3, GS4)"""
    
    all_syllabus = await get_complete_syllabus()
    
    for paper in all_syllabus:
        if paper_name.upper() in paper["paper"].upper():
            return paper
    
    raise HTTPException(status_code=404, detail="Paper not found")


@router.get("/topic/{topic_id}")
async def get_topic_details(topic_id: str):
    """Get detailed information about a specific topic"""
    
    all_syllabus = await get_complete_syllabus()
    
    for paper in all_syllabus:
        for section in paper["sections"]:
            if section["id"] == topic_id:
                return section
    
    raise HTTPException(status_code=404, detail="Topic not found")