import streamlit as st
from streamlit_star_rating import st_star_rating
from pkg_utils.utils import padding_set


def load_view():
    padding_set()
    st.title('**Collabo + Rate**')  # st.title(':rainbow[Collabo + Rate]')
    st.write('_Real-time team project evaluation system_')  # rating system?
    st.divider()

    student_id = st.session_state['student_id']
    student_name = st.session_state['name']
    student_group =st.session_state['group_number']

    st.write(f'[{student_name}]')
    st.write(f'[학번] {student_id}\t[클래스코드]\t{st.session_state["selected_class_code"]}\t[그룹] {student_group} ')
    st.divider()

    # students = get_students(st.session_state['selected_class_code'])
    # groups = set([student['group_number'] for student in students])
    # group_members = {group: [student['name'] for student in students if student['group_number'] == group] for group in
    #                  groups}
    # evaluation_points = get_evaluation_points(st.session_state['selected_class_code'], student_id)
    # project_infos = get_project_infos(st.session_state['selected_class_code'])
    points = {}