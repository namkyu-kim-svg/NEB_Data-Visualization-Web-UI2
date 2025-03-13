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
            # 다중 선택을 통해 여러 컬럼 선택 (최소 2개 이상)
            selected_cols = st.multiselect("T-test할 컬럼 선택 (최소 2개)", data.columns)
            if len(selected_cols) < 2:
                st.warning("적어도 2개 이상의 컬럼을 선택하세요.")
            else:
                # 선택된 컬럼 중 숫자형 데이터만 남김
                numeric_cols = [col for col in selected_cols if pd.api.types.is_numeric_dtype(data[col])]
                if len(numeric_cols) < 2:
                    st.error("선택된 컬럼 중 숫자형 데이터가 2개 이상이어야 합니다.")
                else:
                    from itertools import combinations
                    results = []
                    for col1, col2 in combinations(numeric_cols, 2):
                        group1 = data[col1].dropna()
                        group2 = data[col2].dropna()
                        res = ttest_ind(group1, group2, nan_policy="omit")
                        results.append({
                            "Column 1": col1,
                            "Column 2": col2,
                            "T-statistic": f"{res.statistic:.4f}",
                            "p-value": f"{res.pvalue:.4e}"
                        })
                    df_results = pd.DataFrame(results)
                    st.write("T-test 결과 (각 컬럼 조합):")
                    st.table(df_results)
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


