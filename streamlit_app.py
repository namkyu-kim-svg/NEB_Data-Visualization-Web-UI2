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

# 메뉴 선택에 따라 페이지 함수 실행
if selected == "홈":
    show_home()
elif selected == "그래프":
    show_graph()
elif selected == "통계 분석":
    show_statistics()
elif selected == "지도":
    show_map()

