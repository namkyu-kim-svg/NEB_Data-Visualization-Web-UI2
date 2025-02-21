# -*- coding:utf-8 -*-
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import matplotlib.font_manager as fm

# 한글 폰트 적용 함수
def font_registered():
    font_dirs = [os.path.join(os.getcwd(), 'customFonts')]
    font_files = fm.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)

# Streamlit 앱 메인 함수
def main():
    # 폰트 등록
    font_registered()
    
    # 등록된 폰트 목록에서 'NanumGothic' 폰트 선택
    plt.rc('font', family='NanumGothic')
    
    # 예제 데이터 로드
    tips = sns.load_dataset("tips")
    
    # 데이터프레임 표시
    st.dataframe(tips)
    
    # 시각화 생성
    fig, ax = plt.subplots()
    sns.scatterplot(data=tips, x='total_bill', y='tip', hue='day', ax=ax)
    ax.set_title("한글 테스트")
    
    # Streamlit을 통해 시각화 출력
    st.pyplot(fig)

if __name__ == "__main__":
    main()



