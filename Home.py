import streamlit as st

def show():
    st.title("NEB 연구원을 위한 데이터 시각화 웹 브라우저")
    st.header("환영합니다!")
    st.write("왼쪽 사이드바에서 메뉴를 선택하세요.")
    st.markdown(
        """
        <div style="text-align: right;">
            made by NEB_김남규
        </div>
        """,
        unsafe_allow_html=True
    )

    # 기본 GitHub 경로 설정
    base_url = "https://raw.githubusercontent.com/namkyu-kim-svg/NEB_Data-Visualization-Web-UI2/main/"

    # 3개의 이미지를 탭으로 구성
    tab1, tab2, tab3 = st.tabs(["1", "2", "3"])

    with tab1:
        image_url1 = f"{base_url}Screen.png"
        st.image(image_url1, caption="메인 대시보드", use_container_width=True)

    with tab2:
        image_url2 = f"{base_url}Screen2.png"
        st.image(image_url2, caption="데이터 분석 화면", use_container_width=True)

    with tab3:
        image_url3 = f"{base_url}Screen3.png"
        st.image(image_url3, caption="분석 결과 화면", use_container_width=True)
   
    # 하단 레이아웃 구성
    st.write("---")  # 구분선

    # GitHub에 올라간 py50logo.png 로드 (raw 파일 URL 사용)
    logo_url = "https://raw.githubusercontent.com/namkyu-kim-svg/NEB_Data-Visualization-Web-UI2/main/py50logo.png"

    # 2개 컬럼으로 나누어 왼쪽은 로고, 오른쪽은 링크 포함 텍스트
    col1, col2 = st.columns([1, 4])  # 비율 조정 가능

    with col1:
        st.image(logo_url, width=200)

    with col2:
        st.markdown(
            """
            <p style="text-align: right; font-size:28px; font-weight:bold; margin-top:5px;">
                <a href="https://py50-app.streamlit.app/" style="text-decoration: none; color: inherit;">
                   Py50: Generate Dose-Response Curve 활용<br>
                   [기능]<br>
                     1. LC50 Cakculator<br>
                   2. Plot Curve<br>
                   3. Statistics Calculator<br>
                   4. Molecular Drawer<br>
                </a>
            </p>
            """,
            unsafe_allow_html=True
        )
if __name__ == '__main__':
    show()

