from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine
from routers.recipes import router as recipes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Создаёт таблицы при старте приложения (асинхронно)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Cookbook API",
    description=(
        "API кулинарной книги: список рецептов, детальная информация, "
        "создание рецептов."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

app.include_router(recipes_router)