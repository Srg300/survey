
# survey


# документация по API

Content-Type: application/json

**Создание вопросов**
Метод POST 
end point: `*/api/question/create/` 
доступен с 2 полями строковыми полями title и type_question варианты для type_question:

-   'string type'- ответ текстом,
-   'pick one' - ответ с выбором одного варианта
-   'pick many' - ответ с выбором нескольких вариантов

Пример:
```
{
    "title": "", 
    "type_question": "string type"
}
```

**Список всех вопросов**
метод GET 
end point: `*/api/questions/` 
Получаем список внутри которого все вопросы в словаре 
Пример:
```
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
```

**Редактирование, удаление, обновление вопроса по ID**
Метод GET, POST, PUT, PATCH, DELETE 
end point: `*/api/question/<int:question_id>/`
 Пример:
```
{
    "title": "Вопрос номер 1",
    "type_question": "string type"
}
```

**Доступ к списку опросников** 
Метод GET 
end point: `*/api/surveys/`
Пример:
```
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
```

**Редактирование, удаление, обновление опросника по ID**
метод GET, POST, PUT, PATCH, DELETE 
end point: `*api/survey/<int:surv_id>/` 

В методе GET мы получаем все поля. В поле questions у нас список вопросов, доступные по id
Пример: 
```
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
```

**Создание опросов**
Метод POST 
end point: `*api/survey/create/` 
Поле questions это список вопросов, в него требуется добавить id вопроса для заполнения 
Пример:
```
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
```

**Начало опроса**
Метод POST
end point `*/api/survey/start/<int:survey_id>/`
При переходе по ссылке end pointа создается опросник для получения ответов пользователя 

> UserAnswer

. 
Пример:


    {
    	"user_answer": {	
    		"id": 6,
    		"user_uuid": "90418cf7-fdbb-11ea-bd86-6c3be534b117",
    		"is_finished": false,
    		"survey": 1,
    		"answers": []
    	},    
    	"question": {
    		"title": "Вопрос номер 11",
    		"type_question": "string type"
    		}
    }
user_uuid - уникальный uuid для каждого опроса
answers - список для получения ответов от пользователя при прохождении опроса

Прохождение опроса:
Метод POST
end point: `*/api/answer/add/<slug:user_uuid>/`
При прохождении опроса, мы делаем POST запрос 
Пример:

    {    
        "question": 2,    
        "user_answer": "Ответ будет 2"    
    }
question -  id вопроса
user_answer - строковое поле, для ответа пользователя

При старте мы получим ответ от сервера:
Пример:

    {
        "user_answer": {
            "id": 7,
            "user_uuid": "1522195d-fdc1-11ea-8b4b-6c3be534b117",
            "is_finished": false,
            "survey": 1,
            "answers": [
                10,
                11
            ]
        },
        "question": {
            "id": 3,
            "title": "Вопрос 3. Выбиретие один из ответов. 1) A; 2) B; 3) C;",
            "type_question": "pick many"
        }
    }

В поле question мы получаем id следующего вопроса, таким образом, мы сможем отслеживать question id и использовать его
Если в опроснике не остается вопросов, то мы получим ответ:
Пример:

    {
        "finished": "Test is finished"
    }

Со статусом 200 OK
