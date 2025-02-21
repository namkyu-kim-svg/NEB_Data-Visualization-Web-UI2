import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from scipy.stats import ttest_ind, f_oneway
import matplotlib.font_manager as fm  # 폰트 설정을 위한 라이브러리

# 나눔고딕 폰트 설정
plt.rc('font', family='sans-serif')

# **2. 페이지 구성**
st.title("데이터 시각화 웹 브라우저")

# **3. 메인 메뉴**
menu = st.sidebar.selectbox(
    "메뉴를 선택하세요",
    ["홈", "그래프", "통계 분석"]
)

# **4. 홈 페이지**
if menu == "홈":
    st.header("환영합니다!")
    st.write("왼쪽 사이드바에서 메뉴를 선택하세요.")
    # 오른쪽 정렬된 텍스트
    st.markdown(
        """
        <div style="text-align: right;">
            made by NEB_김남규
        </div>
        """,
        unsafe_allow_html=True
    )
    # 첫 화면 이미지 표시
    #image_url = "https://raw.githubusercontent.com/namkyu-kim-svg/main/Screen.png"
    st.image(Screen.png, caption="데이터 시각화 웹 앱", use_container_width=True)

# **5. 그래프 페이지**
elif menu == "그래프":
    st.header("그래프 종류를 선택하세요")

    graph_type = st.selectbox(
        "그래프 종류",
        ["막대그래프", "꺾은선 그래프", "Scatter Plot", "Stack 막대그래프", "누적 그래프"]
    )

    # 파일 업로드
    uploaded_file = st.file_uploader("CSV 또는 Excel 파일을 업로드하세요", type=["csv", "xlsx"])

    if uploaded_file:
        # 파일 읽기
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)

        # 데이터 미리보기
        st.write("업로드된 데이터 미리보기:")
        st.dataframe(data)

        # 컬럼 선택
        x_col = st.selectbox("X축 데이터 선택", data.columns)
        y_col = st.selectbox("Y축 데이터 선택", data.columns)

        # 그래프 그리기
        fig, ax = plt.subplots(figsize=(10, 6))

        if graph_type == "막대그래프":
            ax.bar(data[x_col], data[y_col], color="skyblue")
        elif graph_type == "꺾은선 그래프":
            ax.plot(data[x_col], data[y_col], color="green", marker="o")
        elif graph_type == "Scatter Plot":
            ax.scatter(data[x_col], data[y_col], color="red")
        elif graph_type == "Stack 막대그래프":
            data.groupby(x_col)[y_col].sum().plot(kind="bar", stacked=True, ax=ax)
        elif graph_type == "누적 그래프":
            ax.fill_between(data[x_col], data[y_col], color="orange", alpha=0.5)

        ax.set_title(graph_type, fontsize=16)
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        st.pyplot(fig)

# **6. 통계 분석 페이지**
elif menu == "통계 분석":
    st.header("통계 분석 종류를 선택하세요")

    analysis_type = st.selectbox(
        "통계 분석 종류",
        ["Spearman Correlation", "Pearson Correlation", "T-test", "ANOVA Test"]
    )

    # 파일 업로드
    uploaded_file = st.file_uploader("CSV 또는 Excel 파일을 업로드하세요", type=["csv", "xlsx"])

    if uploaded_file:
        # 파일 읽기
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)

        # 데이터 미리보기
        st.write("업로드된 데이터 미리보기:")
        st.dataframe(data)

        if analysis_type in ["Spearman Correlation", "Pearson Correlation"]:
            # 상관관계 분석: 전체 컬럼 간 계산
            st.write(f"{analysis_type} 결과 (전체 컬럼):")
            method = "spearman" if analysis_type == "Spearman Correlation" else "pearson"
            correlation_matrix = data.corr(method=method)
            st.dataframe(correlation_matrix)

        elif analysis_type == "T-test":
            # T-test: 두 컬럼 선택
            st.write("T-test를 수행할 두 컬럼을 선택하세요:")
            col1 = st.selectbox("첫 번째 컬럼 선택", data.columns)
            col2 = st.selectbox("두 번째 컬럼 선택", data.columns)

            # 데이터 타입 확인 및 처리
            if pd.api.types.is_numeric_dtype(data[col1]) and pd.api.types.is_numeric_dtype(data[col2]):
                result = ttest_ind(data[col1].dropna(), data[col2].dropna(), nan_policy="omit")
                st.write("T-test 결과:")
                st.write(result)
            else:
                st.error("선택한 컬럼은 숫자형 데이터여야 합니다.")

        elif analysis_type == "ANOVA Test":
            # ANOVA Test: 여러 컬럼 선택
            st.write("ANOVA Test를 수행할 컬럼들을 선택하세요:")
            selected_columns = st.multiselect("컬럼 선택", data.columns)

            # 데이터 타입 확인 및 처리
            if len(selected_columns) >= 2:
                numeric_columns = [col for col in selected_columns if pd.api.types.is_numeric_dtype(data[col])]
                if len(numeric_columns) < 2:
                    st.error("선택한 컬럼 중 최소 2개는 숫자형 데이터여야 합니다.")
                else:
                    result = f_oneway(*(data[col].dropna() for col in numeric_columns))
                    st.write("ANOVA Test 결과:")
                    st.write(result)
            else:
                st.warning("ANOVA Test를 위해 최소 2개 이상의 컬럼을 선택하세요.")

