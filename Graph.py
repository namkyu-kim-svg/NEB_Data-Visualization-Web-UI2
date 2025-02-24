import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show():
    st.title("그래프 페이지")
    st.header("그래프 종류를 선택하세요")

    # 1) 샘플 데이터 생성
    df_sample = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D', 'E'],
        'Value1': [10, 20, 15, 25, 18],
        'Value2': [3, 4, 8, 6, 7]
    })

    # 2) CSV로 변환
    csv_data = df_sample.to_csv(index=False)

    # 3) 샘플 데이터 다운로드 버튼
    st.download_button(
        label="샘플 데이터 다운로드",
        data=csv_data,
        file_name="sample_data.csv",
        mime="text/csv"
    )

    st.write("위 버튼을 클릭해 샘플 데이터를 다운로드한 후, 아래에 업로드하여 그래프를 시각화해 보세요.")

    # 그래프 종류 선택
    graph_type = st.selectbox(
        "그래프 종류",
        ["막대그래프", "꺾은선 그래프", "Scatter Plot", "Stack 막대그래프", "누적 그래프"]
    )

    # 파일 업로드
    uploaded_file = st.file_uploader("CSV 또는 Excel 파일을 업로드하세요", type=["csv", "xlsx"])

    if uploaded_file:
        # 업로드된 파일 읽기
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)

        st.write("업로드된 데이터 미리보기:")
        st.dataframe(data)

        # X축, Y축 컬럼 선택
        x_col = st.selectbox("X축 데이터 선택", data.columns)
        y_col = st.selectbox("Y축 데이터 선택", data.columns)

        fig, ax = plt.subplots(figsize=(10, 6))

        # 그래프 타입에 따른 시각화
        if graph_type == "막대그래프":
            ax.bar(data[x_col], data[y_col], color="skyblue")
        elif graph_type == "꺾은선 그래프":
            ax.plot(data[x_col], data[y_col], color="green", marker="o")
        elif graph_type == "Scatter Plot":
            ax.scatter(data[x_col], data[y_col], color="red")
        elif graph_type == "Stack 막대그래프":
            # 같은 x_col을 기준으로 y_col을 합산하여 스택 형태로 시각화
            data.groupby(x_col)[y_col].sum().plot(kind="bar", stacked=True, ax=ax)
        elif graph_type == "누적 그래프":
            ax.fill_between(data[x_col], data[y_col], color="orange", alpha=0.5)

        ax.set_title(graph_type, fontsize=16)
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        st.pyplot(fig)

# 이 파일을 단독으로 실행했을 때 동작하도록 하는 코드
if __name__ == '__main__':
    show()

