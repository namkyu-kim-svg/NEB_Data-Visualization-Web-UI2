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

if __name__ == '__main__':
    show()

