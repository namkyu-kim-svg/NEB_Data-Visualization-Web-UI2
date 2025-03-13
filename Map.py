import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import re

# PNG 변환을 위해 imgkit 사용 (필요 시 설치: pip install imgkit)
# wkhtmltoimage는 시스템에 설치되어 있어야 합니다.
import os

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

    # Zoom Level과 Heading 입력 (방위)
    zoom_level = st.number_input("Zoom Level", min_value=1, max_value=20, value=12, step=1)
    heading = st.number_input("Heading (방위)", min_value=0, max_value=360, value=0, step=1)

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

        # 5) Folium 지도 생성 (Zoom Level을 zoom_start에 반영)
        if "attr" in tile_info:
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=zoom_level, tiles=None)
            folium.TileLayer(
                tiles=tile_info["tiles"],
                attr=tile_info["attr"],
                name=selected_tile
            ).add_to(m)
        else:
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=zoom_level, tiles=tile_info["tiles"])

        # 6) 지도에 추가 정보 오버레이 (화면 하단 좌측에 표시)
        info_html = f"""
        <div style="
            position: fixed;
            bottom: 10px;
            left: 10px;
            z-index: 9999;
            background-color: white;
            padding: 10px;
            border: 1px solid black;
            font-size: 14px;
            ">
            Zoom: {zoom_level}<br>
            Heading: {heading}°<br>
            Center: {avg_lat:.4f}, {avg_lon:.4f}
        </div>
        """
        m.get_root().html.add_child(folium.Element(info_html))

        # 7) 마커/서클 표시
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
                            html=(f'<div style="white-space: nowrap; font-size:12px; '
                                  f'font-weight:bold; color:{text_color};">'
                                  f'{row[label_col]}</div>')
                        )
                    ).add_to(m)
        else:
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

        # 8) PNG 파일 다운로드 버튼 (지도 저장)
        if st.button("PNG 파일 다운로드 (지도)"):
            # 지도 HTML을 문자열로 추출
            map_html = m.get_root().render()
            try:
                import imgkit
                # 임시 PNG 파일로 저장 (wkhtmltoimage 필요)
                imgkit.from_string(map_html, 'map.png')
                with open('map.png', 'rb') as f:
                    st.download_button(
                        label="지도 PNG 다운로드",
                        data=f,
                        file_name="map.png",
                        mime="image/png"
                    )
            except Exception as e:
                st.error("PNG 변환에 실패했습니다. imgkit과 wkhtmltoimage가 설치되어 있는지 확인하세요.\n" + str(e))

if __name__ == '__main__':
    show()


