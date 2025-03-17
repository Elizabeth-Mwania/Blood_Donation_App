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
    df_2019 = df[0]
    df_2020 = df[1]
    df_Volonteer = df[2]
    RAS = "--"
    
    columns_names_2019 = df_2019.columns.to_list()
    selected_columns_2019 = [col for col in columns_names_2019 if col in ['Date de naissance', "Niveau d'etude", 'Genre', 'Situation Matrimoniale (SM)', 'Religion']]
    columns_names_volonteer = df_Volonteer.columns.to_list()
    selected_columns_volonteer = [col for col in columns_names_volonteer if col in ['Age_', "Niveau_d'etude", 'Genre_', 'Situation_Matrimoniale_(SM)', 'Religion_']]

    #print(columns_names_2019)
    
    st.title("Blood Donation Campaign Analytics")
    st.subheader("Dashboard Overview")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Donors", f"{len(df[3]):,}")
    with col2:
        eligible1 = df[3][df[3]['ÉLIGIBILITÉ AU DON.'] == 'Eligible'].shape[0]
        eligible2 = df[3][df[3]['ÉLIGIBILITÉ_AU_DON.'] == 'Eligible'].shape[0]
        st.metric("Eligible Donors", f"{eligible1 + eligible2:,} ({(eligible1 + eligible2)/len(df[3]):.1%})")
    with col3:
        st.metric("Districts Covered", f"{df[3]['Arrondissement de résidence'].nunique()}")
    with col4:
        same_quarter, different_quarter = 0, 0
        for i in range(len(df_2019['Quartier de Résidence'].unique())):
            for j in range(len(df_Volonteer['Quartier_de_Résidence_'].unique())):
                if i == j :
                    if df_2019['Quartier de Résidence'].unique()[i] == df_Volonteer['Quartier_de_Résidence_'].unique()[j]:
                        same_quarter += 1
                    else:
                        different_quarter += 2 
        #for quarter1 in df_2019['Quartier de Résidence'].unique():
        #    for quarter2 in df_Volonteer['Quartier_de_Résidence_'].unique():
        #        if quarter1 == quarter2:
        #            same_quarter += 1
        #        else:
        #            different_quarter += 2
        st.metric("Quarters Covered", f"{same_quarter + different_quarter}")


    col1_1, col1_2, col1_3 = st.columns(3)
    #st.subheader("Campaign 2019")
    with col1_1:
        st.metric("Total Donors in 2019", f"{len(df_2019):,}")
        eligible = df_2019[df_2019['ÉLIGIBILITÉ AU DON.'] == 'Eligible'].shape[0]
        st.metric("Eligible Donors", f"{eligible:,} ({eligible/len(df_2019):.1%})")
        st.metric("Districts Covered", f"{df_2019['Arrondissement de résidence'].nunique()}")
        st.metric("Quarters Covered", f"{df_2019['Quartier de Résidence'].nunique()}")
    #with col4:

    #st.subheader("Campaign 2020")
    with col1_2:
        st.metric("Total Donors in 2020", f"{len(df_2020):,}")
        st.metric("Eligible Donors ", f"{RAS}")
        st.metric("Districts Covered ", f"{RAS}")
        st.metric("Quarters Covered", f"{RAS}")
    #with col4:

    #st.subheader("Volonteer Overview")
    with col1_3:
        st.metric("Total Donors for Volonteer", f"{len(df_Volonteer):,}")
        eligible = df_Volonteer[df_Volonteer['ÉLIGIBILITÉ_AU_DON.'] == 'Eligible'].shape[0]
        st.metric("Eligible Donors", f"{eligible:,} ({eligible/len(df_Volonteer):.1%})")
        st.metric("Districts Covered", f"{df_Volonteer['Arrondissement_de_résidence_'].nunique()}")
        st.metric("Quarters Covered", f"{df_Volonteer['Quartier_de_Résidence_'].nunique()}")
    #with col4:
    #    st.metric("Campaigns", f"{df['Campaign_ID'].nunique()}")
    
    # Dataset preview
    st.subheader("Dataset Preview")
    st.dataframe(df[3].head())
    
    # Basic distributions
    st.subheader("Basic Distributions / Data Quality Overview")
    year1, year2, volonteer = st.columns(3)

    with year1:
        year_2019 = st.checkbox("2019", value=True)
    
    with year2:
        year_2020 = st.checkbox("2020", value=False)

    with volonteer:
        page_volonteer = st.checkbox("Volonteer", value=False)

    # Display figures based on checkbox selection
    if year_2019:
        # Dataset description
        st.subheader("Dataset Statistics for 2019")
        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            st.subheader("Summary Statistics for 2019")
            st.write(df_2019.describe())
        with col1_2:
            st.subheader("Missing values - Percentage: 2029")
            missing_data = pd.DataFrame({
                'Missing Values': df_2019.isnull().sum(),
                'Percentage': df_2019.isnull().sum() / len(df_2019) * 100
            }).sort_values('Missing Values', ascending=False)
        
            st.write(missing_data[missing_data['Missing Values'] > 0])
        with col1_3:
            st.metric("Total Donors in 2019", f"{len(df_2019):,}")
            eligible = df_2019[df_2019['ÉLIGIBILITÉ AU DON.'] == 'Eligible'].shape[0]
            st.metric("Eligible Donors", f"{eligible:,} ({eligible/len(df_2019):.1%})")
            st.metric("Districts Covered", f"{df_2019['Arrondissement de résidence'].nunique()}")
            st.metric("Quarters Covered", f"{df_2019['Quartier de Résidence'].nunique()}")

        st.subheader("Data Distribution for 2019")
        variables = st.selectbox(
        "Select Valriables to display Distribution Analysis:",
        selected_columns_2019, key="variables_distribution_2019")
        columns = st.columns(len(selected_columns_2019))
        for i, col in enumerate(columns):
            with col:
                if i == 0:
                    df_2019['Date de naissance'] = pd.to_datetime(df_2019['Date de naissance'], errors='coerce')
                    df_2019['Age'] = 2019 - df_2019['Date de naissance'].dt.year
                    fig = px.histogram(df_2019, x='Age', title='Age Distribution for 2019')
                    st.plotly_chart(fig, use_container_width=True)
                elif i == 1:
                    fig = px.pie(df_2019, names='Niveau d\'etude', title='Education Level Distribution for 2019')
                    st.plotly_chart(fig, use_container_width=True)
                elif i == 2:
                    fig = px.pie(df_2019, names='Genre', title='Gender Distribution for 2019')
                    st.plotly_chart(fig, use_container_width=True)
                elif i == 3:
                    fig = px.pie(df_2019, names='Situation Matrimoniale (SM)', title='Marital Status Distribution for 2019')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig = px.pie(df_2019, names='Religion', title='Religion Distribution for 2019')
                    st.plotly_chart(fig, use_container_width=True)

        st.subheader("Blood Donation by Classes")
        col1, col2 = st.columns(2)
        with col1:
            # Count occurrences for each Religion & Blood Donation status
            df_count_religion_2019 = df_2019.groupby(["Religion", "A-t-il (elle) déjà donné le sang"]).size().reset_index(name="Count")

            # Create a bar plot
            fig = px.bar(
                df_count_religion_2019,
                x="Religion",
                y="Count",
                color="A-t-il (elle) déjà donné le sang",
                title="Blood Donation by Religion",
                barmode="group",  # Change to 'stack' if you want stacked bars
                color_discrete_map={"Oui": "#4CAF50", "Non": "#F44336"}  # Green for Yes, Red for No
            )
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            # Count occurrences for each Education Level & Blood Donation status
            df_count_etude_2019 = df_2019.groupby(["Niveau d'etude", "A-t-il (elle) déjà donné le sang"]).size().reset_index(name="Count")

            # Create a bar plot
            fig = px.bar(
                df_count_etude_2019,
                x="Niveau d'etude",
                y="Count",
                color="A-t-il (elle) déjà donné le sang",
                title="Blood Donation by Education Level",
                barmode="group",  # Change to 'stack' if you want stacked bars
                color_discrete_map={"Oui": "#4CAF50", "Non": "#F44336"}  # Green for Yes, Red for No
            )
            st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        with col3:
            # Count occurrences for
            df_count_genre_2019 = df_2019.groupby(["Genre", "A-t-il (elle) déjà donné le sang"]).size().reset_index(name="Count")

            # Create a bar plot
            fig = px.bar(
                df_count_genre_2019,
                x="Genre",
                y="Count",
                color="A-t-il (elle) déjà donné le sang",
                title="Blood Donation by Gender",
                barmode="group",  # Change to 'stack' if you want stacked bars
                color_discrete_map={"Oui": "#4CAF50", "Non": "#F44336"}  # Green for Yes, Red for No
            )
            st.plotly_chart(fig, use_container_width=True)
        with col4:
            # Count occurrences for
            df_count_SM_2019 = df_2019.groupby(["Situation Matrimoniale (SM)", "A-t-il (elle) déjà donné le sang"]).size().reset_index(name="Count")

            # Create a bar plot
            fig = px.bar(
                df_count_SM_2019,
                x="Situation Matrimoniale (SM)",
                y="Count",
                color="A-t-il (elle) déjà donné le sang",
                title="Blood Donation by Marital Status",
                barmode="group",  # Change to 'stack' if you want stacked bars
                color_discrete_map={"Oui": "#4CAF50", "Non": "#F44336"}  # Green for Yes, Red for No
            )
            st.plotly_chart(fig, use_container_width=True)

   
    if year_2020:
        # Dataset description
        st.subheader("Dataset Statistics for 2020")
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.subheader("Summary Statistics for 2020")
            st.write(df_2020.describe())
        with col1_2:
            st.subheader("Missing values - Percentage : 2020")
            missing_data = pd.DataFrame({
                'Missing Values': df_2020.isnull().sum(),
                'Percentage': df_2020.isnull().sum() / len(df_2019) * 100
            }).sort_values('Missing Values', ascending=False)
        
            st.write(missing_data[missing_data['Missing Values'] > 0])

        st.subheader("Data Distribution for 2020")
        col1, col2= st.columns(2)
        with col1:
            fig = px.pie(df_2020, names='Sexe', title='Gender Distribution for 2020')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.histogram(df_2020, x='Age ', title='Age Distribution for 2020')
            st.plotly_chart(fig, use_container_width=True)
        col3, col4 = st.columns(2)
        with col3:
            df_sanguin = pd.DataFrame(df_2020, columns=["Groupe Sanguin ABO / Rhesus "])
            # Count occurrences
            sanguin_counts = df_sanguin["Groupe Sanguin ABO / Rhesus "].value_counts().reset_index()
            sanguin_counts.columns = ["Blood group", "Count"]
            # Create interactive bar chart
            fig = px.bar(
                sanguin_counts,
                x='Blood group',
                y='Count',
                title='Distribution of Blood Types',
                color='Count',
                color_continuous_scale='reds'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            df_donation = pd.DataFrame(df_2020, columns=["Type de donation"])
            # Count occurrences
            donation_counts = df_donation["Type de donation"].value_counts().reset_index()
            donation_counts.columns = ["Type of donation", "Count"]
            # Create interactive bar chart
            fig = px.bar(
                donation_counts,
                x='Type of donation',
                y='Count',
                title='Distribution of Donation Types',
                color='Count',
                color_continuous_scale='redor'
            )
            st.plotly_chart(fig, use_container_width=True)

    if page_volonteer:
        # Dataset description
        st.subheader("Dataset Statistics for Volonteer")
        col1_1, col1_2 = st.columns(2)
        with col1_1:
            st.subheader("Summary Statistics for Volonteer")
            st.write(df_Volonteer.describe())
        with col1_2:
            st.subheader("Missing values - Percentage: Volonteer")
            missing_data = pd.DataFrame({
                'Missing Values': df_Volonteer.isnull().sum(),
                'Percentage': df_Volonteer.isnull().sum() / len(df_Volonteer) * 100
            }).sort_values('Missing Values', ascending=False)
        
            st.write(missing_data[missing_data['Missing Values'] > 0])
        
        st.subheader("Data Distribution for VOlonteer")
        variables = st.selectbox(
        "Select Valriables to display Distribution Analysis:",
        selected_columns_volonteer, key="variables_distribution_volonteer")
        columns = st.columns(len(selected_columns_volonteer))
        for i, col in enumerate(columns):
            with col:
                if i == 0:
                    fig = px.histogram(df_Volonteer, x='Age_', title='Age Distribution for Volonteer')
                    st.plotly_chart(fig, use_container_width=True)
                elif i == 1:
                    fig = px.pie(df_Volonteer, names='Niveau_d\'etude', title='Education Level Distribution for Volonteer')
                    st.plotly_chart(fig, use_container_width=True)
                elif i == 2:
                    fig = px.pie(df_Volonteer, names='Genre_', title='Gender Distribution for Volonteer')
                    st.plotly_chart(fig, use_container_width=True)
                elif i == 3:
                    fig = px.pie(df_Volonteer, names='Situation_Matrimoniale_(SM)', title='Marital Status Distribution for Volonteer')
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig = px.pie(df_Volonteer, names='Religion_', title='Religion Distribution for Volonteer')
                    st.plotly_chart(fig, use_container_width=True)

        st.subheader("Blood Donation by Classes")
        col1, col2 = st.columns(2)
        with col1:
            # Count occurrences for each Religion & Blood Donation status
            df_count_religion_volonteer = df_Volonteer.groupby(["Religion_", "A-t-il_(elle)_déjà_donné_le_sang_"]).size().reset_index(name="Count")

            # Create a bar plot
            fig = px.bar(
                df_count_religion_volonteer,
                x="Religion_",
                y="Count",
                color="A-t-il_(elle)_déjà_donné_le_sang_",
                title="Blood Donation by Religion",
                barmode="group",  # Change to 'stack' if you want stacked bars
                color_discrete_map={"Oui": "#4CAF50", "Non": "#F44336"}  # Green for Yes, Red for No
            )
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            # Count occurrences for each Education Level & Blood Donation status
            df_count_etude_volonteer = df_Volonteer.groupby(["Niveau_d'etude", "A-t-il_(elle)_déjà_donné_le_sang_"]).size().reset_index(name="Count")

            # Create a bar plot
            fig = px.bar(
                df_count_etude_volonteer,
                x="Niveau_d'etude",
                y="Count",
                color="A-t-il_(elle)_déjà_donné_le_sang_",
                title="Blood Donation by Education Level",
                barmode="group",  # Change to 'stack' if you want stacked bars
                color_discrete_map={"Oui": "#4CAF50", "Non": "#F44336"}  # Green for Yes, Red for No
            )
            st.plotly_chart(fig, use_container_width=True)
        
        col3, col4 = st.columns(2)
        with col3:
            # Count occurrences for
            df_count_Gender_volonteer = df_Volonteer.groupby(["Genre_", "A-t-il_(elle)_déjà_donné_le_sang_"]).size().reset_index(name="Count")

            # Create a bar plot
            fig = px.bar(
                df_count_Gender_volonteer,
                x="Genre_",
                y="Count",
                color="A-t-il_(elle)_déjà_donné_le_sang_",
                title="Blood Donation by Gender",
                barmode="group",  # Change to 'stack' if you want stacked bars
                color_discrete_map={"Oui": "#4CAF50", "Non": "#F44336"}  # Green for Yes, Red for No
            )
            st.plotly_chart(fig, use_container_width=True)
        with col4:
            # Count occurrences for
            df_count_SM_volonteer = df_Volonteer.groupby(["Situation_Matrimoniale_(SM)", "A-t-il_(elle)_déjà_donné_le_sang_"]).size().reset_index(name="Count")

            # Create a bar plot
            fig = px.bar(
                df_count_SM_volonteer,
                x="Situation_Matrimoniale_(SM)",
                y="Count",
                color="A-t-il_(elle)_déjà_donné_le_sang_",
                title="Blood Donation by Marital Status",
                barmode="group",  # Change to 'stack' if you want stacked bars
                color_discrete_map={"Oui": "#4CAF50", "Non": "#F44336"}  # Green for Yes, Red for No
            )
            st.plotly_chart(fig, use_container_width=True)


def show_health_eligibility(df):
    df_2019 = df[0]
    df_2020 = df[1]
    df_Volonteer = df[2]
    df_All = df[3]
    RAS = "--"

    st.title("Health and Eligibility Analysis")
    
    # Eligibility overview
    st.subheader("Eligibility Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        eligible = df_All[df_All['ÉLIGIBILITÉ AU DON.'] == 'Eligible'].shape[0]
        st.metric("Eligible Donors", f"{eligible:,}")
    
    with col2:
        ineligible = df_All[df_All['ÉLIGIBILITÉ AU DON.'] != 'Eligible'].shape[0]
        st.metric("Ineligible Donors", f"{ineligible:,}")
    
    with col3:
        st.metric("Eligibility Rate", f"{eligible/len(df_All):.1%}")
    
    # Reasons for ineligibility
    st.subheader("Reasons for Ineligibility")
    
    # Simulated reasons data
    reasons = pd.DataFrame({
        'Reason': ['Low Hemoglobin', 'Recent Illness', 'Low Weight', 'High Blood Pressure', 'Recent Medication'],
        'Count': [120, 80, 60, 40, 30]
    })
    
    fig = px.bar(
        reasons,
        x='Reason',
        y='Count',
        title='Top Reasons for Ineligibility',
        color='Count',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Health metrics distribution
    st.subheader("Health Metrics Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(
            df_All,
            x="Taux d’hémoglobine",
            title='Hemoglobin Level Distribution',
            color='ÉLIGIBILITÉ AU DON.',
            color_discrete_map={1: '#4CAF50', 0: '#F44336'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(
            df_All,
            x='ÉLIGIBILITÉ AU DON.',
            y='Taux d’hémoglobine',
            title='Hemoglobin Level by Eligibility',
            color='ÉLIGIBILITÉ AU DON.',
            color_discrete_map={1: '#4CAF50', 0: '#F44336'}
        )
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
    elif page == "Health & Eligibility":
        show_health_eligibility(df)
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