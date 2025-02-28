import streamlit as st
from Home import show as show_home
from Graph import show as show_graph
from Statistics import show as show_statistics
from Map import show as show_map

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
    
st.markdown(
    """
    <h1 style="text-align: center; font-size: 48px;">
      <a href="https://py50-app.streamlit.app/" style="text-decoration: none; color: inherit;">
        내 Streamlit 앱 보기 -> Py50: Generate Dose-Response Curve 활용
      </a>
    </h1>
    """,
    unsafe_allow_html=True
)

