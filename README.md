# Cookbook API

Асинхронный REST API кулинарной книги на FastAPI + SQLAlchemy (async).

## Функциональность
- GET /recipes — список рецептов, отсортированный по популярности
- GET /recipes/{id} — детальная информация с атомарным счётчиком просмотров
- POST /recipes — создание нового рецепта

## CI/CD
Пайплайн на GitHub Actions запускает isort, black, flake8, mypy и pytest на каждый push и pull request.

## Запуск локально
\`\`\`
pip install -r requirements.txt -r requirements-dev.txt
uvicorn main:app --reload
\`\`\`
