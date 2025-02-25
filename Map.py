import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

def show():
    st.title("정점 지도 표시")
    st.write("지도에 각 정점을 표시합니다. CSV 또는 Excel 파일을 업로드해 주세요.")

    # 파일 업로드
    uploaded_file = st.file_uploader("정점 파일 업로드 (CSV 또는 Excel)", type=["csv", "xlsx"])
    if uploaded_file:
        # 데이터 읽기
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.write("업로드된 데이터 미리보기:")
        st.dataframe(data)

        # 컬럼 선택: 위도, 경도, 정점 라벨(이름)
        lat_col = st.selectbox("위도 컬럼 선택", data.columns)
        lon_col = st.selectbox("경도 컬럼 선택", data.columns)
        label_col = st.selectbox("정점 이름(라벨) 컬럼 선택", data.columns)

        # 지도 중심 좌표를 데이터 평균 좌표로 설정
        avg_lat = data[lat_col].mean()
        avg_lon = data[lon_col].mean()

        # Folium 지도 생성 (zoom_start 조절 가능)
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

        # 각 행에 대해 마커 추가
        for i, row in data.iterrows():
            lat_val = row[lat_col]
            lon_val = row[lon_col]
            label_val = row[label_col]

            # 마커 생성 (popup과 tooltip에 라벨 표시)
            folium.Marker(
                location=[lat_val, lon_val],
                popup=str(label_val),
                tooltip=str(label_val),
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)

        # Streamlit에 Folium 지도 표시
        st_folium(m, width=700, height=500)

if __name__ == '__main__':
    show()

