import streamlit as st
from pkg_utils.utils import menu_hide
from pkg_pages import page_admin, page_login, page_student


def main():
    if 'student' not in st.session_state:
        st.session_state['student'] = False
    if 'admin' not in st.session_state:
        st.session_state['admin'] = False

    if st.session_state['admin']:
        page_admin.load_view()
    elif st.session_state['student']:
        page_student.load_view()
    else:
        page_login.load_view()

if __name__ == '__main__':
    menu_hide()
    main()
