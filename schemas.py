from pydantic import BaseModel, Field


class CategoriaCreate(BaseModel):
    nombre: str


class CategoriaResponse(CategoriaCreate):
    id: int

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    nombre: str


class TagResponse(TagCreate):
    id: int

    class Config:
        from_attributes = True


class ItemCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    en_stock: bool = True
    categoria_id: int


class ItemResponse(ItemCreate):
    id: int
    categoria: CategoriaResponse | None = None
    tags: list[TagResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True