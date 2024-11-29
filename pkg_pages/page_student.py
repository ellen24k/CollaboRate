import asyncio
import threading
from time import sleep

import streamlit as st
from streamlit_star_rating import st_star_rating

from pkg_utils.utils import logo
from pkg_utils.db_data import get_students_by_class, get_rating_points, insert_rating_point, get_project_infos, \
    update_rating_point, run_asyncio_get



def load_view():
    logo()

    student_id = st.session_state['student_id']
    student_name = st.session_state['name']
    student_group =st.session_state['group_number']
    class_code = st.session_state['selected_class_code']

    # students = get_students_by_class(class_code) #todo 1
    students, rating_points, project_infos = run_asyncio_get(class_code, student_id)

    groups = set(student['group_number'] for student in students)
    group_members = {group: [student['name'] for student in students if student['group_number'] == group] for group in groups}

    # rating_points = get_rating_points(class_code,student_id) #todo 2
    # project_infos = get_project_infos(class_code) #todo 3

    points = {}

    st.markdown(f'[{student_name}]님 환영합니다.')
    st.markdown(f'[학번]{student_id} [클래스코드]{class_code} [그룹]{student_group}')

    for group in groups:
        # point = next((item['point'] for item in rating_points if item['group_number'] == group), 0)
        points_list = [item['point'] for item in rating_points if item['group_number'] == group]
        if points_list:
            point = points_list[0]
        else:
            point = 0

        with st.container(border=True, key=f'container_{group}'):
            st.markdown(f'### 그룹 {group}')

            if point == 0:
                try:
                    insert_rating_point(group, student_id, 1, class_code)
                    point = 1
                except Exception as e:
                    st.error(e)

            # project_info = next((item for item in project_infos if item['group_number'] == group), None)
            project_info_list = [item for item in project_infos if item['group_number'] == group]
            project_info = project_info_list[0] if project_info_list else None


            if project_info:
                st.markdown(f'### :rainbow[{project_info['project_name']}]')
                st.markdown(project_info['project_desc'])
                st.divider()
                st.markdown(f'###### project by :rainbow[{project_info['team_name']}]')
                st.markdown(group_members[group])
            else:
                st.markdown('프로젝트 정보 없음')
                st.divider()
                st.markdown(group_members[group])

            points[group] = st_star_rating(
                label='',
                maxValue=10,
                defaultValue=point,
                key=f'star_{group}',
                size=18,
                customCSS='''
                #root > div > ul > li {
                position: relative;
                left: 4px;
                bottom: 4px;
                }
                '''
            )

            if points[group] != point:
                try:
                    update_rating_point(group, student_id, points[group], class_code)
                    st.balloons()
                except Exception as e:
                    st.error(e)
    st.markdown(' ')
    st.divider()