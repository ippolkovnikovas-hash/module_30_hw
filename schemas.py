from pydantic import BaseModel, ConfigDict, Field


class RecipeBase(BaseModel):
    """Общие поля рецепта, задаваемые пользователем при создании."""

    title: str = Field(..., max_length=255, description="Название блюда")
    cooking_time: int = Field(..., gt=0, description="Время приготовления в минутах")
    ingredients: str = Field(..., description="Список ингредиентов (текст)")
    description: str = Field(..., description="Текстовое описание рецепта")


class RecipeCreate(RecipeBase):
    """Схема для создания нового рецепта (тело POST-запроса)."""
    pass


class RecipeListItem(BaseModel):
    """Элемент списка рецептов: краткая информация для таблицы на главном экране."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Идентификатор рецепта")
    title: str = Field(..., description="Название блюда")
    views: int = Field(..., description="Количество просмотров")
    cooking_time: int = Field(..., description="Время приготовления в минутах")


class RecipeDetail(BaseModel):
    """Полная информация о рецепте для экрана детального просмотра."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Идентификатор рецепта")
    title: str = Field(..., description="Название блюда")
    cooking_time: int = Field(..., description="Время приготовления в минутах")
    ingredients: str = Field(..., description="Список ингредиентов (текст)")
    description: str = Field(..., description="Текстовое описание рецепта")
    views: int = Field(..., description="Количество просмотров")
