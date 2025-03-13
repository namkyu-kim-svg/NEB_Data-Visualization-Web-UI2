import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import matplotlib as mpl
import koreanize_matplotlib

# Linux 환경에서 한글 폰트 설정 (NanumGothic)
mpl.rcParams['font.family'] = 'NanumGothic'
mpl.rcParams['axes.unicode_minus'] = False

def show():
    st.title("그래프 페이지")
    st.write("샘플 데이터를 먼저 다운로드하거나, 직접 CSV/XLSX 파일을 업로드해 보세요.")

    # 1) 샘플 데이터 생성
    df_sample = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D', 'E'],
        'Value1': [10, 20, 15, 25, 18],
        'Value2': [3, 4, 8, 6, 7]
    })

    # 2) CSV로 변환 후 다운로드 버튼 제공
    csv_data = df_sample.to_csv(index=False)
    st.download_button(
        label="샘플 데이터 다운로드",
        data=csv_data,
        file_name="sample_data.csv",
        mime="text/csv"
    )

    st.divider()
    # 3) 파일 업로드
    uploaded_file = st.file_uploader("CSV 또는 Excel 파일을 업로드하세요", type=["csv", "xlsx"])
    data = None
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)
        st.write("업로드된 데이터 미리보기:")
        st.dataframe(data)

    if data is not None:
        st.divider()
        st.subheader("그래프 설정")
        graph_type = st.selectbox(
            "그래프 종류",
            ["막대그래프", "꺾은선 그래프", "Scatter Plot", "Stack 막대그래프", "누적 그래프"]
        )
        # X축 설정 (한 줄에 2칸)
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("X축 데이터 선택", data.columns)
        with col2:
            x_label = st.text_input("X축 라벨", x_col)

        # Y축 설정: 일반 그래프는 단일 선택, 스택 그래프는 다중 선택
        if graph_type != "Stack 막대그래프":
            col3, col4 = st.columns(2)
            with col3:
                y_col = st.selectbox("Y축 데이터 선택", data.columns)
            with col4:
                y_label = st.text_input("Y축 라벨", y_col)
        else:
            # 스택 막대그래프의 경우 여러 컬럼 선택
            y_label = st.text_input("Y축 라벨 (예: 여러 값)", "여러 값")
            stack_y = st.multiselect("Stack 막대그래프: Y축 데이터 선택 (여러 컬럼 선택)", data.columns)

        # 그래프 타이틀, 폰트 크기, 간격을 한 줄에 3칸으로 배치
        colT1, colT2, colT3 = st.columns([2,1,1])
        with colT1:
            custom_title = st.text_input("그래프 타이틀", "내 그래프")
        with colT2:
            title_fontsize = st.number_input("타이틀 폰트 크기", min_value=1, max_value=50, value=16, step=1)
        with colT3:
            title_pad = st.number_input("타이틀 간격", min_value=0, max_value=100, value=10, step=1)

        # 그래프 크기 및 색상 설정
        width = st.number_input("그래프 너비 (inch)", min_value=1.0, max_value=20.0, value=10.0, step=0.5)
        height = st.number_input("그래프 높이 (inch)", min_value=1.0, max_value=20.0, value=6.0, step=0.5)
        color = st.color_picker("그래프 색상", "#87CEEB")

        # X축, Y축 라벨 폰트 크기 및 라벨 간격 (각각 한 줄에 2칸)
        colX1, colX2 = st.columns(2)
        with colX1:
            x_label_fontsize = st.number_input("X축 라벨 폰트 크기", min_value=1, max_value=40, value=12, step=1)
        with colX2:
            x_label_pad = st.number_input("X축 라벨 간격", min_value=0, max_value=50, value=5, step=1)
        colY1, colY2 = st.columns(2)
        with colY1:
            y_label_fontsize = st.number_input("Y축 라벨 폰트 크기", min_value=1, max_value=40, value=12, step=1)
        with colY2:
            y_label_pad = st.number_input("Y축 라벨 간격", min_value=0, max_value=50, value=5, step=1)

        # 그래프 그리기 버튼
        if st.button("그래프 그리기"):
            fig, ax = plt.subplots(figsize=(width, height))
            if graph_type == "막대그래프":
                ax.bar(data[x_col], data[y_col], color=color)
            elif graph_type == "꺾은선 그래프":
                ax.plot(data[x_col], data[y_col], color=color, marker="o")
            elif graph_type == "Scatter Plot":
                ax.scatter(data[x_col], data[y_col], color=color)
            elif graph_type == "Stack 막대그래프":
                if len(stack_y) < 2:
                    st.warning("Stacked bar chart를 위해서는 최소 2개 이상의 Y축 데이터를 선택하세요.")
                else:
                    # 그룹별로 선택한 Y 컬럼의 합계를 구해 스택 형태로 그리기
                    pivot_data = data.groupby(x_col)[stack_y].sum()
                    pivot_data.plot(kind="bar", stacked=True, ax=ax)
            elif graph_type == "누적 그래프":
                ax.fill_between(data[x_col], data[y_col], color=color, alpha=0.5)

            ax.set_title(custom_title, fontsize=title_fontsize, pad=title_pad)
            ax.set_xlabel(x_label, fontsize=x_label_fontsize, labelpad=x_label_pad)
            # 스택 그래프면 y_label은 전체 레이블로, 아니면 선택한 컬럼 이름 사용
            if graph_type != "Stack 막대그래프":
                ax.set_ylabel(y_label, fontsize=y_label_fontsize, labelpad=y_label_pad)
            else:
                ax.set_ylabel(y_label, fontsize=y_label_fontsize, labelpad=y_label_pad)

            st.pyplot(fig)

            # PNG 파일 다운로드
            buf = BytesIO()
            fig.savefig(buf, format="png")
            st.download_button(
                label="PNG 파일 다운로드",
                data=buf.getvalue(),
                file_name="mygraph.png",
                mime="image/png"
            )

if __name__ == '__main__':
    show()

