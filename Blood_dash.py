import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from textblob import TextBlob
import requests
from PIL import Image
import pickle


# Set page configuration
st.set_page_config(
    page_title="Blood Donation Campaign Analytics",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Add custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e6394a;
        color: white;
    }
    h1, h2, h3 {
        color: #e6394a;
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    # Replace with actual data loading
    import pandas as pd

    # Load all sheets into a dictionary of DataFrames
    file_path = "/home/student24/Documents/AIMS_Folder/IndabaX_Cam/Project_test/data/Challenge dataset.xlsx"
    dfs = pd.read_excel(file_path, sheet_name=None)  # None loads all sheets

    # Access individual sheets
    df_2019 = dfs['2019']
    df_2020 = dfs['2020']
    df_Volonteer = dfs['Volontaire']

    df_combined = pd.concat(dfs.values(), ignore_index=True)

    return df_2019, df_2020, df_Volonteer, df_combined


# Individual page functions
def show_overview(df):
    st.title("Blood Donation Campaign Analytics")
    st.subheader("Dashboard Overview")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Donors", f"{len(df[3]):,}")
        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            st.metric("Total Donors in 2019", f"{len(df[0]):,}")
        with col1_2:
            st.metric("Total Donors in 2020", f"{len(df[1]):,}")
        with col1_3:
            st.metric("Total Donors for Volonteer", f"{len(df[2]):,}")
    with col2:
        eligible = df[df['ÉLIGIBILITÉ AU DON.'] == 'Eligible'].shape[0]
        st.metric("Eligible Donors", f"{eligible:,} ({eligible/len(df):.1%})")
    with col3:
        st.metric("Districts Covered", f"{df['Arrondissement de résidence'].nunique()}")
    #with col4:
    #    st.metric("Campaigns", f"{df['Campaign_ID'].nunique()}")
    
    # Dataset preview
    st.subheader("Dataset Preview")
    st.dataframe(df.head())
    
    # Dataset description
    st.subheader("Dataset Statistics")
    st.write(df.describe())
    
    # Data quality section
    st.subheader("Data Quality Overview")
    missing_data = pd.DataFrame({
        'Missing Values': df.isnull().sum(),
        'Percentage': df.isnull().sum() / len(df) * 100
    }).sort_values('Missing Values', ascending=False)
    
    st.write(missing_data[missing_data['Missing Values'] > 0])
    
    # Basic distributions
    st.subheader("Basic Distributions")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(df, names='Sexe', title='Gender Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.histogram(df, x='Age', title='Age Distribution')
        st.plotly_chart(fig, use_container_width=True)


# Main function
def main():
    # Sidebar
    st.sidebar.image("logo.png", width=150)
    st.sidebar.title("Blood Donation Dashboard")
    
    page = st.sidebar.selectbox(
        "Select a page:",
        ["Overview", "Donor Distribution", "Health & Eligibility", 
         "Donor Profiles", "Campaign Analysis", "Donor Retention", 
         "Feedback Analysis", "Eligibility Predictor"]
    )
    
    # Load data
    try:
        df = load_data()
        st.sidebar.success("Data loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading data: {e}")
        return
    
    # Display selected page
    if page == "Overview":
        show_overview(df)
    #elif page == "Donor Distribution":
    #    show_donor_distribution(df)
    #elif page == "Health & Eligibility":
    #    show_health_eligibility(df)
    #elif page == "Donor Profiles":
    #    show_donor_profiles(df)
    #elif page == "Campaign Analysis":
    #    show_campaign_analysis(df)
    #elif page == "Donor Retention":
    #    show_donor_retention(df)
    #elif page == "Feedback Analysis":
    #    show_feedback_analysis(df)
    #elif page == "Eligibility Predictor":
    #    show_eligibility_predictor(df)


if __name__ == "__main__":
    main()