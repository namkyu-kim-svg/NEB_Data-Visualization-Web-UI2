import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show():
    st.title("그래프 페이지")
    st.header("그래프 종류를 선택하세요")

    graph_type = st.selectbox(
        "그래프 종류",
        ["막대그래프", "꺾은선 그래프", "Scatter Plot", "Stack 막대그래프", "누적 그래프"]
    )

    uploaded_file = st.file_uploader("CSV 또는 Excel 파일을 업로드하세요", type=["csv", "xlsx"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)

        st.write("업로드된 데이터 미리보기:")
        st.dataframe(data)

        x_col = st.selectbox("X축 데이터 선택", data.columns)
        y_col = st.selectbox("Y축 데이터 선택", data.columns)

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

if __name__ == '__main__':
    show()
