"""
================================================================================
TIGRAY INTEGRATED ANTICIPATORY EARLY WARNING SYSTEM (A-EWS)
Kiremt 2026 Tabia-Level Drought Assessment | Percent of Normal Rainfall Approach
Based on Ethiopian Meteorological Institute's (EMI) Tercile Probabilistic Forecast
================================================================================
Repository: https://github.com/Goitafa/Tigray-AEWS
Last Updated: June 12, 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
import json
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Tigray A-EWS - Kiremt 2026",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CONFIGURATION - GITHUB REPOSITORY INFORMATION
# ============================================================================

# Your GitHub repository information
GITHUB_USERNAME = "Goitafa"
REPO_NAME = "Tigray-AEWS"
BRANCH = "main"
JSON_FILE_PATH = "Tigray_Tabias_Kiremt_2026_Percent_of_Normal.json"

# Construct the raw GitHub URL
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/{BRANCH}/{JSON_FILE_PATH}"

# Author information - UPDATED
AUTHOR_NAME = "Yosef W. Kinfe"
AUTHOR_EMAIL = "Woyosef@caa.Columbia.edu / Woyosef@yahoo.com"
AUTHOR_TITLE = "Strategic Climate Systems Architect"
AUTHOR_ORGANIZATION = "Climate Adaptation Analytics"

# Dashboard information
DASHBOARD_VERSION = "2.0.0"
CURRENT_DATE = "June 12, 2026"
LAST_UPDATE = datetime.now().strftime("%B %d, %Y %H:%M")

# Color schemes
CATEGORY_COLORS = {
    'Extremely much below normal': '#4A0000',
    'Much below normal': '#8B0000',
    'Below normal': '#CC5500',
    'Near to normal': '#FFD700',
    'Above normal': '#228B22'
}

TIER_COLORS = {
    'Emergency': '#4A0000',
    'Action': '#8B0000',
    'Alert': '#CC5500',
    'Watch': '#FFD700'
}

@st.cache_data(ttl=3600, show_spinner="Loading Tigray assessment data from GitHub...")
def load_data_from_github():
    """Load Tigray tabia-level assessment data directly from GitHub repository"""
    try:
        response = requests.get(GITHUB_RAW_URL, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            return df
        else:
            st.error(f"Failed to load data from GitHub. Status code: {response.status_code}")
            st.info(f"Please ensure the file exists at: {GITHUB_RAW_URL}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Network error while loading data from GitHub: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON data: {str(e)}")
        return None

# Load the data
df = load_data_from_github()

if df is None:
    st.stop()

# Custom CSS styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7f9;
    }
    .data-status {
        font-size: 12px;
        color: #27ae60;
        text-align: center;
        padding: 5px;
        background-color: #e8f5e9;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .header-container {
        background: linear-gradient(135deg, #1a2a3a 0%, #2c3e50 100%);
        color: white;
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .warning-note {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.title("🌾 Tigray Integrated A-EWS")
    st.markdown("**Kiremt 2026 Early Warning System**")
    st.markdown(f"**Version:** {DASHBOARD_VERSION}")
    st.markdown(f"**Date:** {CURRENT_DATE}")
    st.markdown("---")
    
    st.markdown(
        '<div class="data-status">✅ Data loaded from GitHub</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("### 📡 Forecast Source")
    st.info(
        "**Ethiopian Meteorological Institute (EMI)**\n"
        "Kiremt 2026 Tercile Probabilistic Forecast\n"
        "June-September 2026"
    )
    st.markdown("---")
    
    st.markdown("### 🎯 Response Tiers")
    st.markdown("🔴 **Emergency** - ≤50% of normal")
    st.markdown("🟠 **Action** - 51-75% of normal")
    st.markdown("🟡 **Alert** - 76-90% of normal")
    st.markdown("🟢 **Watch** - >90% of normal")
    st.markdown("---")
    
    st.markdown("### 📊 Percent of Normal Categories")
    st.markdown("🔴 **≤50%** - Extremely much below normal")
    st.markdown("🟠 **51-75%** - Much below normal")
    st.markdown("🟡 **76-90%** - Below normal")
    st.markdown("🟢 **91-125%** - Near to normal")
    st.markdown("🔵 **>125%** - Above normal")
    st.markdown("---")
    
    st.markdown("### 👤 Dashboard Information")
    st.markdown(f"**Developer:** {AUTHOR_NAME}")
    st.markdown(f"**Title:** {AUTHOR_TITLE}")
    st.markdown(f"**Organization:** {AUTHOR_ORGANIZATION}")
    st.markdown(f"**Email:** {AUTHOR_EMAIL}")
    st.markdown(f"**Repository:** [GitHub](https://github.com/Goitafa/Tigray-AEWS)")
    st.markdown("---")
    
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.caption(f"Last sync: {LAST_UPDATE}")

# Header
st.markdown(
    f"""
    <div class="header-container">
        <h2 style="margin:0;">🌧️ TIGRAY INTEGRATED ANTICIPATORY EARLY WARNING SYSTEM</h2>
        <p style="margin:5px 0 0 0;">Kiremt 2026 Tabia-Level Drought Assessment</p>
        <p style="margin:5px 0 0 0; font-size:14px;">Percent of Normal = (Expected Rainfall / Climatological Mean) × 100</p>
        <p style="margin:5px 0 0 0; font-size:12px;">Based on EMI Tercile Probabilistic Seasonal Forecast</p>
        <p style="margin:5px 0 0 0; font-size:11px;">📅 Assessment Date: {CURRENT_DATE}</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("🌾 Tigray Integrated Anticipatory Early Warning Dashboard")
st.caption(f"Kiremt 2026 Season | Version {DASHBOARD_VERSION} | Last Updated: {LAST_UPDATE}")

# Warning note for users
st.markdown(
    """
    <div class="warning-note">
        ⚠️ <strong>Important:</strong> This dashboard is for Tigray regional planning and coordination purposes only.
        Anticipatory actions should be implemented based on response tier classifications.
    </div>
    """,
    unsafe_allow_html=True
)

# Key metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📊 Total Tabias", f"{len(df):,}")

with col2:
    emergency = len(df[df['RESPONSE_TIER'] == 'Emergency'])
    st.metric("🚨 Emergency", emergency, delta=f"{emergency/len(df)*100:.0f}%")

with col3:
    action = len(df[df['RESPONSE_TIER'] == 'Action'])
    st.metric("🔴 Action", action, delta=f"{action/len(df)*100:.0f}%")

with col4:
    alert = len(df[df['RESPONSE_TIER'] == 'Alert'])
    st.metric("🟠 Alert", alert, delta=f"{alert/len(df)*100:.0f}%")

with col5:
    avg_pct = df['PERCENT_OF_NORMAL'].mean()
    st.metric("📉 Avg % of Normal", f"{avg_pct:.1f}%")

st.markdown("---")

# Filters - Updated column names
st.subheader("🔍 Filter Dashboard Data")

col1, col2, col3, col4 = st.columns(4)

with col1:
    zones = ["All"] + sorted(df['ZONE'].unique().tolist())
    selected_zone = st.selectbox("Zone", zones)

with col2:
    if selected_zone != "All":
        filtered_by_zone = df[df['ZONE'] == selected_zone]
    else:
        filtered_by_zone = df
    woredas = ["All"] + sorted(filtered_by_zone['WEREDA'].unique().tolist())
    selected_woreda = st.selectbox("Woreda", woredas)

with col3:
    if selected_woreda != "All":
        filtered_by_woreda = filtered_by_zone[filtered_by_zone['WEREDA'] == selected_woreda]
    else:
        filtered_by_woreda = filtered_by_zone
    tabias = ["All"] + sorted(filtered_by_woreda['TABIA'].unique().tolist())
    selected_tabia = st.selectbox("Tabia", tabias)

with col4:
    tiers = ["All"] + sorted(df['RESPONSE_TIER'].unique().tolist())
    selected_tier = st.selectbox("Response Tier", tiers)

# Apply filters
filtered_df = df.copy()
if selected_zone != "All":
    filtered_df = filtered_df[filtered_df['ZONE'] == selected_zone]
if selected_woreda != "All":
    filtered_df = filtered_df[filtered_df['WEREDA'] == selected_woreda]
if selected_tabia != "All":
    filtered_df = filtered_df[filtered_df['TABIA'] == selected_tabia]
if selected_tier != "All":
    filtered_df = filtered_df[filtered_df['RESPONSE_TIER'] == selected_tier]

st.caption(f"Showing {len(filtered_df)} Tabias in Tigray")

# Most affected tabias
st.subheader("⚠️ Most At-Risk Tabias in Tigray")

tabia_summary = filtered_df.groupby(['ZONE', 'WEREDA', 'TABIA']).agg({
    'PERCENT_OF_NORMAL': 'mean',
    'EXPECTED_RAINFALL_MM': 'mean',
    'EMI_PROB_BELOW_NORMAL': 'mean',
    'RESPONSE_TIER': lambda x: x.mode().iloc[0] if len(x) > 0 else 'Unknown'
}).reset_index()

top_tabias = tabia_summary.nsmallest(20, 'PERCENT_OF_NORMAL')

if len(top_tabias) > 0:
    fig = px.bar(
        top_tabias,
        x='PERCENT_OF_NORMAL',
        y='TABIA',
        orientation='h',
        title="Top 20 Most At-Risk Tabias (Lowest % of Normal Rainfall)",
        color='PERCENT_OF_NORMAL',
        color_continuous_scale='Reds',
        hover_data=['ZONE', 'WEREDA', 'EMI_PROB_BELOW_NORMAL']
    )
    fig.update_layout(
        height=600,
        xaxis_title="Percent of Normal (%)",
        yaxis_title="Tabia"
    )
    st.plotly_chart(fig, use_container_width=True)

# EMI Probability Distribution
st.subheader("📊 EMI Tercile Probability Distribution Across Tabias")

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=filtered_df['EMI_PROB_ABOVE_NORMAL'], name='Above Normal', marker_color='#228B22', opacity=0.7))
    fig.add_trace(go.Histogram(x=filtered_df['EMI_PROB_NORMAL'], name='Normal', marker_color='#FFD700', opacity=0.7))
    fig.add_trace(go.Histogram(x=filtered_df['EMI_PROB_BELOW_NORMAL'], name='Below Normal', marker_color='#8B0000', opacity=0.7))
    fig.update_layout(
        title="Distribution of EMI Probabilities Across Tabias",
        xaxis_title="Probability (%)",
        yaxis_title="Number of Tabias",
        barmode='overlay',
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    tier_prob = filtered_df.groupby('RESPONSE_TIER').agg({
        'EMI_PROB_ABOVE_NORMAL': 'mean',
        'EMI_PROB_NORMAL': 'mean',
        'EMI_PROB_BELOW_NORMAL': 'mean'
    }).reset_index()
    
    fig = px.bar(
        tier_prob,
        x='RESPONSE_TIER',
        y=['EMI_PROB_ABOVE_NORMAL', 'EMI_PROB_NORMAL', 'EMI_PROB_BELOW_NORMAL'],
        title="Average EMI Probabilities by Response Tier",
        labels={'value': 'Probability (%)', 'variable': 'Forecast Category'},
        barmode='group',
        color_discrete_map={
            'EMI_PROB_ABOVE_NORMAL': '#228B22',
            'EMI_PROB_NORMAL': '#FFD700',
            'EMI_PROB_BELOW_NORMAL': '#8B0000'
        }
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

# Results table
st.subheader("📋 Tigray Tabia-Level Assessment Results")

display_cols = ['ZONE', 'WEREDA', 'TABIA', 'LIVELIHOOD_ZONE', 'MAIN_CROPS', 'HECTARES',
                'CLIMATOLOGICAL_MEAN_MM', 'EXPECTED_RAINFALL_MM', 'RAINFALL_ANOMALY_MM', 
                'PERCENT_OF_NORMAL', 'EMI_PROB_BELOW_NORMAL', 'CATEGORY', 'RESPONSE_TIER']

available_cols = [col for col in display_cols if col in filtered_df.columns]
display_df = filtered_df[available_cols].copy()

rename_map = {
    'ZONE': 'Zone',
    'WEREDA': 'Woreda',
    'TABIA': 'Tabia',
    'LIVELIHOOD_ZONE': 'Livelihood Zone',
    'MAIN_CROPS': 'Main Crops',
    'HECTARES': 'Area (Hectares)',
    'CLIMATOLOGICAL_MEAN_MM': 'Climatological Mean (mm)',
    'EXPECTED_RAINFALL_MM': 'Expected Rainfall (mm)',
    'RAINFALL_ANOMALY_MM': 'Anomaly (mm)',
    'PERCENT_OF_NORMAL': 'Percent of Normal (%)',
    'EMI_PROB_BELOW_NORMAL': 'EMI Below Normal Prob (%)',
    'CATEGORY': 'Category',
    'RESPONSE_TIER': 'Response Tier'
}
display_df = display_df.rename(columns=rename_map)

def highlight_tier(row):
    tier = row.get('Response Tier', '')
    if tier == 'Emergency':
        return ['background-color: #4A0000; color: white'] * len(row)
    elif tier == 'Action':
        return ['background-color: #8B0000; color: white'] * len(row)
    elif tier == 'Alert':
        return ['background-color: #CC5500; color: white'] * len(row)
    elif tier == 'Watch':
        return ['background-color: #FFD700; color: black'] * len(row)
    return [''] * len(row)

st.dataframe(
    display_df.style.apply(highlight_tier, axis=1),
    use_container_width=True,
    hide_index=True
)

# Download buttons
col1, col2 = st.columns(2)
with col1:
    csv = display_df.to_csv(index=False)
    st.download_button(
        "📥 Download CSV Report",
        csv,
        f"tigray_tabia_assessment_{datetime.now().strftime('%Y%m%d')}.csv",
        "text/csv"
    )

with col2:
    summary_data = {
        'Metric': ['Total Tabias', 'Total Woredas', 'Total Zones', 'Emergency Tier', 'Action Tier', 'Alert Tier', 'Watch Tier',
                   'Average % of Normal', 'Average Expected Rainfall (mm)', 'Average EMI Below Normal Prob (%)'],
        'Value': [
            len(filtered_df),
            filtered_df['WEREDA'].nunique(),
            filtered_df['ZONE'].nunique(),
            len(filtered_df[filtered_df['RESPONSE_TIER'] == 'Emergency']),
            len(filtered_df[filtered_df['RESPONSE_TIER'] == 'Action']),
            len(filtered_df[filtered_df['RESPONSE_TIER'] == 'Alert']),
            len(filtered_df[filtered_df['RESPONSE_TIER'] == 'Watch']),
            f"{filtered_df['PERCENT_OF_NORMAL'].mean():.1f}%",
            f"{filtered_df['EXPECTED_RAINFALL_MM'].mean():.0f} mm",
            f"{filtered_df['EMI_PROB_BELOW_NORMAL'].mean():.1f}%"
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_csv = summary_df.to_csv(index=False)
    st.download_button(
        "📊 Download Summary Report",
        summary_csv,
        f"tigray_tabia_summary_{datetime.now().strftime('%Y%m%d')}.csv",
        "text/csv"
    )

# Risk Analysis Dashboard
st.subheader("📊 Risk Analysis Dashboard")

col1, col2 = st.columns(2)

with col1:
    category_counts = filtered_df['CATEGORY'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']
    fig = px.pie(
        category_counts,
        values='Count',
        names='Category',
        title="Drought Category Distribution",
        color='Category',
        color_discrete_map=CATEGORY_COLORS
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    tier_counts = filtered_df['RESPONSE_TIER'].value_counts().reset_index()
    tier_counts.columns = ['Tier', 'Count']
    tier_counts['Percentage'] = (tier_counts['Count'] / tier_counts['Count'].sum() * 100).round(1)
    fig = px.bar(
        tier_counts,
        x='Tier',
        y='Count',
        title="Response Tier Distribution",
        color='Tier',
        color_discrete_map=TIER_COLORS,
        text='Percentage'
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

# Percent of Normal Distribution
st.subheader("📊 Percent of Normal Rainfall Distribution")

fig = px.histogram(
    filtered_df,
    x='PERCENT_OF_NORMAL',
    nbins=30,
    title="Distribution of Percent of Normal Across Tigray Tabias",
    labels={'PERCENT_OF_NORMAL': 'Percent of Normal (%)'},
    color_discrete_sequence=['#2c3e50']
)
fig.add_vline(x=50, line_dash="dash", line_color="#4A0000", annotation_text="Emergency", annotation_position="top")
fig.add_vline(x=75, line_dash="dash", line_color="#8B0000", annotation_text="Action", annotation_position="top")
fig.add_vline(x=90, line_dash="dash", line_color="#CC5500", annotation_text="Alert", annotation_position="top")
fig.update_layout(height=450)
st.plotly_chart(fig, use_container_width=True)

# Livelihood Zone Analysis
if 'LIVELIHOOD_ZONE' in filtered_df.columns and filtered_df['LIVELIHOOD_ZONE'].notna().any():
    st.subheader("🏷️ Risk Analysis by Livelihood Zone")
    
    lz_risk = filtered_df.groupby('LIVELIHOOD_ZONE').agg({
        'TABIA': 'count',
        'PERCENT_OF_NORMAL': 'mean',
        'EXPECTED_RAINFALL_MM': 'mean',
        'EMI_PROB_BELOW_NORMAL': 'mean'
    }).round(1).reset_index()
    lz_risk.columns = ['Livelihood Zone', 'Tabia Count', 'Avg Percent of Normal', 
                       'Avg Expected Rainfall (mm)', 'Avg EMI Below Normal Prob (%)']
    lz_risk = lz_risk.sort_values('Avg Percent of Normal', ascending=True)
    
    fig = px.bar(
        lz_risk.head(15),
        x='Avg Percent of Normal',
        y='Livelihood Zone',
        orientation='h',
        title="Average Percent of Normal by Livelihood Zone",
        color='Avg Percent of Normal',
        color_continuous_scale='Reds',
        hover_data=['Tabia Count', 'Avg EMI Below Normal Prob (%)']
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# Woreda Summary Analysis
st.subheader("📊 Woreda-Level Summary")

woreda_risk = filtered_df.groupby('WEREDA').agg({
    'ZONE': 'first',
    'TABIA': 'count',
    'PERCENT_OF_NORMAL': 'mean',
    'EXPECTED_RAINFALL_MM': 'mean',
    'EMI_PROB_BELOW_NORMAL': 'mean',
    'HECTARES': 'sum'
}).round(1).reset_index()
woreda_risk.columns = ['Woreda', 'Zone', 'Tabia Count', 'Avg Percent of Normal', 
                       'Avg Expected Rainfall (mm)', 'Avg EMI Below Normal Prob (%)',
                       'Total Hectares']
woreda_risk = woreda_risk.sort_values('Avg Percent of Normal', ascending=True)

fig = px.bar(
    woreda_risk.head(20),
    x='Avg Percent of Normal',
    y='Woreda',
    orientation='h',
    title="Average Percent of Normal by Woreda (Top 20 Most At-Risk)",
    color='Avg Percent of Normal',
    color_continuous_scale='Reds',
    hover_data=['Zone', 'Tabia Count', 'Total Hectares']
)
fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True)

# Tabia Deep Dive
st.subheader("🔍 Tabia Deep Dive - Anticipatory Action Planning")

selected_tabia_deep = st.selectbox(
    "Select Tabia for Detailed Analysis",
    sorted(filtered_df['TABIA'].unique())
)

if selected_tabia_deep:
    tabia_data = filtered_df[filtered_df['TABIA'] == selected_tabia_deep].iloc[0]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Zone", tabia_data['ZONE'])
    with col2:
        st.metric("Woreda", tabia_data['WEREDA'])
    with col3:
        st.metric("Livelihood Zone", tabia_data.get('LIVELIHOOD_ZONE', 'N/A'))
    with col4:
        st.metric("Response Tier", tabia_data['RESPONSE_TIER'])
    with col5:
        st.metric("% of Normal", f"{tabia_data['PERCENT_OF_NORMAL']:.0f}%")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**📊 Rainfall Metrics:**")
        rain_data = pd.DataFrame({
            'Metric': ['Climatological Mean', 'Expected Rainfall', 'Rainfall Anomaly'],
            'Value (mm)': [
                tabia_data['CLIMATOLOGICAL_MEAN_MM'],
                tabia_data['EXPECTED_RAINFALL_MM'],
                tabia_data['RAINFALL_ANOMALY_MM']
            ]
        })
        st.dataframe(rain_data, hide_index=True, use_container_width=True)
    
    with col2:
        st.write("**📡 EMI Probabilistic Forecast:**")
        emi_data = pd.DataFrame({
            'Forecast Category': ['Above Normal', 'Normal', 'Below Normal'],
            'Probability (%)': [
                tabia_data['EMI_PROB_ABOVE_NORMAL'],
                tabia_data['EMI_PROB_NORMAL'],
                tabia_data['EMI_PROB_BELOW_NORMAL']
            ]
        })
        st.dataframe(emi_data, hide_index=True, use_container_width=True)
    
    if 'HECTARES' in tabia_data and pd.notna(tabia_data['HECTARES']):
        st.write(f"**📐 Area:** {tabia_data['HECTARES']:,.0f} hectares")
    if 'MAIN_CROPS' in tabia_data and pd.notna(tabia_data['MAIN_CROPS']):
        st.write(f"**🌾 Main Crops:** {tabia_data['MAIN_CROPS']}")
    
    tier = tabia_data['RESPONSE_TIER']
    st.write("**📋 Recommended Anticipatory Actions:**")
    
    if tier == "Emergency":
        st.markdown("""
        - 🔴 **Immediate Alert:** Activate emergency response protocols
        - 🔴 **Food Security:** Pre-position emergency food assistance for September-December 2026
        - 🔴 **Water:** Immediate pre-positioning of emergency water trucking contracts
        - 🔴 **Agriculture:** Rain-fed cropping NOT advisable; promote drought-resilient livelihoods
        - 🔴 **Livestock:** Urgent strategic off-take support and destocking programs
        - 🔴 **Monitoring:** Daily monitoring of rainfall and rangeland conditions
        """)
    elif tier == "Action":
        st.markdown("""
        - 🟠 **High Alert:** Prepare for potential drought emergency
        - 🟠 **Agriculture:** Distribute short-cycle (<90 days) drought-tolerant seed varieties
        - 🟠 **Water:** Promote in-situ moisture conservation (tie ridges, contour plowing)
        - 🟠 **Livestock:** Support strategic off-take and supplementary feeding programs
        - 🟠 **Monitoring:** Weekly rainfall tracking and vegetation condition assessment
        - 🟠 **Contingency:** Pre-position livestock feed and veterinary supplies
        """)
    elif tier == "Alert":
        st.markdown("""
        - 🟡 **Enhanced Monitoring:** Close tracking of within-season rainfall distribution
        - 🟡 **Agriculture:** Promote water harvesting and soil moisture conservation techniques
        - 🟡 **Water:** Identify and prepare emergency water sources
        - 🟡 **Contingency:** Update drought contingency plans for all program sectors
        - 🟡 **Coordination:** Brief local authorities and community structures on forecast
        - 🟡 **Preparedness:** Pre-identify vulnerable households for targeted support
        """)
    else:
        st.markdown("""
        - 🟢 **Routine Monitoring:** Continue standard early warning monitoring
        - 🟢 **Agriculture:** Promote standard moisture conservation practices
        - 🟢 **Capacity Building:** Strengthen community drought preparedness
        - 🟢 **Contingency Planning:** Maintain updated contingency plans
        - 🟢 **Coordination:** Regular information sharing with EMI and regional bureaus
        - 🟢 **Documentation:** Document lessons learned for future planning
        """)

# Methodology
with st.expander("📖 Methodology: How Percent of Normal is Calculated"):
    st.markdown("""
    **Percent of Normal Rainfall Approach**
    
    **Formula:** 
    Percent of Normal = (Expected Rainfall / Climatological Mean) × 100
    
    **Where:**
    - **Expected Rainfall**: Derived from EMI's tercile probabilistic forecast
      - Expected = (P_below × BN_tercile) + (P_normal × NN_tercile) + (P_above × AN_tercile)
    - **Climatological Mean**: 30-year average (1991-2020) Kiremt rainfall from CHIRPS data

    **Classification Thresholds:**
    | Percent of Normal | Category | Response Tier |
    |------------------|----------|---------------|
    | ≤ 50% | Extremely much below normal | Emergency |
    | 51% - 75% | Much below normal | Action |
    | 76% - 90% | Below normal | Alert |
    | 91% - 125% | Near to normal | Watch |
    | > 125% | Above normal | Watch |

    **Data Sources:**
    - **Rainfall Data**: CHIRPS pentad rainfall (1991-2020)
    - **Forecast**: Ethiopian Meteorological Institute (EMI) Kiremt 2026
    - **Geospatial**: Tigray Tabia shapefile with livelihood zone attributes

    **Expected Rainfall Calculation Details:**
    - **BN_tercile (Below Normal)** = Q1 / 2 (25th percentile divided by 2)
    - **NN_tercile (Normal)** = (Q1 + Q3) / 2 (Average of 25th and 75th percentiles)
    - **AN_tercile (Above Normal)** = Q3 + (Q3 - median) / 2 (75th percentile plus half the distance to median)

    **Intended Use:**
    This dashboard is designed to support anticipatory action planning for Kiremt 2026.
    Results should be interpreted in conjunction with other early warning information sources
    and validated with local knowledge.
    """)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")

footer_html = f'''
<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1a2a3a 0%, #2c3e50 100%); color: white; border-radius: 10px;">
<p style="margin: 0;">🌾 Tigray Integrated Anticipatory Early Warning System | Kiremt 2026</p>
<p style="margin: 5px 0 0 0; font-size: 12px;">
    Developed by {AUTHOR_NAME}, {AUTHOR_TITLE} | {AUTHOR_ORGANIZATION}<br>
    📧 {AUTHOR_EMAIL}
</p>
<p style="margin: 5px 0 0 0; font-size: 11px;">
    📡 Forecast Source: Ethiopian Meteorological Institute (EMI)<br>
    📊 Method: Percent of Normal Rainfall Approach | Version {DASHBOARD_VERSION}
</p>
<p style="margin: 5px 0 0 0; font-size: 11px;">
    🔗 <a href="https://github.com/Goitafa/Tigray-AEWS" style="color: #FFD700;">GitHub Repository</a> | 
    📅 Assessment Date: {CURRENT_DATE}
</p>
</div>
'''

st.markdown(footer_html, unsafe_allow_html=True)