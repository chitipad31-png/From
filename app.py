# ============================================================
#  ระบบจองหัวข้อรายงานกลุ่ม — Unilever Valuation Project
#  รันด้วย: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# 1. ข้อมูลหัวข้อทั้ง 12 ข้อ
# ─────────────────────────────────────────────────────────────
TOPICS = {
    1:  {"title": "เป้าหมายรักษ์โลก",        "desc": "ไปหาว่าแผน 'Unilever Compass' มีเป้าหมายลดคาร์บอน (Net Zero) ภายในปีไหน และเป้าหมายลดพลาสติกคืออะไร (หาแบบสรุปสั้นๆ)"},
    2:  {"title": "สัดส่วนรายได้",             "desc": "ไปหาตาราง 'Revenue Breakdown' ว่าปีล่าสุดบริษัทมีรายได้รวมเท่าไหร่ และมาจากหมวดไหนบ้าง (เช่น ของกิน ของใช้ส่วนตัว) แคปตารางมาเลย"},
    3:  {"title": "ความเสี่ยงอากาศ",           "desc": "เปิดหน้า Principal Risks หาหัวข้อ 'Climate Change' แล้วก๊อปปี้มาว่า บริษัทเขียนว่ามันกระทบธุรกิจยังไงบ้าง"},
    4:  {"title": "ตัวเลขวัตถุดิบ",            "desc": "ไปหาตัวเลขว่าปัจจุบันบริษัทใช้วัตถุดิบทางการเกษตรแบบยั่งยืน (Sustainably Sourced) กี่เปอร์เซ็นต์ เช่น น้ำมันปาล์ม กระดาษ"},
    5:  {"title": "ยอดขายแบรนด์รักษ์โลก",     "desc": "ค้นหาคำว่า 'Purpose-led brands' หรือ 'Sustainable living brands' แล้วหาตัวเลขว่าแบรนด์กลุ่มนี้ยอดขายโต (Growth) กี่เปอร์เซ็นต์"},
    6:  {"title": "การตั้งราคา",               "desc": "ค้นหาคำว่า 'Pricing' หรือ 'Premiumisation' ดูว่าบริษัทมีการขึ้นราคาสินค้าได้เท่าไหร่ในปีล่าสุด แคปตัวเลขมา"},
    7:  {"title": "ตัวเลขลดต้นทุน",            "desc": "ค้นหาคำว่า 'Cost savings' หรือ 'Eco-efficiency' หายอดเงิน (หน่วยล้าน/พันล้านยูโร) ที่บริษัทประหยัดไฟ ประหยัดน้ำในโรงงานได้"},
    8:  {"title": "ตัวเลขงบลงทุน",             "desc": "ค้นหาคำว่า 'Capital Expenditure' (CAPEX) หรือ 'R&D' หาตัวเลขว่าปีล่าสุดบริษัทใช้เงินลงทุนไปกี่ยูโร"},
    9:  {"title": "กำไรจากการดำเนินงาน",       "desc": "ไปหน้างบการเงิน หาคำว่า 'Operating Margin' หรือ 'Underlying Operating Margin' ว่าปีล่าสุดอยู่ที่กี่เปอร์เซ็นต์"},
    10: {"title": "หนี้และดอกเบี้ย",           "desc": "ค้นหาคำว่า 'Green Bond' หรือ 'Sustainability-linked bond' หาว่าบริษัทเคยออกหุ้นกู้รักษ์โลกไหม และมีอัตราดอกเบี้ย (Interest rate) เท่าไหร่"},
    11: {"title": "คะแนน ESG",                 "desc": "ไม่ต้องหาในเล่ม แต่ให้เสิร์ช Google ว่า 'Unilever ESG Rating S&P Global' หรือ 'MSCI' แล้วแคปหน้าจอคะแนนล่าสุดมา"},
    12: {"title": "คะแนนพนักงาน",              "desc": "ค้นหาคำว่า 'Employer of choice' หรือ 'Employee engagement' ในเล่ม หาตัวเลขสถิติว่าพนักงานอยากทำงานกับบริษัทนี้มากแค่ไหน"},
}

# ─────────────────────────────────────────────────────────────
# 2. CSV helpers
# ─────────────────────────────────────────────────────────────
CSV_FILE = "bookings.csv"
CSV_COLUMNS = ["topic_num", "topic_title", "full_name", "nickname", "student_id", "seat_num", "booked_at"]

def load_bookings():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE, dtype=str)
    df = pd.DataFrame(columns=CSV_COLUMNS)
    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
    return df

def save_booking(topic_num, full_name, nickname, student_id, seat_num):
    df = load_bookings()
    new_row = pd.DataFrame([{
        "topic_num":   topic_num,
        "topic_title": TOPICS[topic_num]["title"],
        "full_name":   full_name,
        "nickname":    nickname,
        "student_id":  student_id,
        "seat_num":    seat_num,
        "booked_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

def get_booked_nums(df):
    if df.empty or "topic_num" not in df.columns:
        return []
    return [int(x) for x in df["topic_num"].dropna().tolist()]

# ─────────────────────────────────────────────────────────────
# 3. Page config & CSS
# ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="จองหัวข้อรายงานกลุ่ม", page_icon="📚", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;700;800&family=Inter:wght@400;500;600&family=Sarabun:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter','Sarabun',sans-serif; }

/* ── background ── */
.stApp { background: #f7f9fd; }
section[data-testid="stSidebar"] { display: none; }

/* ── hide streamlit default header padding ── */
.block-container { padding-top: 2rem !important; }

/* ── top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0 20px 0;
    border-bottom: 1px solid #e8eaf0;
    margin-bottom: 28px;
}
.topbar-brand {
    font-family: 'Public Sans',sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: #003d7c;
    letter-spacing: -0.02em;
}
.topbar-sub { font-size: 0.75rem; color: #727782; margin-top: 1px; }

/* ── editorial header ── */
.eyebrow {
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.2em;
    color: #003d7c;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.page-title {
    font-family: 'Public Sans',sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #191c1f;
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin: 0 0 8px 0;
}
.page-subtitle { color: #424751; font-size: 0.95rem; margin: 0 0 28px 0; }

/* ── stat cards ── */
.stat-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 28px; }
.stat-card {
    background: #fff;
    border-radius: 20px;
    padding: 20px 22px;
    border: 1px solid rgba(194,198,211,0.2);
    box-shadow: 0 4px 20px rgba(0,27,61,0.04);
}
.stat-label {
    font-size: 0.62rem; font-weight: 800; color: #727782;
    text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 6px;
}
.stat-value {
    font-family: 'Public Sans',sans-serif;
    font-size: 2.2rem; font-weight: 800; line-height: 1;
}
.stat-value.blue  { color: #003d7c; }
.stat-value.red   { color: #ba1a1a; }
.stat-value.green { color: #16a34a; }
.stat-value.navy  { color: #1254a1; }

/* ── progress bar ── */
.stProgress > div > div > div { background: #003d7c !important; border-radius: 99px; }
.stProgress > div > div { background: #e8eaf0 !important; border-radius: 99px; }

/* ── section title ── */
.sec-title {
    font-family: 'Public Sans',sans-serif;
    font-size: 1rem; font-weight: 700; color: #191c1f;
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 16px;
}
.sec-title::before {
    content: '';
    display: inline-block;
    width: 4px; height: 18px;
    background: #003d7c;
    border-radius: 99px;
}

/* ── topic card (description box) ── */
.topic-card {
    background: #fff;
    border-radius: 16px;
    border: 1px solid #dde3f0;
    padding: 18px 22px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,27,61,0.04);
}
.topic-card .tc-num {
    font-size: 0.65rem; font-weight: 800; color: #003d7c;
    text-transform: uppercase; letter-spacing: 0.15em;
}
.topic-card .tc-title {
    font-family: 'Public Sans',sans-serif;
    font-size: 1.05rem; font-weight: 700; color: #191c1f;
    margin: 4px 0 8px 0;
}
.topic-card .tc-desc { font-size: 0.88rem; color: #424751; line-height: 1.6; }

/* ── input labels ── */
.stTextInput label, .stSelectbox label,
.stTextArea label, .stFileUploader label {
    color: #191c1f !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.01em !important;
    text-transform: uppercase !important;
}

/* ── inputs ── */
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid #dde3f0 !important;
    font-size: 0.95rem !important;
    padding: 10px 14px !important;
    background: #fff !important;
}
.stTextInput > div > div > input:focus {
    border-color: #003d7c !important;
    box-shadow: 0 0 0 3px rgba(0,61,124,0.1) !important;
}

/* ── submit button ── */
div[data-testid="stForm"] .stButton > button {
    background: #003d7c;
    color: #fff;
    border: none;
    border-radius: 12px;
    padding: 13px 0;
    font-size: 0.85rem;
    font-weight: 800;
    font-family: 'Inter','Sarabun',sans-serif;
    width: 100%;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    transition: background .15s, transform .1s, box-shadow .15s;
    box-shadow: 0 4px 14px rgba(0,61,124,0.25);
}
div[data-testid="stForm"] .stButton > button:hover {
    background: #00468c;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(0,61,124,0.3);
}

/* ── dashboard list ── */
.dash-header {
    font-family: 'Public Sans',sans-serif;
    font-size: 1rem; font-weight: 700; color: #191c1f;
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 12px;
}
.dash-header::before {
    content: '';
    display: inline-block;
    width: 4px; height: 18px;
    background: #003d7c; border-radius: 99px;
}

/* topic row cards */
.topic-row {
    background: #fff;
    border-radius: 14px;
    border: 1px solid #eaecf2;
    padding: 14px 18px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 1px 6px rgba(0,27,61,0.03);
    transition: box-shadow .15s;
}
.topic-row:hover { box-shadow: 0 4px 16px rgba(0,27,61,0.07); }
.topic-row-left { display: flex; align-items: center; gap: 14px; }
.topic-num-bubble {
    width: 36px; height: 36px; border-radius: 50%;
    background: #eef2fb;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Public Sans',sans-serif;
    font-size: 0.9rem; font-weight: 800; color: #003d7c;
    flex-shrink: 0;
}
.topic-row-title { font-size: 0.92rem; font-weight: 600; color: #191c1f; }
.topic-row-sub   { font-size: 0.75rem; color: #727782; margin-top: 1px; }
.badge-booked {
    display: flex; align-items: center; gap: 6px;
    background: rgba(186,26,26,0.07);
    border-radius: 10px; padding: 5px 12px;
    font-size: 0.75rem; font-weight: 700; color: #93000a;
    white-space: nowrap;
}
.badge-available {
    display: flex; align-items: center; gap: 6px;
    background: #f0faf4;
    border: 1px solid #bbf0ce;
    border-radius: 10px; padding: 5px 12px;
    font-size: 0.75rem; font-weight: 700; color: #16a34a;
    white-space: nowrap;
}
.dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.dot.red   { background: #ba1a1a; }
.dot.green { background: #16a34a; }

/* ── metric override ── */
[data-testid="stMetric"] {
    background: #fff;
    border-radius: 16px;
    padding: 16px 20px;
    border: 1px solid rgba(194,198,211,0.2);
    box-shadow: 0 4px 20px rgba(0,27,61,0.04);
}
[data-testid="stMetricLabel"] { color:#727782!important; font-size:0.65rem!important; font-weight:800!important; text-transform:uppercase; letter-spacing:0.12em; }
[data-testid="stMetricValue"] { color:#003d7c!important; font-family:'Public Sans',sans-serif!important; font-weight:800!important; }

/* ── download button ── */
.stDownloadButton > button {
    background: #fff !important;
    color: #003d7c !important;
    border: 1.5px solid #dde3f0 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em !important;
    transition: background .15s !important;
}
.stDownloadButton > button:hover {
    background: #f0f4ff !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 4. Load data
# ─────────────────────────────────────────────────────────────
bookings_df  = load_bookings()
booked_nums  = get_booked_nums(bookings_df)
total_booked = len(booked_nums)
remaining    = 12 - total_booked
pct          = int(total_booked / 12 * 100)

available_options = [f"ข้อ {n}: {TOPICS[n]['title']}" for n in TOPICS if n not in booked_nums]

# ─────────────────────────────────────────────────────────────
# 5. Top bar
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div>
        <div class="topbar-brand">📚 Unilever Valuation</div>
        <div class="topbar-sub">Management Dashboard · ระบบจองหัวข้อรายงานกลุ่ม</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 6. Editorial header
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="eyebrow">Booking Status</div>
<div class="page-title">สถานะการจอง</div>
<div class="page-subtitle">เลือกหัวข้อ 1 ข้อต่อคน · จองแล้วจองเลย ห้ามซ้ำ!</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 7. Stat cards
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-row">
    <div class="stat-card">
        <div class="stat-label">ทั้งหมด</div>
        <div class="stat-value blue">12</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">จองแล้ว</div>
        <div class="stat-value red">{total_booked}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">คงเหลือ</div>
        <div class="stat-value green">{remaining}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">ความคืบหน้า</div>
        <div class="stat-value navy">{pct}%</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.progress(total_booked / 12)
st.markdown("<div style='margin-bottom:28px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 8. ฟอร์มจองหัวข้อ
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="sec-title">กรอกข้อมูลเพื่อจองหัวข้อ</div>', unsafe_allow_html=True)

if not available_options:
    st.warning("🎊 ทุกหัวข้อถูกจองครบแล้ว! ดูรายชื่อด้านล่างได้เลย")
else:
    selected_label = st.selectbox("เลือกหัวข้อที่ต้องการจอง *", options=available_options,
                                   help="หัวข้อที่จองแล้วจะไม่ปรากฏ")

    if selected_label:
        selected_num = int(selected_label.split(":")[0].replace("ข้อ","").strip())
        info = TOPICS[selected_num]
        st.markdown(f"""
        <div class="topic-card">
            <div class="tc-num">ข้อ {selected_num} · หน้าที่ของคุณ</div>
            <div class="tc-title">{info['title']}</div>
            <div class="tc-desc">{info['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

    with st.form("booking_form", clear_on_submit=True):
        r1c1, r1c2, r1c3, r1c4 = st.columns([3, 2, 2, 1])
        with r1c1: full_name  = st.text_input("ชื่อ-นามสกุล *",  placeholder="สมชาย ใจดี")
        with r1c2: nickname   = st.text_input("ชื่อเล่น *",       placeholder="ฟลุค")
        with r1c3: student_id = st.text_input("รหัสนักศึกษา *",   placeholder="1680103619")
        with r1c4: seat_num   = st.text_input("เลขที่ *",          placeholder="1")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔒  ยืนยันการจอง")

    if submitted:
        errors = []
        if not full_name.strip():  errors.append("ชื่อ-นามสกุล")
        if not nickname.strip():   errors.append("ชื่อเล่น")
        if not student_id.strip(): errors.append("รหัสนักศึกษา")
        if not seat_num.strip():   errors.append("เลขที่")
        if errors:
            st.error(f"⚠️ กรุณากรอกให้ครบ: **{', '.join(errors)}**")
        else:
            save_booking(selected_num, full_name.strip(), nickname.strip(),
                         student_id.strip(), seat_num.strip())
            st.success(f"✅ **{nickname.strip()}** จองข้อ {selected_num}: **{TOPICS[selected_num]['title']}** สำเร็จแล้ว!")
            st.balloons()
            st.rerun()

st.markdown("<div style='margin:32px 0 8px 0'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 9. Dashboard — topic row cards (Stitch style)
# ─────────────────────────────────────────────────────────────
bookings_df = load_bookings()

st.markdown('<div class="dash-header">รายชื่อหัวข้อและสถานะ</div>', unsafe_allow_html=True)

# build rows — render ทีละ row
for num, info in TOPICS.items():
    match = bookings_df[bookings_df["topic_num"].astype(str) == str(num)]
    if match.empty:
        badge = '<div class="badge-available"><div class="dot green"></div>ว่าง · เปิดให้ลงทะเบียน</div>'
        person = ""
    else:
        row = match.iloc[0]
        name = row.get("nickname", "—")
        seat = row.get("seat_num", "—")
        badge = f'<div class="badge-booked"><div class="dot red"></div>จองแล้ว</div>'
        person = f'<div class="topic-row-sub">{name} · เลขที่ {seat}</div>'

    st.markdown(f"""
    <div class="topic-row">
        <div class="topic-row-left">
            <div class="topic-num-bubble">{num}</div>
            <div>
                <div class="topic-row-title">{info['title']}</div>
                {person}
            </div>
        </div>
        {badge}
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 10. Export + แก้ไข/ลบ
# ─────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
col_dl, col_gap = st.columns([2, 5])
with col_dl:
    dashboard_rows = []
    for num, info in TOPICS.items():
        match = bookings_df[bookings_df["topic_num"].astype(str) == str(num)]
        if match.empty:
            dashboard_rows.append({"ข้อที่": num, "หัวข้อ": info["title"], "สถานะ": "ว่าง",
                                    "ชื่อ-นามสกุล": "—", "ชื่อเล่น": "—", "รหัสนักศึกษา": "—", "เลขที่": "—"})
        else:
            r = match.iloc[0]
            dashboard_rows.append({"ข้อที่": num, "หัวข้อ": info["title"], "สถานะ": "จองแล้ว",
                                    "ชื่อ-นามสกุล": r.get("full_name","—"), "ชื่อเล่น": r.get("nickname","—"),
                                    "รหัสนักศึกษา": r.get("student_id","—"), "เลขที่": r.get("seat_num","—")})
    csv_export = pd.DataFrame(dashboard_rows).to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️  Export สรุปการจอง (.csv)", data=csv_export,
                       file_name=f"booking_summary_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
with st.expander("✏️ แก้ไขหรือลบรายการจอง"):
    if bookings_df.empty:
        st.info("ยังไม่มีข้อมูลการจอง")
    else:
        options = [f"ข้อ {row['topic_num']} — {row['nickname']} ({row['full_name']})"
                   for _, row in bookings_df.iterrows()]
        selected = st.selectbox("เลือกรายการที่อยากแก้/ลบ", options)
        idx = options.index(selected)
        row = bookings_df.iloc[idx]
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("ชื่อ-นามสกุล", value=row["full_name"])
            new_nick = st.text_input("ชื่อเล่น",      value=row["nickname"])
        with col2:
            new_sid  = st.text_input("รหัสนักศึกษา",  value=row["student_id"])
            new_seat = st.text_input("เลขที่",         value=row["seat_num"])
        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("💾 บันทึกการแก้ไข"):
                bookings_df.at[idx, "full_name"]  = new_name.strip()
                bookings_df.at[idx, "nickname"]   = new_nick.strip()
                bookings_df.at[idx, "student_id"] = new_sid.strip()
                bookings_df.at[idx, "seat_num"]   = new_seat.strip()
                bookings_df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
                st.success("✅ แก้ไขเรียบร้อย!")
                st.rerun()
        with btn2:
            if st.button("🗑️ ลบรายการนี้", type="primary"):
                bookings_df = bookings_df.drop(index=idx).reset_index(drop=True)
                bookings_df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
                st.success("✅ ลบเรียบร้อย!")
                st.rerun()
