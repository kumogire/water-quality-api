"""
Pydantic models for API requests
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum

class ReportFormat(str, Enum):
    json = "json"
    csv = "csv"
    html = "html"

class ReportType(str, Enum):
    summary = "summary"
    detailed = "detailed"
    trend = "trend"
    comparison = "comparison"

class WaterQualityQuery(BaseModel):
    """Model for water quality query parameters"""
    site_no: Optional[List[str]] = Field(None, description="USGS site numbers")
    state_cd: Optional[List[str]] = Field(["CA"], description="State codes (default: California)")
    county_cd: Optional[List[str]] = Field(None, description="County codes")
    huc: Optional[List[str]] = Field(None, description="Hydrologic Unit Codes")
    bbox: Optional[List[float]] = Field(None, description="Bounding box [minx, miny, maxx, maxy]")
    characteristic_name: Optional[List[str]] = Field(None, description="Parameter names (e.g., 'Temperature', 'pH')")
    start_date: Optional[date] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[date] = Field(None, description="End date (YYYY-MM-DD)")
    sample_media: Optional[List[str]] = Field(["Water"], description="Sample media types")
    organization: Optional[List[str]] = Field(None, description="Organization identifiers")

class ReportConfig(BaseModel):
    """Configuration for report generation"""
    report_type: ReportType = Field(ReportType.summary, description="Type of report to generate")
    format: ReportFormat = Field(ReportFormat.json, description="Output format")
    include_metadata: bool = Field(True, description="Include metadata in report")
    max_records: int = Field(10000, description="Maximum records to process")