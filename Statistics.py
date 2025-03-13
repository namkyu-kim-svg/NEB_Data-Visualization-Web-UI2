import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from scipy.stats import ttest_ind, f_oneway
from itertools import combinations

# PCA 분석을 위한 라이브러리
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
# Heatmap 생성을 위한 seaborn
import seaborn as sns
import numpy as np

def pca_biplot(df, numeric_cols, target_col=None, scale_data=True):
    """
    df          : 전체 데이터프레임
    numeric_cols: PCA에 사용할 숫자형 컬럼 리스트
    target_col  : (선택) 관측치의 그룹(범주) 정보를 담은 컬럼명 (색상 구분)
    scale_data  : True면 StandardScaler로 데이터 스케일링

    Returns: matplotlib Figure 객체 (Streamlit에서 st.pyplot(fig)로 표시),
             (pc1_var, pc2_var) 주성분 1,2의 분산 비율
    """
    # 1) 숫자형 데이터 추출 & 결측 제거
    X = df[numeric_cols].dropna()

    # 2) 스케일링 여부
    if scale_data:
        X_scaled = StandardScaler().fit_transform(X)
    else:
        X_scaled = X.values

    # 3) PCA 분석 (주성분 2개)
    pca = PCA(n_components=2)
    pca_fit = pca.fit_transform(X_scaled)
    pc1_var = pca.explained_variance_ratio_[0] * 100
    pc2_var = pca.explained_variance_ratio_[1] * 100

    # 주성분 점수 DataFrame
    pc_df = pd.DataFrame(data=pca_fit, columns=['PC1', 'PC2'], index=X.index)

    # 4) 시각화 준비
    fig, ax = plt.subplots(figsize=(8, 6))

    # (선택) target_col로 색상 구분
    if target_col and target_col in df.columns:
        # PC 점수 DF와 target_col 매핑
        pc_df[target_col] = df.loc[pc_df.index, target_col]
        sns.scatterplot(data=pc_df, x='PC1', y='PC2', hue=target_col, ax=ax, s=60, alpha=0.8)
    else:
        ax.scatter(pc_df['PC1'], pc_df['PC2'], alpha=0.8)

    ax.set_xlabel(f"PC1 ({pc1_var:.2f}% Var)")
    ax.set_ylabel(f"PC2 ({pc2_var:.2f}% Var)")
    ax.set_title("PCA Biplot")

    # 5) 변수 로딩(Loadings) 계산 (주성분 벡터 * sqrt 고유값)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

    # 6) 변수 로딩 벡터 + 라벨 표시
    for i, col in enumerate(numeric_cols):
        ax.arrow(0, 0, loadings[i, 0]*2, loadings[i, 1]*2,
                 color='r', alpha=0.7, head_width=0.03, length_includes_head=True)
        ax.text(loadings[i, 0]*2.2, loadings[i, 1]*2.2, col,
                color='r', ha='center', va='center', fontsize=10)

    return fig, (pc1_var, pc2_var)


def show():
    st.title("통계 분석 페이지")
    st.header("분석 종류를 선택하세요")

    analysis_type = st.selectbox(
        "분석 종류 선택",
        ["Spearman Correlation", "Pearson Correlation", "T-test", "ANOVA Test", "Heatmap", "PCA (Biplot)"]
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

        # T-test: 여러 컬럼 선택 -> 모든 2개 조합 T-test
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

        # ANOVA Test
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

        # Heatmap: 사용자가 원하는 숫자형 컬럼 다중 선택
        elif analysis_type == "Heatmap":
            st.subheader("Heatmap 설정")
            numeric_cols_all = data.select_dtypes(include=['number']).columns.tolist()
            selected_cols = st.multiselect("Heatmap에 사용할 숫자형 컬럼 선택 (최소 2개)",
                                           numeric_cols_all,
                                           default=numeric_cols_all)
            if len(selected_cols) < 2:
                st.warning("Heatmap을 위해서는 최소 2개 이상의 숫자형 컬럼을 선택하세요.")
            else:
                corr_matrix = data[selected_cols].corr()
                st.write("상관계수 Heatmap:")
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
                st.pyplot(fig)

        # PCA (Biplot)
        elif analysis_type == "PCA (Biplot)":
            st.subheader("PCA Biplot 분석")
            numeric_cols_all = data.select_dtypes(include='number').columns.tolist()

            # 사용자에게 숫자형 컬럼 선택
            selected_numeric = st.multiselect("PCA에 사용할 숫자형 컬럼 선택", numeric_cols_all,
                                              default=numeric_cols_all)
            # (선택) 그룹(범주) 컬럼
            group_options = ["(없음)"] + [c for c in data.columns if data[c].dtype == object]
            group_col = st.selectbox("그룹(범주) 컬럼(색상 구분)", group_options)

            # 스케일링 여부
            scale_option = st.checkbox("데이터 스케일링 (StandardScaler)", value=True)

            if len(selected_numeric) < 2:
                st.warning("PCA를 위해서는 최소 2개 이상의 숫자형 컬럼이 필요합니다.")
            else:
                if st.button("PCA Biplot 그리기"):
                    t_col = None if group_col == "(없음)" else group_col
                    fig, (pc1_var, pc2_var) = pca_biplot(data, selected_numeric, target_col=t_col,
                                                         scale_data=scale_option)
                    st.write(f"주성분 1 설명 분산 비율: {pc1_var:.2f}%")
                    st.write(f"주성분 2 설명 분산 비율: {pc2_var:.2f}%")
                    st.pyplot(fig)


if __name__ == '__main__':
    show()


