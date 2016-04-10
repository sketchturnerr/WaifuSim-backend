# WaifuSim-backend
## Как развернуть
`docker-compose up -d` - запуск в демон-режиме.

`docker-compose -f docker-compose-testing.yml up` - запустить тесты.
Если поменялась структура базы, то перед этим нужно удалить контейнеры `docker-compose -f docker-compose-testing.yml rm -f` потом придумаю, как без этого обойтись.
## Api
### [Формат ошибок](#errors-format)
`{"title": <код ошибки>, "description": <человекопонятное описание>, "link": <ссылка на эту документацию>}`
### [Users](#users)
`POST:/users` - cоздаст пользователя, в ответ вернет `{"token": <token>}`, его нужно сохранить на устройстве и спользоватьзовать для всех остальных запросав к api, см. [тут](#auth).

`POST:/users?cookies=1` - не только создаст, но и сразу поставит авторизационную куку (актуально для web-клиента).
### [Auth](#auth)
Запросы к api должны либо соделжать query-пареметр `token=<token>`, либо иметь аналогичную куку.
`POST:/users/auth` - автоирзует пользователя и поставит авторизационную куку.
Ошибки:
* `401` - токен не передан или некорректен.
* `404` - обращение к ресурсу на который на хватет прав.
