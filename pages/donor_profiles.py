import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_cluster_data():
    """Load donor cluster dataset from Excel file."""
    return pd.read_excel("data/clustered_data.xlsx")  # Ensure the correct file path

def render():
    """Render the Donor Profiles page with cluster dataset filtering and visualization"""

    df = load_cluster_data()  # Load donor profile data

    # Sidebar Filters
    st.sidebar.header("Filter Options")

    # Numeric Filters
    age_range = st.sidebar.slider("Age Range", int(df["Age"].min()), int(df["Age"].max()), 
                                  (int(df["Age"].min()), int(df["Age"].max())))
    hemoglobin_range = st.sidebar.slider("Hemoglobin Range", float(df["Taux d\'hemoglobine"].min()), float(df["Taux d\'hemoglobine"].max()), 
                                         (float(df["Taux d\'hemoglobine"].min()), float(df["Taux d\'hemoglobine"].max())))
    weight_range = st.sidebar.slider("Weight Range", int(df["Poids"].min()), int(df["Poids"].max()), 
                                     (int(df["Poids"].min()), int(df["Poids"].max())))

    # Categorical Filters
    selected_gender = st.sidebar.multiselect("Select Gender", df["Genre"].unique(), default=df["Genre"].unique())
    selected_marital_status = st.sidebar.multiselect("Select Marital Status", df["Situation Matrimoniale (SM)"].unique(), 
                                                     default=df["Situation Matrimoniale (SM)"].unique())
    selected_cluster = st.sidebar.selectbox("Select Cluster", df["Cluster"].unique())  # Single cluster selection

    # Apply Filters
    filtered_df = df[
        (df["Age"].between(age_range[0], age_range[1])) &
        (df["Taux d\'hemoglobine"].between(hemoglobin_range[0], hemoglobin_range[1])) &
        (df["Poids"].between(weight_range[0], weight_range[1])) &
        (df["Genre"].isin(selected_gender)) &
        (df["Situation Matrimoniale (SM)"].isin(selected_marital_status)) &
        (df["Cluster"] == selected_cluster)
    ]

    # Title
    st.title("Donor Profile Summary and Visualization")

    # Display filtered data
    st.write(f"### Profile {selected_cluster} Data Preview")
    st.dataframe(filtered_df)

    # Cluster Summary Profile
    st.write(f"## Profile Summary for Cluster {selected_cluster}")

    # General Cluster Information
    cluster_count = len(filtered_df)
    total_count = len(df)
    percentage = (cluster_count / total_count) * 100

    st.write(f"### General Information")
    st.write(f"- **Total individuals in Cluster {selected_cluster}:** {cluster_count}")
    st.write(f"- **Percentage of total dataset:** {percentage:.2f}%")

    # Numeric Feature Averages
    st.write(f"### Numeric Feature Averages")
    num_features = ["Age", "Taux d\'hemoglobine", "Poids"]
    num_means = filtered_df[num_features].mean()
    st.write(pd.DataFrame(num_means).rename(columns={0: "Average"}).style.format({"Taux d\'hemoglobine": "{:.1f}"}))

    # Categorical Feature Distribution
    st.write(f"### Most Frequent Categories")

    categorical_features = [
        "Genre", "Situation Matrimoniale (SM)", "Religion", "Profession", 
        "Quartier de Residence", "Nationalite", "Niveau d\'etude"
    ]

    for col in categorical_features:
        most_common = filtered_df[col].value_counts().head(4)  # Show top 4 if many unique values
        
        if not most_common.empty:
            st.write(f"#### {col} Distribution")
            fig = px.bar(most_common, x=most_common.index, y=most_common.values, 
                         labels={"x": col, "y": "Count"}, text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
