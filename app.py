
from datetime import datetime

import streamlit as st
st.set_page_config(page_title="Catfish stock", page_icon="🐰", layout="centered")
st.title("로그인")
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    add_selectbox = st.sidebar.selectbox("후보들", ("김민성", "나규승", "조현욱", "박요한", "조서현"))
    # def main():
    st.title("증권거래소")
    st.header("2023년 5월 3일")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("김민성", "72.5%", "-4.5%")
    col2.metric("나규승", "21%", "6%")
    col3.metric("조현욱", "0.5%", "-1.5%")
    col4.metric("박요한", "4%", "0%")
    col5.metric("조서현", "2%", "0%")
    st.text("*무단배포를 절대 금지합니다")
    st.header("주식 소개")
    st.subheader("김민성")
    st.markdown("현재 가장 유력한 후보이다. 없는 질문도 만들어서 질문하는 그의 이름 김정배!")
    st.subheader("나규승")
    st.markdown("일요일 데이트와 같이하는 수많은 대회...규승이의 성장가능성은 무궁무진하다.")
    st.subheader("조현욱")
    st.markdown("현욱이는 슬프다....그냥 슬프다...조만간 상장 폐지가 유력하다....")
    st.subheader("박요한")
    st.markdown("그냥 로리콘이다 그는 이제 자포자기하고 자학개그를 하고있다.")
    st.subheader("조서현")
    st.markdown("솔직히 그냥 억까다. 근데 알빠노?")

