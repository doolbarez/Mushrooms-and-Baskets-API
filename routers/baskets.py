from fastapi import APIRouter, HTTPException, status
from models import BasketCreate, BasketOut, AddMushroom
from database import baskets_db, mushrooms_db

router = APIRouter()

@router.post("", response_model=BasketOut, status_code=status.HTTP_201_CREATED)
def create_basket(basket: BasketCreate):
    if basket.id in baskets_db:
        raise HTTPException(status_code=400, detail="Корзинка с таким id уже существует")
    baskets_db[basket.id] = {
        "id": basket.id,
        "owner": basket.owner,
        "capacity": basket.capacity,
        "mushrooms": []  # список id грибов
    }
    return BasketOut(id=basket.id, owner=basket.owner, capacity=basket.capacity, mushrooms=[])

@router.post("/{basket_id}/mushrooms", response_model=BasketOut)
def add_mushroom_to_basket(basket_id: int, item: AddMushroom):
    basket = baskets_db.get(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Корзинка не найдена")
    
    mushroom = mushrooms_db.get(item.mushroom_id)
    if not mushroom:
        raise HTTPException(status_code=404, detail="Гриб не найден")
    
    # Проверка: гриб не должен быть уже в какой-либо корзинке
    for b in baskets_db.values():
        if item.mushroom_id in b["mushrooms"]:
            raise HTTPException(status_code=400, detail="Гриб уже находится в корзинке")
    
    current_weight = sum(mushrooms_db[mid].weight for mid in basket["mushrooms"])
    if current_weight + mushroom.weight > basket["capacity"]:
        raise HTTPException(status_code=400, detail="Превышена вместимость корзинки")
    
    basket["mushrooms"].append(item.mushroom_id)
    mushrooms_in_basket = [mushrooms_db[mid] for mid in basket["mushrooms"]]
    return BasketOut(
        id=basket["id"],
        owner=basket["owner"],
        capacity=basket["capacity"],
        mushrooms=mushrooms_in_basket
    )

@router.delete("/{basket_id}/mushrooms/{mushroom_id}", response_model=BasketOut)
def remove_mushroom_from_basket(basket_id: int, mushroom_id: int):
    basket = baskets_db.get(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Корзинка не найдена")
    
    if mushroom_id not in basket["mushrooms"]:
        raise HTTPException(status_code=404, detail="Гриб не найден в данной корзинке")
    
    basket["mushrooms"].remove(mushroom_id)
    mushrooms_in_basket = [mushrooms_db[mid] for mid in basket["mushrooms"]]
    return BasketOut(
        id=basket["id"],
        owner=basket["owner"],
        capacity=basket["capacity"],
        mushrooms=mushrooms_in_basket
    )

@router.get("/{basket_id}", response_model=BasketOut)
def get_basket(basket_id: int):
    basket = baskets_db.get(basket_id)
    if not basket:
        raise HTTPException(status_code=404, detail="Корзинка не найдена")
    mushrooms_in_basket = [mushrooms_db[mid] for mid in basket["mushrooms"]]
    return BasketOut(
        id=basket["id"],
        owner=basket["owner"],
        capacity=basket["capacity"],
        mushrooms=mushrooms_in_basket
    )
