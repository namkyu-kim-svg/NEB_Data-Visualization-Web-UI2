import matplotlib.font_manager as fm
import streamlit as st
import matplotlib.pyplot as plt
import os

# ✅ 프로젝트 내부 폰트 경로 지정
font_path = "./MALGUN.TTF"

# ✅ 폰트 존재 여부 확인
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()  # 폰트 적용
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
    st.success(f"폰트 적용됨: {font_prop.get_name()}")
else:
    st.error(f"❌ 폰트 파일을 찾을 수 없습니다: {font_path}")

# ✅ 테스트용 그래프
fig, ax = plt.subplots()
ax.bar(['A', 'B', 'C', 'D', 'E'], [5, 7, 3, 8, 6], color='skyblue')
ax.set_title("한글 폰트 테스트")
st.pyplot(fig)




