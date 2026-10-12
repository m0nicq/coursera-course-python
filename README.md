# Финальный проект: онлайн-курс Django

Реализованы семь моделей (Instructor, Learner, Course, Lesson, Question, Choice, Submission), административный сайт с вложенными вопросами и ответами, уроки и экзамен. Полный набор правильных ответов даёт баллы за вопрос; лишний или пропущенный ответ даёт 0. Проходной результат — не менее 70%. Попытки сохраняются, результаты доступны только их владельцу.

## Запуск

Нужны Python 3.12+ и доступ к PyPI. Bootstrap загружается с CDN.

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
export DEMO_ADMIN_PASSWORD='choose-a-strong-password'
python manage.py seed_demo
python manage.py test
python manage.py runserver
```

Откройте http://127.0.0.1:8000/ и войдите как `demo` с выбранным паролем. Команда seed_demo создаёт администратора только при первом запуске и не меняет пароль существующего пользователя.

## Материалы для сдачи

Загрузите проект в собственный репозиторий GitHub. Замените OWNER, REPO и BRANCH в адресах ниже своими значениями. Это шаблоны адресов, а не опубликованные ссылки.

| Задание | Файл / адрес |
| --- | --- |
| 1 | `https://github.com/OWNER/REPO/blob/BRANCH/onlinecourse/models.py` |
| 2 | `https://github.com/OWNER/REPO/blob/BRANCH/onlinecourse/admin.py` |
| 3 | `screenshots/03-admin-site.png` |
| 4 | `https://github.com/OWNER/REPO/blob/BRANCH/onlinecourse/templates/onlinecourse/course_details_bootstrap.html` |
| 5 | `https://github.com/OWNER/REPO/blob/BRANCH/onlinecourse/views.py` |
| 6 | `https://github.com/OWNER/REPO/blob/BRANCH/onlinecourse/urls.py` |
| 7 | `screenshots/07-final.png` |

Для 03-admin-site войдите в http://127.0.0.1:8000/admin/ и сделайте скриншот главной страницы: на ней должны быть видны «Аутентификация и авторизация» и «Онлайн-курс».

Для 07-final откройте курс, выберите ForeignKey, csrf_token и for, POST. Нажмите «Отправить ответы». Сделайте скриншот страницы с «Поздравляем», оценкой 100% (15 из 15 баллов) и результатами всех вопросов. Сохраните реальные скриншоты с указанными именами в screenshots/.

## Проверка в текущей среде

Синтаксис Python проверен. Установка Django недоступна из-за отсутствия сетевого доступа к PyPI, поэтому Django-тесты не запускались, миграция добавлена, но не применена; скриншоты ещё не созданы. Репозиторий GitHub ещё не опубликован.

Перед публичным развёртыванием установите DJANGO_SECRET_KEY, DJANGO_DEBUG=0 и DJANGO_ALLOWED_HOSTS; демонстрационный сервер предназначен для локального запуска.
