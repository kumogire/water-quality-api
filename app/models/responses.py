"""
Pydantic models for API responses
"""
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime

class WaterQualityReport(BaseModel):
    """Model for water quality report response"""
    query_info: Dict[str, Any]
    report_type: str
    generated_at: datetime
    data_summary: Dict[str, Any]
    records_processed: int
    data: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None

class SitesResponse(BaseModel):
    """Model for sites endpoint response"""
    sites: List[Dict[str, Any]]
    count: int
    query_params: Dict[str, Any]

class ParametersResponse(BaseModel):
    """Model for parameters endpoint response"""
    parameters: Dict[str, List[str]]
    total_categories: int
    usage_note: str