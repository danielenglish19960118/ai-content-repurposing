"""
Pydantic Data Models for Strict Enterprise Output Guarantees
"""
from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    task: str = Field(description="Clear description of the required action item or task.")
    owner: str = Field(default="Unassigned", description="Individual, lead, or team responsible for execution.")
    deadline: str = Field(default="Unspecified", description="Target completion date, milestone, or timeframe.")
    priority: str = Field(default="Medium", description="Priority ranking: High, Medium, or Low.")


class EnterpriseReportSchema(BaseModel):
    executive_summary: str = Field(description="High-level synthesis and summary tailored for leadership.")
    key_insights: List[str] = Field(description="Bullet points outlining key findings, operational risks, and bottlenecks.")
    action_items: List[ActionItem] = Field(description="Structured array of action items with explicit fields.")
