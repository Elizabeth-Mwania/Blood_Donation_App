import streamlit as st
import plotly.express as px
import pandas as pd
from utils.helpers import apply_filters
def render(data):
    """Render the overview page"""
    st.markdown("<div class='sub-header'>Key Metrics</div>", unsafe_allow_html=True)
    
    # Apply filters
    filtered_candidates = apply_filters(data['donor_candidates'], data['filters'])
    filtered_donors = apply_filters(data['donors'], data['filters'])
    
    # Display metrics
    display_metrics(filtered_candidates, filtered_donors)
    
    # Display charts
    display_charts(filtered_candidates, filtered_donors)

def display_metrics(donor_candidates_birth, donors):
    """Display key metrics in a row"""
    metrics_row = st.columns(4)

    if donor_candidates_birth is not None and donors is not None:
        with metrics_row[0]:
            total_candidates = len(donor_candidates_birth)
            st.markdown(f'<div class="metric-container"><h3>Total Candidates</h3>'
                        f'<p class="highlight" style="font-size: 2rem;">{total_candidates}</p></div>',
                        unsafe_allow_html=True)

        with metrics_row[1]:
            total_donors = len(donors)
            conversion_rate = round((total_donors / total_candidates) * 100, 1) if total_candidates > 0 else 0
            st.markdown(f'<div class="metric-container"><h3>Total Donors</h3>'
                        f'<p class="highlight" style="font-size: 2rem;">{total_donors}</p>'
                        f'<p>Conversion Rate: {conversion_rate}%</p></div>',
                        unsafe_allow_html=True)

        with metrics_row[2]:
            if 'gender' in donors.columns:
                gender_counts = donors['gender'].value_counts()
                male_pct = round((gender_counts.get('Homme', 0) / total_donors) * 100, 1) if total_donors > 0 else 0
                female_pct = round((gender_counts.get('Femme', 0) / total_donors) * 100, 1) if total_donors > 0 else 0
                st.markdown(f'<div class="metric-container"><h3>Gender Distribution</h3>'
                            f'<p>Male: <span class="highlight">{male_pct}%</span></p>'
                            f'<p>Female: <span class="highlight">{female_pct}%</span></p></div>',
                            unsafe_allow_html=True)

        with metrics_row[3]:
            if 'donation_type' in donors.columns:
                donation_type_counts = donors['donation_type'].value_counts()
                voluntary_pct = round((donation_type_counts.get('B', 0) / total_donors) * 100, 1) if total_donors > 0 else 0
                family_pct = round((donation_type_counts.get('F', 0) / total_donors) * 100, 1) if total_donors > 0 else 0
                st.markdown(f'<div class="metric-container"><h3>Donation Types</h3>'
                            f'<p>Voluntary: <span class="highlight">{voluntary_pct}%</span></p>'
                            f'<p>Family: <span class="highlight">{family_pct}%</span></p></div>',
                            unsafe_allow_html=True)


def display_charts(candidates, donors):
    """Display overview charts"""
    charts_row = st.columns(2)
    
    with charts_row[0]:
        display_blood_group_chart(donors)
    
    with charts_row[1]:
        display_age_distribution_chart(donors)

def display_blood_group_chart(donors):
    """Display blood group distribution chart"""
    if 'blood_group' in donors.columns:
        st.subheader("Blood Group Distribution")
        blood_group_counts = donors['blood_group'].value_counts()
        fig = px.pie(
            values=blood_group_counts.values, 
            names=blood_group_counts.index, 
            color_discrete_sequence=px.colors.sequential.Reds, 
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

def display_age_distribution_chart(donors):
    """Display age distribution chart"""
    if 'age' in donors.columns:
        st.subheader("Age Distribution of Donors")
        fig = px.histogram(
            donors, 
            x='age', 
            nbins=20, 
            color_discrete_sequence=['#B22222']
        )
        st.plotly_chart(fig, use_container_width=True)