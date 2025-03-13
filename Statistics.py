import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from scipy.stats import ttest_ind, f_oneway
from itertools import combinations

# PCA 분석을 위한 라이브러리
from sklearn.decomposition import PCA
# Heatmap 생성을 위한 seaborn
import seaborn as sns

def show():
    st.title("통계 분석 페이지")
    st.header("분석 종류를 선택하세요")

    analysis_type = st.selectbox(
        "분석 종류 선택",
        ["Spearman Correlation", "Pearson Correlation", "T-test", "ANOVA Test", "PCA 분석", "Heatmap"]
    )

    uploaded_file = st.file_uploader("CSV 또는 Excel 파일을 업로드하세요", type=["csv", "xlsx"])

    if uploaded_file:
        # 파일 읽기
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)

        st.write("업로드된 데이터 미리보기:")
        st.dataframe(data)

        # 상관계수 계산
        if analysis_type in ["Spearman Correlation", "Pearson Correlation"]:
            method = "spearman" if analysis_type == "Spearman Correlation" else "pearson"
            numeric_data = data.select_dtypes(include=['number'])
            correlation_matrix = numeric_data.corr(method=method)
            st.dataframe(correlation_matrix)

        # T-test: 선택한 여러 컬럼의 모든 2개 조합에 대해 T-test 수행
        elif analysis_type == "T-test":
            selected_cols = st.multiselect("T-test할 컬럼 선택 (최소 2개)", data.columns)
            if len(selected_cols) < 2:
                st.warning("적어도 2개 이상의 컬럼을 선택하세요.")
            else:
                numeric_cols = [col for col in selected_cols if pd.api.types.is_numeric_dtype(data[col])]
                if len(numeric_cols) < 2:
                    st.error("선택된 컬럼 중 숫자형 데이터가 2개 이상이어야 합니다.")
                else:
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

        # ANOVA Test: 선택한 여러 컬럼에 대해 ANOVA Test 수행
        elif analysis_type == "ANOVA Test":
            selected_columns = st.multiselect("ANOVA Test할 컬럼 선택 (최소 2개)", data.columns)
            if len(selected_columns) < 2:
                st.warning("ANOVA Test를 위해 최소 2개 이상의 컬럼을 선택하세요.")
            else:
                numeric_columns = [col for col in selected_columns if pd.api.types.is_numeric_dtype(data[col])]
                if len(numeric_columns) < 2:
                    st.error("선택한 컬럼 중 최소 2개는 숫자형 데이터여야 합니다.")
                else:
                    result = f_oneway(*(data[col].dropna() for col in numeric_columns))
                    st.write("ANOVA Test 결과:")
                    st.write(result)

        # PCA 분석: 숫자형 데이터에 대해 PCA 수행 후 결과와 산점도 출력
        elif analysis_type == "PCA 분석":
            numeric_data = data.select_dtypes(include=['number'])
            if numeric_data.shape[1] < 2:
                st.warning("PCA 분석을 위해서는 최소 2개 이상의 숫자형 컬럼이 필요합니다.")
            else:
                pca = PCA(n_components=2)
                principal_components = pca.fit_transform(numeric_data)
                explained_var = pca.explained_variance_ratio_

                st.write("PCA 분석 결과:")
                st.write(f"주성분 1, 2의 설명 분산 비율: {explained_var[0]:.4f}, {explained_var[1]:.4f}")

                # PCA 결과를 DataFrame으로 만들어 출력
                pc_df = pd.DataFrame(data = principal_components, columns = ['PC1', 'PC2'])
                st.dataframe(pc_df.head())

                # PCA 산점도
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.scatter(pc_df['PC1'], pc_df['PC2'], alpha=0.7)
                ax.set_xlabel("PC1")
                ax.set_ylabel("PC2")
                ax.set_title("PCA 산점도")
                st.pyplot(fig)

        # Heatmap: 숫자형 데이터 상관계수를 Heatmap으로 시각화
        elif analysis_type == "Heatmap":
            numeric_data = data.select_dtypes(include=['number'])
            if numeric_data.shape[1] < 2:
                st.warning("Heatmap을 위해서는 최소 2개 이상의 숫자형 컬럼이 필요합니다.")
            else:
                corr_matrix = numeric_data.corr()
                st.write("상관계수 Heatmap:")
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
                st.pyplot(fig)

if __name__ == '__main__':
    show()



