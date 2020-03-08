
/*
Создаем представление, которое содержит пользователей - только учителей ('tutor')  
*/
create view tutor as
select id
FROM    users
WHERE  role = 'tutor'

/* 
1) Отбираем на основании таблицы users, пользователя учитель(tutor)-id
2) На основании этого из таблицы выбираем event_id
3) На основании этого выбираем уроки(lessons.id) из таблицы lessons, только
предмет - 'phys'
4) Сохраняем результат во временной таблице - #MyTempTable
*/
select lessons.id, participants.user_id, lessons.scheduled_time
into #MyTempTable 
from tutor, participants, lessons
where tutor.id = participants.user_id and lessons.event_id = participants.event_id
and lessons.subject = 'phys'



/*
Находим среднюю арифметическую оценку из временой таблицы - #MyTempTable(где
у нас есть уроки, учитель и дата) и таблицы quality для каждой даты и
учителя
*/
select FORMAT(#MyTempTable.scheduled_time,'yyyy-dd-MM') as date, #MyTempTable.user_id as user_id , round(avg(quality.tech_quality), 2) as Srd_quality
into #MyTempTable2
from quality, #MyTempTable
where quality.lesson_id = #MyTempTable.id
group by FORMAT(#MyTempTable.scheduled_time,'yyyy-dd-MM'), #MyTempTable.user_id
order by FORMAT(#MyTempTable.scheduled_time,'yyyy-dd-MM'), #MyTempTable.user_id


/*
Находим наименьшше значение ср. арифметической из всех учителей 
каждого дня
*/
select date, user_id, min(srd_quality)
from #MyTempTable2
group by date, user_id 
order by date, user_id 




