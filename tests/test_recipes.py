import pytest


@pytest.mark.asyncio
async def test_create_recipe(async_client):
    """Создание рецепта: проверяем код 201 и что views выставлен в 0."""
    response = await async_client.post(
        "/recipes",
        json={
            "title": "Борщ",
            "cooking_time": 60,
            "ingredients": "свекла, капуста, мясо",
            "description": "Классический борщ",
        },
    )
    data = response.json()

    assert response.status_code == 201
    assert data["id"] is not None
    assert data["title"] == "Борщ"
    assert data["views"] == 0


@pytest.mark.asyncio
async def test_get_recipe_detail_increments_views(async_client):
    """Каждое открытие детальной страницы должно атомарно увеличивать views."""
    create_response = await async_client.post(
        "/recipes",
        json={
            "title": "Омлет",
            "cooking_time": 10,
            "ingredients": "яйца, молоко",
            "description": "Быстрый завтрак",
        },
    )
    recipe_id = create_response.json()["id"]

    first = await async_client.get(f"/recipes/{recipe_id}")
    assert first.status_code == 200
    assert first.json()["views"] == 1

    second = await async_client.get(f"/recipes/{recipe_id}")
    assert second.status_code == 200
    assert second.json()["views"] == 2


@pytest.mark.asyncio
async def test_get_recipe_detail_not_found(async_client):
    """Запрос несуществующего рецепта должен возвращать 404."""
    response = await async_client.get("/recipes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


@pytest.mark.asyncio
async def test_get_recipes_sorted_by_views_then_cooking_time(async_client):
    """Список рецептов сортируется по views (убыв.), при равенстве — по cooking_time (возр.)."""
    await async_client.post(
        "/recipes",
        json={
            "title": "Быстрый рецепт",
            "cooking_time": 5,
            "ingredients": "вода",
            "description": "Просто вода",
        },
    )
    slow_response = await async_client.post(
        "/recipes",
        json={
            "title": "Долгий рецепт",
            "cooking_time": 120,
            "ingredients": "мясо",
            "description": "Долго готовим",
        },
    )
    slow_id = slow_response.json()["id"]

    await async_client.get(f"/recipes/{slow_id}")

    response = await async_client.get("/recipes")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] == "Долгий рецепт"
    assert data[0]["views"] == 1
    assert data[1]["title"] == "Быстрый рецепт"
    assert data[1]["views"] == 0


@pytest.mark.asyncio
async def test_get_recipes_empty_list(async_client):
    """Если рецептов нет, список должен быть пустым, но код ответа 200."""
    response = await async_client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == []
    
