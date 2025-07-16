"""
Data cleaning and validation functionality
"""
import pandas as pd

class DataProcessor:
    """Handles data cleaning and validation"""
    
    @staticmethod
    def clean_and_validate_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and validate water quality data"""
        if df.empty:
            return df
        
        # Remove rows with missing essential data
        essential_cols = ['OrganizationIdentifier', 'MonitoringLocationIdentifier', 
                         'ActivityStartDate', 'CharacteristicName']
        
        for col in essential_cols:
            if col in df.columns:
                df = df.dropna(subset=[col])
        
        # Clean numeric columns
        numeric_cols = ['ResultMeasureValue', 'DetectionQuantitationLimitMeasureValue']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert date columns
        date_cols = ['ActivityStartDate', 'ActivityEndDate']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df
    
    @staticmethod
    def limit_records(df: pd.DataFrame, max_records: int) -> pd.DataFrame:
        """Limit the number of records"""
        if len(df) > max_records:
            return df.head(max_records)
        return df