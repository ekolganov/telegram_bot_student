create table student(
    id integer primary key,
    full_name varchar(255),
    grade_number varchar(255),
    description text,

    FOREIGN KEY(grade_number) REFERENCES themes(themes_grade_number)
);

create table themes(
    id integer primary key,
    themes_grade_number varchar(255),
    theme_name text
);

create table code_status(
    id integer primary key,
    status_name varchar(255)
);

insert into student(full_name, grade_number, description) values
    ("Петров Евгений", "6 класс", "не очень прилежный"),
    ("Пупкин Василий", "6 класс", "прилежный"),
    ("Герасимов Гена", "7 класс", "отличнег");

insert into themes(themes_grade_number, theme_name) values
    ("6 класс","Глагол. Контрольная работа с грамматическим заданием"),
    ("6 класс","Глагол. Правописание суффиксов глаголов -ОВА- (-ЕВА-), -ЫВА- (-ИВА-)"),
    ("7 класс","Наречие. Суффиксы О и А на конце наречий"),
    ("7 класс","Причастие. Гласные в суффиксах причастий");

insert into code_status(status_name) values
    ("undefined"),
    ("learned"),
    ("not learned");
