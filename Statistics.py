import streamlit as st
import pandas as pd
from scipy.stats import ttest_ind, f_oneway

def show():
    st.title("통계 분석 페이지")
    st.header("통계 분석 종류를 선택하세요")

    analysis_type = st.selectbox(
        "통계 분석 종류",
        ["Spearman Correlation", "Pearson Correlation", "T-test", "ANOVA Test"]
    )

    uploaded_file = st.file_uploader("CSV 또는 Excel 파일을 업로드하세요", type=["csv", "xlsx"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)

        st.write("업로드된 데이터 미리보기:")
        st.dataframe(data)

        if analysis_type in ["Spearman Correlation", "Pearson Correlation"]:
            method = "spearman" if analysis_type == "Spearman Correlation" else "pearson"
            # 숫자형 열만 추출
            numeric_data = data.select_dtypes(include=['number'])
            correlation_matrix = numeric_data.corr(method=method)
            st.dataframe(correlation_matrix)

        elif analysis_type == "T-test":
            col1 = st.selectbox("첫 번째 컬럼 선택", data.columns)
            col2 = st.selectbox("두 번째 컬럼 선택", data.columns)

            if pd.api.types.is_numeric_dtype(data[col1]) and pd.api.types.is_numeric_dtype(data[col2]):
                result = ttest_ind(data[col1].dropna(), data[col2].dropna(), nan_policy="omit")
                st.write("T-test 결과:")
                st.write(result)
            else:
                st.error("선택한 컬럼은 숫자형 데이터여야 합니다.")

        elif analysis_type == "ANOVA Test":
            selected_columns = st.multiselect("컬럼 선택", data.columns)

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

if __name__ == '__main__':
    show()


