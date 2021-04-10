create table student(
    id integer primary key,
    full_name varchar(255),
    grade_number varchar(255),
    description text
);

insert into student(id, full_name, grade_number, description) values
(1, "Петров Евгений", "6 класс", "не очень прилежный"),
(2, "Пупкин Василий", "6 класс", "прилежный"),
(3, "Герасимов Гена", "7 класс", "отличнег");

create table themes(
    id integer primary key,
    themes_grade_number varchar(255),
    theme_name text,

    FOREIGN KEY(themes_grade_number) REFERENCES student(grade_number)
);

insert into themes(id, themes_grade_number, theme_name) values
(1,"6 класс","Глагол. Контрольная работа с грамматическим заданием"),
(2,"6 класс","Глагол. Правописание суффиксов глаголов -ОВА- (-ЕВА-), -ЫВА- (-ИВА-)"),
(3,"7 класс","Наречие. Суффиксы О и А на конце наречий"),
(4,"7 класс","Причастие. Гласные в суффиксах причастий");


create table marks(
    theme text primary key,
    student_id integer,
    theme_status integer

    FOREIGN KEY(theme) REFERENCES themes(theme_name)
    FOREIGN KEY(student_id) REFERENCES student(id)
    FOREIGN KEY(theme_status) REFERENCES code_status(id)
)

create table code_status(
    id integer primary key,
    status_name varchar(255)
)

insert into code_status(id, status_name) values
    (1, "undefined"),
    (2, "learned"),
    (3, "not learned");
