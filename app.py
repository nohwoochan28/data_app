import google_auth_httplib2
import httplib2
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Catfish stock", page_icon="🐰", layout="centered")
SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1hoWLJJsiCcic77qyiAAGsxlrW2seaW9D3aUBY8JbldI"
SHEET_NAME = "Database"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"


# def check_password():
#     """Returns `True` if the user had a correct password."""
#
#     def password_entered():
#         """Checks whether a password entered by the user is correct."""
#         if (
#                 st.session_state["username"] in st.secrets["passwords"]
#                 and st.session_state["password"]
#                 == st.secrets["passwords"][st.session_state["username"]]
#         ):
#             st.session_state["password_correct"] = True
#             del st.session_state["password"]  # don't store username + password
#             del st.session_state["username"]
#         else:
#             st.session_state["password_correct"] = False
#
#     if "password_correct" not in st.session_state:
#         # First run, show inputs for username + password.
#         st.text_input("Username", on_change=password_entered, key="username")
#         st.text_input(
#             "Password", type="password", on_change=password_entered, key="password"
#         )
#         return False
#     elif not st.session_state["password_correct"]:
#         # Password not correct, show input + error.
#         st.text_input("Username", on_change=password_entered, key="username")
#         st.text_input(
#             "Password", type="password", on_change=password_entered, key="password"
#         )
#         st.error("😕 User not known or password incorrect")
#         return False
#     else:
#         # Password correct.
#         return True
#
#
# if check_password():
add_selectbox = st.sidebar.selectbox("후보들", ("김민성", "나규승", "조현욱", "박요한", "조서현"))
# def main():
# st.title("증권거래소")
# st.header("2023년 5월 4일")
# col1, col2, col3, col4, col5 = st.columns(5)
# col1.metric("김민성", "71.6%", "-0.9%")
# col2.metric("나규승", "21.8%", "0.8%")
# col3.metric("조현욱", "0.2%", "-0.3%")
# col3.markdown("")
# col4.metric("박요한", "2.2%", "-1.8%")
# col5.metric("조서현", "4.2%", "2.2%")
# st.markdown("*무단배포를 절대 금지합니다")
# st.header("주식 소개")

@st.cache_resource()
def connect_to_gsheet():
    # Create a connection object.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[SCOPE],
    )

    # Create a new Http() object for every request
    def build_request(http, *args, **kwargs):
        new_http = google_auth_httplib2.AuthorizedHttp(
            credentials, http=httplib2.Http()
        )
        return HttpRequest(new_http, *args, **kwargs)

    authorized_http = google_auth_httplib2.AuthorizedHttp(
        credentials, http=httplib2.Http()
    )
    service = build(
        "sheets",
        "v4",
        requestBuilder=build_request,
        http=authorized_http,
    )
    gsheet_connector = service.spreadsheets()
    return gsheet_connector


def get_data(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!A:E",
        )
        .execute()
    )

    df = pd.DataFrame(values["values"])
    df.columns = df.iloc[0]
    df = df[1:]
    return df


def add_row_to_gsheet(gsheet_connector, row) -> None:
    gsheet_connector.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:D",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()

st.title("증권거래소")
st.subheader(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
st.markdown("*무단배포를 절대 금지합니다")
st.text("\n\n")
st.header("코인구매")
gsheet_connector = connect_to_gsheet()

form = st.form(key="annotation")
def get_data2(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!G:H",
        )
        .execute()
    )

    df2 = pd.DataFrame(values["values"])
    df2.columns = df2.iloc[0]
    df2 = df2[1:]
    return df2

with form:
    colors = ['#d2453f', '#1793d0', '#65d34f', '#f6a616', '#ebe614']
    fig2 = px.pie(get_data2(gsheet_connector), names='can', values='vot', title='코인 지지율')
    st.plotly_chart(fig2)
    cols = st.columns((1, 1))
    author = cols[0].text_input("구매자:")
    bug_type = cols[1].selectbox(
        "구매할 코인:", ["김민성", "나규승", "조현욱", "박요한", "조서현"], index=2
    )
    comment = st.text_area("코멘트:")
    cols = st.columns(2)
    # date = cols[0].date_input("언제있었던 일인가요?:")
    bug_severity = st.slider("구매할 수량:", 1, 5, 2)
    submitted = st.form_submit_button(label="제출")

if submitted:
    add_row_to_gsheet(
        gsheet_connector,
        [[author, bug_type, comment, bug_severity]],
    )
    st.success("친구들이 기뻐할거야!")
    st.balloons()

expander = st.expander("주식투자 기록보기")
with expander:
    st.write(f"원본 보기 [Google Sheet]({GSHEET_URL})")
    st.dataframe(get_data(gsheet_connector))

st.header("코인 소개")
st.subheader("김민성")
st.markdown("현재 가장 유력한 후보이다. 없는 질문도 만들어서 질문하는 그의 이름 김정배!")
st.subheader("나규승")
st.markdown("일요일 데이트와 같이하는 수많은 대회...규승이의 성장가능성은 무궁무진하다.")
st.subheader("조현욱")
st.markdown("현욱이는 슬프다....그냥 슬프다...조만간 상장 폐지가 유력하다....오늘도 내렸다...")
st.subheader("박요한")
st.markdown("그냥 로리콘이다 그는 이제 자포자기하고 자학개그를 하고있다.")
st.subheader("조서현")
st.markdown("솔직히 그냥 억까다. 근데 알빠노? 하지만 슬슬 억까가 아닌거같다.")
