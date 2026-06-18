# 📡 SIRTI Field Operations Dashboard

**Vodafone Qatar | Field Operations Performance Tracker**

A real-time web dashboard for monitoring SIRTI (Service Installation, Repair, Troubleshooting & Installation) field operations, technician performance, and daily quota compliance.

---

## 🔗 Live Dashboard

**Access URL:** `https://your-app-url.streamlit.app` *(Update after Streamlit Cloud deployment)*

---

## 📊 Dashboard Features

### 1. Team Overview (All Technicians)
- **KPI Cards:** Total tasks, completion rate, cancellation rate, active technicians
- **Performance Table:** Per-technician task counts, quota status, average duration
- **Quota Compliance Chart:** Visual bar chart showing who met the 4-task daily target
- **Status Distribution:** Pie chart of completed / canceled / suspended tasks
- **Zone Breakdown:** Geographic workload distribution (Al Wakrah, Al Wukair, etc.)

### 2. Individual Technician View
- **Select by Name:** Dropdown menu with all 25 field engineers
- **Daily Quota Tracker:** Color-coded progress bar (4 tasks/day requirement)
  - 🟢 Green = Quota Met (4/4)
  - 🟠 Orange = In Progress (1-3/4)
  - 🔴 Red = Not Met (0/4)
- **Task Cards:** Complete customer details, addresses, plans, durations
- **Expandable Details:** Full technical information, resolution notes
- **Smart Filters:** Filter by status, activity type, order type
- **Personal Analytics:** Activity breakdown and status charts

---

## 📁 Repository Files

| File | Purpose | Type |
|------|---------|------|
| `sirti_dashboard_final.py` | Main dashboard application | Python |
| `Activities-SIRTI_04_12_26.csv` | Field operations data export | CSV |
| `requirements.txt` | Python dependencies | Text |
| `README.md` | This documentation file | Markdown |

---

## 📊 Data Overview

**Dataset:** `Activities-SIRTI_04_12_26.csv`

| Metric | Value |
|--------|-------|
| **Total Records** | 165 activities |
| **Date** | April 12, 2026 |
| **Technicians** | 25 field engineers |
| **Activity Types** | Installation (121), IPTV (5), MBB Recovery (4), Audit (4), Troubleshooting (3), 5G Service (3), Home Move (2), Sales Rejection (2) |
| **Order Types** | Triple Play (81), Dual Play (40), ADD IPTV (5), Home Move (2) |
| **Customer Types** | Residential (131), Business (7) |
| **Status Breakdown** | Completed 42.4%, Canceled 38.2%, Suspended 19.4% |
| **Top Zones** | Al Wakrah (25), Al Wukair (18), Old Airport (14), Muaither (8), Nuaija (5) |
| **Service Plans** | GigaHome 1Gbps, 2Gbps, 5G, Business Broadband |

---

## 🛠️ Technology Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Programming language | 3.11+ |
| **Streamlit** | Web dashboard framework | 1.28+ |
| **Plotly** | Interactive charts | 5.15+ |
| **Pandas** | Data processing | 2.0+ |
| **OpenPyXL** | Excel support | 3.1+ |

---

## 🚀 Deployment

### Streamlit Cloud (Recommended - Free)
1. Push code to this GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click **"New app"**
5. Select this repository → `main` branch → `sirti_dashboard_final.py`
6. Click **Deploy**

### Local Development
```bash
pip install -r requirements.txt
streamlit run sirti_dashboard_final.py
