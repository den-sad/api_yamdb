# api_yamdb
## **Описание проекта api_yamdb**

Проект предназначен для сбора отзывов и оценок пользователей на различные произведения.
Зарегистрированным пользователям предоставляется возможность публикации постов и комментариев к ним. 
Проект автоматически рассчитывает рейтинг произведения на основе оценок, выставленных 
пользователями.
Всем пользователям доступно чтение отзывов и комментариев в ним.
Проект представляет доступ к своей функциональности через API, что расширяет применение проекта как для десктопных так и для мобильных приложений.


## **Как запустить проект:**
### 1. Клонировать репозиторий и перейти в него в командной строке:

```
    git clone 'git@github.com:den-sad/api_yamdb.git'
    cd api_yamdb
```

### 2. Cоздать и активировать виртуальное окружение:

```
    python -m venv venv
    source venv/bin/activate
```

### 3. Установить зависимости из файла requirements.txt:

```
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

### 4. Выполнить миграции:

```
    python manage.py migrate
```

### 5. Запустить проект:

```
    python manage.py runserver
```

## **Примеры запросов к API:**

**GET _http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/_**

**Пример ответа: _200 (или 404)_**
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

**POST _http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/_**
```
{
  "text": "string",
  "score": 1
}
```
**Пример ответа: _200 (или 400, 401, 404)_**
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

**GET _http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/_**

**Пример ответа: _200 (или 404)_**
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

**PATCH _http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/_**
```
{
  "text": "string",
  "score": 1
}
```
**Пример ответа: _200 (или 400, 401, 403, 404)_**
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

**DELETE _http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/_**

**Пример ответа: _204 (или 401, 403, 404)_**


**GET _http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/_**

**Пример ответа: _200 (или 404)_**
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

**POST _http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/_**
```
{
  "text": "string"
}
```
**Пример ответа: _201 (или 400, 401, 404)_**
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

**GET _http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/_**

**Пример ответа: _200 (или 404)_**
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

**PATCH _http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/_**
```
{
  "text": "string"
}
```
**Пример ответа: _200 (или 400, 401, 403, 404)_**
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```

**DELETE _http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/_**

**Пример ответа: _204 (или 401, 403, 404)_**
