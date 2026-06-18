import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import glob
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SIRTI Field Operations Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .kpi-card-green { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
    .kpi-card-red { background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); }
    .kpi-card-orange { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    .kpi-card-blue { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    .kpi-number { font-size: 42px; font-weight: bold; margin: 0; }
    .kpi-label { font-size: 14px; opacity: 0.9; margin-top: 5px; }
    .kpi-sub { font-size: 12px; opacity: 0.8; margin-top: 3px; }
    .tech-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .tech-card.completed { border-left-color: #11998e; }
    .tech-card.canceled { border-left-color: #eb3349; }
    .tech-card.suspended { border-left-color: #f093fb; }
    .quota-met { 
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .quota-not-met { 
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .quota-pending { 
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        margin: 25px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        color: white;
    }
    .badge-completed { background: #11998e; }
    .badge-canceled { background: #eb3349; }
    .badge-suspended { background: #f093fb; }
    .badge-installation { background: #4facfe; }
    .badge-iptv { background: #9b59b6; }
    .badge-troubleshoot { background: #e67e22; }
    .progress-container {
        width: 100%;
        height: 20px;
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
    }
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    .progress-green { background: linear-gradient(90deg, #11998e, #38ef7d); }
    .progress-red { background: linear-gradient(90deg, #eb3349, #f45c43); }
    .progress-orange { background: linear-gradient(90deg, #f093fb, #f5576c); }
    .upload-box {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background: #f8f9ff;
        margin: 10px 0;
    }
    .file-found {
        background: #d4edda;
        border-left: 4px solid #11998e;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .data-loaded {
        background: #d4edda;
        border-left: 4px solid #11998e;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

DAILY_QUOTA = 4

# ═══════════════════════════════════════════════════════════════
# BULLETPROOF FILE LOADER - Works on both local and Streamlit Cloud
# ═══════════════════════════════════════════════════════════════
@st.cache_data

def load_data_auto():
    """Auto-find and load CSV from multiple sources"""

    # SOURCE 1: Look in the same folder as the script (GitHub repo on Streamlit Cloud)
    script_dir = Path(__file__).parent.absolute()

    # Possible CSV file names
    csv_names = [
        'Activities-SIRTI_04_12_26.csv',
        'Activities-SIRTI.csv',
        'SIRTI.csv',
        'activities.csv'
    ]

    # Try to find CSV in script directory (this works on Streamlit Cloud)
    for csv_name in csv_names:
        csv_path = script_dir / csv_name
        if csv_path.exists():
            st.sidebar.markdown(f"<div class='data-loaded'>✅ Auto-loaded: {csv_name}</div>", unsafe_allow_html=True)
            return pd.read_csv(csv_path, encoding='utf-8-sig')

    # SOURCE 2: Search subfolders (work, data, etc.)
    search_folders = [script_dir / 'work', script_dir / 'data', script_dir / 'Data']
    for folder in search_folders:
        if folder.exists():
            for csv_name in csv_names:
                csv_path = folder / csv_name
                if csv_path.exists():
                    st.sidebar.markdown(f"<div class='data-loaded'>✅ Found in {folder.name}: {csv_name}</div>", unsafe_allow_html=True)
                    return pd.read_csv(csv_path, encoding='utf-8-sig')

    # SOURCE 3: Try glob patterns
    for pattern in ['*.csv', '**/*.csv']:
        matches = list(script_dir.glob(pattern))
        if matches:
            # Filter out tiny files (not real data)
            valid_matches = [m for m in matches if m.stat().st_size > 1000]
            if valid_matches:
                # Prefer files with "SIRTI" or "Activities" in name
                priority = [m for m in valid_matches if 'sirti' in m.name.lower() or 'activities' in m.name.lower()]
                if priority:
                    st.sidebar.markdown(f"<div class='data-loaded'>✅ Auto-detected: {priority[0].name}</div>", unsafe_allow_html=True)
                    return pd.read_csv(priority[0], encoding='utf-8-sig')
                else:
                    st.sidebar.markdown(f"<div class='data-loaded'>✅ Using: {valid_matches[0].name}</div>", unsafe_allow_html=True)
                    return pd.read_csv(valid_matches[0], encoding='utf-8-sig')

    return None

def clean_dataframe(df):
    """Clean and prepare the dataframe"""
    df['Resource'] = df['Resource'].str.strip().str.title()
    df['Technician_Name'] = df['Resource'].fillna('Unknown')
    df['Activity Status'] = df['Activity Status'].str.strip().str.lower()

    def parse_duration(d):
        if pd.isna(d) or d == '00:00' or d == '':
            return 0
        try:
            d = str(d).strip()
            parts = d.split(':')
            if len(parts) == 3:
                return int(parts[0]) * 60 + int(parts[1]) + int(parts[2])/60
            elif len(parts) == 2:
                return int(parts[0]) + int(parts[1])/60
        except:
            return 0
        return 0

    df['Duration_Minutes'] = df['Duration'].apply(parse_duration)
    df['Date_Clean'] = pd.to_datetime(df['Date'], format='%m/%d/%y', errors='coerce')
    df['Customer_Phone'] = df['Phone'].fillna(df['Telephone Number']).fillna('N/A')
    df['Plan_Speed_Display'] = df['Plan Speed'].fillna('N/A').astype(str)
    return df

# ═══════════════════════════════════════════════════════════════
# SIDEBAR - FILE STATUS
# ═══════════════════════════════════════════════════════════════
st.sidebar.markdown("## 📁 Data File")
st.sidebar.markdown("---")

# Try to auto-load first
df = load_data_auto()

if df is not None:
    df = clean_dataframe(df)
    st.sidebar.markdown("<div class='data-loaded'>✅ Data loaded successfully!</div>", unsafe_allow_html=True)
    st.sidebar.markdown(f"- **Records:** {len(df)}")
    st.sidebar.markdown(f"- **Technicians:** {df['Technician_Name'].nunique()}")
    st.sidebar.markdown(f"- **Date:** {df['Date_Clean'].iloc[0].strftime('%Y-%m-%d') if len(df) > 0 and df['Date_Clean'].notna().any() else 'N/A'}")
else:
    st.sidebar.warning("⚠️ No CSV found in repo. Please upload below.")

    # Manual upload fallback
    uploaded_file = st.sidebar.file_uploader("Upload CSV file:", type=['csv'])

    if uploaded_file is not None:
        df = clean_dataframe(pd.read_csv(uploaded_file, encoding='utf-8-sig'))
        st.sidebar.success("✅ Uploaded file loaded!")
    else:
        st.sidebar.error("❌ No data loaded!")
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h1>📁 SIRTI Dashboard</h1>
            <h3>Data file not found</h3>
            <div class="upload-box" style="max-width: 600px; margin: 30px auto;">
                <p><b>Expected file:</b> <code>Activities-SIRTI_04_12_26.csv</code></p>
                <p>Please upload your CSV file using the sidebar button.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

# ═══════════════════════════════════════════════════════════════
# SIDEBAR - TECHNICIAN SELECTOR
# ═══════════════════════════════════════════════════════════════
st.sidebar.markdown("---")
st.sidebar.markdown("## 👷 Select Technician")
st.sidebar.markdown("---")

tech_list = df['Technician_Name'].value_counts().index.tolist()
tech_list = [t for t in tech_list if t != 'Unknown']
all_option = "📊 ALL TECHNICIANS (Overview)"
tech_options = [all_option] + tech_list

selected_tech = st.sidebar.selectbox("Choose a person:", tech_options, index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Daily Quota")
st.sidebar.markdown(f"**Required: {DAILY_QUOTA} tasks/day**")
st.sidebar.markdown("---")

# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("<h1 style='text-align: center; color: #2c3e50; margin-bottom: 5px;'>📡 SIRTI Field Operations Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #7f8c8d; margin-bottom: 30px;'>Vodafone Qatar | Daily Performance Tracker</h4>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def render_kpi_card(title, value, subtitle, color_class="", icon="📊"):
    st.markdown(f"""
    <div class="kpi-card {color_class}">
        <div style="font-size: 28px; margin-bottom: 5px;">{icon}</div>
        <div class="kpi-number">{value}</div>
        <div class="kpi-label">{title}</div>
        <div class="kpi-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def get_status_badge(status):
    status = str(status).lower()
    if status == 'completed': return '<span class="badge badge-completed">COMPLETED</span>'
    elif status == 'canceled': return '<span class="badge badge-canceled">CANCELED</span>'
    elif status == 'suspended': return '<span class="badge badge-suspended">SUSPENDED</span>'
    else: return f'<span class="badge">{status.upper()}</span>'

def get_type_badge(act_type):
    act_type = str(act_type).lower()
    if 'installation' in act_type: return '<span class="badge badge-installation">INSTALLATION</span>'
    elif 'iptv' in act_type: return '<span class="badge badge-iptv">IPTV</span>'
    elif 'troubleshoot' in act_type: return '<span class="badge badge-troubleshoot">TROUBLESHOOT</span>'
    else: return f'<span class="badge">{act_type.upper()}</span>'

def render_quota_progress(current, quota=DAILY_QUOTA):
    pct = min((current / quota) * 100, 100)
    remaining = max(quota - current, 0)
    if current >= quota:
        status_html = f'<span class="quota-met">QUOTA MET ({current}/{quota})</span>'
        bar_class = "progress-green"
    elif current > 0:
        status_html = f'<span class="quota-pending">IN PROGRESS ({current}/{quota}) - {remaining} more needed</span>'
        bar_class = "progress-orange"
    else:
        status_html = f'<span class="quota-not-met">NO TASKS ({current}/{quota})</span>'
        bar_class = "progress-red"
    st.markdown(f"""
    <div style="margin: 15px 0;">
        {status_html}
        <div class="progress-container" style="margin-top: 10px;">
            <div class="progress-bar {bar_class}" style="width: {pct}%;"></div>
        </div>
        <div style="text-align: center; font-size: 12px; color: #666; margin-top: 5px;">
            {current} of {quota} required tasks completed today
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_tech_detail_card(row):
    status = str(row['Activity Status']).lower()
    card_class = status
    duration = row['Duration_Minutes']
    dur_str = f"{int(duration // 60)}h {int(duration % 60)}m" if duration >= 60 else f"{int(duration)}m" if duration > 0 else "N/A"
    time_slot = str(row.get('Time Slot', 'N/A'))
    if time_slot == 'nan': time_slot = 'N/A'
    st.markdown(f"""
    <div class="tech-card {card_class}">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
                <div style="display: flex; gap: 10px; margin-bottom: 8px;">
                    {get_status_badge(status)}
                    {get_type_badge(row['Activity Type'])}
                </div>
                <div style="font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 5px;">
                    {row.get('Name', 'N/A')}
                </div>
                <div style="font-size: 13px; color: #7f8c8d; margin-bottom: 8px;">
                    {str(row.get('Address', 'N/A'))[:60]}...
                </div>
                <div style="display: flex; gap: 20px; font-size: 13px; color: #555;">
                    <span>{row.get('Customer_Phone', 'N/A')}</span>
                    <span>{row.get('Plan Name', 'N/A')} ({row.get('Plan_Speed_Display', 'N/A')})</span>
                    <span>{dur_str}</span>
                    <span>{time_slot}</span>
                </div>
            </div>
            <div style="text-align: right; min-width: 120px;">
                <div style="font-size: 24px; font-weight: bold; color: {'#11998e' if status == 'completed' else '#eb3349' if status == 'canceled' else '#f093fb'};">
                    {status.upper()[:3]}
                </div>
                <div style="font-size: 11px; color: #999;">ID: {str(row.get('Activity ID', 'N/A'))}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# OVERVIEW MODE
# ═══════════════════════════════════════════════════════════════
if selected_tech == all_option:
    col1, col2, col3, col4, col5 = st.columns(5)
    total_tasks = len(df)
    completed = len(df[df['Activity Status'] == 'completed'])
    canceled = len(df[df['Activity Status'] == 'canceled'])
    suspended = len(df[df['Activity Status'] == 'suspended'])
    active_techs = df['Technician_Name'].nunique()

    with col1: render_kpi_card("Total Tasks", total_tasks, "All activities", "kpi-card-blue", "📋")
    with col2: render_kpi_card("Completed", completed, f"{completed/total_tasks*100:.1f}%", "kpi-card-green", "✅")
    with col3: render_kpi_card("Canceled", canceled, f"{canceled/total_tasks*100:.1f}%", "kpi-card-red", "❌")
    with col4: render_kpi_card("Suspended", suspended, f"{suspended/total_tasks*100:.1f}%", "kpi-card-orange", "⏸️")
    with col5: render_kpi_card("Technicians", active_techs, "Active", "kpi-card", "👷")

    st.markdown("---")
    st.markdown('<div class="section-header">Technician Performance & Quota Status</div>', unsafe_allow_html=True)

    tech_data = []
    for tech in tech_list:
        tech_df = df[df['Technician_Name'] == tech]
        total = len(tech_df)
        completed_count = len(tech_df[tech_df['Activity Status'] == 'completed'])
        canceled_count = len(tech_df[tech_df['Activity Status'] == 'canceled'])
        suspended_count = len(tech_df[tech_df['Activity Status'] == 'suspended'])
        avg_dur = tech_df['Duration_Minutes'].mean()
        if completed_count >= DAILY_QUOTA:
            quota_status = "✅ MET"
        elif completed_count > 0:
            quota_status = f"⏳ {completed_count}/{DAILY_QUOTA}"
        else:
            quota_status = "❌ NONE"
        tech_data.append({
            'Technician': tech,
            'Total': total,
            'Completed': completed_count,
            'Canceled': canceled_count,
            'Suspended': suspended_count,
            'Quota': f"{completed_count}/{DAILY_QUOTA}",
            'Status': quota_status,
            'Avg Duration': f"{avg_dur:.0f}m" if avg_dur > 0 else "N/A"
        })

    tech_summary_df = pd.DataFrame(tech_data)

    # ROBUST STYLING - No applymap, uses simple column coloring
    def highlight_status(val):
        if 'MET' in val: return 'background-color: #d4edda; color: #155724; font-weight: bold'
        elif 'NONE' in val: return 'background-color: #f8d7da; color: #721c24; font-weight: bold'
        else: return 'background-color: #fff3cd; color: #856404; font-weight: bold'

    # Use apply with axis=0 for column-wise styling (most compatible)
    try:
        styled_df = tech_summary_df.style.apply(lambda x: [highlight_status(v) if i == 5 else '' for i, v in enumerate(x)], axis=1)
    except Exception:
        styled_df = tech_summary_df  # Fallback: no styling

    st.dataframe(styled_df, use_container_width=True, height=600)

    st.markdown("---")
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.markdown('<div class="section-header">Quota Compliance</div>', unsafe_allow_html=True)
        quota_data = tech_summary_df.copy()
        quota_data['Completed_Count'] = quota_data['Quota'].apply(lambda x: int(x.split('/')[0]))
        fig = go.Figure()
        fig.add_hline(y=DAILY_QUOTA, line_dash="dash", line_color="red", annotation_text=f"Quota: {DAILY_QUOTA}", annotation_position="top right")
        colors = ['#11998e' if c >= DAILY_QUOTA else '#f093fb' if c > 0 else '#eb3349' for c in quota_data['Completed_Count']]
        fig.add_trace(go.Bar(x=quota_data['Technician'], y=quota_data['Completed_Count'], marker_color=colors, text=quota_data['Completed_Count'], textposition='auto', name='Completed'))
        fig.update_layout(xaxis_title="Technician", yaxis_title="Tasks Completed", showlegend=False, height=400, margin=dict(l=20, r=20, t=30, b=100), xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        st.markdown('<div class="section-header">Status Distribution</div>', unsafe_allow_html=True)
        status_fig = px.pie(names=['Completed', 'Canceled', 'Suspended'], values=[completed, canceled, suspended], color=['Completed', 'Canceled', 'Suspended'], color_discrete_map={'Completed': '#11998e', 'Canceled': '#eb3349', 'Suspended': '#f093fb'}, hole=0.4)
        status_fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(status_fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# SINGLE TECHNICIAN MODE
# ═══════════════════════════════════════════════════════════════
else:
    tech_df = df[df['Technician_Name'] == selected_tech].copy()

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; color: white; margin-bottom: 25px;">
        <h2 style="margin: 0; color: white;">👷 {selected_tech}</h2>
        <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 16px;">Field Engineer | {len(tech_df)} Tasks Assigned</p>
    </div>
    """, unsafe_allow_html=True)

    completed_count = len(tech_df[tech_df['Activity Status'] == 'completed'])
    render_quota_progress(completed_count, DAILY_QUOTA)

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1: render_kpi_card("Total Tasks", len(tech_df), "Assigned", "kpi-card-blue", "📋")
    with col2: render_kpi_card("Completed", completed_count, "Done", "kpi-card-green", "✅")
    with col3: render_kpi_card("Canceled", len(tech_df[tech_df['Activity Status'] == 'canceled']), "Lost", "kpi-card-red", "❌")
    with col4: render_kpi_card("Suspended", len(tech_df[tech_df['Activity Status'] == 'suspended']), "Pending", "kpi-card-orange", "⏸️")

    st.markdown("---")
    st.markdown('<div class="section-header">Filter Tasks</div>', unsafe_allow_html=True)

    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        status_filter = st.multiselect("Status:", ['completed', 'canceled', 'suspended'], default=['completed', 'canceled', 'suspended'])
    with filter_col2:
        type_filter = st.multiselect("Activity Type:", tech_df['Activity Type'].unique().tolist(), default=tech_df['Activity Type'].unique().tolist())
    with filter_col3:
        order_opts = tech_df['Order Type'].dropna().unique().tolist()
        order_filter = st.multiselect("Order Type:", order_opts, default=order_opts)

    filtered_df = tech_df[(tech_df['Activity Status'].isin(status_filter)) & (tech_df['Activity Type'].isin(type_filter)) & (tech_df['Order Type'].isin(order_filter) | tech_df['Order Type'].isna())]
    st.markdown(f"**Showing {len(filtered_df)} of {len(tech_df)} tasks**")

    st.markdown('<div class="section-header">All Task Details</div>', unsafe_allow_html=True)
    if len(filtered_df) == 0:
        st.warning("No tasks match filters.")
    else:
        for idx, row in filtered_df.iterrows():
            render_tech_detail_card(row)
            with st.expander("View Full Details"):
                detail_col1, detail_col2 = st.columns(2)
                with detail_col1:
                    st.markdown("**Order Information**")
                    st.write(f"- Order Number: {row.get('Siebel Order Number reference', 'N/A')}")
                    st.write(f"- TT ID: {row.get('TT ID', 'N/A')}")
                    st.write(f"- Activity ID: {row.get('Activity ID', 'N/A')}")
                    st.write(f"- Order Type: {row.get('Order Type', 'N/A')}")
                    st.markdown("**Customer Details**")
                    st.write(f"- Name: {row.get('Name', 'N/A')}")
                    st.write(f"- Phone: {row.get('Customer_Phone', 'N/A')}")
                    st.write(f"- Email: {row.get('Email', 'N/A')}")
                    st.write(f"- Address: {row.get('Address', 'N/A')}")
                with detail_col2:
                    st.markdown("**Service Details**")
                    st.write(f"- Plan: {row.get('Plan Name', 'N/A')}")
                    st.write(f"- Speed: {row.get('Plan Speed', 'N/A')} Mbps")
                    st.write(f"- Work Zone: {row.get('Work Zone', 'N/A')}")
                    st.markdown("**Timing**")
                    st.write(f"- Time Slot: {row.get('Time Slot', 'N/A')}")
                    st.write(f"- Duration: {row['Duration_Minutes']:.1f} minutes")
                    st.markdown("**Technical**")
                    st.write(f"- CPE Serial: {row.get('CPE Serial Number', 'N/A')}")
                    st.write(f"- ONT Serial: {row.get('ONT Serial Number', 'N/A')}")
                    st.write(f"- Resolution: {row.get('Resolution', 'N/A')}")

    st.markdown("---")
    st.markdown('<div class="section-header">Personal Analytics</div>', unsafe_allow_html=True)
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        type_counts = tech_df['Activity Type'].value_counts()
        fig = px.pie(values=type_counts.values, names=type_counts.index, title="Activity Type Breakdown", color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    with stat_col2:
        status_counts = tech_df['Activity Status'].value_counts()
        colors = {'completed': '#11998e', 'canceled': '#eb3349', 'suspended': '#f093fb'}
        fig = px.bar(x=status_counts.index, y=status_counts.values, title="Task Status Count", color=status_counts.index, color_discrete_map=colors)
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #95a5a6; font-size: 12px; padding: 20px;'>📡 SIRTI Dashboard | Vodafone Qatar | Daily Quota: 4 tasks/technician</div>", unsafe_allow_html=True)
