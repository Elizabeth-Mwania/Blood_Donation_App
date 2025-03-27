import pandas as pd
import streamlit as st
from typing import Dict, Any

def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply filters to a DataFrame based on the filter criteria.
    
    Args:
        df: The DataFrame to filter
        filters: Dictionary containing filter parameters
        
    Returns:
        Filtered DataFrame
    """
    if df is None or not isinstance(df, pd.DataFrame):
        return pd.DataFrame()
    
    filtered_df = df.copy()
    
    # Age filter
    if 'age' in filtered_df.columns and 'age_range' in filters:
        age_min, age_max = filters['age_range']
        filtered_df = filtered_df[
            (filtered_df['age'] >= age_min) & 
            (filtered_df['age'] <= age_max)
        ]
    
    # Gender filter
    if 'gender' in filtered_df.columns and 'gender' in filters and filters['gender'] != 'All':
        filtered_df = filtered_df[filtered_df['gender'] == filters['gender']]
    
    # District filter
    if ('residence_district' in filtered_df.columns and 
        'district' in filters and 
        filters['district'] != 'All'):
        filtered_df = filtered_df[filtered_df['residence_district'] == filters['district']]
    
    return filtered_df

def metric(title: str, value: Any, delta: str = None) -> None:
    """
    Display a metric card with consistent styling.
    
    Args:
        title: Title of the metric
        value: The value to display
        delta: Optional delta value (change indicator)
    """
    st.markdown(
        f"""
        <div class="metric-container">
            <h3>{title}</h3>
            <p class="highlight" style="font-size: 2rem;">{value}</p>
            {f'<p>{delta}</p>' if delta else ''}
        </div>
        """, 
        unsafe_allow_html=True
    )

def calculate_conversion_rate(donors: pd.DataFrame, candidates: pd.DataFrame) -> float:
    """
    Calculate the conversion rate from candidates to donors.
    
    Args:
        donors: DataFrame of donors
        candidates: DataFrame of candidates
        
    Returns:
        Conversion rate as a percentage (0-100)
    """
    if donors.empty or candidates.empty:
        return 0.0
    return round((len(donors) / len(candidates)) * 100, 1)

def get_eligibility_stats(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate eligibility statistics from candidate data.
    
    Args:
        df: DataFrame containing candidate data
        
    Returns:
        Dictionary with eligibility statistics
    """
    stats = {
        'eligible_count': 0,
        'ineligible_count': 0,
        'eligibility_rate': 0.0
    }
    
    if df.empty or 'is_eligible' not in df.columns:
        return stats
    
    stats['eligible_count'] = df['is_eligible'].sum()
    stats['ineligible_count'] = len(df) - stats['eligible_count']
    stats['eligibility_rate'] = round((stats['eligible_count'] / len(df)) * 100, 1)
    
    return stats

def get_gender_distribution(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate gender distribution percentages.
    
    Args:
        df: DataFrame containing gender data
        
    Returns:
        Dictionary with gender percentages
    """
    distribution = {
        'male_pct': 0.0,
        'female_pct': 0.0
    }
    
    if df.empty or 'gender' not in df.columns:
        return distribution
    
    gender_counts = df['gender'].value_counts()
    total = len(df)
    
    distribution['male_pct'] = round((gender_counts.get('Homme', 0) / total) * 100, 1)
    distribution['female_pct'] = round((gender_counts.get('Femme', 0) / total) * 100, 1)
    
    return distribution

def get_blood_type_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Get blood type distribution from donor data.
    
    Args:
        df: DataFrame containing blood group data
        
    Returns:
        Series with blood type counts
    """
    if df.empty or 'blood_group' not in df.columns:
        return pd.Series(dtype='float64')
    return df['blood_group'].value_counts()