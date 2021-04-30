create table student(
    id integer primary key,
    full_name varchar(255),
    grade_number varchar(255),
    description text,
);

create table themes(
    id integer primary key,
    themes_grade_number varchar(255),
    theme_name text
);


insert into student(full_name, grade_number, description) values
    ('Петров Евгений', '6 класс', 'не очень прилежный'),
    ('Вася Пупкин Сергеевич', '8 класс', 'оболтус'),
    ('Егор Петров', '9 класс', 'серьёзный'),
    ('Женя Валерий', '6 класс', 'трудолюбивый'),
    ('Женя Валерий', '6 класс', ''),
    ('Леша Васильев', '7 класс', '');

insert into themes(themes_grade_number, theme_name) values
    ('6 класс', 'Глагол. Контрольная работа с грамматическим заданием'),
    ('6 класс', 'Глагол. Правописание суффиксов глаголов -ОВА- (-ЕВА-), -ЫВА- (-ИВА-)'),
    ('7 класс', 'Наречие. Суффиксы О и А на конце наречий'),
    ('7 класс', 'Причастие. Гласные в суффиксах причастий'),
    ('8 класс', 'Деепричастия');
