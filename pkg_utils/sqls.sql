--tables

create table collaborate.group_info
(
    group_name   varchar,
    project_name varchar,
    group_number integer not null,
    class_code   varchar not null,
    project_desc varchar,
    constraint pk_group_info
        primary key (group_number, class_code)
);

alter table collaborate.group_info
    owner to postgres;

grant delete, insert, select, update on collaborate.group_info to anon;

--
create table collaborate.rating
(
    group_number integer not null,
    point        integer,
    student_id   varchar not null,
    class_code   varchar not null,
    constraint pk_rating
        primary key (group_number, student_id, class_code)
);

alter table collaborate.rating
    owner to postgres;

grant delete, insert, select, update on collaborate.rating to anon;

--
create table collaborate.students
(
    student_id   varchar not null,
    class_code   varchar not null,
    group_number integer not null,
    name         varchar,
    department   varchar,
    college      varchar,
    constraint pk_students
        primary key (student_id, class_code)
);

alter table collaborate.students
    owner to postgres;

grant delete, insert, select, update on collaborate.students to anon;


--routines

create function collaborate.get_distinct_group_numbers(p_class_code character varying)
    returns TABLE(group_number integer)
    language plpgsql
as
$$
BEGIN
RETURN QUERY
SELECT DISTINCT students.group_number
FROM collaborate.students
WHERE class_code = p_class_code
ORDER BY students.group_number;
END;
$$;

alter function collaborate.get_distinct_group_numbers(varchar) owner to postgres;

create function collaborate.get_distinct_class_codes()
    returns TABLE(class_code character varying)
    language plpgsql
as
$$
BEGIN
RETURN QUERY
SELECT DISTINCT s.class_code
FROM collaborate.students as s
ORDER BY s.class_code;
END;
$$;

alter function collaborate.get_distinct_class_codes() owner to postgres;

create function collaborate.get_students_by_class(p_class_code character varying)
    returns TABLE(student_id character varying, name character varying, group_number integer, college character varying, department character varying, class_code character varying)
    language plpgsql
as
$$
BEGIN
RETURN QUERY
SELECT s.student_id,
       s.name,
       s.group_number,
       s.college,
       s.department,
       s.class_code
FROM collaborate.students as s
WHERE s.class_code = p_class_code;
END;
$$;

alter function collaborate.get_students_by_class(varchar) owner to postgres;

create function collaborate.get_project_infos(p_class_code character varying)
    returns TABLE(group_number integer, team_name character varying, project_name character varying, project_desc character varying)
    language plpgsql
as
$$
BEGIN
RETURN QUERY
SELECT  g.group_number, g.group_name, g.project_name, g.project_desc
FROM group_info as g
WHERE g.class_code = p_class_code;
END;
$$;

alter function collaborate.get_project_infos(varchar) owner to postgres;

create function collaborate.get_rating_points(p_student_id character varying, p_class_code character varying)
    returns TABLE(group_number integer, point integer)
    language plpgsql
as
$$
BEGIN
RETURN QUERY
SELECT r.group_number, r.point
FROM rating r
WHERE r.student_id = p_student_id
  AND r.class_code = p_class_code;
END;
$$;

alter function collaborate.get_rating_points(varchar, varchar) owner to postgres;

create function collaborate.update_rating_point(p_group_number integer, p_student_id character varying, p_class_code character varying, p_point integer) returns void
    language plpgsql
as
$$
BEGIN
UPDATE rating as r
SET point = p_point
WHERE r.group_number = p_group_number
  AND r.student_id = p_student_id
  AND r.class_code = p_class_code;
END;
$$;

alter function collaborate.update_rating_point(integer, varchar, varchar, integer) owner to postgres;

create function collaborate.get_rating_by_class(p_class_code character varying)
    returns TABLE(group_number integer, student_id character varying, class_code character varying, point integer)
    language plpgsql
as
$$
BEGIN
RETURN QUERY
SELECT r.group_number, r.student_id, r.class_code, r.point
FROM rating r
WHERE r.class_code = p_class_code;
END;
$$;

alter function collaborate.get_rating_by_class(varchar) owner to postgres;


-- cache
create extension pg_prewarm;
select pg_prewarm('group_info');
select pg_prewarm('rating');
select pg_prewarm('students');

select relname, heap_blks_read, heap_blks_hit
from pg_statio_user_tables
where relname in ('rating', 'students', 'group_info')

-- select collaborate.get_distinct_group_numbers('DKU001')

-- sample data
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '사이버보안학과', '32245241', '김기영', 7, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '사이버보안학과', '32244498', '김용영', 13, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32246307', '김준영', 13, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32245562', '태랑영', 11, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32247382', '박영채', 3, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32249607', '태방영', 14, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32249588', '영수환', 1, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '사이버보안학과', '32249844', '김영원', 1, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32227788', '태영비', 1, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32242636', '박태성', 11, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32225235', '태김김', 12, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32244645', '김쿠영', 2, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32241215', '태얼얼', 5, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32242093', '김영빈', 4, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32243728', '김영우', 4, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '사이버보안학과', '32227963', '태영주', 14, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32243742', '태김연', 4, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '사이버보안학과', '32243917', '김영주', 7, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '사이버보안학과', '32240904', '김시원', 6, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32244934', '태김준', 6, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32243042', '영유성', 5, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32249175', '태영원', 5, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32248459', '태태솔', 2, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '사이버보안학과', '32248250', '김태우', 13, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32245560', '김김인', 13, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '사이버보안학과', '32249540', '김김환', 12, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32244930', '김학영', 6, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32245742', '김영영', 5, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32240008', '태결영', 4, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32242814', '김채영', 3, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32244009', '김희영', 3, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32245358', '영빈영', 3, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32243772', '김진영', 2, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32248979', '태원영', 2, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '사이버보안학과', '32245459', '김우영', 14, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '사이버보안학과', '32240085', '영정민', 11, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32243751', '영영민', 11, 'VIRTUAL');
INSERT INTO collaborate.students (college, department, student_id, name, group_number, class_code) VALUES ('SW융합대학', '소프트웨어학과', '32248888', '영영영', 2, 'VIRTUAL');
