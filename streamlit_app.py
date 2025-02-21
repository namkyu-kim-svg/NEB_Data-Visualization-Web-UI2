import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import streamlit as st
import os

# ✅ 폰트 경로 지정
font_path = "./fonts/MALGUN.TTF"

# ✅ 폰트 존재 여부 확인
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name() if font_prop else 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지
    st.success(f"폰트 적용됨: {font_prop.get_name()}")
else:
    st.error(f"❌ 폰트 파일을 찾을 수 없습니다: {font_path}")

# ✅ 테스트 그래프
fig, ax = plt.subplots()
ax.bar(['A', 'B', 'C', 'D', 'E'], [5, 7, 3, 8, 6], color='skyblue')
ax.set_title("한글 폰트 테스트", fontsize=16)
st.pyplot(fig)





