import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเว็บให้เต็มจอและรองรับมือถือ
st.set_page_config(
    page_title="ระบบค้นหาข้อมูล (CODE & NAME)", page_icon="🔍", layout="wide"
)

st.title("🔍 ระบบค้นหาข้อมูลสินค้า/รหัสผ่านเว็บแอป")
st.write(
    "พิมพ์รหัส (**CODE**) หรือชื่อ (**NAME**) เพื่อค้นหาข้อมูลจากไฟล์ Excel ทั้งหมด"
)

# ส่วนอัปโหลดไฟล์ Excel
uploaded_file = st.file_uploader(
    "📁 อัปโหลดไฟล์ Excel ของคุณ (.xlsx)", type=["xlsx"]
)

# โหลดข้อมูล
sheets_data = None

if uploaded_file is not None:
  try:
    # อ่านชีตทั้งหมดในไฟล์ที่อัปโหลด
    xls = pd.ExcelFile(uploaded_file)
    sheets_data = {
        sh: pd.read_excel(uploaded_file, sheet_name=sh) for sh in xls.sheet_names
    }
  except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
else:
  # เผื่อต้องการตั้งค่าไฟล์ตั้งต้นไว้ในโฟลเดอร์เดียวกัน (ตั้งชื่อว่า data.xlsx)
  try:
    xls = pd.ExcelFile("data.xlsx")
    sheets_data = {
        sh: pd.read_excel("data.xlsx", sheet_name=sh) for sh in xls.sheet_names
    }
    st.caption("📂 กำลังใช้งานข้อมูลจากไฟล์ตั้งต้น (data.xlsx)")
  except FileNotFoundError:
    st.info("💡 กรุณาอัปโหลดไฟล์ Excel ของคุณเพื่อเริ่มต้นใช้งานระบบค้นหา")

if sheets_data:
  # ช่องค้นหาหลัก
  search_query = st.text_input(
      "🔍 ค้นหา (พิมพ์ CODE หรือ NAME):",
      placeholder="พิมพ์คำที่ต้องการค้นหา เช่น A001 หรือ ชื่อสินค้า...",
  )

  if search_query:
    st.markdown("---")
    st.subheader(f"ผลการค้นหาสำหรับ: '{search_query}'")
    found_any = False

    # ค้นหาทีละชีต
    for sheet_name, df in sheets_data.items():
      # แปลงทุกคอลัมน์เป็น String เพื่อให้ค้นหาแบบไม่สนตัวพิมพ์เล็ก-ใหญ่ได้ง่าย
      # ค้นหาคำที่ตรงกันในแถวใดๆ
      mask = df.astype(str).apply(
          lambda col: col.str.contains(search_query, case=False, na=False)
      ).any(axis=1)
      match_df = df[mask]

      if not match_df.empty:
        found_any = True
        with st.expander(
            f"📁 ชีต: {sheet_name} (พบ {len(match_df)} รายการ)", expanded=True
        ):
          st.dataframe(match_df, use_container_width=True, hide_index=True)

    if not found_any:
      st.warning(f"ไม่พบข้อมูลที่ตรงกับ '{search_query}' ในชีตใดเลย")

  # ส่วนแสดงข้อมูลทั้งหมดแยกตามชีต (สำหรับเรียกดูทั่วไป)
  st.markdown("---")
  with st.expander("📋 ดูข้อมูลทั้งหมดแยกตามชีต"):
    sheet_tabs = st.tabs(list(sheets_data.keys()))
    for i, (sheet_name, df) in enumerate(sheets_data.items()):
      with sheet_tabs[i]:
        st.write(f"ข้อมูลในชีต: **{sheet_name}** ({len(df)} แถว)")
        st.dataframe(df, use_container_width=True, hide_index=True)