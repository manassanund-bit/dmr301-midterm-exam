import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="ตรวจสอบที่นั่งสอบ DMR 301", page_icon="🎓", layout="centered")

# ปรับแต่งฟอนต์ภาษาไทยสไตล์เอกสารทางการ (Sarabun / Angsana New Style) และตกแต่ง UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"], div, span, p, h1, h2, h3, h4, input, button {
        font-family: 'Sarabun', 'Angsana New', sans-serif !important;
    }
    
    .header-box {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
        margin-bottom: 25px;
    }
    
    .header-box h2 {
        color: #ffffff !important;
        font-size: 26px !important;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .header-box h4 {
        color: #e0e0e0 !important;
        font-size: 19px !important;
        font-weight: 400;
        margin-top: 0px;
    }
    
    .card-info {
        background-color: #f8f9fa;
        border-left: 6px solid #2c5364;
        padding: 15px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# ส่วนหัวข้อหลัก
st.markdown("""
    <div class="header-box">
        <h2>🎓 ตรวจสอบรายชื่อผู้มีสิทธิ์สอบกลางภาค ภาคเรียนที่ 1/2569</h2>
        <h4>รายวิชา DMR 301 กลยุทธ์การจัดการการสื่อสารในยุคดิจิทัล</h4>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="card-info">
        <p style="font-size: 17px; margin: 0;"><b>💡 คำชี้แจง:</b> กรุณากรอกรหัสนักศึกษาลงในช่องด้านล่าง เพื่อตรวจสอบ วัน เวลา ห้องสอบ และลำดับที่นั่งสอบส่วนบุคคล</p>
    </div>
""", unsafe_allow_html=True)

# Sheet ID สำหรับวิชา DMR 301
GOOGLE_SHEET_ID = "1sLG_aOcQPlkMxbOa4OiTWJp0O6zYu7hOixUJIuE5Y2A"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"

@st.cache_data(ttl=10)
def load_data():
    try:
        return pd.read_csv(SHEET_URL, dtype=str)
    except Exception as e:
        return None

df = load_data()

student_id = st.text_input("🔑 กรุณากรอกรหัสนักศึกษาของคุณ:", placeholder="เช่น 6501433")

if student_id:
    if df is not None and not df.empty:
        search_id = str(student_id).strip()
        
        # คอลัมน์ A (Index 0) คือ รหัสนักศึกษา
        df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.strip()
        
        student_row = df[df.iloc[:, 0] == search_id]
        
        if not student_row.empty:
            row = student_row.iloc[0]
            
            # ดึงข้อมูลตรงตามคอลัมน์ A-G ของไฟล์ DMR 301
            student_name = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "-" # คอลัมน์ B: ชื่อ-นามสกุล
            sec = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else "-"          # คอลัมน์ C: SEC.
            exam_date = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else "-"    # คอลัมน์ D: วันที่สอบ
            exam_time = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else "-"    # คอลัมน์ E: เวลาสอบ
            exam_room = str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else "-"    # คอลัมน์ F: ห้องสอบ
            seat_no = str(row.iloc[6]).strip() if pd.notna(row.iloc[6]) else "-"      # คอลัมน์ G: ลำดับที่นั่ง
            
            st.success(f"🔓 **พบข้อมูลผู้มีสิทธิ์สอบ:** {student_name}")
            st.divider()
            
            # แสดงข้อมูลวันและเวลาสอบ
            st.info(f"📅 **กำหนดการสอบ:** {exam_date} | ⏰ **เวลาสอบ:** {exam_time}")
            
            # แสดงห้องสอบและลำดับที่นั่ง
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="🏫 ห้องสอบ", value=f"{exam_room}")
                st.metric(label="📌 กลุ่มเรียน (SEC)", value=f"{sec}")
            with col2:
                st.metric(label="🪑 ลำดับที่นั่งสอบ", value=f"เลขที่ {seat_no}")
            
            st.warning("⚠️ **ข้อปฏิบัติในการเข้าสอบ:** กรุณาแต่งกายด้วยชุดนักศึกษาถูกต้องตามระเบียบมหาวิทยาลัย และแสดงบัตรนักศึกษาหรือบัตรประชาชนก่อนเข้าห้องสอบ")
        else:
            st.error(f"❌ ไม่พบรหัสนักศึกษา '{search_id}' ในรายชื่อผู้มีสิทธิ์สอบวิชานี้")
    else:
        st.error("⚠️ ไม่สามารถเชื่อมต่อฐานข้อมูลได้ กรุณาตรวจสอบการตั้งค่าแชร์ไฟล์ Google Sheet ให้เป็น 'ทุกคนที่มีลิงก์'")
else:
    st.caption("ℹ️ ป้อนรหัสนักศึกษาของคุณในช่องด้านบน เพื่อค้นหาตารางสอบส่วนบุคคล")
