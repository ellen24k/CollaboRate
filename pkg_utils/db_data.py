import asyncio
import random

import psycopg2
import streamlit as st
from psycopg2.extras import DictCursor

conn = None

def get_supabase_client():
    global conn
    if conn is None:
        PG_HOST = st.secrets['PG_HOST']
        PG_DBNAME = st.secrets["PG_DBNAME"]
        PG_USER = st.secrets["PG_USER"]
        PG_PASSWORD = st.secrets["PG_PASSWORD"]
        PG_PORT = st.secrets["PG_PORT"]
        try:
            conn = psycopg2.connect(host = PG_HOST, dbname = PG_DBNAME, user = PG_USER, password = PG_PASSWORD, port = PG_PORT)
        except:
            print("db conn failed")
            return None
    return conn


def get_distinct_class_codes():
    try:
        conn = get_supabase_client()
        with conn.cursor() as cursor:
            cursor.execute("SELECT DISTINCT class_code FROM students as s ORDER BY class_code;")
            return [class_code[0] for class_code in cursor.fetchall()]
    except Exception as e:
        st.error(e)
        return None

def login_student(id, name, group, class_code):
    try:
        conn = get_supabase_client()
        with conn.cursor() as cursor:
            cursor.execute(f'select * from students where student_id = \'{id}\' and class_code = \'{class_code}\' limit 1;')
            response = cursor.fetchone()
            parsed_response = {'student_id': response[0], 'class_code': response[1], 'group_number' : response[2], 'name' : response[3], 'department' : response[4], 'college' : response[5]}
            return parsed_response if parsed_response else None
    except Exception as e:
        st.error(f'login_student: {e}')
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


async def get_rating_points(class_code, student_id):
    try:
        conn = get_supabase_client()
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute('select get_rating_points(%s, %s);', (student_id, class_code))
            response = cursor.fetchall()
        parsed_response = []
        for item in response:
            group_number, point = map(int, item[0][1:-1].split(','))
            parsed_response.append({ 'group_number': group_number, 'point': point })
        return parsed_response
    except Exception as e:
        st.error(e)
        return None

def insert_rating_point(group_number, student_id, point, class_code): #todo check 이미 값이 다 들어가있어서 체크 패스
    try:
        conn = get_supabase_client()
        with conn.cursor() as cursor:
            cursor.execute('insert into rating (class_code, group_number, student_id, point) values (%s, %s, %s, %s);', (class_code, group_number, student_id, point))
            return True
    except Exception as e:
        st.error(e)
        return False


async def get_project_infos(class_code):
    try:
        conn = get_supabase_client()
        with conn.cursor() as cursor:
            cursor.execute('SELECT  g.group_number, g.group_name, g.project_name, g.project_desc \
            FROM group_info as g \
            WHERE g.class_code = (%s);', (class_code,))
            responses = cursor.fetchall()
            # print(responses)
        parsed_responses = []
        for item in responses:
            parsed_responses.append({ 'group_number': item[0], 'team_name': item[1], 'project_name': item[2], 'project_desc': item[3]})
        return parsed_responses
    except Exception as e:
        st.error(e)
        return None

def update_rating_point(group_number, student_id, point, class_code):
    try:
        conn = get_supabase_client()
        with conn.cursor() as cursor:
            cursor.execute(f'UPDATE rating as r \
            SET point = {point} \
            WHERE r.group_number = {group_number} \
            AND r.student_id = \'{student_id}\' \
            AND r.class_code = \'{class_code}\';')
    except Exception as e:
        st.error(e)

async def get_students_by_class(class_code):
    try:
        conn = get_supabase_client()
        with conn.cursor() as cursor:
            cursor.execute(f'select get_students_by_class(\'{class_code}\')')
            response = cursor.fetchall()
        # print(response)
        parsed_response = []
        for item in response:
            student_id, name, group_number, college, major, class_code = item[0][1:-1].split(',')
            parsed_response.append({ 'student_id': student_id.strip(), 'name': name.strip(), 'group_number': int(group_number.strip()), 'college': college.strip(), 'major': major.strip(), 'class_code': class_code.strip() })
        return parsed_response
    except Exception as e:
        # print('err',e)
        st.error(e)
        return None


def get_distinct_group_numbers(class_code):
    try:
        conn = get_supabase_client()
        with conn.cursor() as cursor:
            cursor.execute(f'select get_distinct_group_numbers(\'{class_code}\')')
            response = cursor.fetchall()
        # print(response)
        return [item[0] for item in response]
    except Exception as e:
        # print(e)
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
    students = asyncio.run(get_students_by_class(class_code))
    student_ids = [item['student_id'] for item in students]
    group_numbers = get_distinct_group_numbers(class_code)
    data = generate_data(group_numbers, student_ids, class_code)
    return data

def get_rating_by_class(class_code):
    try:
        conn = get_supabase_client()
        with conn.cursor() as cursor:
            cursor.execute(f'select get_rating_by_class(\'{class_code}\')')
            response = cursor.fetchall()
            # print(response)
        parsed_response = []
        for item in response:
            group_number, student_id, class_code, point = item[0][1:-1].split(',')
            parsed_response.append({'group_number': int(group_number), 'student_id': student_id, 'class_code': class_code, 'point': int(point)})
        return parsed_response
    except Exception as e:
        # print('err: ',e)
        st.error(e)
        return None

def delete_class_rating_data(class_code):
    try:
        conn = get_supabase_client()
        with conn.cursor() as cursor:
            cursor.execute(f'delete from rating where class_code = \'{class_code}\' and student_id <> \'{0}\'')
    except Exception as e:
        st.error(e)


async def insert_simulation_data(data): # todo check
    try:
        conn = get_supabase_client()
        with conn.cursor() as cursor:
            for record in data:
                cursor.execute(f'insert into rating (group_number, point, student_id, class_code) values (\'{record[0]}\', \'{record[1]}\', \'{record[2]}\', \'{record[3]}\');')
                await asyncio.sleep(random.uniform(0.05, 0.1))
    except Exception as e:
        st.error(e)
        # print('err: ',e)


async def insert_simulation_data_limit(data, once_limit):
    try:
        conn = get_supabase_client()
        with conn.cursor() as cursor:
            for i in range(0, len(data), once_limit):
                batch = data[i: i + once_limit]
                for record in batch:
                    cursor.execute(f'insert into rating (group_number, point, student_id, class_code) values (\'{record[0]}\', \'{record[1]}\', \'{record[2]}\', \'{record[3]}\');')
                    conn.commit()
                await asyncio.sleep(random.uniform(0.1,0.2))
    except Exception as e:
        # print('err: ', e)
        st.error(e)

async def insert_simulation_data_once(data):
    try:
        conn = get_supabase_client()
        with conn.cursor() as cursor:
            for record in data:
                cursor.execute(f'insert into rating (group_number, point, student_id, class_code) values (\'{record[0]}\', \'{record[1]}\', \'{record[2]}\', \'{record[3]}\');')
                conn.commit()
                await asyncio.sleep(random.uniform(0.1,0.2))
    except Exception as e:
        # print('err: ', e)
        st.error(e)

def run_asyncio_simulation_data(data, once_limit=3):
    if once_limit == 1:
        asyncio.run(insert_simulation_data(data))
    elif once_limit > 1:
        asyncio.run(insert_simulation_data_limit(data, once_limit))
    else:
        asyncio.run(insert_simulation_data_once(data))

def run_asyncio_get(class_code, student_id):
    return asyncio.run(get_students_by_class(class_code)), asyncio.run(get_rating_points(class_code, student_id)), asyncio.run(get_project_infos(class_code))
