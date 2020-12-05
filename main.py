import os

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
import uvicorn

from models import User as ModelUser
from schema import User as SchemaUser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.get("/")
def all_users():
    return db.session.query(ModelUser).all()


@app.post("/user/", response_model=SchemaUser)
def create_user(user: SchemaUser):
    db_user = ModelUser(
        first_name=user.first_name, last_name=user.last_name, age=user.age
    )
    db.session.add(db_user)
    db.session.commit()
    return db_user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
