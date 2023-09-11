import streamlit as st
import pandas as pd
import dataframe_image as dfi
import matplotlib as mpl
import matplotlib.font_manager as fm


mpl.font_manager.fontManager.addfont('malgun.ttf')

mpl.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['font.size'] = 25
import streamlit_ext as ste




@st.cache_data
def read_excel():
    file_name = 'rawdata.pkl'
    df = pd.read_pickle(file_name)
    return df

st.set_page_config("GA2 신상품용 (과거)가계약리스트 조회",layout="wide")
st.header('GA2 신상품용 (과거) 가계약리스트 조회')



df = read_excel()

# st.write(df.head())


col1, col2, col3 = st.columns(3)

with col1:
    jijum_name = ['GA2-3지점','GA2-1지점','GA2-2지점','GA2-4지점','GA2-5지점','GA2-6지점','GA2-7지점']
    jijum = st.selectbox("지점명",jijum_name)

with col2:
    manager_name = df[df['지점']==jijum].매니저명.unique().tolist()
    manager = st.selectbox("매니저명",manager_name)

with col3:
    jisa_name = df[(df['지점']==jijum) & (df['매니저명']==manager)].지사명.unique().tolist()
    jisa = st.selectbox('지사명',["전체"]+jisa_name)

    if type(jisa) is str:
        temp = []
        temp.append(jisa)
        jisa = temp

    if jisa == ["전체"]:
        jisa = jisa_name


options = ['모두','승인',
'자동승인',
'보완요청',
'심사대상',
'조정대상',
'심사미필',
'수납대기',
'심사요청완료',
'(조건부승인)',
'조건부승인',
'심사중']

select_option = st.multiselect("가계약상태명(복수선택가능)",options,placeholder="가계약상태명을 클릭해주세요")
# print(select_option)
if select_option == ["모두"]:
    select_option = options
else:
    pass


##조건문
con1 = df['지점'] == jijum
con2 = df['매니저명'] == manager
con3 = df['지사명'].isin(jisa)
con4 = df['계약상태'].isin(select_option)

df_out = df[con1 & con2 & con3 & con4].copy()
df_out = df_out.sort_values('기준일자', ascending=False)
df_out = df_out[['기준일자','가계약번호','계약상태','상품명','조직코드','조직명','피보험자명','보험연령','성별코드']]


column_count = min(13, len(df_out)+1)


st.dataframe(df_out,use_container_width=True,hide_index=True, height=column_count*35+3)


colb1, colb2 = st.columns(2)

with colb1:
    make_filebtn = st.button(
            label=str('파일생성하기'),
        )


with colb2:
    if make_filebtn:
        file_name = str('temp')+'.PNG'

        dfi.export(df_out.style.hide(axis='index'), file_name, max_cols=-1, max_rows=-1, table_conversion='matplotlib')
        with open(file_name, "rb") as file:
            btn = ste.download_button(
                    label=str('다운로드받기' ),
                    data=file,
                    file_name=file_name,
                    mime="image/png",
                )