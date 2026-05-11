from pydantic import BaseModel


class ItemCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    en_stock: bool = True


class ItemResponse(ItemCreate):
    id: int

    class Config:
        from_attributes = True