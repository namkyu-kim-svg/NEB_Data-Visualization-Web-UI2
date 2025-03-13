import streamlit as st
from Home import show as show_home
from Graph import show as show_graph
from Statistics import show as show_statistics
from Map import show as show_map
from streamlit_option_menu import option_menu  # streamlit-option-menu 추가

# 사이드바에 메뉴 배치
with st.sidebar:
    selected = option_menu(
        "메뉴",                         # 메뉴 제목
        ["홈", "그래프", "통계 분석", "지도"],  # 메뉴 항목
        icons=["house", "bar-chart", "calculator", "map"],  # 각 항목의 아이콘
        menu_icon="cast",               # 전체 메뉴 아이콘
        default_index=0,                # 기본 선택 항목
    )

# 선택된 메뉴에 따라 내용 표시
if selected == "홈":
    st.title("홈 페이지")
    st.write("홈 페이지 내용")
elif selected == "그래프":
    st.title("그래프 페이지")
    st.write("그래프 페이지 내용")
elif selected == "통계 분석":
    st.title("통계 분석 페이지")
    st.write("통계 분석 페이지 내용")
elif selected == "지도":
    st.title("지도 페이지")
    st.write("지도 페이지 내용")

