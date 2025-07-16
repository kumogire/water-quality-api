"""
Report generation functionality
"""
import pandas as pd
from typing import Dict, List, Any

class ReportGenerator:
    """Handles generation of different report types"""
    
    @staticmethod
    def generate_summary_report(df: pd.DataFrame, query_info: Dict) -> Dict[str, Any]:
        """Generate summary report from water quality data"""
        if df.empty:
            return {
                "total_records": 0,
                "date_range": "No data",
                "parameters": [],
                "organizations": [],
                "locations": []
            }
        
        summary = {
            "total_records": len(df),
            "date_range": {
                "start": df['ActivityStartDate'].min().isoformat() if not df['ActivityStartDate'].isnull().all() else None,
                "end": df['ActivityStartDate'].max().isoformat() if not df['ActivityStartDate'].isnull().all() else None
            },
            "parameters": df['CharacteristicName'].value_counts().head(10).to_dict(),
            "organizations": df['OrganizationIdentifier'].value_counts().head(10).to_dict(),
            "locations": df['MonitoringLocationIdentifier'].nunique(),
            "unique_parameters": df['CharacteristicName'].nunique()
        }
        
        return summary

    @staticmethod
    def generate_detailed_report(df: pd.DataFrame, query_info: Dict) -> List[Dict[str, Any]]:
        """Generate detailed report with individual records"""
        if df.empty:
            return []
        
        # Select relevant columns for detailed report
        detail_cols = [
            'OrganizationIdentifier', 'MonitoringLocationIdentifier', 
            'ActivityStartDate', 'CharacteristicName', 'ResultMeasureValue',
            'ResultMeasureUnitCode', 'ResultStatusIdentifier', 'ResultCommentText'
        ]
        
        available_cols = [col for col in detail_cols if col in df.columns]
        detail_df = df[available_cols].copy()
        
        # Convert to records
        records = detail_df.to_dict('records')
        
        # Clean up records
        for record in records:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif isinstance(value, pd.Timestamp):
                    record[key] = value.isoformat()
        
        return records

    @staticmethod
    def generate_trend_report(df: pd.DataFrame, query_info: Dict) -> Dict[str, Any]:
        """Generate trend analysis report"""
        if df.empty or 'ActivityStartDate' not in df.columns:
            return {"error": "Insufficient data for trend analysis"}
        
        # Group by year and parameter
        df['Year'] = df['ActivityStartDate'].dt.year
        
        trend_data = {}
        for param in df['CharacteristicName'].unique():
            if pd.isna(param):
                continue
                
            param_data = df[df['CharacteristicName'] == param]
            if 'ResultMeasureValue' in param_data.columns:
                yearly_stats = param_data.groupby('Year')['ResultMeasureValue'].agg([
                    'count', 'mean', 'median', 'std', 'min', 'max'
                ]).round(3)
                
                trend_data[param] = {
                    'yearly_statistics': yearly_stats.to_dict('index'),
                    'total_samples': len(param_data),
                    'years_covered': len(yearly_stats)
                }
        
        return trend_data