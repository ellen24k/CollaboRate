import asyncio
import random

import streamlit as st
from supabase import create_client
from supabase.lib.client_options import ClientOptions

_supabase_client = None

def get_supabase_client():
    global _supabase_client
    if _supabase_client is None:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_ANON_KEY"]
        opts = ClientOptions().replace(schema = "collaborate")
        _supabase_client = create_client(url, key, options=opts)
    return _supabase_client


def get_distinct_class_codes():
    try:
        response = get_supabase_client().rpc('get_distinct_class_codes').execute()
        return [item['class_code'] for item in response.data]
    except Exception as e:
        st.error(e)
        return None

def login_student(id, name, group, class_code):
    response = (
        get_supabase_client()
        .table('students')
        .select('*')
        .eq('student_id', id)
        .eq('class_code', class_code)
        .maybe_single()
        .execute()
    )
    if response:
        return response.data
    else:
        return None

def get_virtual_students():
    data = """
    그룹    이름      학번     
    1       김영원     33333333
    1       태영비     32227788
    1       영수환     32249588
    2       영영영     32248888
    2       김쿠영     32244645
    2       태태솔     32248459
    2       김진영     32243772
    2       태원영     32248979
    3       영빈영     32245358
    3       박영채     32247382
    3       김채영     32242814
    3       김희영     32244009
    4       태김연     32243742
    4       김영빈     32242093
    4       김영우     32243728
    4       태결영     32240008
    5       태얼얼     32241215
    5       영유성     32243042
    5       태영원     32249175
    5       김영영     32245742
    6       김시원     32240904
    6       김학영     32244930
    6       태김준     32244934
    7       김기영     32245241
    7       김영주     32243917
    11      영영민     32243751
    11      영정민     32240085
    11      박태성     32242636
    11      태랑영     32245562
    12      김김환     32249540
    12      태김김     32225235
    13      김준영     32246307
    13      김태우     32248250
    13      김김인     32245560
    13      김용영     32244498
    14      태방영     32249607
    14      김우영     32245459
    14      태영주     32227963
"""
    return data


def get_rating_points(class_code, student_id):
    try:
        response = get_supabase_client().rpc(
            'get_rating_points',
            {'p_class_code': class_code, 'p_student_id': student_id}
        ).execute()
        return response.data
    except Exception as e:
        st.error(e)
        return None

def insert_rating_point(group_number, student_id, point, class_code):
    try:
        response = (
            get_supabase_client()
            .table('rating')
            .insert({
                'class_code': str(class_code),
                'group_number': int(group_number),
                'student_id': str(student_id),
                'point':int(point)
            })
            .execute()
        )
        return response
    except Exception as e:
        st.error(e)
        return None

def get_project_infos(class_code):
    try:
        response = get_supabase_client().rpc(
            'get_project_infos',
            {'p_class_code': class_code}
        ).execute()
        return response.data
    except Exception as e:
        st.error(e)
        return None

def update_rating_point(group_number, student_id, point, class_code):
    try:
        get_supabase_client().rpc(
            'update_rating_point',
            {
                'p_group_number': group_number,
                'p_student_id': student_id,
                'p_class_code': class_code,
                'p_point': point
            }
        ).execute()
    except Exception as e:
        st.error(e)

def get_students_by_class(class_code):
    try:
        response = get_supabase_client().rpc(
            'get_students_by_class',
            {'p_class_code': class_code}
        ).execute()
        return response.data
    except Exception as e:
        st.error(e)
        return None


def get_distinct_group_numbers(class_code):
    try:
        response = get_supabase_client().rpc(
            'get_distinct_group_numbers',
            {'p_class_code': class_code}
        ).execute()
        return [item['group_number'] for item in response.data]
    except Exception as e:
        st.error(e)
        return None

def generate_data(group_numbers, student_ids, class_code):
    data = []

    for student_id in student_ids:
        for group_number in group_numbers:
            point = random.randint(1, 10)
            data.append((group_number, point, student_id, class_code))
    random.shuffle(data)

    return data

def generate_data_from_class(class_code):
    students = get_students_by_class(class_code)
    student_ids = [item['student_id'] for item in students]
    group_numbers = get_distinct_group_numbers(class_code)
    data = generate_data(group_numbers, student_ids, class_code)
    return data

def get_rating_by_class(class_code):
    try:
        response = get_supabase_client().rpc(
            'get_rating_by_class',
            {'p_class_code': class_code}
        ).execute()
        return response.data
    except Exception as e:
        st.error(e)
        return None

def delete_class_rating_data(class_code):
    try:
        (get_supabase_client().table('rating')
         .delete()
         .eq('class_code', class_code)
         .neq('student_id', 0)
         .execute())
    except Exception as e:
        st.error(e)


async def insert_simulation_data(data):
    for record in data:
        (get_supabase_client()
        .table('rating')
        .insert({
            'group_number': record[0],
            'point': record[1],
            'student_id': record[2],
            'class_code': record[3]
        }).execute())
        await asyncio.sleep(random.uniform(0.05, 0.1))


async def insert_simulation_data_limit(data, once_limit):
    try:
        for i in range(0, len(data), once_limit):
            batch = data[i: i + once_limit]
            (get_supabase_client()
             .table('rating')
             .insert([{
                'group_number': record[0],
                'point': record[1],
                'student_id': record[2],
                'class_code': record[3]
             } for record in batch])
            .execute())
            await asyncio.sleep(random.uniform(0.1,0.2))
    except Exception as e:
        st.error(e)


async def insert_simulation_data_once(data):
    try:
        (get_supabase_client()
         .table('rating')
         .insert([{
            'group_number': record[0],
            'point': record[1],
            'student_id': record[2],
            'class_code': record[3]
        } for record in data])
        .execute())
    except Exception as e:
        st.error(e)

def run_asyncio_simulation_data(data, once_limit=3):
    if once_limit == 1:
        asyncio.run(insert_simulation_data(data))
    elif once_limit > 1:
        asyncio.run(insert_simulation_data_limit(data, once_limit))
    else:
        asyncio.run(insert_simulation_data_once(data))
