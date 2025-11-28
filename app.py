import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="해외결제 혜택", page_icon="💳")

st.title("💳 이번 달 해외결제 혜택 모음")

# 파일이 존재하는지 확인
if os.path.exists("benefits.csv"):
    try:
        # 파일이 비어있는지 확인 (크기가 0보다 커야 함)
        if os.path.getsize("benefits.csv") > 0:
            df = pd.read_csv("benefits.csv")
            st.write(f"최신 업데이트: {len(df)}개의 혜택을 찾았습니다.")
            st.dataframe(df)
        else:
            st.warning("데이터 파일은 있지만 내용이 비어있습니다. 크롤러가 실행될 때까지 기다려주세요.")
            if st.button("로봇 상태 확인하러 가기"):
                st.markdown("[GitHub Actions 바로가기](https://github.com/) (본인 저장소 주소로 이동하세요)")
    except pd.errors.EmptyDataError:
        st.warning("데이터 파일이 비어있습니다. (EmptyDataError)")
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
else:
    st.info("아직 수집된 데이터가 없습니다. 매월 1일에 자동으로 생성됩니다.")
