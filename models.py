from pydantic import BaseModel, Field
from typing import List

class Mushroom(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор гриба")
    name: str = Field(..., description="Название гриба")
    edible: bool = Field(..., description="Съедобен ли гриб")
    weight: int = Field(..., gt=0, description="Вес гриба в граммах")
    freshness: bool = Field(..., description="Является ли гриб свежим")

class BasketCreate(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор корзинки")
    owner: str = Field(..., description="Имя владельца корзинки")
    capacity: int = Field(..., gt=0, description="Вместимость корзинки в граммах")

class BasketOut(BaseModel):
    id: int
    owner: str
    capacity: int
    mushrooms: List[Mushroom] = Field(default_factory=list, description="Список грибов в корзинке")

class AddMushroom(BaseModel):
    mushroom_id: int = Field(..., description="ID гриба, который нужно добавить в корзинку")
