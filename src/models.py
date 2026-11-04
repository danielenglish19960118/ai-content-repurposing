"""
Pydantic Data Models for Strict Enterprise Output Guarantees
"""
from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field

class ActionItem(BaseModel):
    task: str = Field(description="Clear description of the action item.")
    owner: str = Field(default="Unassigned", description="Individual or team responsible.")
    deadline: str = Field(default="Unspecified", description="Target completion date or timeframe.")
    priority: str = Field(default="Medium", description="Priority level: High, Medium, Low.")

class EnterpriseReportSchema(BaseModel):
    executive_summary: str = Field(description="High-level narrative summary for leadership.")
    key_insights: List[str] = Field(description="Bullet points of key findings, risks, and operational impacts.")
    action_items: List[ActionItem] = Field(description="Structured action items with owner, deadline, and priority.")
