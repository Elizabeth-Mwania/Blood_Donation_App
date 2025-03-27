import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="Campaign Effectiveness",
    page_icon="📊",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
<style>
.header-container {
    background: linear-gradient(to right, #fee2e2, #fff1f2);
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 2rem;
}
.main-header {
    color: #b91c1c;
    margin-bottom: 0.5rem !important;
}
.sub-header {
    color: #7f1d1d;
    font-size: 1.1rem;
}
.metric-card {
    background: white;
    border-radius: 10px;
    padding: 1.2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
    border-left: 4px solid #dc2626;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: bold;
    color: #b91c1c;
}
.metric-delta {
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

def load_campaign_data():
    """Load campaign data - replace with your actual data source"""
    return pd.DataFrame({
        'Channel': ['Social Media', 'Community Events', 'University Drives', 
                   'Radio', 'SMS', 'Partner Orgs'],
        'Impressions': [15000, 8000, 6500, 20000, 25000, 5000],
        'Conversions': [450, 380, 310, 280, 220, 180],
        'Cost': [5400, 3800, 3100, 4200, 3500, 2500]
    })

def show_metrics():
    """Display key performance metrics"""
    metrics_row = st.columns(3)
    with metrics_row[0]:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 1rem; color: #4b5563; margin-bottom: 0.5rem;'>Conversion Rate</div>
            <div class='metric-value'>28.5%</div>
            <div class='metric-delta' style='color: #16a34a;'>↑ 3.2% from last quarter</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metrics_row[1]:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 1rem; color: #4b5563; margin-bottom: 0.5rem;'>Cost per Donor</div>
            <div class='metric-value'>$12.80</div>
            <div class='metric-delta' style='color: #16a34a;'>↓ $2.40 from last quarter</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metrics_row[2]:
        st.markdown("""
        <div class='metric-card'>
            <div style='font-size: 1rem; color: #4b5563; margin-bottom: 0.5rem;'>ROI</div>
            <div class='metric-value'>320%</div>
            <div class='metric-delta' style='color: #16a34a;'>↑ 15% from last quarter</div>
        </div>
        """, unsafe_allow_html=True)

def show_channel_performance(df):
    """Display channel performance visualizations"""
    df['Conversion_Rate'] = (df['Conversions']/df['Impressions']*100).round(1)
    df['Cost_Per_Conversion'] = (df['Cost']/df['Conversions']).round(2)
    
    tab1, tab2, tab3 = st.tabs(["Overview", "Conversion Rates", "Cost Analysis"])
    
    with tab1:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(x=df['Channel'], y=df['Impressions'], name='Impressions',
                  marker_color='#93c5fd', opacity=0.7),
            secondary_y=False
        )
        fig.add_trace(
            go.Bar(x=df['Channel'], y=df['Conversions'], name='Conversions',
                  marker_color='#ef4444', opacity=0.7),
            secondary_y=False
        )
        fig.add_trace(
            go.Scatter(x=df['Channel'], y=df['Conversion_Rate'], 
                      name='Conversion Rate %', line=dict(color='#7c3aed', width=3),
                      mode='lines+markers'),
            secondary_y=True
        )
        fig.update_layout(
            title='Performance Across Channels',
            xaxis_title='Marketing Channel',
            yaxis_title='Count',
            yaxis2_title='Conversion Rate (%)',
            height=500,
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = px.bar(
            df, x='Channel', y='Conversion_Rate', color='Channel',
            title='Conversion Rates by Channel', text='Conversion_Rate',
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(yaxis_title='Conversion Rate (%)', height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = go.Figure()
        fig.add_trace(
            go.Bar(x=df['Channel'], y=df['Cost_Per_Conversion'],
                  name='Cost per Conversion', marker_color='#f97316')
        )
        fig.update_layout(
            title='Cost Efficiency by Channel',
            yaxis_title='Cost per Conversion ($)',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

def show_recommendations():
    """Display optimization recommendations"""
    with st.expander("🚀 Optimization Recommendations", expanded=True):
        st.markdown("""
        - **Double down on Social Media**: Highest conversion rate (3.0%) at moderate cost
        - **Increase Community Events budget**: Second highest conversions despite fewer impressions
        - **Improve SMS targeting**: High impressions but low conversion rate (0.88%)
        - **Maintain Radio campaigns**: Good reach but needs better conversion optimization
        - **Review Partner Orgs strategy**: Low volume but highest conversion rate (3.6%)
        """)

def main():
    """Main page function"""
    # Page header
    st.markdown("""
    <div class='header-container'>
        <h2 class='main-header'>📊 Campaign Effectiveness Dashboard</h2>
        <p class='sub-header'>Analyze performance across all donation campaigns</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    campaign_data = load_campaign_data()
    
    # Show metrics
    show_metrics()
    st.markdown("---")
    
    # Show channel performance
    st.markdown("### 📈 Campaign Performance by Channel")
    show_channel_performance(campaign_data)
    
    # Show recommendations
    st.markdown("---")
    show_recommendations()

if __name__ == "__main__":
    main()