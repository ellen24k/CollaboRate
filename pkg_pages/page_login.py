import streamlit as st
from streamlit.net_util import get_external_ip
from pkg_utils.utils import padding_set, shorten_url, url_to_qr_code


def load_view():
    padding_set()
    st.title('**Collabo + Rate**') #st.title(':rainbow[Collabo + Rate]')
    st.write('_Real-time team project evaluation system_') # rating system?
    st.divider()

    class_codes = ['tempClass1', 'tempClass2']
    # class_codes = get_distinct_class_codes()
    selected_class_code = st.radio('수업 코드를 선택하세요:', class_codes)
    st.session_state['selected_class_code'] = selected_class_code
    st.divider()

    student_login_col, blank_col, admin_login_col = st.columns((4,1,4)) # 4:1:4
    with student_login_col:
        st.subheader('학생 로그인')

        id = st.text_input('학번을 입력하세요.', '3224')
        name = st.text_input('이름을 입력하세요.', '김태영') # 홍길동
        # group_number = int(st.text_input('그룹 번호를 입력하세요.', '1')) # 숫자 아니면 에러
        group_number = st.number_input('그룹 번호를 입력하세요.', placeholder='숫자 입력', value=1, min_value=1, max_value=15, step=1)

        if 'student' not in st.session_state:
            st.session_state['student'] = False

        login_btn = st.button('학생 로그인')
        if login_btn:
            if id and name and group_number:
                try:
                    res = {'id': 3224, 'name': '김태영', 'group_number': 1}
                    # res = login_student(id, name, group_number, st.session_state['selected_class_code'])
                    pass # 로그인 시도
                except Exception as e:
                    res = None
                    st.error('로그인 실패: ', str(e))

                if res is not None:
                    if res['name'] == name and res['group_number'] == group_number:
                        st.write(f'{name}님 로그인 성공')
                        st.session_state['student'] = True
                        st.session_state['student_id'] = id
                        st.session_state['name'] = name
                        st.session_state['group_number'] = group_number

                        st.rerun() #refresh
                    else:
                        st.error('로그인 실패')
                else:
                    st.error('학번이 존재하지 않습니다.')
            else:
                st.error('학번, 이름, 그룹번호를 입력하세요.')
        st.divider()

    with blank_col:
        st.write('')

    with admin_login_col:
        st.subheader('관리자 로그인')
        admin_password = st.text_input('관리자 비밀번호를 입력하세요.', type='password')
        correct_password = 1 # st.secrets['passwords']['admin_password']

        if st.button('관리자 로그인'):
            if admin_password == correct_password:
                st.session_state['admin'] = True
                st.write('관리자 로그인 성공')
                st.rerun()
        st.divider()

    st.subheader('유틸리티')
    if 'show_element' not in st.session_state:
        st.session_state['show_element'] = False

    if st.button('짧은 URL / QR CODE'):
        st.session_state['show_element'] = not st.session_state['show_element']
        st.rerun()

    if st.session_state['show_element']:
        # st.image('resources/streamlit_qr.png')
        streamlit_url = st.text_input(
            'streamlit URL',
            'https://collaborate.streamlit.app'
        )
        if st.button('streamlit short URL 생성'):
            streamlit_s_url = shorten_url(streamlit_url)
            st.write(streamlit_s_url)

        ngrok_url = st.text_input( #todo ngrok shorten_url 생성 에러
            'ngrok URL',
            f'https://????-{get_external_ip().replace('.', '-')}.ngrok-free.app'
        )
        if st.button('ngrok short URL/QR 생성'):
            ngrok_s_url = shorten_url(ngrok_url)
            st.write(ngrok_s_url)
            st.image(url_to_qr_code(ngrok_s_url))
