import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# The title shows at the top of the interactive docs at /docs.
# Set API_TITLE on Light Cloud to change it without touching the code.
app = FastAPI(title=os.getenv("API_TITLE", "Book API"))


class BookIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1450, le=2100)


class Book(BookIn):
    id: int


# In memory, so the list starts empty again after every restart.
books: dict[int, Book] = {}


@app.get("/")
def root():
    return {"message": "Hello from FastAPI", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/books")
def list_books() -> list[Book]:
    return list(books.values())


@app.post("/books", status_code=201)
def add_book(book: BookIn) -> Book:
    new = Book(id=len(books) + 1, **book.model_dump())
    books[new.id] = new
    return new


@app.get("/books/{book_id}")
def get_book(book_id: int) -> Book:
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]
