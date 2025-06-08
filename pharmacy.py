# Файл: pharmacy.py
# Мета цього файлу — реалізувати API-сервіс для управління списком лікарських засобів в аптеці.
# API дозволяє додавати препарати, переглядати всі наявні та виконувати фільтрацію за ціною.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
# Ініціалізація FastAPI-застосунку
# Основна точка входу для всіх запитів
app = FastAPI()
# Клас Medicine описує структуру одного лікарського препарату
# Він визначає, які дані можуть бути передані у запитах
class Medicine(BaseModel):
    # Назва препарату. Має бути вказана обов’язково.
    name: str = Field(..., example="Ібупрофен")
    # Виробник. Наприклад, "Дарниця", "Фармак"
    manufacturer: str = Field(..., example="Дарниця")
    # Ціна у гривнях. Перевіряється, щоб була більшою за 0.
    price: float = Field(..., gt=0, example=42.00)
# Тимчасове сховище для ліків, яке зберігається у пам’яті сервера
# Після перезапуску застосунку дані будуть втрачені
medicines: List[Medicine] = []
# POST /medicines
# Додає новий препарат до списку
# Приймає: JSON-об'єкт із полями name, manufacturer, price
# Повертає: повідомлення про успішне додавання
@app.post("/medicines")
def add_medicine(med: Medicine):
    medicines.append(med)
    return {"message": "Препарат успішно додано"}
# GET /medicines
# Повертає повний список усіх доданих препаратів
# Не приймає параметрів
# Повертає: список об’єктів типу Medicine
@app.get("/medicines", response_model=List[Medicine])
def list_medicines():
    return medicines
# GET /medicines/filter
# Фільтрує список препаратів за максимальною ціною
# Параметр: max_price — максимальна допустима ціна в гривнях
# Повертає: список препаратів із ціною меншою або рівною зазначеній
# Якщо ціна недійсна — повертає HTTP помилку 400
@app.get("/medicines/filter", response_model=List[Medicine])
def filter_by_price(max_price: float):
    if max_price <= 0:
        raise HTTPException(status_code=400, detail="Ціна повинна бути більшою за 0")
    return [m for m in medicines if m.price <= max_price]