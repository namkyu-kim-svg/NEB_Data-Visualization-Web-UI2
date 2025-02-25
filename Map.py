import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import re

def parse_coord(coord_str):
    # 위의 parse_coord 함수 내용 그대로 복붙
    try:
        return float(coord_str)
    except:
        pass
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", str(coord_str))
    numbers = list(map(float, numbers))
    if len(numbers) == 3:
        return numbers[0] + numbers[1]/60 + numbers[2]/3600
    elif len(numbers) == 2:
        return numbers[0] + numbers[1]/60
    elif len(numbers) == 1:
        return numbers[0]
    return None

def show():
    st.title("지도 페이지")
    st.header("지도 시각화")
    st.write("CSV 또는 Excel 파일을 업로드하면 위경도+라벨 데이터를 지도에 표시합니다.")

    uploaded_file = st.file_uploader("CSV 또는 Excel 파일 업로드", type=["csv", "xlsx"])
    if uploaded_file:
        # 1) 파일 읽기
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.write("업로드된 데이터 미리보기:")
        st.dataframe(data.head())

        # 2) 컬럼 선택
        lat_col = st.selectbox("위도 컬럼 선택", data.columns)
        lon_col = st.selectbox("경도 컬럼 선택", data.columns)
        label_col = st.selectbox("정점 이름(라벨) 컬럼 선택", data.columns)

        # 3) 위경도 문자열 → float 변환
        data['lat_dec'] = data[lat_col].apply(parse_coord)
        data['lon_dec'] = data[lon_col].apply(parse_coord)

        # 변환 결과 확인 (필요하다면)
        # st.write(data[['lat_dec', 'lon_dec']].head())

        # 4) 지도 중심 좌표를 십진수 컬럼 기준으로 평균
        avg_lat = data['lat_dec'].mean()
        avg_lon = data['lon_dec'].mean()

        # 5) Folium 지도 생성
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

        # 6) 각 행에 대해 마커 추가
        for i, row in data.iterrows():
            if pd.notnull(row['lat_dec']) and pd.notnull(row['lon_dec']):
                folium.Marker(
                    location=[row['lat_dec'], row['lon_dec']],
                    popup=str(row[label_col]),
                    tooltip=str(row[label_col]),
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m)

        # 7) Streamlit에 Folium 지도 표시
        st_folium(m, width=700, height=500)

if __name__ == '__main__':
    show()

