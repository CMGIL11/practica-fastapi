from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from dependencies import get_db
from models import Item
from schemas import ItemCreate, ItemResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido a FastAPI con base de datos!"}


@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = Item(**item.dict())

    db.add(db_item)

    await db.commit()
    await db.refresh(db_item)

    return db_item


@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    return item


@app.get("/items/", response_model=list[ItemResponse])
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    return result.scalars().all()


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_actualizado: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    item.nombre = item_actualizado.nombre
    item.descripcion = item_actualizado.descripcion
    item.precio = item_actualizado.precio
    item.en_stock = item_actualizado.en_stock

    await db.commit()
    await db.refresh(item)

    return item


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    await db.delete(item)
    await db.commit()

    return {"mensaje": f"Item {item_id} eliminado"}