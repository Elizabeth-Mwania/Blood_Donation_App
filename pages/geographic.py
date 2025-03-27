import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
from utils.helpers import apply_filters

def render(data):
    """Render the Geographic Distribution page"""
    st.markdown("<div class='sub-header'>Geographic Distribution of Donors</div>", unsafe_allow_html=True)
    
    # Apply filters
    filtered_candidates = apply_filters(data['donor_candidates'], data['filters'])
    
    # Create two-column layout
    map_col, stats_col = st.columns([3, 1])
    
    with map_col:
        render_map(filtered_candidates, data['geo_data'])
    
    with stats_col:
        render_statistics(filtered_candidates)

def render_map(candidates, geo_data):
    """Render the interactive map visualization"""
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    if geo_data is not None and candidates is not None:
        # Create base map centered on Douala
        m = folium.Map(location=[4.05, 9.7], zoom_start=12, tiles='CartoDB positron')
        
        # Add district boundaries (simplified example - in reality you'd use GeoJSON)
        for _, row in geo_data.iterrows():
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=10,
                popup=row['district'],
                color='#B22222',
                fill=True,
                fill_color='#B22222',
                fill_opacity=0.6
            ).add_to(m)
        
        # Add heatmap of donor candidates
        if 'residence_district' in candidates.columns:
            district_counts = candidates['residence_district'].value_counts()
            
            for district, count in district_counts.items():
                geo_row = geo_data[geo_data['district'] == district]
                if not geo_row.empty:
                    folium.CircleMarker(
                        location=[geo_row.iloc[0]['lat'], geo_row.iloc[0]['lon']],
                        radius=max(5, count / 5),  # Scale radius by count
                        popup=f"{district}: {count} candidates",
                        color='#B22222',
                        fill=True,
                        fill_opacity=0.7
                    ).add_to(m)
        
        # Display the map
        folium_static(m, width=700, height=500)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_statistics(candidates):
    """Render the statistics panel"""
    st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
    st.subheader("District Statistics")
    
    if candidates is not None and 'residence_district' in candidates.columns:
        # Top districts by donor count
        district_counts = candidates['residence_district'].value_counts()
        st.write("**Top Districts by Candidate Count:**")
        for district, count in district_counts.head(5).items():
            st.write(f"- {district}: *{count}*")
        
        st.write("---")
        
        # Donor density (simulated data)
        st.write("**Candidate Density (per km²):**")
        density_data = {
            'Douala I': 3.2,
            'Douala II': 2.8,
            'Douala III': 1.9,
            'Douala IV': 1.5,
            'Douala V': 2.1
        }
        for district, density in density_data.items():
            st.write(f"- {district}: *{density}*")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='metric-container' style='margin-top: 1rem;'>", unsafe_allow_html=True)
    st.subheader("Access Analysis")
    
    # Access metrics (simulated data)
    st.write("**Average Distance to Donation Center:**")
    st.metric("All Districts", "3.2 km")
    
    st.write("**Districts with Limited Access:**")
    st.write("- Douala IV: *5.8 km*")
    st.write("- Douala V (outskirts): *7.2 km*")
    
    st.markdown("</div>", unsafe_allow_html=True)