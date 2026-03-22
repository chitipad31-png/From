# ============================================================
#  ระบบจองหัวข้อรายงานกลุ่ม — Unilever Valuation Project
#  รันด้วย: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import datetime

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

@st.cache_resource
def get_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_client()

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

def load_bookings():
    res = supabase.table("bookings").select("*").execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

def save_booking(topic_num, full_name, nickname, student_id, seat_num):
    supabase.table("bookings").insert({
        "topic_num":   topic_num,
        "topic_title": TOPICS[topic_num]["title"],
        "full_name":   full_name,
        "nickname":    nickname,
        "student_id":  student_id,
        "seat_num":    seat_num,
        "booked_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }).execute()

def delete_booking(row_id):
    supabase.table("bookings").delete().eq("id", row_id).execute()

def update_booking(row_id, full_name, nickname, student_id, seat_num):
    supabase.table("bookings").update({
        "full_name":  full_name,
        "nickname":   nickname,
        "student_id": student_id,
        "seat_num":   seat_num,
    }).eq("id", row_id).execute()

def get_booked_nums(df):
    if df.empty or "topic_num" not in df.columns:
        return []
    return [int(x) for x in df["topic_num"].dropna().tolist()]

st.set_page_config(page_title="จองหัวข้อรายงานกลุ่ม", page_icon="📚", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;600;700;800&family=Sarabun:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Sarabun',sans-serif; }
.stApp { background: #f7f9fd; }
.block-container { padding-top: 2rem !important; }
.stTextInput label { color:#191c1f !important; font-weight:600 !important; font-size:0.82rem !important; text-transform:uppercase !important; }
div[data-testid="stForm"] .stButton > button {
    background:#003d7c; color:#fff; border:none; border-radius:12px;
    padding:13px 0; font-size:0.85rem; font-weight:800; width:100%;
    letter-spacing:0.1em; text-transform:uppercase;
    box-shadow:0 4px 14px rgba(0,61,124,0.25);
}
div[data-testid="stForm"] .stButton > button:hover { background:#00468c; }
.stDownloadButton > button {
    background:#fff !important; color:#003d7c !important;
    border:1.5px solid #dde3f0 !important; border-radius:10px !important; font-weight:700 !important;
}
</style>
""", unsafe_allow_html=True)

bookings_df  = load_bookings()
booked_nums  = get_booked_nums(bookings_df)
total_booked = len(booked_nums)
remaining    = 12 - total_booked
available_options = [f"ข้อ {n}: {TOPICS[n]['title']}" for n in TOPICS if n not in booked_nums]

st.markdown("""
<div style="display:flex;align-items:center;padding:0 0 20px 0;border-bottom:1px solid #e8eaf0;margin-bottom:28px;">
  <div>
    <div style="font-family:'Public Sans',sans-serif;font-size:1.1rem;font-weight:800;color:#003d7c;">📚 Unilever Valuation</div>
    <div style="font-size:0.75rem;color:#727782;margin-top:1px;">Management Dashboard · ระบบจองหัวข้อรายงานกลุ่ม</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-size:0.65rem;font-weight:800;letter-spacing:0.2em;color:#003d7c;text-transform:uppercase;margin-bottom:6px;">Booking Status</div>
<div style="font-family:'Public Sans',sans-serif;font-size:2.2rem;font-weight:800;color:#191c1f;letter-spacing:-0.04em;line-height:1.1;margin:0 0 8px 0;">สถานะการจอง</div>
<div style="color:#424751;font-size:0.95rem;margin:0 0 28px 0;">เลือกหัวข้อ 1 ข้อต่อคน · จองแล้วจองเลย ห้ามซ้ำ!</div>
""", unsafe_allow_html=True)

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

st.markdown("""
<div style="font-size:1rem;font-weight:700;color:#191c1f;display:flex;align-items:center;gap:8px;margin-bottom:16px;">
  <span style="display:inline-block;width:4px;height:18px;background:#003d7c;border-radius:99px;"></span>
  กรอกข้อมูลเพื่อจองหัวข้อ
</div>
""", unsafe_allow_html=True)

if not available_options:
    st.warning("🎊 ทุกหัวข้อถูกจองครบแล้ว!")
else:
    if "selected_topic" not in st.session_state:
        st.session_state["selected_topic"] = None

    selected_num = st.session_state["selected_topic"]

    if selected_num and selected_num in TOPICS:
        col_msg, col_reset = st.columns([5, 1])
        with col_msg:
            st.markdown(f"""
<div style="background:#eef4ff;border-radius:12px;border:1.5px solid #003d7c;padding:12px 18px;margin-bottom:16px;display:flex;align-items:center;gap:10px;">
  <span style="font-size:1.2rem">✅</span>
  <span style="font-size:0.9rem;font-weight:700;color:#003d7c;">เลือกข้อ {selected_num}: {TOPICS[selected_num]['title']} แล้ว — กรอกข้อมูลด้านล่างแล้วกดยืนยัน</span>
</div>
""", unsafe_allow_html=True)
        with col_reset:
            if st.button("❌ ยกเลิก", use_container_width=True):
                st.session_state["selected_topic"] = None
                st.rerun()
    else:
        st.markdown("""
<div style="background:#fff8e1;border-radius:12px;border:1.5px solid #f59e0b;padding:12px 18px;margin-bottom:16px;display:flex;align-items:center;gap:10px;">
  <span style="font-size:1.2rem">👇</span>
  <span style="font-size:0.9rem;font-weight:700;color:#92400e;">กดปุ่ม "จอง" ที่หัวข้อด้านล่างก่อน แล้วค่อยกรอกข้อมูล</span>
</div>
""", unsafe_allow_html=True)

    with st.form("booking_form", clear_on_submit=True):
        r1c1, r1c2, r1c3, r1c4 = st.columns([3, 2, 2, 1])
        with r1c1: full_name  = st.text_input("ชื่อ-นามสกุล *",  placeholder="สมชาย ใจดี")
        with r1c2: nickname   = st.text_input("ชื่อเล่น *",       placeholder="ฟลุ๊คเอง")
        with r1c3: student_id = st.text_input("รหัสนักศึกษา *",   placeholder="168010XXXX")
        with r1c4: seat_num   = st.text_input("เลขที่ *",          placeholder="1")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "🔒  ยืนยันการจอง" if selected_num else "⬇️  เลือกหัวข้อก่อนกดจอง",
            disabled=not selected_num
        )

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
            st.session_state["selected_topic"] = None
            st.success(f"✅ **{nickname.strip()}** จองข้อ {selected_num}: **{TOPICS[selected_num]['title']}** สำเร็จแล้ว!")
            st.balloons()
            st.rerun()

st.markdown("<div style='margin:32px 0 8px 0'></div>", unsafe_allow_html=True)

bookings_df = load_bookings()

st.markdown("""
<div style="font-size:1rem;font-weight:700;color:#191c1f;display:flex;align-items:center;gap:8px;margin-bottom:12px;">
  <span style="display:inline-block;width:4px;height:18px;background:#003d7c;border-radius:99px;"></span>
  รายชื่อหัวข้อและสถานะ
</div>
""", unsafe_allow_html=True)

for num, info in TOPICS.items():
    match = bookings_df[bookings_df["topic_num"].astype(str) == str(num)] if not bookings_df.empty else pd.DataFrame()
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

    col_detail, col_book = st.columns([4, 1])
    with col_detail:
        with st.expander(f"　📖 ดูรายละเอียดข้อ {num}"):
            st.markdown(f"""
<div style="background:#f7f9ff;border-radius:10px;padding:14px 18px;font-size:0.88rem;color:#424751;line-height:1.7;border-left:3px solid #003d7c;">
  {info['desc']}
</div>
""", unsafe_allow_html=True)
    with col_book:
        if match.empty:
            is_selected = st.session_state.get("selected_topic") == num
            if st.button("✅ เลือก" if is_selected else "จอง", key=f"book_{num}",
                         use_container_width=True, type="secondary" if is_selected else "primary"):
                st.session_state["selected_topic"] = num
                st.rerun()
        else:
            st.markdown("<div style='padding:8px 0;font-size:0.8rem;color:#727782;text-align:center'>จองแล้ว</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
col_dl, col_gap = st.columns([2, 5])
with col_dl:
    export_rows = []
    for num, info in TOPICS.items():
        match = bookings_df[bookings_df["topic_num"].astype(str) == str(num)] if not bookings_df.empty else pd.DataFrame()
        if match.empty:
            export_rows.append({"ข้อที่": num, "หัวข้อ": info["title"], "สถานะ": "ว่าง",
                                 "ชื่อ-นามสกุล": "—", "ชื่อเล่น": "—", "รหัสนักศึกษา": "—", "เลขที่": "—"})
        else:
            r = match.iloc[0]
            export_rows.append({"ข้อที่": num, "หัวข้อ": info["title"], "สถานะ": "จองแล้ว",
                                 "ชื่อ-นามสกุล": r.get("full_name","—"), "ชื่อเล่น": r.get("nickname","—"),
                                 "รหัสนักศึกษา": r.get("student_id","—"), "เลขที่": r.get("seat_num","—")})
    csv = pd.DataFrame(export_rows).to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️  Export สรุปการจอง (.csv)", data=csv,
                       file_name=f"booking_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

st.markdown("<div style='margin-top:16px'></div>", unsafe_allow_html=True)
with st.expander("✏️ แก้ไขหรือลบรายการจอง"):
    if bookings_df.empty:
        st.info("ยังไม่มีข้อมูลการจอง")
    else:
        options = [f"ข้อ {r['topic_num']} — {r['nickname']} ({r['full_name']})"
                   for _, r in bookings_df.iterrows()]
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
                update_booking(row["id"], new_name.strip(), new_nick.strip(),
                               new_sid.strip(), new_seat.strip())
                st.success("✅ แก้ไขเรียบร้อย!")
                st.rerun()
        with btn2:
            if st.button("🗑️ ลบรายการนี้", type="primary"):
                delete_booking(row["id"])
                st.success("✅ ลบเรียบร้อย!")
                st.rerun()
