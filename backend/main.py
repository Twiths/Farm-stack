from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import Todo

#App object
app = FastAPI()

from database import (
    fetch_all_todos,
    fetch_one_todo,
    create_todo,
    update_todo,
    remove_todo,
)

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
def read_root():
    return { "ping": "pong" }

@app.get('/api/v1/todo')
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get('/api/v1/todo{title}', response_model=Todo)
async def get_todo_by_id(title):
    response = fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"There is no TODO item with this title {title}")

@app.post('/api/v1/todo')
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    if response:
        return response
    raise HTTPException(400, "something went wrong/Bad request")

@app.put('/api/v1/todo{title}/', response_model=Todo)
async def put_todo(title:str, desc:str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no TODO item with this title {title}")


@app.delete('/api/v1/todo{title}')
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return "Successfully deleted todo Item"
    if response:
        return response
    raise HTTPException(404, f"There is no TODO item with this title {title}")