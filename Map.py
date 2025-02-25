import streamlit as st
import pandas as pd
import pydeck as pdk
import re

def parse_coord(coord):
    """
    좌표 값이 숫자면 그대로 반환하고, 문자열인 경우 도, 분, 초 형식을 찾아 십진법으로 변환합니다.
    예)
      "37 30 12.34"  -> 37 + 30/60 + 12.34/3600
      "37°30.123'"  -> 37 + 30.123/60
    """
    try:
        # 이미 숫자형이면 그대로 반환
        return float(coord)
    except:
        pass

    # 문자열인 경우, 정규식으로 숫자 부분 추출
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", str(coord))
    numbers = list(map(float, numbers))
    if len(numbers) == 3:
        # DMS 형식
        return numbers[0] + numbers[1] / 60 + numbers[2] / 3600
    elif len(numbers) == 2:
        # DM 형식
        return numbers[0] + numbers[1] / 60
    elif len(numbers) == 1:
        return numbers[0]
    else:
        return None

def show():
    st.title("지도 페이지")
    st.header("지도 시각화")
    st.write("기본 지도가 아래에 표시됩니다. CSV 또는 Excel 파일을 업로드하면 위경도+농도 데이터를 시각화할 수 있습니다.")

    # 기본 지도: 한국 중심(대략 36.5, 127.5)에서 zoom=7
    default_view = pdk.ViewState(
        latitude=36.5, 
        longitude=127.5,
        zoom=7,
        pitch=0
    )
    base_map = pdk.Deck(layers=[], initial_view_state=default_view)
    st.pydeck_chart(base_map)

    # 파일 업로드
    uploaded_file = st.file_uploader("CSV 또는 Excel 파일 업로드", type=["csv", "xlsx"])
    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
        
        st.write("업로드된 데이터 미리보기:")
        st.dataframe(data.head())

        # 사용자에게 위도, 경도, 농도 컬럼 선택 요청
        lat_col = st.selectbox("위도 컬럼 선택", data.columns)
        lon_col = st.selectbox("경도 컬럼 선택", data.columns)
        conc_col = st.selectbox("농도 컬럼 선택", data.columns)
        
        # 위경도 값을 십진법으로 변환한 새로운 컬럼 추가
        data['lat_dec'] = data[lat_col].apply(parse_coord)
        data['lon_dec'] = data[lon_col].apply(parse_coord)

        # 농도 컬럼은 숫자형으로 변환
        try:
            data[conc_col] = pd.to_numeric(data[conc_col])
        except Exception as e:
            st.error("농도 컬럼은 숫자형으로 변환할 수 없습니다.")
            return

        # Pydeck을 이용해 ScatterplotLayer로 지도에 시각화
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=data,
            get_position=["lon_dec", "lat_dec"],
            get_color="[255, 0, 0, 160]",  # 빨간색 (투명도 160)
            get_radius=f"{conc_col} * 10",   # 농도에 비례한 원 크기 (스케일 조정 가능)
            pickable=True
        )
        
        # 데이터의 중심을 계산하여 초기 뷰 설정
        if data['lat_dec'].notnull().any() and data['lon_dec'].notnull().any():
            avg_lat = data['lat_dec'].mean()
            avg_lon = data['lon_dec'].mean()
        else:
            avg_lat, avg_lon = 36.5, 127.5
        
        view_state = pdk.ViewState(
            latitude=avg_lat,
            longitude=avg_lon,
            zoom=10,
            pitch=0
        )
        
        # 툴팁을 통해 농도 정보를 표시
        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"html": "농도: {"+conc_col+"}"}
        )
        st.pydeck_chart(deck)

if __name__ == '__main__':
    show()

