from sqlalchemy import Column, Integer, String, Text

from database import Base


class Recipe(Base):
    """ORM-модель рецепта."""

    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    cooking_time = Column(Integer, nullable=False)
    ingredients = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    views = Column(Integer, default=0, nullable=False)