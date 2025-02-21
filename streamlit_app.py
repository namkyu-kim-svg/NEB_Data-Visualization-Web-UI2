import matplotlib.font_manager as fm
import streamlit as st

# ✅ 시스템에 설치된 폰트 가져오기
font_list = [f.name for f in fm.fontManager.ttflist]

# ✅ 중복 제거 후 정렬
unique_fonts = sorted(list(set(font_list)))

# ✅ Streamlit으로 출력
st.title("시스템에 설치된 사용 가능한 폰트 목록")

st.write(f"총 {len(unique_fonts)}개의 폰트가 발견되었습니다.")
st.write(unique_fonts)




