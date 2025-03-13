import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import re

def parse_coord(coord_str):
    """
    도분초(DMS) 또는 도분(DM) 형태의 문자열을 십진법(float)으로 변환.
    예: "37°30'20.5\"" 또는 "37 30 20.5" -> 37 + 30/60 + 20.5/3600
    """
    try:
        return float(coord_str)
    except:
        pass
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", str(coord_str))
    numbers = list(map(float, numbers))
    if len(numbers) == 3:
        return numbers[0] + numbers[1] / 60 + numbers[2] / 3600
    elif len(numbers) == 2:
        return numbers[0] + numbers[1] / 60
    elif len(numbers) == 1:
        return numbers[0]
    return None

def show():
    st.title("지도 시각화")

    # 1) 지도 시각화 모드 선택
    mode = st.selectbox("지도 시각화 모드 선택", ["정점도", "위경도 농도 시각화"])

    # 2) 지도 스타일 옵션 (Folium에서 인식되는 정확한 tiles 문자열 사용)
    tile_options = {
        "OpenStreetMap": {
            "tiles": "OpenStreetMap"
        },
        "Stamen Terrain": {
            "tiles": "Stamen Terrain",
            "attr": 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under CC BY 3.0. ' 
                    'Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under ODbL.'
        },
        "Stamen Toner": {
            "tiles": "Stamen Toner",
            "attr": 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under CC BY 3.0. '
                    'Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under ODbL.'
        },
        "Stamen Watercolor": {
            "tiles": "Stamen Watercolor",
            "attr": 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under CC BY 3.0. '
                    'Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under CC BY 3.0.'
        },
        "CartoDB Positron": {
            "tiles": "CartoDB positron"
        },
        "CartoDB Dark Matter": {
            "tiles": "CartoDB dark_matter"
        },
        "Esri WorldImagery": {
            "tiles": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            "attr": "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, "
                    "GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"
        }
    }

    selected_tile = st.selectbox("지도 스타일 선택", list(tile_options.keys()))
    tile_info = tile_options[selected_tile]

    st.write("CSV 또는 Excel 파일을 업로드해 주세요.")
    uploaded_file = st.file_uploader("파일 업로드", type=["csv", "xlsx"])

    if uploaded_file:
        # 3) 파일 읽기
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        st.write("업로드된 데이터 미리보기:")
        st.dataframe(data.head())

        # 4) 모드별 설정
        if mode == "정점도":
            lat_col = st.selectbox("위도 컬럼 선택", data.columns)
            lon_col = st.selectbox("경도 컬럼 선택", data.columns)
            label_col = st.selectbox("정점 이름(라벨) 컬럼 선택", data.columns)
            marker_color = st.selectbox("마커 색상 선택", ["blue", "green", "red", "purple", "orange"])
            text_color = st.selectbox("정점명 글씨 색상 선택", ["black", "white"])

            data['lat_dec'] = data[lat_col].apply(parse_coord)
            data['lon_dec'] = data[lon_col].apply(parse_coord)

            avg_lat = data['lat_dec'].mean() if data['lat_dec'].notnull().any() else 36.5
            avg_lon = data['lon_dec'].mean() if data['lon_dec'].notnull().any() else 127.5

        else:  # "위경도 농도 시각화"
            lat_col = st.selectbox("위도 컬럼 선택", data.columns)
            lon_col = st.selectbox("경도 컬럼 선택", data.columns)
            conc_col = st.selectbox("농도 컬럼 선택", data.columns)

            data['lat_dec'] = data[lat_col].apply(parse_coord)
            data['lon_dec'] = data[lon_col].apply(parse_coord)

            try:
                data[conc_col] = pd.to_numeric(data[conc_col])
            except Exception:
                st.error("농도 컬럼을 숫자로 변환할 수 없습니다.")
                return

            avg_lat = data['lat_dec'].mean() if data['lat_dec'].notnull().any() else 36.5
            avg_lon = data['lon_dec'].mean() if data['lon_dec'].notnull().any() else 127.5

        # 5) Folium 지도 생성
        if "attr" in tile_info:
            # attribution이 필요한 커스텀 타일
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12, tiles=None)
            folium.TileLayer(
                tiles=tile_info["tiles"],
                attr=tile_info["attr"],
                name=selected_tile
            ).add_to(m)
        else:
            # 일반 타일 (OpenStreetMap, CartoDB 등)
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12, tiles=tile_info["tiles"])

        # 6) 마커/서클 표시
        if mode == "정점도":
            for _, row in data.iterrows():
                if pd.notnull(row['lat_dec']) and pd.notnull(row['lon_dec']):
                    folium.Marker(
                        location=[row['lat_dec'], row['lon_dec']],
                        icon=folium.Icon(color=marker_color, icon="star", prefix="fa")
                    ).add_to(m)

                    # 정점 이름 DivIcon
                    folium.map.Marker(
                        [row['lat_dec'], row['lon_dec']],
                        icon=folium.DivIcon(
                            html=(
                                f'<div style="white-space: nowrap; font-size:12px; '
                                f'font-weight:bold; color:{text_color};">'
                                f'{row[label_col]}</div>'
                            )
                        )
                    ).add_to(m)
        else:
            # 위경도 농도 시각화
            for _, row in data.iterrows():
                if pd.notnull(row['lat_dec']) and pd.notnull(row['lon_dec']):
                    radius = max(5, min(row[conc_col] * 0.5, 20))
                    folium.CircleMarker(
                        location=[row['lat_dec'], row['lon_dec']],
                        radius=radius,
                        popup=f"{conc_col}: {row[conc_col]}",
                        tooltip=f"{conc_col}: {row[conc_col]}",
                        color='red',
                        fill=True,
                        fill_color='red',
                        fill_opacity=0.6
                    ).add_to(m)

        st.write("지도:")
        st_folium(m, width=1400, height=800)

if __name__ == '__main__':
    show()

