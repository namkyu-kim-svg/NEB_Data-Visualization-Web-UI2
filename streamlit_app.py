import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 시스템에서 사용 가능한 한글 폰트 찾기
font_list = [f.name for f in fm.fontManager.ttflist if 'Gothic' in f.name or 'Nanum' in f.name or 'Batang' in f.name]

# 한글 폰트가 하나라도 있으면 사용
if font_list:
    plt.rcParams['font.family'] = font_list[0]  # 첫 번째 한글 폰트 사용
else:
    plt.rcParams['font.family'] = 'DejaVu Sans'  # 기본 폰트 사용 (한글이 깨질 수 있음)

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# ✅ 사용 중인 폰트 표시
st.write(f"현재 사용 중인 폰트: {plt.rcParams['font.family']}")

# ✅ 테스트용 그래프
st.title("한글 폰트 테스트")

fig, ax = plt.subplots()
ax.bar(['A', 'B', 'C', 'D', 'E'], [5, 7, 3, 8, 6], color='skyblue')
ax.set_title("테스트 그래프")
ax.set_xlabel("카테고리")
ax.set_ylabel("값")
st.pyplot(fig)


