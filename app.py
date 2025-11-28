import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="해외결제 혜택", page_icon="💳")

st.title("💳 이번 달 해외결제 혜택 모음")

# 데이터 파일이 있으면 보여주고, 없으면 경고
if os.path.exists("benefits.csv"):
    df = pd.read_csv("benefits.csv")
    st.write(f"최신 업데이트: {len(df)}개의 혜택을 찾았습니다.")
    st.dataframe(df)
else:
    st.warning("데이터 수집 중입니다. 1~2분 뒤에 새로고침 해주세요!")
