from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from dependencies import get_db
from models import Item, Categoria, Tag
from schemas import ItemCreate, ItemResponse, CategoriaCreate, CategoriaResponse, TagCreate, TagResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido a FastAPI con relaciones!"}


# CATEGORÍAS

@app.post("/categorias/", response_model=CategoriaResponse)
async def create_categoria(
    categoria: CategoriaCreate,
    db: AsyncSession = Depends(get_db)
):
    db_categoria = Categoria(**categoria.dict())

    db.add(db_categoria)
    await db.commit()
    await db.refresh(db_categoria)

    return db_categoria


@app.get("/categorias/", response_model=list[CategoriaResponse])
async def list_categorias(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Categoria))
    return result.scalars().all()


# ITEMS

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Categoria).where(Categoria.id == item.categoria_id)
    )
    categoria = result.scalar_one_or_none()

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db_item = Item(**item.dict())

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)

    result = await db.execute(
        select(Item)
        .options(selectinload(Item.categoria), selectinload(Item.tags))
        .where(Item.id == db_item.id)
    )

    return result.scalar_one()

@app.post("/categorias/{cat_id}/items/", response_model=ItemResponse)
async def create_item_in_categoria(
    cat_id: int,
    item: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Categoria).where(Categoria.id == cat_id)
    )
    categoria = result.scalar_one_or_none()

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    db_item = Item(
        nombre=item.nombre,
        descripcion=item.descripcion,
        precio=item.precio,
        en_stock=item.en_stock,
        categoria_id=cat_id
    )

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)

    result = await db.execute(
        select(Item)
        .options(selectinload(Item.categoria), selectinload(Item.tags))
        .where(Item.id == db_item.id)
    )

    return result.scalar_one()


@app.get("/items/", response_model=list[ItemResponse])
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Item).options(selectinload(Item.categoria), selectinload(Item.tags))
    )
    return result.scalars().all()


@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Item)
        .options(selectinload(Item.categoria), selectinload(Item.tags))
        .where(Item.id == item_id)
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    return item


@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item_actualizado: ItemCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Item)
        .options(selectinload(Item.categoria), selectinload(Item.tags))
        .where(Item.id == item_id)
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    result = await db.execute(
        select(Categoria).where(Categoria.id == item_actualizado.categoria_id)
    )
    categoria = result.scalar_one_or_none()

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    item.nombre = item_actualizado.nombre
    item.descripcion = item_actualizado.descripcion
    item.precio = item_actualizado.precio
    item.en_stock = item_actualizado.en_stock
    item.categoria_id = item_actualizado.categoria_id

    await db.commit()
    await db.refresh(item)

    result = await db.execute(
        select(Item)
        .options(selectinload(Item.categoria), selectinload(Item.tags))
        .where(Item.id == item.id)
    )

    return result.scalar_one()


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    await db.delete(item)
    await db.commit()

    return {"mensaje": f"Item {item_id} eliminado"}


# TAGS

@app.post("/tags/", response_model=TagResponse)
async def create_tag(tag: TagCreate, db: AsyncSession = Depends(get_db)):
    db_tag = Tag(**tag.dict())

    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)

    return db_tag


@app.get("/tags/", response_model=list[TagResponse])
async def list_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag))
    return result.scalars().all()


@app.post("/items/{item_id}/tags/{tag_id}", response_model=ItemResponse)
async def add_tag_to_item(
    item_id: int,
    tag_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Item)
        .options(selectinload(Item.categoria), selectinload(Item.tags))
        .where(Item.id == item_id)
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()

    if not tag:
        raise HTTPException(status_code=404, detail="Tag no encontrado")

    item.tags.append(tag)

    await db.commit()

    result = await db.execute(
        select(Item)
        .options(selectinload(Item.categoria), selectinload(Item.tags))
        .where(Item.id == item_id)
    )

    return result.scalar_one()