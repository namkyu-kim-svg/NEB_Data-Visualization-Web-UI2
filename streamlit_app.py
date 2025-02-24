import streamlit as st
from home import show as show_home
from graph import show as show_graph
from statistics import show as show_statistics
from map_page import show as show_map

st.sidebar.title("메뉴")
page = st.sidebar.selectbox("페이지 선택", ["홈", "그래프", "통계 분석", "지도"])

if page == "홈":
    show_home()
elif page == "그래프":
    show_graph()
elif page == "통계 분석":
    show_statistics()
elif page == "지도":
    show_map()
