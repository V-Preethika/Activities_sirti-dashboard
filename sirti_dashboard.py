import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SIRTI Operations Dashboard | Vodafone Qatar",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# PROFESSIONAL CSS - Clean Enterprise Design
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* Global */
    .main { 
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }

    /* Header Bar */
    .header-bar {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%);
        padding: 20px 30px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(30, 58, 95, 0.15);
    }
    .header-title {
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        color: rgba(255,255,255,0.7);
        font-size: 14px;
        margin: 5px 0 0 0;
        font-weight: 400;
    }

    /* KPI Cards */
    .kpi-container {
        background: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kpi-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    .kpi-icon {
        font-size: 32px;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 36px;
        font-weight: 800;
        color: #1e293b;
        margin: 0;
        line-height: 1;
    }
    .kpi-label {
        font-size: 13px;
        color: #64748b;
        margin-top: 8px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-sub {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 4px;
    }
    .kpi-blue { border-top: 4px solid #3b82f6; }
    .kpi-green { border-top: 4px solid #10b981; }
    .kpi-red { border-top: 4px solid #ef4444; }
    .kpi-orange { border-top: 4px solid #f59e0b; }
    .kpi-purple { border-top: 4px solid #8b5cf6; }

    /* Section Headers */
    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #1e293b;
        margin: 30px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Technician Cards */
    .task-card {
        background: white;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 12px;
        border-left: 4px solid #cbd5e1;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        transition: all 0.2s;
    }
    .task-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left-width: 6px;
    }
    .task-card.completed { border-left-color: #10b981; }
    .task-card.canceled { border-left-color: #ef4444; }
    .task-card.suspended { border-left-color: #f59e0b; }

    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .status-completed { background: #d1fae5; color: #065f46; }
    .status-canceled { background: #fee2e2; color: #991b1b; }
    .status-suspended { background: #fef3c7; color: #92400e; }
    .type-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: #e0e7ff;
        color: #3730a3;
    }

    /* Quota Progress */
    .quota-box {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
    }
    .quota-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 14px;
    }
    .quota-met { background: #d1fae5; color: #065f46; }
    .quota-pending { background: #fef3c7; color: #92400e; }
    .quota-not-met { background: #fee2e2; color: #991b1b; }
    .progress-track {
        width: 100%;
        height: 10px;
        background: #e2e8f0;
        border-radius: 5px;
        overflow: hidden;
        margin-top: 12px;
    }
    .progress-fill {
        height: 100%;
        border-radius: 5px;
        transition: width 0.6s ease;
    }
    .fill-green { background: linear-gradient(90deg, #10b981, #34d399); }
    .fill-orange { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .fill-red { background: linear-gradient(90deg, #ef4444, #f87171); }

    /* Upload Screen */
    .upload-hero {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%);
        border-radius: 16px;
        padding: 50px 40px;
        text-align: center;
        color: white;
        margin: 20px 0;
    }
    .upload-hero h2 {
        color: white;
        font-size: 32px;
        margin-bottom: 15px;
        font-weight: 700;
    }
    .upload-hero p {
        color: rgba(255,255,255,0.8);
        font-size: 16px;
        margin-bottom: 30px;
    }
    .upload-zone {
        background: white;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        margin: 20px 0;
        transition: border-color 0.2s;
    }
    .upload-zone:hover {
        border-color: #3b82f6;
    }
    .upload-zone h3 {
        color: #1e293b;
        font-size: 22px;
        margin-bottom: 10px;
    }
    .upload-zone p {
        color: #64748b;
        font-size: 14px;
    }

    /* Instructions */
    .guide-card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
    }
    .guide-step {
        display: flex;
        align-items: flex-start;
        gap: 15px;
        padding: 12px 0;
        border-bottom: 1px solid #f1f5f9;
    }
    .guide-step:last-child { border-bottom: none; }
    .step-number {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 13px;
        flex-shrink: 0;
    }
    .step-text {
        color: #475569;
        font-size: 14px;
        line-height: 1.5;
    }
    .step-text strong {
        color: #1e293b;
    }

    /* Data Table */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        padding: 30px 0;
        border-top: 1px solid #e2e8f0;
        margin-top: 40px;
    }

    /* Sidebar */
    .css-1d391kg { background: #f8fafc; }
</style>
""", unsafe_allow_html=True)

DAILY_QUOTA = 4

# ═══════════════════════════════════════════════════════════════
# DATA LOADING FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def clean_dataframe(df):
    """Clean and prepare the dataframe"""
    df['Resource'] = df['Resource'].astype(str).str.strip().str.title()
    df['Technician_Name'] = df['Resource'].fillna('Unknown')
    df['Activity Status'] = df['Activity Status'].astype(str).str.strip().str.lower()

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
    df['Customer_Phone'] = df['Phone'].fillna(df.get('Telephone Number', pd.Series(['N/A']*len(df)))).fillna('N/A')
    df['Plan_Speed_Display'] = df['Plan Speed'].fillna('N/A').astype(str)
    return df

@st.cache_data
def try_load_from_repo():
    """Try to load CSV from the same folder as script"""
    script_dir = Path(__file__).parent.absolute()
    possible_names = [
        'Activities-SIRTI_04_12_26.csv',
        'Activities-SIRTI.csv',
        'SIRTI.csv',
        'activities.csv'
    ]
    for name in possible_names:
        csv_path = script_dir / name
        if csv_path.exists():
            return pd.read_csv(csv_path, encoding='utf-8-sig')
    for subfolder in ['work', 'data', 'Data']:
        for name in possible_names:
            csv_path = script_dir / subfolder / name
            if csv_path.exists():
                return pd.read_csv(csv_path, encoding='utf-8-sig')
    return None

# ═══════════════════════════════════════════════════════════════
# SIDEBAR - FILE UPLOAD
# ═══════════════════════════════════════════════════════════════
st.sidebar.markdown("## 📁 Upload Data")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "**Drop CSV file here**",
    type=['csv'],
    help="Upload any SIRTI activities CSV"
)

df = None
source = None

if uploaded_file is not None:
    try:
        df = clean_dataframe(pd.read_csv(uploaded_file, encoding='utf-8-sig'))
        source = uploaded_file.name
        st.sidebar.markdown(f"<div style='background:#d1fae5;color:#065f46;padding:10px;border-radius:8px;font-weight:600;'>✅ {uploaded_file.name}</div>", unsafe_allow_html=True)
        st.sidebar.markdown(f"<div style='font-size:12px;color:#64748b;margin-top:5px;'>📊 {len(df)} records | 👷 {df['Technician_Name'].nunique()} technicians</div>", unsafe_allow_html=True)
    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")
        st.stop()
else:
    repo_df = try_load_from_repo()
    if repo_df is not None:
        df = clean_dataframe(repo_df)
        source = "Repository"
        st.sidebar.markdown("<div style='background:#d1fae5;color:#065f46;padding:10px;border-radius:8px;font-weight:600;'>✅ Auto-loaded</div>", unsafe_allow_html=True)
    else:
        st.sidebar.info("👆 Upload a CSV to begin")

# ═══════════════════════════════════════════════════════════════
# UPLOAD SCREEN (No Data)
# ═══════════════════════════════════════════════════════════════
if df is None:
    st.markdown("""
    <div class="header-bar">
        <div style="display:flex;align-items:center;gap:15px;">
            <div style="font-size:40px;">📡</div>
            <div>
                <div class="header-title">SIRTI Field Operations Dashboard</div>
                <div class="header-subtitle">Vodafone Qatar | Daily Performance & Quota Tracking</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="upload-zone">
            <div style="font-size:48px;margin-bottom:15px;">📤</div>
            <h3>Upload Your CSV File</h3>
            <p>Drag and drop your SIRTI activities CSV file here<br>or use the sidebar to browse files.</p>
            <p style="font-size:12px;color:#94a3b8;margin-top:15px;">Supports any CSV exported from the WFM system</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="guide-card">
            <div style="font-size:16px;font-weight:700;color:#1e293b;margin-bottom:15px;">📋 How to Use</div>
            <div class="guide-step">
                <div class="step-number">1</div>
                <div class="step-text">Export the daily activities CSV from your <strong>WFM system</strong></div>
            </div>
            <div class="guide-step">
                <div class="step-number">2</div>
                <div class="step-text">Click <strong>"Browse files"</strong> in the left sidebar or drag file here</div>
            </div>
            <div class="guide-step">
                <div class="step-number">3</div>
                <div class="step-text">Dashboard will automatically load and display all data with quota tracking</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="guide-card">
            <div style="font-size:16px;font-weight:700;color:#1e293b;margin-bottom:15px;">✅ Expected Format</div>
            <div style="font-size:13px;color:#475569;line-height:1.8;">
                <div style="display:flex;gap:8px;margin:6px 0;"><span style="color:#3b82f6;">●</span> <strong>Resource</strong> — Technician name</div>
                <div style="display:flex;gap:8px;margin:6px 0;"><span style="color:#3b82f6;">●</span> <strong>Activity Type</strong> — Installation, IPTV, etc.</div>
                <div style="display:flex;gap:8px;margin:6px 0;"><span style="color:#3b82f6;">●</span> <strong>Activity Status</strong> — Completed, Canceled</div>
                <div style="display:flex;gap:8px;margin:6px 0;"><span style="color:#3b82f6;">●</span> <strong>Name</strong> — Customer name</div>
                <div style="display:flex;gap:8px;margin:6px 0;"><span style="color:#3b82f6;">●</span> <strong>Address</strong> — Location</div>
                <div style="display:flex;gap:8px;margin:6px 0;"><span style="color:#3b82f6;">●</span> <strong>Plan Name</strong> — Service plan</div>
                <div style="display:flex;gap:8px;margin:6px 0;"><span style="color:#3b82f6;">●</span> <strong>Duration</strong> — Time spent</div>
            </div>
            <div style="margin-top:15px;padding-top:15px;border-top:1px solid #e2e8f0;font-size:12px;color:#94a3b8;">
                Standard WFM export format
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='footer'>📡 SIRTI Dashboard | Vodafone Qatar | Built for Field Operations Excellence</div>", unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════════════════
# DASHBOARD HEADER (With Data)
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="header-bar">
    <div style="display:flex;align-items:center;gap:15px;">
        <div style="font-size:40px;">📡</div>
        <div>
            <div class="header-title">SIRTI Field Operations Dashboard</div>
            <div class="header-subtitle">Vodafone Qatar | {len(df)} Activities | {df['Technician_Name'].nunique()} Technicians | Source: {source}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SIDEBAR - TECHNICIAN SELECTOR
# ═══════════════════════════════════════════════════════════════
st.sidebar.markdown("---")
st.sidebar.markdown("## 👷 Technician")
st.sidebar.markdown("---")

tech_list = df['Technician_Name'].value_counts().index.tolist()
tech_list = [t for t in tech_list if t != 'Unknown']
all_option = "📊 All Technicians"
tech_options = [all_option] + tech_list

selected_tech = st.sidebar.selectbox("Select person:", tech_options, index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size:12px;color:#64748b;'>🎯 Daily Quota</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='font-size:18px;font-weight:700;color:#1e293b;'>{DAILY_QUOTA} tasks/day</div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def render_kpi(title, value, subtitle, style, icon):
    st.markdown(f"""
    <div class="kpi-container {style}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{title}</div>
        <div class="kpi-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def get_status_badge(status):
    status = str(status).lower()
    if status == 'completed': return '<span class="status-badge status-completed">● Completed</span>'
    elif status == 'canceled': return '<span class="status-badge status-canceled">● Canceled</span>'
    elif status == 'suspended': return '<span class="status-badge status-suspended">● Suspended</span>'
    else: return f'<span class="status-badge">● {status.upper()}</span>'

def get_type_badge(act_type):
    act_type = str(act_type).lower()
    if 'installation' in act_type: return '<span class="type-badge">🔧 Installation</span>'
    elif 'iptv' in act_type: return '<span class="type-badge">📺 IPTV</span>'
    elif 'troubleshoot' in act_type: return '<span class="type-badge">🔍 Troubleshoot</span>'
    elif 'audit' in act_type: return '<span class="type-badge">📋 Audit</span>'
    elif '5g' in act_type: return '<span class="type-badge">📶 5G</span>'
    else: return f'<span class="type-badge">● {act_type.upper()}</span>'

def render_quota(current, quota=DAILY_QUOTA):
    pct = min((current / quota) * 100, 100)
    remaining = max(quota - current, 0)
    if current >= quota:
        status = f'<span class="quota-status quota-met">✅ Quota Met — {current}/{quota}</span>'
        fill = "fill-green"
    elif current > 0:
        status = f'<span class="quota-status quota-pending">⏳ In Progress — {current}/{quota} ({remaining} more)</span>'
        fill = "fill-orange"
    else:
        status = f'<span class="quota-status quota-not-met">❌ No Tasks — {current}/{quota}</span>'
        fill = "fill-red"
    st.markdown(f"""
    <div class="quota-box">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <div style="font-size:16px;font-weight:700;color:#1e293b;">Daily Quota Progress</div>
            {status}
        </div>
        <div class="progress-track">
            <div class="progress-fill {fill}" style="width:{pct}%;"></div>
        </div>
        <div style="text-align:center;font-size:12px;color:#94a3b8;margin-top:8px;">{current} of {quota} required tasks completed</div>
    </div>
    """, unsafe_allow_html=True)

def render_task_card(row):
    status = str(row['Activity Status']).lower()
    duration = row['Duration_Minutes']
    dur_str = f"{int(duration // 60)}h {int(duration % 60)}m" if duration >= 60 else f"{int(duration)}m" if duration > 0 else "N/A"
    time_slot = str(row.get('Time Slot', 'N/A'))
    if time_slot == 'nan': time_slot = 'N/A'
    st.markdown(f"""
    <div class="task-card {status}">
        <div style="display:flex;justify-content:space-between;align-items:start;gap:15px;">
            <div style="flex:1;min-width:0;">
                <div style="display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap;">
                    {get_status_badge(status)}
                    {get_type_badge(row['Activity Type'])}
                </div>
                <div style="font-size:17px;font-weight:700;color:#1e293b;margin-bottom:6px;">{row.get('Name', 'N/A')}</div>
                <div style="font-size:13px;color:#64748b;margin-bottom:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                    📍 {str(row.get('Address', 'N/A'))[:70]}
                </div>
                <div style="display:flex;gap:20px;font-size:13px;color:#475569;flex-wrap:wrap;">
                    <span>📞 {row.get('Customer_Phone', 'N/A')}</span>
                    <span>⚡ {row.get('Plan Name', 'N/A')} ({row.get('Plan_Speed_Display', 'N/A')})</span>
                    <span>⏱️ {dur_str}</span>
                    <span>🕐 {time_slot}</span>
                </div>
            </div>
            <div style="text-align:right;min-width:100px;flex-shrink:0;">
                <div style="font-size:22px;font-weight:800;color:{'#10b981' if status=='completed' else '#ef4444' if status=='canceled' else '#f59e0b'};">
                    {status.upper()[:3]}
                </div>
                <div style="font-size:11px;color:#94a3b8;margin-top:4px;">ID: {str(row.get('Activity ID', 'N/A'))}</div>
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

    with col1: render_kpi("Total Tasks", total_tasks, "All activities", "kpi-blue", "📋")
    with col2: render_kpi("Completed", completed, f"{completed/total_tasks*100:.1f}% rate", "kpi-green", "✅")
    with col3: render_kpi("Canceled", canceled, f"{canceled/total_tasks*100:.1f}% rate", "kpi-red", "❌")
    with col4: render_kpi("Suspended", suspended, f"{suspended/total_tasks*100:.1f}% rate", "kpi-orange", "⏸️")
    with col5: render_kpi("Technicians", active_techs, "Active today", "kpi-purple", "👷")

    st.markdown('<div class="section-title">📊 Technician Performance & Quota Status</div>', unsafe_allow_html=True)

    tech_data = []
    for tech in tech_list:
        tech_df = df[df['Technician_Name'] == tech]
        total = len(tech_df)
        completed_count = len(tech_df[tech_df['Activity Status'] == 'completed'])
        canceled_count = len(tech_df[tech_df['Activity Status'] == 'canceled'])
        suspended_count = len(tech_df[tech_df['Activity Status'] == 'suspended'])
        avg_dur = tech_df['Duration_Minutes'].mean()
        if completed_count >= DAILY_QUOTA:
            quota_status = "✅ Met"
        elif completed_count > 0:
            quota_status = f"⏳ {completed_count}/{DAILY_QUOTA}"
        else:
            quota_status = "❌ None"
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

    def highlight_status(val):
        if 'Met' in val: return 'background-color: #d1fae5; color: #065f46; font-weight: 600'
        elif 'None' in val: return 'background-color: #fee2e2; color: #991b1b; font-weight: 600'
        else: return 'background-color: #fef3c7; color: #92400e; font-weight: 600'

    try:
        styled_df = tech_summary_df.style.apply(lambda x: [highlight_status(v) if i == 5 else '' for i, v in enumerate(x)], axis=1)
    except Exception:
        styled_df = tech_summary_df

    st.dataframe(styled_df, use_container_width=True, height=600)

    st.markdown('<div class="section-title">📈 Analytics</div>', unsafe_allow_html=True)
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        quota_data = tech_summary_df.copy()
        quota_data['Completed_Count'] = quota_data['Quota'].apply(lambda x: int(x.split('/')[0]))
        fig = go.Figure()
        fig.add_hline(y=DAILY_QUOTA, line_dash="dash", line_color="#ef4444", annotation_text=f"Quota: {DAILY_QUOTA}", annotation_position="top right")
        colors = ['#10b981' if c >= DAILY_QUOTA else '#f59e0b' if c > 0 else '#ef4444' for c in quota_data['Completed_Count']]
        fig.add_trace(go.Bar(x=quota_data['Technician'], y=quota_data['Completed_Count'], marker_color=colors, text=quota_data['Completed_Count'], textposition='auto'))
        fig.update_layout(xaxis_title="Technician", yaxis_title="Tasks Completed", showlegend=False, height=400, margin=dict(l=20, r=20, t=30, b=100), xaxis_tickangle=-45, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        status_fig = px.pie(names=['Completed', 'Canceled', 'Suspended'], values=[completed, canceled, suspended], color=['Completed', 'Canceled', 'Suspended'], color_discrete_map={'Completed': '#10b981', 'Canceled': '#ef4444', 'Suspended': '#f59e0b'}, hole=0.4)
        status_fig.update_layout(height=400, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(status_fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════
# SINGLE TECHNICIAN MODE
# ═══════════════════════════════════════════════════════════════
else:
    tech_df = df[df['Technician_Name'] == selected_tech].copy()

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%); padding: 25px 30px; border-radius: 12px; color: white; margin-bottom: 25px;">
        <div style="display:flex;align-items:center;gap:15px;">
            <div style="font-size:36px;">👷</div>
            <div>
                <div style="font-size:24px;font-weight:700;">{selected_tech}</div>
                <div style="font-size:14px;opacity:0.8;margin-top:4px;">Field Engineer | {len(tech_df)} Tasks Assigned</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    completed_count = len(tech_df[tech_df['Activity Status'] == 'completed'])
    render_quota(completed_count, DAILY_QUOTA)

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1: render_kpi("Total Tasks", len(tech_df), "Assigned", "kpi-blue", "📋")
    with col2: render_kpi("Completed", completed_count, "Done", "kpi-green", "✅")
    with col3: render_kpi("Canceled", len(tech_df[tech_df['Activity Status'] == 'canceled']), "Lost", "kpi-red", "❌")
    with col4: render_kpi("Suspended", len(tech_df[tech_df['Activity Status'] == 'suspended']), "Pending", "kpi-orange", "⏸️")

    st.markdown("---")
    st.markdown('<div class="section-title">🔍 Filter Tasks</div>', unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        status_filter = st.multiselect("Status:", ['completed', 'canceled', 'suspended'], default=['completed', 'canceled', 'suspended'])
    with fc2:
        type_filter = st.multiselect("Activity Type:", tech_df['Activity Type'].unique().tolist(), default=tech_df['Activity Type'].unique().tolist())
    with fc3:
        order_opts = tech_df['Order Type'].dropna().unique().tolist()
        order_filter = st.multiselect("Order Type:", order_opts, default=order_opts)

    filtered_df = tech_df[(tech_df['Activity Status'].isin(status_filter)) & (tech_df['Activity Type'].isin(type_filter)) & (tech_df['Order Type'].isin(order_filter) | tech_df['Order Type'].isna())]
    st.markdown(f"<div style='font-size:13px;color:#64748b;margin-bottom:15px;'>Showing <strong>{len(filtered_df)}</strong> of <strong>{len(tech_df)}</strong> tasks</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">📋 Task Details</div>', unsafe_allow_html=True)
    if len(filtered_df) == 0:
        st.warning("No tasks match the selected filters.")
    else:
        for idx, row in filtered_df.iterrows():
            render_task_card(row)
            with st.expander("🔍 View Full Details"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**📋 Order Information**")
                    st.write(f"- Order: {row.get('Siebel Order Number reference', 'N/A')}")
                    st.write(f"- TT ID: {row.get('TT ID', 'N/A')}")
                    st.write(f"- Activity ID: {row.get('Activity ID', 'N/A')}")
                    st.write(f"- Order Type: {row.get('Order Type', 'N/A')}")
                    st.markdown("**👤 Customer**")
                    st.write(f"- Name: {row.get('Name', 'N/A')}")
                    st.write(f"- Phone: {row.get('Customer_Phone', 'N/A')}")
                    st.write(f"- Email: {row.get('Email', 'N/A')}")
                    st.write(f"- Address: {row.get('Address', 'N/A')}")
                with c2:
                    st.markdown("**⚡ Service**")
                    st.write(f"- Plan: {row.get('Plan Name', 'N/A')}")
                    st.write(f"- Speed: {row.get('Plan Speed', 'N/A')} Mbps")
                    st.write(f"- Zone: {row.get('Work Zone', 'N/A')}")
                    st.markdown("**⏱️ Timing**")
                    st.write(f"- Slot: {row.get('Time Slot', 'N/A')}")
                    st.write(f"- Duration: {row['Duration_Minutes']:.1f} min")
                    st.markdown("**🔧 Technical**")
                    st.write(f"- CPE: {row.get('CPE Serial Number', 'N/A')}")
                    st.write(f"- ONT: {row.get('ONT Serial Number', 'N/A')}")
                    st.write(f"- Resolution: {row.get('Resolution', 'N/A')}")

    st.markdown("---")
    st.markdown('<div class="section-title">📊 Personal Analytics</div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        type_counts = tech_df['Activity Type'].value_counts()
        fig = px.pie(values=type_counts.values, names=type_counts.index, title="Activity Types", color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    with sc2:
        status_counts = tech_df['Activity Status'].value_counts()
        colors = {'completed': '#10b981', 'canceled': '#ef4444', 'suspended': '#f59e0b'}
        fig = px.bar(x=status_counts.index, y=status_counts.values, title="Status Breakdown", color=status_counts.index, color_discrete_map=colors)
        fig.update_layout(height=350, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

st.markdown("<div class='footer'>📡 SIRTI Dashboard | Vodafone Qatar | Built for Field Operations Excellence</div>", unsafe_allow_html=True)
