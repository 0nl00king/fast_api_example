# FastAPI App
Библиотеки: 
    alembic,
    sqlalchemy,
    fastapi-users,
    fastapi-cache,
    celery,
    redis,
    jinja.

Технологии:
    аутентификация пользователей (fastapi-users),
    кэширование запросов (redis),
    отложенные задачи (celery + redis),
    тестирование (pytest).

Фронтенд:
    react.

## Инструкция
    
    `/HOST:PORT/docs` - просмотр доступных эндпоинтов.
    `/HOST:PORT/redoc` - просмотр доступных эндпоинтов.

    alembic init migrations (migrations - name of dirictory)
    alembic revision --autogenerate -m 'some msg'
    # Example: alembic revision --autogenerate -m 'DB creation'
    alembic upgrade head
    alembic downgrade 'SOME_HEAD'- хеш обновления

    Для накатывания миграций, если файла alembic.ini ещё нет, нужно запустить в терминале команду:
    
    alembic init migrations
    После этого будет создана папка с миграциями и конфигурационный файл для алембика.
    
    В alembic.ini нужно задать адрес базы данных, в которую будем катать миграции.
    Дальше идём в папку с миграциями и открываем env.py, там вносим изменения в блок, где написано
    from myapp import mymodel
    Дальше вводим: alembic revision --autogenerate -m "comment" - делается при любых изменениях моделей
    Будет создана миграция
    Дальше вводим: alembic upgrade heads