"""
USGS data fetching functionality
"""
import pandas as pd
import dataretrieval.nwis as nwis
import dataretrieval.wqp as wqp
from typing import Dict, Any, Tuple, Optional, List
from datetime import date

class USGSDataFetcher:
    """Handles fetching data from USGS APIs"""
    
    @staticmethod
    def build_wqp_query_params(
        site_no: Optional[List[str]] = None,
        state_cd: Optional[List[str]] = None,
        county_cd: Optional[List[str]] = None,
        huc: Optional[List[str]] = None,
        bbox: Optional[List[float]] = None,
        characteristic_name: Optional[List[str]] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        sample_media: Optional[List[str]] = None,
        organization: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Build query parameters for Water Quality Portal"""
        query_params = {}
        
        if site_no:
            query_params['siteid'] = site_no
        if state_cd:
            query_params['statecode'] = state_cd
        if county_cd:
            query_params['countycode'] = county_cd
        if huc:
            query_params['huc'] = huc
        if bbox:
            query_params['bbox'] = ','.join(map(str, bbox))
        if characteristic_name:
            query_params['characteristicName'] = characteristic_name
        if start_date:
            query_params['startDateLo'] = start_date.strftime('%m-%d-%Y')
        if end_date:
            query_params['startDateHi'] = end_date.strftime('%m-%d-%Y')
        if sample_media:
            query_params['sampleMedia'] = sample_media
        if organization:
            query_params['organization'] = organization
            
        return query_params
    
    @staticmethod
    def fetch_water_quality_data(query_params: Dict[str, Any]) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
        """Fetch water quality data from WQP"""
        return wqp.get_results(**query_params)
    
    @staticmethod
    def fetch_site_info(
        state_cd: List[str],
        site_type: List[str],
        has_data_since: Optional[date] = None
    ) -> pd.DataFrame:
        """Fetch site information from NWIS"""

        # Map site types to USGS codes
        site_type_mapping = {
            'Stream': 'ST',
            'Lake': 'LK', 
            'Groundwater': 'GW',
            # Add more mappings as needed
        }

        # Convert site types to USGS codes
        mapped_site_types = []
        for st in site_type:
            mapped_site_types.append(site_type_mapping.get(st, st))

        query_params = {
            'stateCd': state_cd,
            'siteType': mapped_site_types,
            'siteOutput': 'expanded'  # need to override the library's "Expanded" value to make this work
        }
        
        if has_data_since:
            query_params['startDt'] = has_data_since.strftime('%Y-%m-%d')
        
        result = nwis.get_info(**query_params)
    
        # Handle if result is a tuple
        if isinstance(result, tuple):
            return result[0]  # Usually the first element is the DataFrame
        else:
            return result