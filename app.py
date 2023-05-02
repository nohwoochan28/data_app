import streamlit as st

# def main():
st.title("증권거래소")
st.header("2023년 5월 2일")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("김민성", "67%", "-3%")
col2.metric("나규승", "25%", "5%")
col3.metric("조현욱", "2%", "0%")
col4.metric("박요한", "4%", "-1%")
col5.metric("조서현", "2%", "-1%")
# st.subheader("This is subheader")
st.text("*무단배포를 절대 금지합니다")
# name = '이설민'
# st.text(f'Hi, {name}')
# st.write("Streamlit study course")
# st.markdown("## 매우중요")
# st.success('설보민지')

# if __name__ == '__main__':
#     main()