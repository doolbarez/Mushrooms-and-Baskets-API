from typing import Dict
from models import Mushroom

# In-memory "базы данных"
mushrooms_db: Dict[int, Mushroom] = {}
baskets_db: Dict[int, dict] = {}
