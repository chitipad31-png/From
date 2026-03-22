# ============================================================
#  ระบบจองหัวข้อรายงานกลุ่ม — Unilever Valuation Project
#  รันด้วย: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import os
from datetime import datetime

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

# ── Page config ──
st.set_page_config(page_title="จองหัวข้อรายงานกลุ่ม", page_icon="📚", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;700;800&family=Sarabun:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Sarabun',sans-serif; }
.stApp { background: #f7f9fd; }
.block-container { padding-top: 2rem !important; }
.stTextInput label, .stSelectbox label, .stTextArea label {
    color: #191c1f !important; font-weight: 600 !important;
    font-size: 0.82rem !important; text-transform: uppercase !important;
}
div[data-testid="stForm"] .stButton > button {
    background: #003d7c; color: #fff; border: none; border-radius: 12px;
    padding: 13px 0; font-size: 0.85rem; font-weight: 800; width: 100%;
    letter-spacing: 0.1em; text-transform: uppercase;
    box-shadow: 0 4px 14px rgba(0,61,124,0.25);
}
div[data-testid="stForm"] .stButton > button:hover { background: #00468c; }
.stDownloadButton > button {
    background: #fff !important; color: #003d7c !important;
    border: 1.5px solid #dde3f0 !important; border-radius: 10px !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load data ──
bookings_df  = load_bookings()
booked_nums  = get_booked_nums(bookings_df)
total_booked = len(booked_nums)
remaining    = 12 - total_booked
available_options = [f"ข้อ {n}: {TOPICS[n]['title']}" for n in TOPICS if n not in booked_nums]

# ── Top bar ──
st.markdown("""
<div style="display:flex;align-items:center;padding:0 0 20px 0;border-bottom:1px solid #e8eaf0;margin-bottom:28px;">
  <div>
    <div style="font-family:'Public Sans',sans-serif;font-size:1.1rem;font-weight:800;color:#003d7c;">📚 Unilever Valuation</div>
    <div style="font-size:0.75rem;color:#727782;margin-top:1px;">Management Dashboard · ระบบจองหัวข้อรายงานกลุ่ม</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown(f"""
<div style="font-size:0.65rem;font-weight:800;letter-spacing:0.2em;color:#003d7c;text-transform:uppercase;margin-bottom:6px;">Booking Status</div>
<div style="font-family:'Public Sans',sans-serif;font-size:2.2rem;font-weight:800;color:#191c1f;letter-spacing:-0.04em;line-height:1.1;margin:0 0 8px 0;">สถานะการจอง</div>
<div style="color:#424751;font-size:0.95rem;margin:0 0 28px 0;">เลือกหัวข้อ 1 ข้อต่อคน · จองแล้วจองเลย ห้ามซ้ำ!</div>
""", unsafe_allow_html=True)

# ── Stat cards ──
c1, c2 = st.columns(2)
for col, label, value, color in [
    (c1, "จองแล้ว", total_booked, "#ba1a1a"),
    (c2, "คงเหลือ", remaining,    "#16a34a"),
]:
    with col:
        st.markdown(f"""
<div style="background:#fff;border-radius:20px;padding:20px 22px;border:1px solid rgba(194,198,211,0.2);box-shadow:0 4px 20px rgba(0,27,61,0.04);margin-bottom:24px;">
  <div style="font-size:0.62rem;font-weight:800;color:#727782;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:6px;">{label}</div>
  <div style="font-family:'Public Sans',sans-serif;font-size:2.2rem;font-weight:800;color:{color};line-height:1;">{value}</div>
</div>
""", unsafe_allow_html=True)

# ── Section: ฟอร์มจอง ──
st.markdown("""
<div style="font-size:1rem;font-weight:700;color:#191c1f;display:flex;align-items:center;gap:8px;margin-bottom:16px;">
  <span style="display:inline-block;width:4px;height:18px;background:#003d7c;border-radius:99px;"></span>
  กรอกข้อมูลเพื่อจองหัวข้อ
</div>
""", unsafe_allow_html=True)

if not available_options:
    st.warning("🎊 ทุกหัวข้อถูกจองครบแล้ว!")
else:
    # ── ปุ่มเลือกหัวข้อ ──
    if "selected_topic" not in st.session_state:
        st.session_state["selected_topic"] = None

    st.markdown("<div style='font-size:0.82rem;font-weight:600;color:#191c1f;text-transform:uppercase;margin-bottom:10px;'>เลือกหัวข้อที่ต้องการจอง *</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    for i, opt in enumerate(available_options):
        num = int(opt.split(":")[0].replace("ข้อ","").strip())
        is_selected = st.session_state["selected_topic"] == num
        with cols[i % 3]:
            if st.button(opt, use_container_width=True,
                         type="primary" if is_selected else "secondary"):
                st.session_state["selected_topic"] = num
                st.rerun()

    selected_num = st.session_state["selected_topic"]

    # ── คำอธิบายหัวข้อที่เลือก ──
    if selected_num and selected_num in TOPICS:
        info = TOPICS[selected_num]
        st.markdown(f"""
<div style="background:#fff;border-radius:16px;border:1px solid #dde3f0;padding:18px 22px;margin:12px 0 16px 0;box-shadow:0 2px 12px rgba(0,27,61,0.04);">
  <div style="font-size:0.65rem;font-weight:800;color:#003d7c;text-transform:uppercase;letter-spacing:0.15em;">ข้อ {selected_num} · หน้าที่ของคุณ</div>
  <div style="font-family:'Public Sans',sans-serif;font-size:1.05rem;font-weight:700;color:#191c1f;margin:4px 0 8px 0;">{info['title']}</div>
  <div style="font-size:0.88rem;color:#424751;line-height:1.6;">{info['desc']}</div>
</div>
""", unsafe_allow_html=True)

    # ── ฟอร์มกรอกข้อมูล ──
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
        if not selected_num:       errors.append("หัวข้อที่จอง")
        if errors:
            st.error(f"⚠️ กรุณากรอกให้ครบ: **{', '.join(errors)}**")
        else:
            save_booking(selected_num, full_name.strip(), nickname.strip(),
                         student_id.strip(), seat_num.strip())
            st.session_state["selected_topic"] = None
            st.success(f"✅ **{nickname.strip()}** จองข้อ {selected_num}: **{TOPICS[selected_num]['title']}** สำเร็จแล้ว!")
            st.balloons()
            st.rerun()

st.markdown("<div style='margin:32px 0 8px 0'></div>", unsafe_allow_html=True)

# ── Dashboard ──
bookings_df = load_bookings()

st.markdown("""
<div style="font-size:1rem;font-weight:700;color:#191c1f;display:flex;align-items:center;gap:8px;margin-bottom:12px;">
  <span style="display:inline-block;width:4px;height:18px;background:#003d7c;border-radius:99px;"></span>
  รายชื่อหัวข้อและสถานะ
</div>
""", unsafe_allow_html=True)

for num, info in TOPICS.items():
    match = bookings_df[bookings_df["topic_num"].astype(str) == str(num)]
    if match.empty:
        badge = '<span style="display:inline-flex;align-items:center;gap:6px;background:#f0faf4;border:1px solid #bbf0ce;border-radius:10px;padding:5px 12px;font-size:0.75rem;font-weight:700;color:#16a34a;white-space:nowrap"><span style="width:7px;height:7px;border-radius:50%;background:#16a34a;display:inline-block;flex-shrink:0"></span>ว่าง</span>'
        sub = ""
    else:
        r = match.iloc[0]
        name = r.get("nickname","—")
        seat = r.get("seat_num","—")
        badge = f'<span style="display:inline-flex;align-items:center;gap:6px;background:rgba(186,26,26,0.07);border-radius:10px;padding:5px 12px;font-size:0.75rem;font-weight:700;color:#93000a;white-space:nowrap"><span style="width:7px;height:7px;border-radius:50%;background:#ba1a1a;display:inline-block;flex-shrink:0"></span>จองแล้ว · {name} เลขที่ {seat}</span>'
        sub = f'<span style="font-size:0.75rem;color:#727782;margin-left:6px;">· {name} เลขที่ {seat}</span>'

    st.markdown(f"""
<div style="background:#fff;border-radius:14px;border:1px solid #eaecf2;padding:14px 18px;margin-bottom:4px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 1px 6px rgba(0,27,61,0.03);">
  <span style="display:inline-flex;align-items:center;gap:14px;">
    <span style="width:36px;height:36px;border-radius:50%;background:#eef2fb;display:inline-flex;align-items:center;justify-content:center;font-size:0.9rem;font-weight:800;color:#003d7c;flex-shrink:0">{num}</span>
    <span style="font-size:0.92rem;font-weight:600;color:#191c1f">{info['title']}{sub}</span>
  </span>
  {badge}
</div>
""", unsafe_allow_html=True)

    with st.expander(f"　📖 ดูรายละเอียดข้อ {num}"):
        st.markdown(f"""
<div style="background:#f7f9ff;border-radius:10px;padding:14px 18px;font-size:0.88rem;color:#424751;line-height:1.7;border-left:3px solid #003d7c;">
  {info['desc']}
</div>
""", unsafe_allow_html=True)

# ── Export + แก้ไข/ลบ ──
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
