import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title='실시간 투표사이트', page_icon=':pencil2:')
    st.title('실시간 투표사이트')

    # CSV 파일에서 데이터를 읽어옵니다.
    df = pd.read_csv('vote.csv')

    # 투표 항목을 보여줍니다.
    st.write('투표 항목:')
    st.write(df['항목'])

    # 투표를 진행합니다.
    vote = st.selectbox('어떤 항목에 투표하시겠습니까?', df['항목'])

    # 투표 결과를 업데이트합니다.
    df.loc[df['항목'] == vote, '투표수'] += 1
    df.to_csv('vote.csv', index=False)

    # 투표 결과를 보여줍니다.
    st.write('투표 결과:')
    st.write(df)

if __name__ == '__main__':
    main()