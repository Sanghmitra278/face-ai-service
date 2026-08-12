import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="AI Face Platform",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Demo data. Replace these with calls to your FastAPI dashboard endpoints.
employees = pd.DataFrame([
    [1, "Aarav Sharma", "Engineering", "Present", "09:02", "18:01", 0.91],
    [2, "Priya Verma", "HR", "Present", "09:18", "18:12", 0.88],
    [3, "Rahul Singh", "Finance", "Present", "09:11", "17:42", 0.82],
    [4, "Neha Gupta", "Engineering", "Late", "10:14", "-", 0.79],
    [5, "Vikram Das", "Operations", "Absent", "-", "-", 0.00],
    [6, "Ananya Rao", "HR", "Present", "08:56", "17:58", 0.94],
    [7, "Rohit Kumar", "Operations", "Present", "09:27", "-", 0.86],
    [8, "Meera Joshi", "Finance", "Present", "09:04", "18:05", 0.90],
], columns=[
    "Employee ID", "Employee", "Department", "Status",
    "Check In", "Check Out", "Similarity"
])

trend = pd.DataFrame({
    "Date": pd.date_range(datetime.now().date() - timedelta(days=6), periods=7),
    "Present": [196, 204, 211, 208, 217, 213, 217],
    "Absent": [32, 24, 17, 20, 11, 15, 13],
    "Late": [18, 21, 14, 17, 14, 19, 14],
})

st.markdown("""
<style>
.stApp { background:#0b1220; color:#e5e7eb; }
[data-testid="stSidebar"] { background:#111827; border-right:1px solid #243047; }
[data-testid="stSidebar"] * { color:#dbe4f0 !important; }
.block-container { padding-top:1.6rem; max-width:1500px; }
.kpi {
 background:linear-gradient(145deg,#111c2e,#0e1727);
 border:1px solid #24324a; border-radius:14px; padding:18px 20px;
 min-height:118px;
}
.kpi-label { color:#94a3b8; font-size:13px; margin-bottom:10px; }
.kpi-value { color:#f8fafc; font-size:30px; font-weight:700; }
.kpi-sub { color:#64748b; font-size:12px; margin-top:5px; }
.small-muted { color:#94a3b8; font-size:13px; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ◉ AI FACE")
    st.markdown("### Platform")
    st.caption("Employee Identity & Attendance")
    st.divider()
    st.radio(
        "Navigation",
        ["Overview", "Employees", "Attendance", "Recognition"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**System Status**")
    st.success("API Online")
    st.success("PostgreSQL Connected")
    st.success("SCRFD Loaded")
    st.success("ArcFace Loaded")
    st.divider()
    st.caption("AI Face Platform v1.0.0")

c1, c2 = st.columns([4, 1])
with c1:
    st.title("Attendance Dashboard")
    st.markdown(
        '<span class="small-muted">AI-powered employee identity verification and attendance</span>',
        unsafe_allow_html=True,
    )
with c2:
    st.date_input("Date", datetime.now().date())

st.write("")

kpis = [
    ("TOTAL EMPLOYEES", "248", "Registered employees"),
    ("PRESENT TODAY", "217", "87.5% attendance"),
    ("LATE ARRIVALS", "14", "5.6% of workforce"),
    ("ABSENT TODAY", "13", "Requires attention"),
    ("VERIFICATION FAILURES", "7", "Last 24 hours"),
]
cols = st.columns(5)
for col, (label, value, sub) in zip(cols, kpis):
    with col:
        st.markdown(
            f'<div class="kpi"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")
left, right = st.columns([2, 1])
with left:
    st.markdown("### Attendance Trend")
    st.line_chart(trend.set_index("Date")[["Present", "Absent", "Late"]], height=310)
with right:
    st.markdown("### Today's Status")
    status = pd.DataFrame({"Employees": [217, 14, 13]},
                          index=["Present", "Late", "Absent"])
    st.bar_chart(status, height=310)

st.write("")
a, b, c = st.columns(3)
with a:
    st.markdown("### Recognition Performance")
    st.metric("Average Similarity", "0.86")
    st.progress(0.86)
    st.caption("Verification threshold: 0.62")
with b:
    st.markdown("### Enrollment Quality")
    st.metric("Average Quality", "91%")
    st.progress(0.91)
    st.caption("Multi-pose enrollment enabled")
with c:
    st.markdown("### Security Events")
    st.metric("Suspicious Attempts", "2")
    st.caption("7 failed verifications in last 24 hours")

st.write("")
st.markdown("### Today's Employee Activity")
search = st.text_input("Search employee", placeholder="Search by employee name or ID...")
filtered = employees.copy()
if search:
    filtered = filtered[
        filtered["Employee"].str.contains(search, case=False, na=False)
        | filtered["Employee ID"].astype(str).str.contains(search, na=False)
    ]
display = filtered.copy()
display["Similarity"] = display["Similarity"].apply(lambda x: f"{x:.2f}" if x > 0 else "-")
st.dataframe(display, use_container_width=True, hide_index=True)

st.write("")
st.markdown("### Recent Verification Events")
events = pd.DataFrame([
    ["09:27:14", "Rohit Kumar", "EMP007", "Verified", "0.86", "Office-PC-01"],
    ["09:18:03", "Priya Verma", "EMP002", "Verified", "0.88", "Office-PC-01"],
    ["09:11:27", "Rahul Singh", "EMP003", "Verified", "0.82", "Office-PC-01"],
    ["09:08:41", "Unknown", "-", "Rejected", "0.41", "Office-PC-01"],
    ["09:04:52", "Meera Joshi", "EMP008", "Verified", "0.90", "Office-PC-01"],
], columns=["Time", "Employee", "Employee ID", "Result", "Similarity", "Device"])
st.dataframe(events, use_container_width=True, hide_index=True)

st.caption("Demo dashboard — connect the widgets to your FastAPI dashboard endpoints when ready.")