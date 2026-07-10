from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from database import get_db

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.get(
    "",
    response_model=List[schemas.RecipeListItem],
    summary="Получить список всех рецептов",
    description=(
        "Возвращает список всех рецептов, отсортированных по убыванию "
        "количества просмотров (views). При равном количестве просмотров "
        "рецепты сортируются по возрастанию времени приготовления (cooking_time)."
    ),
)
async def get_recipes(db: AsyncSession = Depends(get_db)):
    """Список рецептов для главного экрана (название, просмотры, время готовки)."""
    result = await db.execute(
        select(models.Recipe).order_by(
            models.Recipe.views.desc(), models.Recipe.cooking_time.asc()
        )
    )
    recipes = result.scalars().all()
    return recipes


@router.get(
    "/{recipe_id}",
    response_model=schemas.RecipeDetail,
    summary="Получить детальную информацию о рецепте",
    description=(
        "Возвращает детальную информацию о рецепте по его id: название, "
        "время приготовления, список ингредиентов и описание. "
        "При каждом обращении счётчик просмотров (views) атомарно "
        "увеличивается на 1 средствами SQL (UPDATE ... SET views = views + 1), "
        "что исключает потерю обновлений при параллельных запросах (race condition)."
    ),
    responses={404: {"description": "Рецепт не найден"}},
)
async def get_recipe_detail(recipe_id: int, db: AsyncSession = Depends(get_db)):
    """Детальная информация о рецепте с атомарным увеличением счётчика просмотров."""
    result = await db.execute(
        select(models.Recipe).where(models.Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    await db.execute(
        update(models.Recipe)
        .where(models.Recipe.id == recipe_id)
        .values(views=models.Recipe.views + 1)
    )
    await db.commit()
    await db.refresh(recipe)
    return recipe


@router.post(
    "",
    response_model=schemas.RecipeDetail,
    status_code=201,
    summary="Создать новый рецепт",
    description=(
        "Создаёт новый рецепт в базе данных. Поле views выставляется "
        "автоматически в 0 и не передаётся клиентом."
    ),
)
async def create_recipe(recipe: schemas.RecipeCreate, db: AsyncSession = Depends(get_db)):
    """Создание нового рецепта. Счётчик просмотров всегда начинается с 0."""
    db_recipe = models.Recipe(**recipe.model_dump(), views=0)
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)
    return db_recipe