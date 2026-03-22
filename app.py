# ============================================================
#  ระบบจองหัวข้อรายงานกลุ่ม — Unilever Valuation Project
#  รันด้วย: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# 1. ข้อมูลหัวข้อทั้ง 12 ข้อ (หมายเลข → ชื่อหัวข้อ + คำอธิบาย)
# ─────────────────────────────────────────────────────────────
TOPICS = {
    1: {
        "title": "เป้าหมายรักษ์โลก",
        "desc": (
            "ไปหาว่าแผน 'Unilever Compass' มีเป้าหมายลดคาร์บอน (Net Zero) ภายในปีไหน "
            "และเป้าหมายลดพลาสติกคืออะไร (หาแบบสรุปสั้นๆ)"
        ),
    },
    2: {
        "title": "สัดส่วนรายได้",
        "desc": (
            "ไปหาตาราง 'Revenue Breakdown' ว่าปีล่าสุดบริษัทมีรายได้รวมเท่าไหร่ "
            "และมาจากหมวดไหนบ้าง (เช่น ของกิน ของใช้ส่วนตัว) แคปตารางมาเลย"
        ),
    },
    3: {
        "title": "ความเสี่ยงอากาศ",
        "desc": (
            "เปิดหน้า Principal Risks หาหัวข้อ 'Climate Change' แล้วก๊อปปี้มาว่า "
            "บริษัทเขียนว่ามันกระทบธุรกิจยังไงบ้าง"
        ),
    },
    4: {
        "title": "ตัวเลขวัตถุดิบ",
        "desc": (
            "ไปหาตัวเลขว่าปัจจุบันบริษัทใช้วัตถุดิบทางการเกษตรแบบยั่งยืน "
            "(Sustainably Sourced) กี่เปอร์เซ็นต์ เช่น น้ำมันปาล์ม กระดาษ"
        ),
    },
    5: {
        "title": "ยอดขายแบรนด์รักษ์โลก",
        "desc": (
            "ค้นหาคำว่า 'Purpose-led brands' หรือ 'Sustainable living brands' "
            "แล้วหาตัวเลขว่าแบรนด์กลุ่มนี้ยอดขายโต (Growth) กี่เปอร์เซ็นต์"
        ),
    },
    6: {
        "title": "การตั้งราคา",
        "desc": (
            "ค้นหาคำว่า 'Pricing' หรือ 'Premiumisation' ดูว่าบริษัทมีการขึ้นราคา "
            "สินค้าได้เท่าไหร่ในปีล่าสุด แคปตัวเลขมา"
        ),
    },
    7: {
        "title": "ตัวเลขลดต้นทุน",
        "desc": (
            "ค้นหาคำว่า 'Cost savings' หรือ 'Eco-efficiency' หายอดเงิน "
            "(หน่วยล้าน/พันล้านยูโร) ที่บริษัทประหยัดไฟ ประหยัดน้ำในโรงงานได้"
        ),
    },
    8: {
        "title": "ตัวเลขงบลงทุน",
        "desc": (
            "ค้นหาคำว่า 'Capital Expenditure' (CAPEX) หรือ 'R&D' หาตัวเลขว่า "
            "ปีล่าสุดบริษัทใช้เงินลงทุนไปกี่ยูโร"
        ),
    },
    9: {
        "title": "กำไรจากการดำเนินงาน",
        "desc": (
            "ไปหน้างบการเงิน หาคำว่า 'Operating Margin' หรือ "
            "'Underlying Operating Margin' ว่าปีล่าสุดอยู่ที่กี่เปอร์เซ็นต์"
        ),
    },
    10: {
        "title": "หนี้และดอกเบี้ย",
        "desc": (
            "ค้นหาคำว่า 'Green Bond' หรือ 'Sustainability-linked bond' หาว่า "
            "บริษัทเคยออกหุ้นกู้รักษ์โลกไหม และมีอัตราดอกเบี้ย (Interest rate) เท่าไหร่"
        ),
    },
    11: {
        "title": "คะแนน ESG",
        "desc": (
            "ไม่ต้องหาในเล่ม แต่ให้เสิร์ช Google ว่า 'Unilever ESG Rating S&P Global' "
            "หรือ 'MSCI' แล้วแคปหน้าจอคะแนนล่าสุดมา"
        ),
    },
    12: {
        "title": "คะแนนพนักงาน",
        "desc": (
            "ค้นหาคำว่า 'Employer of choice' หรือ 'Employee engagement' ในเล่ม "
            "หาตัวเลขสถิติว่าพนักงานอยากทำงานกับบริษัทนี้มากแค่ไหน"
        ),
    },
}

# ─────────────────────────────────────────────────────────────
# 2. ไฟล์ CSV สำหรับเก็บข้อมูลการจอง
# ─────────────────────────────────────────────────────────────
CSV_FILE = "bookings.csv"
CSV_COLUMNS = ["topic_num", "topic_title", "full_name", "nickname", "student_id", "seat_num", "booked_at"]

def load_bookings() -> pd.DataFrame:
    """โหลดข้อมูลการจองจาก CSV ถ้าไม่มีไฟล์ให้สร้างใหม่"""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE, dtype=str)
    else:
        df = pd.DataFrame(columns=CSV_COLUMNS)
        df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
        return df

def save_booking(topic_num: int, full_name: str, nickname: str, student_id: str, seat_num: str):
    """บันทึกการจองใหม่ลง CSV"""
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

def get_booked_topic_nums(df: pd.DataFrame) -> list[int]:
    """คืนค่าหมายเลขหัวข้อที่ถูกจองไปแล้ว"""
    if df.empty or "topic_num" not in df.columns:
        return []
    return [int(x) for x in df["topic_num"].dropna().tolist()]

# ─────────────────────────────────────────────────────────────
# 3. Page Config & CSS
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="จองหัวข้อรายงานกลุ่ม",
    page_icon="📚",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Sarabun', sans-serif; }
.stApp { background: #f0f4ff; }

/* Header gradient */
.page-header {
    background: linear-gradient(135deg, #1e3a8a 0%, #4f46e5 60%, #7c3aed 100%);
    border-radius: 16px;
    padding: 28px 36px;
    color: white;
    margin-bottom: 24px;
}
.page-header h1 { font-size: 2rem; font-weight: 800; margin: 0 0 6px 0; }
.page-header p  { font-size: 1rem; margin: 0; opacity: 0.85; }

/* Section card */
.card {
    background: white;
    border-radius: 14px;
    padding: 24px 28px;
    box-shadow: 0 2px 16px rgba(79,70,229,0.09);
    margin-bottom: 20px;
}

/* Section title */
.sec-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1e3a8a;
    border-left: 4px solid #4f46e5;
    padding-left: 12px;
    margin-bottom: 16px;
}

/* Available / booked badge in selectbox area */
.avail-badge  { color: #16a34a; font-weight: 700; }
.booked-badge { color: #dc2626; font-weight: 700; }

/* Submit button */
div[data-testid="stForm"] .stButton > button {
    background: linear-gradient(135deg, #1e3a8a, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 13px 0;
    font-size: 17px;
    font-weight: 700;
    font-family: 'Sarabun', sans-serif;
    width: 100%;
    letter-spacing: 0.4px;
    transition: opacity .2s, transform .1s;
}
div[data-testid="stForm"] .stButton > button:hover {
    opacity: 0.9; transform: translateY(-1px);
}

/* Dashboard header row */
.dash-header {
    background: #e8ecfa;
    color: #1e3a8a;
    border-left: 5px solid #4f46e5;
    border-radius: 0 10px 10px 0;
    padding: 10px 20px;
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 12px;
}

/* Progress bar custom color */
.stProgress > div > div > div { background: linear-gradient(90deg,#4f46e5,#7c3aed); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 4. Header
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>📚 ระบบจองหัวข้อรายงานกลุ่ม</h1>
    <p>Unilever Valuation Project · เลือกหัวข้อ 1 ข้อต่อคน · จองแล้วจองเลย ห้ามซ้ำ!</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# 5. โหลดข้อมูลการจอง & สร้าง selectbox options
# ─────────────────────────────────────────────────────────────
bookings_df    = load_bookings()
booked_nums    = get_booked_topic_nums(bookings_df)
total_booked   = len(booked_nums)

# สร้างรายการตัวเลือกสำหรับ selectbox (ตัดที่จองไปแล้วออก)
available_options = []
for num, info in TOPICS.items():
    if num not in booked_nums:
        available_options.append(f"ข้อ {num}: {info['title']}")

# ─────────────────────────────────────────────────────────────
# 6. Progress bar แสดงภาพรวม
# ─────────────────────────────────────────────────────────────
col_prog1, col_prog2 = st.columns([3, 1])
with col_prog1:
    st.markdown(f"**สถานะการจอง:** {total_booked} / 12 หัวข้อ ({'เต็มแล้ว! 🎉' if total_booked == 12 else f'เหลืออีก {12 - total_booked} หัวข้อ'})")
    st.progress(total_booked / 12)
with col_prog2:
    st.metric("จองแล้ว", f"{total_booked} ข้อ", delta=f"ว่าง {12 - total_booked} ข้อ")

st.divider()

# ─────────────────────────────────────────────────────────────
# 7. ฟอร์มจองหัวข้อ
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="sec-title">✏️ กรอกข้อมูลเพื่อจองหัวข้อ</div>', unsafe_allow_html=True)

if not available_options:
    # ถ้าจองครบแล้วทุกข้อ
    st.warning("🎊 ทุกหัวข้อถูกจองครบแล้ว! ดูรายชื่อด้านล่างได้เลย")
else:
    # ── Dropdown อยู่นอก form เพื่อให้คำอธิบายอัปเดตทันทีเมื่อเปลี่ยน ──
    selected_label = st.selectbox(
        "เลือกหัวข้อที่ต้องการจอง *",
        options=available_options,
        help="หัวข้อที่ถูกจองไปแล้วจะไม่ปรากฏในรายการนี้",
    )

    # ── คำอธิบายอัปเดตทันทีเมื่อเปลี่ยน dropdown ──
    if selected_label:
        selected_num = int(selected_label.split(":")[0].replace("ข้อ", "").strip())
        st.info(
            f"📌 **หน้าที่ของข้อ {selected_num} — {TOPICS[selected_num]['title']}:**\n\n"
            f"{TOPICS[selected_num]['desc']}"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("booking_form", clear_on_submit=True):
        # ── ข้อมูลผู้จอง ──
        r1c1, r1c2, r1c3, r1c4 = st.columns([3, 2, 2, 1])
        with r1c1:
            full_name  = st.text_input("ชื่อ-นามสกุล *", placeholder="สมชาย ใจดี")
        with r1c2:
            nickname   = st.text_input("ชื่อเล่น *", placeholder="ฟลุ๊คเองจ้า")
        with r1c3:
            student_id = st.text_input("รหัสนักศึกษา *", placeholder="168010XXXX")
        with r1c4:
            seat_num   = st.text_input("เลขที่ *", placeholder="1")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔒  ยืนยันการจอง")

    # ── ประมวลผลการจอง ──
    if submitted:
        # Validation: ตรวจว่ากรอกครบ
        errors = []
        if not full_name.strip():  errors.append("ชื่อ-นามสกุล")
        if not nickname.strip():   errors.append("ชื่อเล่น")
        if not student_id.strip(): errors.append("รหัสนักศึกษา")
        if not seat_num.strip():   errors.append("เลขที่")

        if errors:
            st.error(f"⚠️ กรุณากรอกให้ครบ: **{', '.join(errors)}**")
        else:
            # บันทึกการจองลง CSV
            save_booking(
                topic_num  = selected_num,
                full_name  = full_name.strip(),
                nickname   = nickname.strip(),
                student_id = student_id.strip(),
                seat_num   = seat_num.strip(),
            )
            st.success(
                f"✅ **{nickname.strip()}** จองข้อ {selected_num}: "
                f"**{TOPICS[selected_num]['title']}** สำเร็จแล้ว!"
            )
            st.balloons()
            # Rerun เพื่ออัปเดต selectbox และ dashboard
            st.rerun()

st.divider()

# ─────────────────────────────────────────────────────────────
# 8. Dashboard — กระดานสรุปผลการจอง
# ─────────────────────────────────────────────────────────────
st.markdown('<div class="dash-header">📋 กระดานสรุปสถานะการจองทั้ง 12 หัวข้อ</div>', unsafe_allow_html=True)

# โหลดข้อมูลใหม่อีกครั้ง (เผื่อมีการจองพอดี)
bookings_df = load_bookings()

# สร้างตาราง dashboard โดยวน loop หัวข้อ 1–12
dashboard_rows = []
for num, info in TOPICS.items():
    # หาแถวที่ตรงกับหัวข้อนี้ใน CSV
    match = bookings_df[bookings_df["topic_num"].astype(str) == str(num)]

    if match.empty:
        # ยังว่างอยู่
        dashboard_rows.append({
            "ข้อที่":         num,
            "หัวข้อ":        info["title"],
            "สถานะ":         "🟢 ว่าง",
            "ชื่อ-นามสกุล":  "—",
            "ชื่อเล่น":      "—",
            "รหัสนักศึกษา":  "—",
            "เลขที่":        "—",
        })
    else:
        # จองแล้ว — เอาแถวแรกที่เจอ
        row = match.iloc[0]
        dashboard_rows.append({
            "ข้อที่":         num,
            "หัวข้อ":        info["title"],
            "สถานะ":         "🔴 จองแล้ว",
            "ชื่อ-นามสกุล":  row.get("full_name", "—"),
            "ชื่อเล่น":      row.get("nickname", "—"),
            "รหัสนักศึกษา":  row.get("student_id", "—"),
            "เลขที่":        row.get("seat_num", "—"),
        })

dashboard_df = pd.DataFrame(dashboard_rows)

st.dataframe(
    dashboard_df,
    use_container_width=True,
    hide_index=True,
    height=460,
    column_config={
        "ข้อที่":        st.column_config.NumberColumn(width="small"),
        "สถานะ":         st.column_config.TextColumn(width="small"),
        "หัวข้อ":        st.column_config.TextColumn(width="medium"),
        "ชื่อ-นามสกุล": st.column_config.TextColumn(width="medium"),
        "ชื่อเล่น":      st.column_config.TextColumn(width="small"),
        "รหัสนักศึกษา":  st.column_config.TextColumn(width="small"),
        "เลขที่":        st.column_config.TextColumn(width="small"),
    },
)

# ── ปุ่ม Export CSV ──
csv_export = dashboard_df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="⬇️  Export สรุปการจอง (.csv)",
    data=csv_export,
    file_name=f"booking_summary_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
    
)
with st.expander("✏️ แก้ไขหรือลบรายการจอง"):
    if bookings_df.empty:
        st.info("ยังไม่มีข้อมูลการจอง")
    else:
        # เลือกแถวที่อยากแก้
        options = [
            f"ข้อ {row['topic_num']} — {row['nickname']} ({row['full_name']})"
            for _, row in bookings_df.iterrows()
        ]
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
