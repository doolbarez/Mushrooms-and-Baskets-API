from fastapi import APIRouter, HTTPException, status
from models import Mushroom
from database import mushrooms_db

router = APIRouter()

@router.post("", response_model=Mushroom, status_code=status.HTTP_201_CREATED)
def create_mushroom(mushroom: Mushroom):
    if mushroom.id in mushrooms_db:
        raise HTTPException(status_code=400, detail="Гриб с таким id уже существует")
    mushrooms_db[mushroom.id] = mushroom
    return mushroom

@router.put("/{mushroom_id}", response_model=Mushroom)
def update_mushroom(mushroom_id: int, updated_mushroom: Mushroom):
    if mushroom_id not in mushrooms_db:
        raise HTTPException(status_code=404, detail="Гриб не найден")
    if mushroom_id != updated_mushroom.id:
        raise HTTPException(status_code=400, detail="ID в пути и теле запроса должны совпадать")
    mushrooms_db[mushroom_id] = updated_mushroom
    return updated_mushroom

@router.get("/{mushroom_id}", response_model=Mushroom)
def get_mushroom(mushroom_id: int):
    mushroom = mushrooms_db.get(mushroom_id)
    if not mushroom:
        raise HTTPException(status_code=404, detail="Гриб не найден")
    return mushroom
