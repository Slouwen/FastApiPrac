import json
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="FastAPIPractice",
    description="First FastAPI application",
    docs_url="/docs",
    redoc_url="/redoc",
)

with open("src/fastapiprac/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def save_data():
    with open("src/fastapiprac/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: str
    price: float
    in_stock: bool

@app.get("/books", response_model=list[Book])
async def get_books():
    return data["books"]

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in data["books"]:
        if book["id"] == book_id:
            return book
    return None

@app.post("/books", response_model=Book)
async def add_book(book: Book):
    data["books"].append(book.model_dump())
    save_data()
    return book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(data["books"]):
        if book["id"] == book_id:
            deleted = data["books"].pop(i)
            save_data()
            return deleted
    return None

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, new_book: Book):
    for i, book in enumerate(data["books"]):
        if book["id"] == book_id:
            data["books"][i] = new_book.model_dump()
            save_data()
            return new_book
    return None

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)