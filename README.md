# survey
# инструкция по разворачиванию приложения
Создаем виртуальное окружение с именем: venv_survey
Устанавливаем необходимые библиотеки командой: pip install -r requirements.txt
Скачиваем проект в ту же директорию, что и папка venv_survey командой: git clone https://github.com/Srg300/survey.git
Проект работает на БД SQLite. Для запуска требуется скопировать файл db.sqlite3 в директорию surveyproject/ рядом с файлом manage.py
Создать миграции python manage.py makemigrations
Сделать миграции python manage.py migrate 
Создать суперюзера: python manage.py createsuperuser <username>



# документация по API
Content-Type: application/json

Создание вопросов:
метод POST
end point: `*/api/question/create/`
доступен с 2 полями строковоми полями title и type_question
варианты для type_question: 

 - 'string type'- ответ текстом, 
 - 'pick one' - ответ с выбором одного варианта  
 - 'pick many' - ответ с выбором нескольких вариантов

Пример:

    {
        "title": "", 
        "type_question": "string type"
    }

Список всех вопросов:
метод GET
end point: `*/api/questions/`
Получаем список внутри которого все вопросы в словаре
Пример:

    [
        {
            "title": "Вопрос номер 1",
            "type_question": "string type"
        },
      ...
        {
            "title": "Вопрос номер 2",
            "type_question": "string type"
        }
    ]

Редактирование, удаление, обновление вопроса по ID:
метод GET, POST, PUT, PATCH, DELETE
end point: `*/api/question/<int:question_id>/`
Пример:

    {
        "title": "Вопрос номер 1",
        "type_question": "string type"
    }

Доступ к списку опросников
метод GET
end point:  `*/api/surveys/`
Пример:

    [
        {
            "id": 1,
            "title": "Опросник 1",
            "discription": "для тестирования",
            "is_active": true,
            "start_date": "23.09.2020 05:51",
            "end_date": "23.09.2020 12:40",
            "questions": [
                {
                    "id": 1,
                    "title": "Вопрос номер 1",
                    "type_question": "string type"
                },
                {
                    "id": 2,
                    "title": "Вопрос номер 2",
                    "type_question": "pick one"
                },
                {
                    "id": 3,
                    "title": "Вопрос 3. Выбиретие один из ответов. 1) A; 2) B; 3) C;",
                    "type_question": "pick many"
                }
            ]
        },
        ...
    ]

Редактирование, удаление, обновление опросника по ID:
метод GET, POST, PUT, PATCH, DELETE
end point: `*api/survey/<int:surv_id>/`
Пример:
Метод GET
В методе GET мы получаем все поля. В поле questions у нас список вопросов, доступные по id

    {
        "id": 1,
        "title": "Опросник 1",
        "discription": "для тестирования",
        "is_active": true,
        "start_date": "23.09.2020 05:51",
        "end_date": "23.09.2020 12:40",
        "questions": [
            1,
            2,
            3
        ]
    }


Создание постов
Метод POST
end point: `*api/survey/create/`
Поле questions это список вопросов, в него требуется добавить id вопроса для заполнения
Пример:

    {
        "id": 1,
        "title": "Опросник 1",
        "discription": "для тестирования",
        "is_active": true,
        "end_date": "23.09.2020 12:40",   - создаются автоматически
        "questions": [
            1,
            2,
            3
        ]
    }

