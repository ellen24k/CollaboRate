import streamlit as st
from streamlit.net_util import get_external_ip

from pkg_utils.db_data import get_distinct_class_codes, login_student, get_virtual_students
from pkg_utils.utils import logo, shorten_url, url_to_qr_code


def load_view():
    logo()

    class_codes = get_distinct_class_codes()
    st.session_state['selected_class_code'] = st.radio('수업 코드를 선택하세요:', class_codes)
    st.markdown("VIRTUAL DATA TEST", help = get_virtual_students())
    st.divider()

    student_login_col, blank_col, admin_login_col = st.columns((8,1,8))
    with student_login_col:
        st.subheader('학생 로그인')

        id = st.text_input('학번을 입력하세요.')
        name = st.text_input('이름을 입력하세요.')
        group_number = st.number_input('그룹 번호를 입력하세요.', value=1, min_value=1, step=1)

        if 'student' not in st.session_state:
            st.session_state['student'] = False

        if st.button('학생 로그인'):
            if id and name and group_number:
                try:
                    student_info = login_student(id, name, group_number, st.session_state['selected_class_code'])
                except Exception as e:
                    st.error('로그인 실패: ', e)
                    student_info = None

                if student_info is not None:
                    if student_info['name'] == name and student_info['group_number'] == group_number:
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
        st.markdown('')

    with admin_login_col:
        st.subheader('관리자 로그인')
        admin_password = st.text_input('관리자 비밀번호를 입력하세요.', type='password')
        correct_password = st.secrets['passwords']['ADMIN_PASSWORD']

        if st.button('관리자 로그인'):
            if admin_password == correct_password:
                st.session_state['admin'] = True
                st.rerun()
            else:
                st.error('로그인 실패')
        st.divider()

    st.subheader('QR CODE / URL')
    if 'show_element' not in st.session_state:
        st.session_state['show_element'] = False

    if st.button('QR CODE / URL'):
        st.session_state['show_element'] = not st.session_state['show_element']
        st.rerun()

    if st.session_state['show_element']:
        st.image('resources/streamlit_qr.png')
        streamlit_url = st.text_input(
            'streamlit URL',
            'https://collaborate.streamlit.app'
        )
        if st.button('streamlit short URL 생성'):
            streamlit_s_url = shorten_url(streamlit_url)
            st.write(streamlit_s_url)

        ngrok_url = st.text_input(
            'ngrok URL',
            f'https://aaaa-{get_external_ip().replace('.', '-')}.ngrok-free.app'
        )
        if st.button('ngrok short URL/QR 생성'):
            ngrok_s_url = shorten_url(ngrok_url)
            st.write(ngrok_s_url)
            st.image(url_to_qr_code(ngrok_s_url))
