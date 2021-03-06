from typing import List

import databases
import sqlalchemy
import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./test.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"


database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


class NoteIn(BaseModel):
    text: str = Field(..., example="it some text ")
    completed: bool = Field(..., example=True)


class Note(NoteIn):
    id: int
    created_at: datetime.datetime


app = FastAPI(title="note app + async sql")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/notes/", response_model=List[Note], tags=['get notes'])
async def read_notes():
    """return all notes"""
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note, tags=['create note'])
async def create_note(note: NoteIn):
    """add a note"""
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}
