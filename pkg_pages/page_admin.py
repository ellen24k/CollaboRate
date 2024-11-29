import asyncio
import time
from threading import Thread

import pandas as pd
import streamlit as st

from pkg_utils.db_data import generate_data_from_class, get_students_by_class, get_distinct_group_numbers, get_rating_by_class, delete_class_rating_data, run_asyncio_simulation_data
from pkg_utils.utils import logo

def load_view():
    logo('[ADMIN]')

    class_code = st.session_state['selected_class_code']
    students = asyncio.run(get_students_by_class(class_code))
    group_numbers = get_distinct_group_numbers(class_code)
    max_vote = len(group_numbers) * len(students)

    admin_menu(class_code)
    placeholder = st.empty()
    while True:
        with placeholder.container():
            st.session_state['df_value'], st.session_state['df_avg'], st.session_state['df_count'], st.session_state['student_vote_counts'] = update_graph(class_code)

            rank_avg_col, cur_rating_status_col = st.columns((5, 8))
            with rank_avg_col:
                st.subheader('순위 및 평균 점수')
                df_avg_sorted = st.session_state['df_avg'].sort_values(by='point', ascending=False).reset_index(drop=True)
                df_avg_sorted['rank'] = df_avg_sorted.index + 1
                df_avg_sorted = df_avg_sorted[['rank', 'group_number', 'point']]

                df_avg_sorted.columns = ['순위', '그룹 번호', '평균 점수']
                st.dataframe(df_avg_sorted, hide_index=True, width=240, height=300)

            with cur_rating_status_col:
                vega_lite_spec = {
                    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
                    "data": {"values": st.session_state['df_value'].to_dict(orient='records')},
                    "mark": "rect",
                    "width": 380,
                    "height": 320,
                    "encoding": {
                        "x": {"field": "group_number", "type": "nominal", "axis": {"labelAngle": 0}, "title": "그룹 번호"},
                        "y": {"field": "point", "type": "ordinal", "sort": "descending", "title": "점수",
                              "axis": {"titleAngle": 0}},
                        "color": {
                            "aggregate": "count",
                            "field": "point",
                            "title": ""
                        },
                    },
                    "config": {
                        "axis": {"grid": True, "tickBand": "extent"},
                        "title": {"fontSize": 18}
                    }
                }
                st.subheader('평가 점수 현황')
                st.vega_lite_chart(vega_lite_spec)

            student_vote_spec = {
                "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
                "data": {
                    "values": [{"student_id": s, "vote_count": v} for s, v in st.session_state['student_vote_counts']]},
                "mark": {"type": "bar", "color": "#4c78a8"},
                "width": 680,
                "height": 180,
                "encoding": {
                    "x": {"field": "student_id", "type": "nominal", "title": ""},
                    "y": {"field": "vote_count", "type": "quantitative", "title": "", "axis": {"titleAngle": 0}},
                },
                "config": {
                    "axis": {"grid": True, "tickBand": "extent"},
                    "title": {"fontSize": 18}
                }
            }
            st.subheader(f'평가 진행 현황 [{st.session_state['df_count']}/{max_vote}]')
            st.vega_lite_chart(student_vote_spec)

        time.sleep(1)
        st.empty()

def admin_menu(class_code):
    data_init_col, rating_simulation_col = st.columns((1, 1))
    with data_init_col:
        if st.button(f'{class_code} 클래스의 입력된 데이터 초기화'):
            delete_class_rating_data(class_code)
    with rating_simulation_col:
        if st.button(f"{class_code}클래스의 평가 입력 시뮬레이션"):
            data = generate_data_from_class(class_code)
            th1 = Thread(target=run_asyncio_simulation_data, args=(data, 3,))
            th1.start()
    st.divider()

def update_graph(class_code):
    ratings = get_rating_by_class(class_code)
    if ratings:
        df = pd.DataFrame(ratings)
        df['point'] = pd.to_numeric(df['point'], errors='coerce')
        df_value = df[['group_number', 'point', 'student_id']]
        df_avg = df_value.groupby('group_number').mean(numeric_only=True).reset_index()
        df_count = len(df_value)

        student_vote_counts = df_value['student_id'].value_counts().reset_index()
        student_vote_counts.columns = ['student_id', 'vote_count']
        student_vote_counts = list(student_vote_counts.itertuples(index=False, name=None))
    else:
        df_value = pd.DataFrame(columns=['group_number', 'point'])
        df_avg = pd.DataFrame(columns=['group_number', 'point'])
        df_count = 0
        student_vote_counts = []

    return df_value, df_avg, df_count, student_vote_counts
