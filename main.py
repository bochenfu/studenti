from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

users_db = {
    1 : {"id" : 1, "name" : "mario", "email" : "mario@gmail.com"},
    2 : {"id" : 2, "name" : "anna", "email" : "anna@gmail.com"},
    3 : {"id" : 3, "name" : "luigi", "email" : "luigi@gmail.com"}
}
class User(BaseModel):
    id: int
    name: str
    email: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None

app = FastAPI()

@app.get("/users")
def get_all_users():
    return list(users_db.values())

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.post("/users")
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User already exist ")
    users_db[user.id] = user.dict()
    return {"message": "User created successfully"}

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user.dict()
    return {"message": "User updated successfully"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db.pop(user_id)
    return {"message": "User deleted successfully"}

@app.patch("/users/{user_id}")
def patch_user(user_id: int, user: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id].update (user.dict(exclude_unset=True))
    return {"message": "User updated successfully"}






