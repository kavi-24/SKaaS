import json
from os.path import exists
from typing import Optional
from fastapi import FastAPI, Depends, Response, Request, Header
from pydantic import BaseModel
import pyperclip
import uuid
import random
import string


app = FastAPI()

logged_ins = {}


class User(BaseModel):
    username: str
    password: str
    uuid: Optional[str]
    # token: Optional[str]
    # disabled: Optional[bool] = None


class ToDo(BaseModel):
    id: Optional[int]
    title: str
    task: str


class UpdatedToDo(BaseModel):
    title: Optional[str]
    task: Optional[str]


@app.get("/")
def hello():
    return {"message": "Hello World"}

# @app.get("/get-token")
# async def hello(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

# def get_user(token):
#     return User(username="joe"+token, password="secret")

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     return {"user": get_user(token)}

# @app.get("/users")
# async def read_user(current_user: User = Depends(get_current_user)):
#     return current_user


def create_token():
    return ''.join(random.SystemRandom().choice(f'{string.ascii_lowercase}{string.ascii_uppercase}{string.digits}') for i in range(16))


def check_if_user_in_users(user: User, dct):
    for i in dct:
        if i["username"] == user.username:
            if i["password"] == user.password:
                return True
    return False


def get_users():
    content = []
    if exists("users.json"):
        with open("users.json", "r") as f:
            temp = f.read()
            if temp:
                content = json.loads(temp)
    return content


def get_uuid(uname, pwd):
    content = get_users()
    for i in content:
        if i["username"] == uname:
            if i["password"] == pwd:
                return i["uuid"]


def get_tasks():
    todoLst = {}
    with open("todolist.json", 'r') as f:
        temp = f.read()
        if temp:
            todoLst = json.loads(temp)
    return todoLst


@app.get("/register")
async def register(user: User):
    global logged_ins
    user.uuid = str(uuid.uuid1())
    content = get_users()
    with open("users.json", "w") as f:
        user_dct = user.dict()
        uuid_lst = [i["uuid"] for i in content]
        if user.uuid in uuid_lst:
            json.dump(content, f)
            return {"message": "User already exists"}
        content.append(user_dct)
        json.dump(content, f)
    todoLst = get_tasks()
    # todoUnameLst = [j for j in [i for i in todoLst]]
    todoLst[user.uuid] = []
    with open("todolist.json", "w") as f:
        json.dump(todoLst, f)
    return user


@app.get("/users")
async def currentUsers():
    return logged_ins


@app.get("/login")
async def login(request: Request, response: Response, user: User):
    global logged_ins
    # print(token_dct)
    users = list(logged_ins.values())
    # print(users)
    user.uuid = get_uuid(user.username, user.password)
    if user.uuid in users:
        todoLst = get_tasks()
        if user.uuid not in todoLst:
            todoLst[user.uuid] = []
            with open("todolist.json", "w") as f:
                json.dump(todoLst, f)
        return {"message": "User already logged in"}
    content = get_users()
    if check_if_user_in_users(user, content):
        temp_token = create_token()
        # print(temp_token)
        pyperclip.copy(temp_token)
        logged_ins[temp_token] = user.uuid
        print(logged_ins)
        response.headers.append("token", temp_token)
        # response.set_cookie("token", temp_token)
        todoLst = get_tasks()
        if user.uuid not in todoLst:
            todoLst[user.uuid] = []
            with open("todolist.json", "w") as f:
                json.dump(todoLst, f)
        return {"message": "Login successful"}
    return {"message": "Login failed"}


@app.get("/logout")
async def logout(request: Request):
    global logged_ins
    # print(request.headers)
    token = request.headers['token']
    # print(token_dct)
    if token in logged_ins:
        del logged_ins[token]
        return {"message": f"Token {token} deleted"}
    return {"message": "Token not found"}


@app.get("/create")
def create(todo: ToDo, request: Request):
    global logged_ins
    todoLst = get_tasks()
    try:
        token = request.headers['token']
        curUUID = logged_ins[token]  # <- Error line
    except:
        return {"message": "No user is logged in or wrong token header"}
    # print(token_dct)
    # print(todoLst[curUser])
    # print(todo in todoLst[curUser])
    if todo.title in [i["title"] for i in todoLst[curUUID]]:
        return {"message": "Duplicate title. Task already exists"}
    if todoLst[curUUID] == []:
        ln = 1
    else:
        ln = max([i["id"] for i in todoLst[curUUID]]) + 1
    todo.id = ln
    todoLst[curUUID].append(todo.dict())
    with open("todolist.json", "w") as f:
        json.dump(todoLst, f)
    return {"message": "Todo created"}


@app.get("/tasks")
def read(request: Request):
    global logged_ins
    try:
        token = request.headers['token']
        curUUID = logged_ins[token]  # <- Error line
    except:
        return {"message": "No user is logged in or wrong token header"}
    todoLst = get_tasks()
    return todoLst[curUUID]


@app.get("/delete/{id}")
def delete(id: int, request: Request):
    try:
        token = request.headers['token']
        curUUID = logged_ins[token]  # <- Error line
    except:
        return {"message": "No user is logged in or wrong token header"}
    todoLst = get_tasks()
    idx = 0
    for i in todoLst[curUUID]:
        if i["id"] == id:
            todoLst[curUUID].pop(idx)
            break
        idx += 1
    for i in todoLst[curUUID]:
        if i["id"] > id:
            i["id"] -= 1
    with open("todolist.json", "w") as f:
        json.dump(todoLst, f)
    return_val = {"message": "Todo deleted"}
    return_val["tasks"] = list(todoLst.values())
    return return_val


@app.get("/update/{id}")
def update(id: int, todo: UpdatedToDo, request: Request):
    try:
        token = request.headers['token']
        curUUID = logged_ins[token]  # <- Error line
    except:
        return {"message": "No user is logged in or wrong token header"}
    todoLst = get_tasks()
    curUserTasks = todoLst[curUUID]
    for i in curUserTasks:
        if i["id"] == id:
            i["title"] = todo.title if todo.title else i["title"]
            i["task"] = todo.task if todo.task else i["task"]
            break
    with open("todolist.json", "w") as f:
        json.dump(todoLst, f)
    return_val = {"message": "Todo updated"}
    return_val["tasks"] = list(todoLst.values())
    return return_val

