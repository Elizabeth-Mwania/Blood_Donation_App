import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import apply_filters

def render(data):
    """Render the Health Conditions page"""
    st.markdown("<div class='sub-header'>Health Conditions Analysis</div>", unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = apply_filters(data['donor_candidates'], data['filters'])
    
    # Main health condition visualizations
    render_eligibility_analysis(filtered_df)
    render_health_metrics(filtered_df)

def render_eligibility_analysis(df):
    """Render the eligibility and rejection reasons analysis"""
    charts_row = st.columns(2)
    
    with charts_row[0]:
        render_rejection_reasons_chart(df)
    
    with charts_row[1]:
        render_hemoglobin_distribution(df)

def render_rejection_reasons_chart(df):
    """Visualize reasons for donor rejection"""
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("Eligibility by Health Condition")
    
    if df.empty:
        st.warning("No data available after filtering")
        return
    
    # Prepare rejection reasons data
    rejection_data = prepare_rejection_data(df)
    
    # Create visualization
    fig = px.bar(
        rejection_data,
        x='Count',
        y='Reason',
        orientation='h',
        color='Count',
        color_continuous_scale='Reds',
        title="Top Rejection Reasons"
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def prepare_rejection_data(df):
    """Prepare rejection reasons data for visualization"""
    # Count each rejection reason (modify based on your actual columns)
    rejection_counts = {
        'Low Hemoglobin': df['ineligible_low_hemoglobin'].eq('Yes').sum(),
        'Recent Donation': df['ineligible_recent_donation'].eq('Yes').sum(),
        'Antibiotics': df['ineligible_antibiotics'].eq('Yes').sum(),
        'Recent STI': df['ineligible_recent_sti'].eq('Yes').sum(),
        'Pregnancy': df['female_ineligible_pregnant'].eq('Yes').sum(),
        'Recent Surgery': df['total_ineligible_surgery'].eq('Yes').sum()
    }
    
    # Convert to DataFrame and sort
    rejection_df = pd.DataFrame({
        'Reason': list(rejection_counts.keys()),
        'Count': list(rejection_counts.values())
    }).sort_values('Count', ascending=False)
    
    return rejection_df

def render_hemoglobin_distribution(df):
    """Visualize hemoglobin distribution by gender"""
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.subheader("Hemoglobin Levels Distribution")
    
    if df.empty or 'hemoglobin_level' not in df.columns or 'gender' not in df.columns:
        st.warning("Required data not available")
        return
    
    # Create figure
    fig = go.Figure()
    
    # Add male distribution
    fig.add_trace(go.Histogram(
        x=df[df['gender'] == 'Homme']['hemoglobin_level'],
        name='Male',
        marker_color='#1f77b4',
        opacity=0.7
    ))
    
    # Add female distribution
    fig.add_trace(go.Histogram(
        x=df[df['gender'] == 'Femme']['hemoglobin_level'],
        name='Female',
        marker_color='#ff7f0e',
        opacity=0.7
    ))
    
    # Add eligibility thresholds
    fig.add_shape(
        type="line",
        x0=13.0, y0=0, x1=13.0, y1=100,
        line=dict(color="red", width=2, dash="dash"),
        name="Min Male Level"
    )
    fig.add_shape(
        type="line",
        x0=12.0, y0=0, x1=12.0, y1=100,
        line=dict(color="orange", width=2, dash="dash"),
        name="Min Female Level"
    )
    
    # Update layout
    fig.update_layout(
        title="Hemoglobin Levels by Gender",
        xaxis_title="Hemoglobin Level (g/dL)",
        yaxis_title="Count",
        barmode='overlay',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_health_metrics(df):
    """Render health metrics in a 3-column layout"""
    metrics_row = st.columns(3)
    
    with metrics_row[0]:
        render_blood_pressure_analysis(df)
    
    with metrics_row[1]:
        render_weight_distribution(df)
    
    with metrics_row[2]:
        render_top_rejection_reasons(df)

def render_blood_pressure_analysis(df):
    """Visualize blood pressure distribution"""
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.subheader("Blood Pressure")
    
    # Simulate blood pressure data (replace with your actual data)
    systolic = df['blood_pressure_systolic'] if 'blood_pressure_systolic' in df.columns else None
    diastolic = df['blood_pressure_diastolic'] if 'blood_pressure_diastolic' in df.columns else None
    
    if systolic is None or diastolic is None:
        systolic = np.random.normal(120, 15, 200)
        diastolic = np.random.normal(80, 10, 200)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=systolic,
        y=diastolic,
        mode='markers',
        marker=dict(
            size=8,
            color=systolic,
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="Systolic")
        ),
        name="BP Readings"
    ))
    
    # Add healthy range
    fig.add_shape(
        type="rect",
        x0=90, y0=60, x1=120, y1=80,
        line=dict(color="green", width=2),
        fillcolor="rgba(0,255,0,0.1)",
        name="Normal"
    )
    
    fig.update_layout(
        title="Blood Pressure Distribution",
        xaxis_title="Systolic (mmHg)",
        yaxis_title="Diastolic (mmHg)",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_weight_distribution(df):
    """Visualize weight distribution"""
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.subheader("Weight Distribution")
    
    if df.empty or 'weight' not in df.columns:
        st.warning("Weight data not available")
        return
    
    fig = px.histogram(
        df,
        x='weight',
        nbins=30,
        color_discrete_sequence=['#B22222'],
        title="Weight Distribution (kg)"
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_top_rejection_reasons(df):
    """Show top rejection reasons in compact form"""
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.subheader("Common Rejection Reasons")
    
    if df.empty:
        st.warning("No data available")
        return
    
    rejection_data = prepare_rejection_data(df)
    top_reasons = rejection_data.head(3)
    
    for _, row in top_reasons.iterrows():
        st.metric(
            label=row['Reason'],
            value=row['Count'],
            help=f"Accounts for {row['Count']/len(df)*100:.1f}% of rejections"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)