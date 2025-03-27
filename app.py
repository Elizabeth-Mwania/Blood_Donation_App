import streamlit as st
import pages.donor_profiles
from utils.data_loader import load_data, load_geo_data
# from utils.models import load_models
# from utils.helpers import apply_filters
import pages.overview
import pages.geographic
import pages.health
import pages.donor_profiles
import pages.campaign
# ... other page imports

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import pickle
from wordcloud import WordCloud
import io
from datetime import datetime, date

# Download NLTK data 
# nltk.download('vader_lexicon')
# nltk.download('stopwords')

# Configuration
PAGE_CONFIG = {
    "page_title": "Blood Donation Dashboard",
    "page_icon": "🩸",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

def main():
    """Main application function"""
    # Initialize app
    st.set_page_config(**PAGE_CONFIG)
    
    # Load data and models
    data = initialize_app()
    
    # Render sidebar navigation
    current_page = render_sidebar(data)
    
    # Render main content based on selected page
    render_page(current_page, data)

def initialize_app():
    """Initialize application data and models"""
    donor_candidates_birth, donors = load_data()
    geo_data = load_geo_data()
    # models = load_models()
    
    # Initialize session state
    if 'new_candidates' not in st.session_state:
        st.session_state.new_candidates = pd.DataFrame()
    if 'new_donors' not in st.session_state:
        st.session_state.new_donors = pd.DataFrame()
    
    return {
        'donor_candidates': donor_candidates_birth,
        'donors': donors,
        'geo_data': geo_data,
        # 'models': models
    }

def render_sidebar(data):
    """Render sidebar navigation and filters"""
    with st.sidebar:
        st.image("assets/images/blood2.png", width=200)
        st.markdown("## Navigation")
        
        page_options = [
            "Overview", "Geographic Distribution", "Health Conditions", 
            "Donor Profiles", "Campaign Effectiveness", "Donor Retention", 
            "Sentiment Analysis", "Eligibility Prediction", "Data Collection"
        ]
        page = st.radio("Select Dashboard Page", page_options)
        
        st.markdown("---")
        st.markdown("## Filters")
        
        if data['donor_candidates'] is not None:
            age_min, age_max = int(data['donor_candidates']['age'].min()), int(data['donor_candidates']['age'].max())
            age_range = st.slider("Age Range", age_min, age_max, (age_min, age_max))
            
            gender_options = ['All'] + data['donor_candidates']['gender'].unique().tolist()
            gender = st.selectbox("Gender", gender_options)
            
            district_options = ['All'] + data['donor_candidates']['residence_district'].unique().tolist()
            district = st.selectbox("District", district_options)
            
            data['filters'] = {
                'age_range': age_range,
                'gender': gender,
                'district': district
            }
    
    return page

def render_page(page, data):
    """Render the selected page content"""
    # Render header (common to all pages)
    render_header()
    
    # Route to the appropriate page
    if page == "Overview":
        pages.overview.render(data)
    elif page == "Geographic Distribution":
        pages.geographic.render(data)
    elif page == "Health Conditions":
        pages.health.render(data)
    elif page == "Donor Profiles":
        pages.donor_profiles.render()
    elif page == "Campaign Effectiveness":
        pages.campaign.render(data)
    # ... other page routes

def render_header():
    """Render the common header section"""
    st.title("Blood Donation Dashboard")
    # Load CSS from external file
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header">
        <div class="logo-section">
            <div>
                <div class="title">CodeFlow</div>
                <div class="subtitle">Blood Donation Platform</div>
            </div>
        </div>
        <div class="tagline">
            <div class="tagline-main">❤️ Every Drop Saves Lives</div>
            <div class="tagline-sub">Connecting Donors | Saving Communities</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()