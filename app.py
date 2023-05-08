import google_auth_httplib2
import httplib2
import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Catfish stock 1.1.8", page_icon="🐰", layout="centered")
SCOPE = "https://www.googleapis.com/auth/spreadsheets"
SPREADSHEET_ID = "1hoWLJJsiCcic77qyiAAGsxlrW2seaW9D3aUBY8JbldI"
SHEET_NAME = "Database"
GSHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"

COMMENT_TEMPLATE_MD = """{} - {}
> {}"""
def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")

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
add_selectbox = st.sidebar.selectbox("후보들", ("김민성", "나규승", "조현욱", "박요한", "조서현", "이용현"))
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
        range=f"{SHEET_NAME}!A:E",
        body=dict(values=row),
        valueInputOption="USER_ENTERED",
    ).execute()

st.title("증권거래소")
st.subheader(datetime.today().strftime("%Y/%m/%d %H:%M:%S"))
st.markdown("*무단배포를 절대 금지합니다")
st.text("\n\n")
st.header("코인구매")
st.markdown("시세조작을 시도할 경우 구매취소 및 제재가 이루어질 수 있습니다.")
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
def get_data3(gsheet_connector) -> pd.DataFrame:
    values = (
        gsheet_connector.values()
        .get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!L:N",
        )
        .execute()
    )

    df3 = pd.DataFrame(values["values"])
    df3.columns = df3.iloc[0]
    df3 = df3[1:]
    return df3


def insert(gsheet_connector, row) -> None:
    values = (
        gsheet_connector.values()
        .append(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_NAME}!L:N",
            body=dict(values=row),
            valueInputOption="USER_ENTERED",
        )
        .execute()
    )
with form:
    colors = ['#d2453f', '#1793d0', '#65d34f', '#f6a616', '#ebe614']
    fig2 = px.pie(get_data2(gsheet_connector), names='can', values='vot', title='코인 지지율')
    st.plotly_chart(fig2)
    cols = st.columns((1, 1))
    author = cols[0].text_input("구매자(임창정 경고 2회):")
    bug_type = cols[1].selectbox(
        "구매할 코인:", ["김민성", "나규승", "조현욱", "박요한", "조서현", "이용현"], index=2
    )
    comment = st.text_area("코멘트:")
    cols = st.columns(2)
    # date = cols[0].date_input("언제있었던 일인가요?:")
    bug_severity = st.slider("구매할 수량:", 1, 7, 3)
    submitted = st.form_submit_button(label="제출")
#
if submitted:
    date = datetime.now().strftime("%d.%m.%Y")
    add_row_to_gsheet(
        gsheet_connector,
        [[author, bug_type, comment, bug_severity, date]],
    )
    st.success("친구들이 기뻐할거야!")
    st.balloons()

expander = st.expander("📈 주식투자 기록보기")
with expander:
    st.write(f"원본 보기 [Google Sheet]({GSHEET_URL})")
    st.dataframe(get_data(gsheet_connector))



with st.expander("💬 토론방 열기"):

    # Show comments

    st.write("**토론방:**")

    for index, entry in enumerate(get_data3(gsheet_connector).itertuples()):
        st.markdown(COMMENT_TEMPLATE_MD.format(entry.name, entry.date, entry.comment))

        is_last = index == len(get_data3(gsheet_connector)) - 1
        is_new = "just_posted" in st.session_state and is_last
        if is_new:
            st.success("☝️ 댓글 작성완료!")


    space(2)

    st.write("**의견을 작성하세요:**")
    form2 = st.form("comment")
    name = form2.text_input("이름")
    comment = form2.text_area("의견")
    submit = form2.form_submit_button("의견 등록")
    # gsheet_connector   connect_to_gsheet()
    if submit:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        insert(gsheet_connector, [[name, comment, date]])
        if "just_posted" not in st.session_state:
            st.session_state["just_posted"] = True
        st.experimental_rerun()
    # if submit:
    #     date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #     add_row_to_gsheet(
    #         gsheet_connector,
    #         [[name, comment, date]],
    #     )
        # if "just_posted" not in st.session_state:
        #     st.session_state["just_posted"] = True
        # st.experimental_rerun()
        st.success("댓글 등록성공")
        st.balloons()

st.header("코인 소개")
st.subheader("김민성")
st.markdown("현재 가장 유력한 후보이다. 없는 질문도 만들어서 질문하는 그의 이름 김정배! 최근들어 조서현과 나규승에게 입지가 조금씩 말리는 모습을 보여주고 있다. 하지만 아직은 정배의 품격을 유지하고 있다.")
st.subheader("나규승")
st.markdown("일요일 데이트와 같이하는 수많은 대회...규승이의 성장가능성은 무궁무진하다. 최근 한사챌 1차에 규승이 팀이 합격을 하는등 기세가 무섭다. 역시 연구하는 남자는 멋져")
st.subheader("조현욱")
st.markdown("현욱이는 슬프다....그냥 슬프다...조만간 상장 폐지가 유력하다....오늘도 내렸다...누군가가 현욱코인을 꾸준히 구매하고 있다. 하지만 모두가 안다...현욱이는 안된다... \n정안나는 조현욱의 관심을 받고 본인도 내심 좋아하였으나 정안나에게는 성적이 더 중요했기에 어쩔 수 없이 조현욱의 멘탈을 터뜨리기 위해 그를 튕겨낼 수 밖에 없었다. 정안나의 본심은 아직 조현욱에 가있다. -이상현-")
st.subheader("박요한")
st.markdown("그냥 로리콘이다 그는 이제 자포자기하고 자학개그를 하고있다.조서현의 강력한 지지를 받고 있다.")
st.subheader("조서현")
st.markdown("솔직히 그냥 억까다. 근데 알빠노? 하지만 슬슬 억까가 아닌거같다. 앞으로의 행보를 기대해보자!")
st.subheader("이용현")
st.markdown("동남아에서온 그는 과연 그녀의 마음을 사로잡을 수 있을것인가")
space(4)
st.subheader("[패치노트]")
st.markdown("[1.1.6]\n -Catfishstock에 지지율 기능이 생겼습니다.\n -기존에 있던 코인 구매하기 기능을 이용해 코인을 구매하면 이를 실시간으로 반영해 코인지지율이 올라갑니다. \n -코인 소개 목차가 코인구매 기능 밑으로 내려갔습니다.\n -코인구매 기능중 날짜 체크 기능을 제거했습니다.")
space(1)
st.markdown("[1.1.7]\n -Catfishstock에 커뮤니티 기능이 생겼습니다! 토론방에 들어가 코인에 대한 자신의 의견을 남겨보세요!")
space(1)
st.markdown("[1.1.8]\n -이용현 코인이 새롭게 상장되었습니다. 많은 관심 부탁드립니다! \n -사이트 하단에 패치노트 항목이 추가되었습니다.")
space(1)
st.markdown("[1.1.9]\n -최대 구매가능한 코인이 5개에서 7개로 증가했습니다.")
