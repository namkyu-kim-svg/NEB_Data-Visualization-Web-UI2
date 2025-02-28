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
    
    # 하단 레이아웃 구성
    st.write("---")  # 구분선
    
    # GitHub에 올라간 py50logo.png 로드 (raw 파일 URL 사용)
    logo_url = "https://raw.githubusercontent.com/namkyu-kim-svg/NEB_Data-Visualization-Web-UI2/main/py50logo.png"

    # 2개 컬럼으로 나누어 왼쪽은 로고, 오른쪽은 문구
    col1, col2 = st.columns([1, 4])  # 비율 조정 가능

    with col1:
        st.image(logo_url, width=80)

    with col2:
        # 오른쪽 정렬 + 원하는 문구
        st.markdown(
            """
            <p style="text-align: right; font-size:16px; font-weight:bold; margin-top:20px;">
            내 Streamlit 앱 보기 → Py50: Generate Dose-Response Curve 활용
            </p>
            """,
            unsafe_allow_html=True
        )


