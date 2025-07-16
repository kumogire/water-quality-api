"""
Water quality endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import date
import pandas as pd

from app.models.requests import WaterQualityQuery, ReportConfig, ReportType
from app.models.responses import WaterQualityReport, SitesResponse, ParametersResponse
from app.core.data_fetcher import USGSDataFetcher
from app.core.data_processor import DataProcessor
from app.core.report_generator import ReportGenerator

router = APIRouter()

@router.post("/query", response_model=WaterQualityReport)
async def query_water_quality(
    query: WaterQualityQuery,
    config: ReportConfig = ReportConfig()
):
    """
    Query water quality data from USGS Water Quality Portal and generate reports
    
    This endpoint allows you to query water quality data with various filters
    and generate different types of reports (summary, detailed, trend analysis).
    """
    
    try:
        # Build query parameters
        query_params = USGSDataFetcher.build_wqp_query_params(
            site_no=query.site_no,
            state_cd=query.state_cd,
            county_cd=query.county_cd,
            huc=query.huc,
            bbox=query.bbox,
            characteristic_name=query.characteristic_name,
            start_date=query.start_date,
            end_date=query.end_date,
            sample_media=query.sample_media,
            organization=query.organization
        )
        
        # Fetch data from WQP
        df, md = USGSDataFetcher.fetch_water_quality_data(query_params)
        
        # Clean and validate data
        df = DataProcessor.clean_and_validate_data(df)
        
        # Limit records if specified
        df = DataProcessor.limit_records(df, config.max_records)
        
        # Generate report based on type
        if config.report_type == ReportType.summary:
            report_data = ReportGenerator.generate_summary_report(df, query_params)
            data_records = []
        elif config.report_type == ReportType.detailed:
            report_data = {}
            data_records = ReportGenerator.generate_detailed_report(df, query_params)
        elif config.report_type == ReportType.trend:
            report_data = ReportGenerator.generate_trend_report(df, query_params)
            data_records = []
        else:  # comparison
            report_data = ReportGenerator.generate_summary_report(df, query_params)
            data_records = ReportGenerator.generate_detailed_report(df, query_params)[:100]
        
        # Create response
        response = WaterQualityReport(
            query_info=query_params,
            report_type=config.report_type.value,
            generated_at=datetime.now(),
            data_summary=report_data,
            records_processed=len(df),
            data=data_records,
            metadata=md.to_dict() if config.include_metadata and md is not None else None
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying data: {str(e)}")

@router.get("/sites", response_model=SitesResponse)
async def get_monitoring_sites(
    state_cd: List[str] = Query(["CA"], description="State codes"),
    site_type: List[str] = Query(["Stream"], description="Site types"),
    has_data_since: Optional[date] = Query(None, description="Sites with data since this date")
):
    """
    Get information about monitoring sites
    
    Returns metadata about water quality monitoring sites including
    location, site type, and data availability.
    """
    
    try:
        sites_df = USGSDataFetcher.fetch_site_info(state_cd, site_type, has_data_since)
        
        if sites_df.empty:
            return SitesResponse(sites=[], count=0, query_params={})
        
        # Convert to records
        sites_records = sites_df.to_dict('records')
        
        # Clean up records
        for record in sites_records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
        
        query_params = {
            'stateCd': state_cd,
            'siteType': site_type
        }
        if has_data_since:
            query_params['startDt'] = has_data_since.strftime('%Y-%m-%d')
        
        return SitesResponse(
            sites=sites_records,
            count=len(sites_records),
            query_params=query_params
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sites: {str(e)}")

@router.get("/parameters", response_model=ParametersResponse)
async def get_available_parameters():
    """
    Get list of available water quality parameters
    
    Returns commonly monitored water quality parameters that can be
    used in queries to filter data.
    """
    
    # Common water quality parameters
    parameters = {
        "physical": [
            "Temperature", "pH", "Dissolved oxygen", "Turbidity",
            "Conductivity", "Total dissolved solids", "Salinity"
        ],
        "chemical": [
            "Nitrogen", "Phosphorus", "Nitrate", "Nitrite", "Ammonia",
            "Total nitrogen", "Total phosphorus", "Chloride", "Sulfate"
        ],
        "biological": [
            "Escherichia coli", "Fecal coliform", "Enterococcus",
            "Total coliform", "Chlorophyll a"
        ],
        "metals": [
            "Lead", "Mercury", "Arsenic", "Cadmium", "Copper",
            "Zinc", "Iron", "Manganese", "Aluminum"
        ]
    }
    
    return ParametersResponse(
        parameters=parameters,
        total_categories=len(parameters),
        usage_note="Use these parameter names in the 'characteristic_name' field when querying data"
    )

@router.get("/example-queries")
async def get_example_queries():
    """
    Get example queries for different use cases
    
    Returns example API calls for common water quality monitoring scenarios.
    """
    
    examples = {
        "yuba_river_temperature": {
            "description": "Temperature data from Yuba River",
            "query": {
                "huc": ["18020125"],  # Yuba River HUC
                "characteristic_name": ["Temperature"],
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "state_cd": ["CA"]
            },
            "config": {
                "report_type": "trend",
                "format": "json"
            }
        },
        "american_river_nutrients": {
            "description": "Nutrient data from American River",
            "query": {
                "huc": ["18020111"],  # American River HUC
                "characteristic_name": ["Nitrogen", "Phosphorus"],
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
                "state_cd": ["CA"]
            },
            "config": {
                "report_type": "detailed",
                "format": "json"
            }
        },
        "california_ph_summary": {
            "description": "pH summary for California water bodies",
            "query": {
                "state_cd": ["CA"],
                "characteristic_name": ["pH"],
                "start_date": "2023-01-01",
                "end_date": "2023-12-31"
            },
            "config": {
                "report_type": "summary",
                "format": "json"
            }
        }
    }
    
    return {
        "examples": examples,
        "note": "Use these examples as templates for your own queries"
    }