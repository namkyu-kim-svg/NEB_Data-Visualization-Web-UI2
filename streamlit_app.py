import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from scipy.stats import ttest_ind, f_oneway
import matplotlib.font_manager as fm  # 폰트 설정을 위한 라이브러리
import matplotlib as mpl  # rc 함수 사용을 위한 라이브러리 추가
import os

# ✅ 맑은고딕 폰트 직접 불러오기
font_path = "./MALGUN.TTF"
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
else:
    st.error(f"❌ 폰트 파일을 찾을 수 없습니다: {font_path}")

# ✅ 테스트용 그래프
st.title("한글 폰트 테스트")

fig, ax = plt.subplots()
ax.bar(['A', 'B', 'C', 'D', 'E'], [5, 7, 3, 8, 6], color='skyblue')
ax.set_title("테스트 그래프")
ax.set_xlabel("카테고리")
ax.set_ylabel("값")
st.pyplot(fig)


